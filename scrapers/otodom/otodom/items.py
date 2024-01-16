# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime
from dataclasses import dataclass, field

import scrapy


@dataclass
class OtodomItem:
    offer_source: str = field(default="otodom")
    offer_id: str = field(default="")
    date_scraped: datetime.datetime = field(default_factory=datetime.datetime.now)
    title: str = field(default="")
    canonical_url: str = field(default="")
    short_description: str = field(default="")
    description: str = field(default="")
    offer_type: str = field(default="")
    offer_date: str = field(default="")
    modified_date: str = field(default="")
    location: str = field(default="")
    city: str = field(default="")
    district: str = field(default="")
    region: str = field(default="")
    price_total: str = field(default="")
    price_per_msq: str = field(default="")
    size: str = field(default="")
    n_rooms: str = field(default="")
    construction_status: str = field(default="")
    ownership_type: str = field(default="")
    floor: str = field(default="")
    rent: str = field(default="")
    outdoor: str = field(default="")
    parking: str = field(default="")
    heating_type: str = field(default="")
    market: str = field(default="")
    offer_type: str = field(default="")
    year_built: str = field(default="")
    building_type: str = field(default="")
    windows_type: str = field(default="")
    lift: str = field(default="")
    media_types: str = field(default="")
    security: str = field(default="")
    equipment: str = field(default="")
    building_material: str = field(default="")
    image_urls: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
