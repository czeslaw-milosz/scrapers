import datetime
from dataclasses import dataclass, field


@dataclass
class OlxItem:
    offer_source: str = field(default="olx")
    offer_id: str = field(default="")
    date_scraped: datetime.datetime = field(default=datetime.datetime.now())
    title: str = field(default="")
    canonical_url: str = field(default="")
    short_description: str = field(default="")
    description: str = field(default="")
    price_total: str = field(default="")
    offer_type: str = field(default="")
    offer_date: str = field(default="")
    modified_date: str = field(default="")
    offer_location: str = field(default="")
    price_per_msq: str = field(default="")
    primary_market: bool = field(default="")
    floor: str = field(default="")
    building_type: str = field(default="")
    size: str = field(default="")
    n_rooms: str = field(default="")
    image_urls: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
