from mapsmefr.steps.locators import LocalizedButtons
from mapsmefr.steps.locators import Locator
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import NoSuchElementException


class BottomPanel:

    def find_button(self, text):
        driver = WebDriverManager.get_instance().driver
        return driver.find_element_by_xpath(
            "//*[@text='{}' or @text='{}' or @text='{}']/parent::*".format(text, text.upper(), text.lower()))

    def find_button_by_id(self, locator):
        return WebDriverManager.get_instance().driver.find_element_by_id(locator)

    def bookmark(self):
        if get_settings("System", "platform") == "Android":
            return self.find_button(LocalizedButtons.BOOKMARK.get())
        else:
            return self.find_button_by_id("ic bookmarks off")

    def book(self):
        if get_settings("System", "platform") == "Android":
            book = None
            try:
                book = self.find_button(LocalizedButtons.BOOK.get())
            except NoSuchElementException:
                book = self.find_button(LocalizedButtons.BOOKING_COM.get())
            return book
        else:
            book = None
            try:
                book = self.find_button_by_id("ic booking logo")
            except NoSuchElementException:
                book = self.find_button_by_id("ic booking search")
            return book

    def bookmarks(self):
        return self.find_button_by_id(Locator.BOOKMARKS_BUTTON.get())

    def to(self):
        if get_settings("System", "platform") == "Android":
            return self.find_button(LocalizedButtons.TO.get())
        else:
            return self.find_button_by_id("ic route to")

    def route_from(self):
        if get_settings("System", "platform") == "Android":
            return self.find_button(LocalizedButtons.FROM.get())
        else:
            return self.find_button_by_id("ic route from")

    def add_stop(self):
        if get_settings("System", "platform") == "Android":
            return self.find_button(LocalizedButtons.ADD_STOP.get())
        else:
            return self.find_button_by_id("ic add route point")

    def delete(self):
        if get_settings("System", "platform") == "Android":
            return self.find_button(LocalizedButtons.REMOVE.get())
        else:
            pass

    def download(self):
        if get_settings("System", "platform") == "Android":
            return self.find_button_by_id(Locator.DOWNLOAD_ICON.get())
        else:
            return WebDriverManager.get_instance().driver.find_element_by_xpath(
                "//*[./following-sibling::*[@name='{}']]".format(LocalizedButtons.DOWNLOAD_FROM_PP_BUTTON.get()))

    def discovery(self):
        return self.find_button_by_id(Locator.DISCOVERY.get())
