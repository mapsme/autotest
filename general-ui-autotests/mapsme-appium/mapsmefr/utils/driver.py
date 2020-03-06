import logging
from time import sleep

import pytest
from appium import webdriver
from mapsmefr.client.device import Device
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import WebDriverException


class WebDriverManager:
    _instance = None
    APPIUM_SERVER = "http://127.0.0.1:4723/wd/hub"

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = WebDriverManager()
        return cls._instance

    def __init__(self):
        self.device = Device.init_device(pytest.config.getoption("--device-id"))
        if not self.device.check_active():
            raise Exception("Device is not active!")
        capabilities = self.device.get_capabilities()

        logging.info("Capabilities: {}".format(capabilities))

        try:
            self.driver = webdriver.Remote(
                command_executor=self.APPIUM_SERVER,
                desired_capabilities=capabilities
            )
        except WebDriverException as e:
            if "xcodebuild failed with code 65" in e.msg or "xcodebuild failure" in e.msg:
                #self.device.reboot()
                #sleep(90)
                self.driver = webdriver.Remote(
                    command_executor=self.APPIUM_SERVER,
                    desired_capabilities=capabilities
                )
            else:
                raise e

        self.driver.update_settings({"normalizeTagNames": True})

    @classmethod
    def destroy(cls):
        if cls._instance:
            cls._instance.driver.quit()
            cls._instance = None

