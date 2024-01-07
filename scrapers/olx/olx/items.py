import scrapy


class OlxItem(scrapy.Item):
    offer_source = scrapy.Field()
    offer_id = scrapy.Field()
    title = scrapy.Field()
    canonical_url = scrapy.Field()
    short_description = scrapy.Field()
    description = scrapy.Field()
    price_total = scrapy.Field()
    offer_type = scrapy.Field()
    offer_date = scrapy.Field()
    modified_date = scrapy.Field()
    offer_location = scrapy.Field()
    price_per_msq = scrapy.Field()
    primary_market = scrapy.Field()
    floor = scrapy.Field()
    building_type = scrapy.Field()
    size = scrapy.Field()
    n_rooms = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
