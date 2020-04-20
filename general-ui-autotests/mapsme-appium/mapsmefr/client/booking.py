import logging
from datetime import datetime
from urllib import parse

import requests
from mapsmefr.utils.tools import get_settings


class Booking:

    def __init__(self, test_result_id):
        self.id = None
        self.name = None
        self.test_result_id = test_result_id
        self.booking_url = None
        self.status = None
        self.aid = None
        self.hotel_id = None
        self.booking_time = None
        self.reservation_id = None
        self.price = None
        self.url = "{}/booking".format(get_settings('ReportServer', 'host'))

    def create(self, name, url):
        self.name = name
        if url:
            self.booking_url = url
            url_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
            logging.info(str(url_params))
            self.aid = int(url_params["aid"])
            self.hotel_id = int(url_params["highlighted_hotels"]) if "highlighted_hotels" in url_params else None
        params = {"name": self.name,
                  "test_result_id": self.test_result_id,
                  "url": self.booking_url,
                  "status": self.status,
                  "booking_time": datetime.now(),
                  "hotel_id": self.hotel_id,
                  "aid": self.aid}
        response = requests.post(self.url, data=params)
        self.id = int(response.text)

    def result(self, status):
        params = {"status": status,
                  "booking_time": datetime.now(),
                  "reservation_id": self.reservation_id,
                  "price": self.price}
        response = requests.post("{}/{}".format(self.url, self.id), data=params)

    def cancel(self):
        response = requests.post("{}/{}".format(self.url, self.id), data={"status": "Cancelled"})
