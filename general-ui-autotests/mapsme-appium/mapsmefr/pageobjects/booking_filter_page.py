from mapsmefr.steps.locators import BookingButtons, LocalizedButtons
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings


class SearchFilter:

    def __init__(self):
        self._instance = self._get()

    def _get(self):
        if WebDriverManager.get_instance().device.platform == "Android":
            return AndroidSearchFilter()
        else:
            return IosSearchFilter()

    def check_in(self):
        return self._instance.check_in()

    def check_out(self):
        return self._instance.check_out()

    def rating_any(self):
        return self._instance.rating_any()

    def rating_good(self):
        return self._instance.rating_good()

    def rating_very_good(self):
        return self._instance.rating_very_good()

    def rating_excellent(self):
        return self._instance.rating_excellent()

    def price_low(self):
        return self._instance.price_low()

    def price_medium(self):
        return self._instance.price_medium()

    def price_high(self):
        return self._instance.price_high()

    def type(self, type_name):
        return self._instance.type(type_name)

    def search_button(self):
        return self._instance.search_button()


class AndroidSearchFilter:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    def _find_by_id(self, id):
        return self.driver.find_element_by_id("{}:id/{}".format(get_settings("Android", "package"), id))

    def check_in(self):
        return self._find_by_id("checkIn")

    def check_out(self):
        return self._find_by_id("checkOut")

    def rating_any(self):
        return self._find_by_id("any")

    def rating_good(self):
        return self._find_by_id("good")

    def rating_very_good(self):
        return self._find_by_id("very_good")

    def rating_excellent(self):
        return self._find_by_id("excellent")

    def price_low(self):
        return self._find_by_id("low")

    def price_medium(self):
        return self._find_by_id("medium")

    def price_high(self):
        return self._find_by_id("high")

    def type(self, type_name):
        return self.driver.find_element_by_xpath("//*[@text='{}']".format(type_name))

    def search_button(self):
        return self._find_by_id("done")


class IosSearchFilter:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    def check_in(self):
        return self.driver.find_element_by_xpath("//*[@name='{}']/following-sibling::*[@type='XCUIElementTypeButton']"
                                                 .format(BookingButtons.CHECK_IN.get()))

    def check_out(self):
        return self.driver.find_element_by_xpath("//*[@name='{}']/following-sibling::*[@type='XCUIElementTypeButton']"
                                                 .format(BookingButtons.CHECK_OUT.get()))

    def rating_any(self):
        return self.driver.find_element_by_id(BookingButtons.RATING_ANY.get())

    def rating_good(self):
        return self.driver.find_element_by_id(BookingButtons.RATING_GOOD.get())

    def rating_very_good(self):
        return self.driver.find_element_by_id(BookingButtons.RATING_VERY_GOOD.get())

    def rating_excellent(self):
        return self.driver.find_element_by_id(BookingButtons.RATING_EXCELLENT.get())

    def price_low(self):
        return self.driver.find_element_by_id("$")

    def price_medium(self):
        return self.driver.find_element_by_id("$$")

    def price_high(self):
        return self.driver.find_element_by_id("$$$")

    def type(self, type_name):
        return self.driver.find_element_by_id(type_name)

    def search_button(self):
        return self.driver.find_element_by_id(LocalizedButtons.SEARCH_HOTEL_FILTER.get())
