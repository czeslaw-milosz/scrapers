import datetime
from typing import Any, Tuple

import scrapy

from olx.items import OlxItem

def extract_fields(response: scrapy.http.response.html.HtmlResponse) -> dict:
    """Extract fields from response of olx scraper.
    
    Args:
        response (scrapy.http.response.html.HtmlResponse): response of olx scraper
    
    Returns:
        dict: dictionary with fields extracted from response:
            - title (str): title of the offer
            - short_description (str): short description of the offer
            - description (str): description of the offer
            - canonical_url (str): canonical url of the offer
            - offer_type (str): type of the offer (private or business, "Prywatne" or "Firmowe")
            - offer_id (str): offer id
            - offer_date (str): date of posting of the offer
            - offer_location (str): location of the offer
            - price_per_msq (int): price of the flat per m^2
            - primary_market (boolean): whether the flat is on primary market (True) or resold (False)
            - floor (int): on which floor the flat is located
            - building_type (str): type of the building
            - size (float): size of the flat in square meters
            - n_rooms (int): number of rooms in the flat
    """
    # select text of title element from response head:
    title = response.xpath("//title/text()").get()
    # select meta element with name attribute equal to "description" and extract its content attribute:
    short_description = response.xpath("//meta[@name='description']/@content").get()
    # select meta element named "canonical" and extract the canonical link
    canonical_url = response.xpath("//link[@rel='canonical']/@href").get()
    # select from body an unordered list with class css-sfcl1s and extract texts of paragraphs in its items, including spans within paragraphs:
    list_items = response.xpath("//ul[@class='css-sfcl1s']/li/p//text()").getall()
    # select from body a div with data-cy 'ad_description' and extract texts of div inside it:
    description = response.xpath("//div[@data-cy='ad_description']/div//text()").get()
    # select from body a div with data-cy 'ad-footer-bar-section' and extract ID from text from a span inside the div:
    offer_id = int(response.xpath("//div[@data-cy='ad-footer-bar-section']/span/text()").getall()[-1])
    # select from body a span with dara-cy 'ad-posted-at' and extract text from it:
    offer_date = response.xpath("//span[@data-cy='ad-posted-at']/text()")

def get_detail_fields(response: scrapy.http.response.html.HtmlResponse) -> tuple[Any]:
    """Extract details fields from response of olx scraper.
    
    Args:
        response (scrapy.http.response.html.HtmlResponse): response of olx scraper

    Returns:
        tuple: tuple of details extracted from response:
            - offer_type (str): type of the offer (private or business, "Prywatne" or "Firmowe")
            - price_per_msq (float): price of the flat per m^2
            - primary_market (boolean): whether the flat is on primary market (True) or resold (False)
            - floor (str): on which floor the flat is located
            - building_type (str): type of the building
            - size (float): size of the flat in square meters
            - n_rooms (int): number of rooms in the flat
    """
    # select from body an unordered list with class css-sfcl1s and extract texts of paragraphs in its items, including spans within paragraphs:
    list_items = response.xpath("//ul[@class='css-sfcl1s']/li/p//text()").getall()
    tmp = [x for x in list_items if x in {"Prywatne", "Firmowe"}]
    offer_type = tmp[0] if tmp else None

    tmp = [x for x in list_items if "zł/m" in x]
    price_per_msq = tmp[0].split(" ")[3].strip().replace(",", ".") if tmp else None

    primary_market = any("Pierwotny" in item for item in list_items)

    tmp = [x for x in list_items if "Poziom" in x]
    floor = tmp[0].split(":")[1].strip() if tmp else None

    tmp = [x for x in list_items if "Rodzaj zabudowy" in x]
    building_type = tmp[0].split(":")[1].strip() if tmp else None

    tmp = [x for x in list_items if "Powierzchnia" in x]
    size = tmp[0].split(" ")[1].strip().replace(",", ".") if tmp else None

    tmp = [x for x in list_items if "Liczba pokoi" in x]
    n_rooms = tmp[0].split(" ")[2].strip() if tmp else None

    return offer_type, price_per_msq, primary_market, floor, building_type, size, n_rooms

