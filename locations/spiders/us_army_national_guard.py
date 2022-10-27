import scrapy

from geonamescache import GeonamesCache

from locations.items import GeojsonPointItem


class USArmyNationalGuardSpider(scrapy.Spider):
    name = "us_army_national_guard"
    item_attributes = {
        "brand": "US Army National Guard",
        "brand_wikidata": "Q928670",
        "country": "US",
    }
    allowed_domains = ["www.nationalguard.com"]

    def start_requests(self):
        for state in GeonamesCache().get_us_states():
            yield scrapy.Request(url="https://www.nationalguard.com/api/state/" + state)
        for state in ["USPR", "USGU", "USVI"]:
            yield scrapy.Request(url="https://www.nationalguard.com/api/state/" + state)

    def parse(self, response, **kwargs):
        data = response.json()
        for row in data["locations"]:
            properties = {
                "name": row["name"],
                "ref": row["id"],
                "addr_full": row["address"],
                "state": row["state"],
                "phone": row["phone"],
                "lat": row["latitude"],
                "lon": row["longitude"],
            }

            yield GeojsonPointItem(**properties)
