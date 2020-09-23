import logging

from mapsmefr.pageobjects.switch import switch
from mapsmefr.utils.driver import WebDriverManager
from selenium.common.exceptions import NoSuchElementException


class SubscriptionBanner:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    @switch("native")
    def try_get(self, id):
        try:
            logging.info("Trying to find element by id: {}".format(id))
            return self.driver.find_element_by_id(id)
        except NoSuchElementException:
            logging.info("Element not found")
            return None

    def title(self):
        return self.try_get("Подписка")

    def city_outdoor(self):
        return self.try_get("City + Outdoor Pass")

    def monthly(self):
        return self.try_get("welcome_storyboard.button_subscription_monthly")

    def yearly(self):
        return self.try_get("welcome_storyboard.button_subscription_annual")

    def close(self):
        return self.try_get("bookmarksSubscriptionClose")
