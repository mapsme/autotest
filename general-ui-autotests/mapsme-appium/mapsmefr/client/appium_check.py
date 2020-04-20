from os import system
from time import sleep

import requests


class AppiumServer:

    def __init__(self, host='127.0.0.1', port='4723'):
        self.host = host
        self.port = port

    def check_if_okay(self):
        response = requests.get("http://{}:{}/wd/hub/sessions".format(self.host, self.port))
        return response.status_code == 200

    def check_if_connected(self):
        try:
            requests.get("http://{}:{}/wd/hub/sessions".format(self.host, self.port))
        except requests.exceptions.ConnectionError as e:
            return False
        return True

    def connect(self):
        system("appium --relaxed-security -a {} -p {} &".format(self.host, self.port))
        sleep(10)

    def restart(self):
        pass
