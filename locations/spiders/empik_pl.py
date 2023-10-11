from scrapy import Request, Spider

from locations.dict_parser import DictParser


class EmpikPLSpider(Spider):
    name = "empik_pl"
    item_attributes = {"brand": "Empik", "brand_wikidata": "Q3045978"}
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def start_requests(self):
        csrfToken = "f0d1b256-85df-41ea-91b4-9d583482c686"
        # TODO: check headers
        # https://www.empik.com/salony-empik
        yield Request(
            url="https://www.empik.com/ajax/delivery-point/empik?query=",
            headers={"X-CSRF-TOKEN": csrfToken},
            cookies={"CSRF": csrfToken},
        )

    def parse(self, response, **kwargs):
        for shop in response.json():
            item = DictParser.parse(shop)
            hours = {
                "Mon": shop["mondayWorkingHours"],
                "Tue": shop["tuesdayWorkingHours"],
                "Wed": shop["wednesdayWorkingHours"],
                "Thu": shop["thursdayWorkingHours"],
                "Fri": shop["fridayWorkingHours"],
                "Sat": shop["saturdayWorkingHours"],
                "Sun": shop["sundayWorkingHours"],
            }
            # item["opening_hours"]
            # "phone": shop["cellPhone"],
            # "email": shop["email"].strip(),
            yield item
