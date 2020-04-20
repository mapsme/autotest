import logging
from datetime import datetime

import requests
from mapsmefr.utils.tools import get_settings


class TestResult:

    def __init__(self):
        self.id = None
        self.session_id = None
        self.test_item_method = None
        self.time_start = None
        self.time_end = None
        self.is_memory = None
        self.is_power = None
        self.is_standart = None
        self.url = "{}/testresult".format(get_settings('ReportServer', 'host'))

    def start(self, session_id, test_method):
        self.session_id = session_id
        self.time_start = datetime.now()
        self.test_item_method = test_method
        params = {"session_id": self.session_id,
                  "time_start": self.time_start,
                  "time_end": self.time_end,
                  "test_item_method": self.test_item_method,
                  "is_memory_test": self.is_memory,
                  "is_power_test": self.is_power}
        if self.is_standart:
            params["is_standart"] = self.is_standart
        response = requests.post(self.url, data=params)
        self.id = int(response.text)
        logging.info("==============================================================================================")
        logging.info("RESULT LINK:    {}#!/top/testresult?id={}".format(self.url.split("testresult")[0], self.id))
        logging.info("==============================================================================================")

    def result(self, status):
        self.time_end = datetime.now()
        params = {"time_end": self.time_end,
                  "status": status}
        requests.post("{}/{}".format(self.url, self.id), data=params)
