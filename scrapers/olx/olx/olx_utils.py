from typing import Any

import scrapy


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

