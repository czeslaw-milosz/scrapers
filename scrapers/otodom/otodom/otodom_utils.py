from typing import Any

import scrapy
import ujson


OTODOM_DETAILS_FIELD2HTML = {
    "size": "table-value-area",
    "n_rooms": "table-value-rooms_num",
    "construction_status": "table-value-construction_status",
    "ownership_type": "table-value-building_ownership",
    "floor": "table-value-floor",
    "rent": "table-value-rent",
    "outdoor": "table-value-outdoor",
    "parking": "table-value-car",
    "heating_type": "table-value-heating",
    "market": "table-value-market",
    "offer_type": "table-value-advertiser_type",
    "year_built": "table-value-build_year",
    "building_type": "table-value-building_type",
    "windows_type": "table-value-windows_type",
    "lift": "table-value-lift",
    "media_types": "table-value-media_types",
    "security": "table-value-security_types",
    "equipment": "table-value-equipment_types",
    "building_material": "table-value-building_material",
}


def get_detail_fields(response: scrapy.http.response.html.HtmlResponse) -> tuple[Any]:
    """Extract data from main details fields from response of otodom scraper.
    
    Args:
        response (scrapy.http.response.html.HtmlResponse): response of otodom scraper

    Returns:
        dict(str, Any): details extracted from response fields
    """
    output = {}
    return {
        field_name: response.xpath(f"//div[@data-testid='{html_name}']/text()").get() or None
        for field_name, html_name in OTODOM_DETAILS_FIELD2HTML.items()
    }

def get_image_urls(response: scrapy.http.response.html.HtmlResponse, img_size: str = "medium") -> list[str]:
    """Extract image urls from response of otodom scraper.
    
    Args:
        response (scrapy.http.response.html.HtmlResponse): response of otodom scraper
    """
    item_json = ujson.loads(
        response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
    )
    return [
        img_url[img_size]
        for img_url in item_json["props"]["pageProps"]["ad"]["images"]
    ]


def get_offer_id(response: scrapy.http.response.html.HtmlResponse) -> str:
    """Extract offer id from response of otodom scraper.
    
    Args:
        response (scrapy.http.response.html.HtmlResponse): response of otodom scraper
    
    Returns:
        str: offer id (formatted according to our convention: otodom_{original_offer_id})
    """
    original_offer_id = ujson.loads(
        response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
    )["props"]["pageProps"]["ad"]["id"]
    return f"otodom_{original_offer_id}"
