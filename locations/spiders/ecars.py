import logging

from scrapy import Spider
from scrapy.http import JsonRequest

from locations.categories import Categories, apply_category
from locations.dict_parser import DictParser


class EcarsSpider(Spider):
    name = "ecars"
    item_attributes = {"brand": "ESB ecars", "brand_wikidata": "Q134882112"}
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def start_requests(self):
        yield JsonRequest(
            url="https://myaccount.esbecars.com/stationFacade/findSitesInBounds",
            data={
                "filterByBounds": {"northEastLat": 90, "northEastLng": 180, "southWestLat": -90, "southWestLng": -180}
            },
        )

    def parse(self, response, **kwargs):
        if not response.json()["success"]:
            self.log(response.json()["errors"], logging.ERROR)
            return
        for location in response.json()["data"]:
            if location["deleted"]:
                continue

            item = DictParser.parse(location)
            item["addr_full"] = location["dn"]
            apply_category(Categories.CHARGING_STATION, item)
            yield item
