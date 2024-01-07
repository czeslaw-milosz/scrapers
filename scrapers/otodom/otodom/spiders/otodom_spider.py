import logging
from pathlib import Path

import autopager
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from otodom import otodom_utils
from otodom.items import OtodomItem

# Suppress scrapy's unreasonable default logging of the whole scraped content
logging.getLogger("scrapy.core.scraper").addFilter(
    lambda x: not x.getMessage().startswith("Scraped from"))


class OtodomSpider(CrawlSpider):
    name = "otodom"
    allowed_domains = [
        "otodom.pl",
    ]
    logging.info("Initializing OtoDomSpider: extracting number of pages...")
    _autopager_base_url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa"
    _n_pages = int(autopager.urls(requests.get(_autopager_base_url))[-1].split("=")[-1])
    start_urls = [
        f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa?page={i}"
        for i in range(1, 2)
    ]
    rules = [
        Rule(LinkExtractor(allow="oferta/", restrict_xpaths="//a[@data-cy='listing-item-link']"),
            callback="parse_details",
            follow=True),
    ]

    def parse_details(self, response):
        # logging.info("ASDF")
        # filename = f"final_test_otodom/{response.url.split('/')[-1]}"
        # Path(filename).write_bytes(response.body)
        l = ItemLoader(item=OtodomItem(), response=response)
        l.add_value("offer_source", "otodom")

        offer_id = otodom_utils.get_offer_id(response)
        l.add_value("offer_id", offer_id)
        l.add_xpath("title", "//title/text()")
        l.add_xpath("canonical_url", "//link[@rel='canonical']/@href")
        l.add_xpath("short_description", "//meta[@name='description']/@content")
        l.add_xpath("description", "//div[@data-cy='adPageAdDescription']//p//text()")
        l.add_xpath("price_total", "//strong[@aria-label='Cena']/text()")
        l.add_xpath("price_per_msq", "//div[@aria-label='Cena za metr kwadratowy']/text()")
        l.add_xpath("location", "//a[@aria-label='Adres']/text()")

        detail_fields = otodom_utils.get_detail_fields(response)
        for field_name, field_value in detail_fields.items():
            l.add_value(field_name, field_value)
        
        img_urls = otodom_utils.get_image_urls(response)
        l.add_value("image_urls", img_urls)
        logging.info(f"IMAGE URLS: {img_urls}")

        offer_date, modified_date = otodom_utils.get_posting_dates(response)
        l.add_value("offer_date", offer_date)
        l.add_value("modified_date", modified_date)
        yield l.load_item()
