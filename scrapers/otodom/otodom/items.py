# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OtodomItem(scrapy.Item):
    offer_source = scrapy.Field()
    offer_id = scrapy.Field()
    title = scrapy.Field()
    canonical_url = scrapy.Field()
    short_description = scrapy.Field()
    description = scrapy.Field()
    offer_type = scrapy.Field()
    offer_date = scrapy.Field()
    modified_date = scrapy.Field()
    location = scrapy.Field()
    price_total = scrapy.Field()
    price_per_msq = scrapy.Field()
    size = scrapy.Field()
    n_rooms = scrapy.Field()
    construction_status = scrapy.Field()
    ownership_type = scrapy.Field()
    floor = scrapy.Field()
    rent = scrapy.Field()
    outdoor = scrapy.Field()
    parking = scrapy.Field()
    heating_type = scrapy.Field()
    market = scrapy.Field()
    offer_type = scrapy.Field()
    year_built = scrapy.Field()
    building_type = scrapy.Field()
    windows_type = scrapy.Field()
    lift = scrapy.Field()
    media_types = scrapy.Field()
    security = scrapy.Field()
    equipment = scrapy.Field()
    building_material = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
