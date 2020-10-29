import logging
from time import sleep

from mapsmefr.steps.base_steps import BaseSteps, AndroidSteps, IosSteps
from mapsmefr.steps.locators import Locator, LocalizedMapsNames, LocalizedButtons
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings


class DownloaderSteps(BaseSteps):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get():
        if WebDriverManager.get_instance().device.platform == "Android":
            return AndroidDownloaderSteps()
        else:
            return IosDownloaderSteps()


class AndroidDownloaderSteps(DownloaderSteps, AndroidSteps):
    def assert_size_and_sublocations(self, country_name, state_name, loc_name):
        self.try_get(Locator.MENU_BUTTON.get()).click()
        self.try_get(Locator.DOWNLOAD_MAPS.get()).click()
        if country_name:
            logging.info("Trying to find {} folder".format(country_name.get()))
            country, _ = self.try_find_map_with_scroll(country_name.get())
            if country:
                logging.info("Folder {} found.".format(country_name.get()))
                country.click()
                if state_name:
                    logging.info("Trying to find {} folder".format(state_name.get()))
                    state, _ = self.try_find_map_with_scroll(state_name.get())
                    if state:
                        logging.info("Folder {} found.".format(state_name.get()))
                        state.click()
        logging.info("Trying to find city {}".format(loc_name.get()))
        city, _ = self.try_find_map_with_scroll(loc_name.get())
        root = self.try_get_by_xpath("//*[@resource-id='{}:id/recycler']".format(get_settings("Android", "package")))
        subtitle = root.find_element_by_xpath(
            ".//*[@class='android.widget.RelativeLayout' and .//*[contains(@resource-id, 'name') and @text='{}']]//*[contains(@resource-id, 'subtitle')]".format(
                loc_name.get()))
        assert len(subtitle.text.split(",")) <= 3

        size = root.find_element_by_xpath(
            ".//*[@class='android.widget.RelativeLayout' and .//*[contains(@resource-id, 'name') and @text='{}']]//*[contains(@resource-id, 'size')]".format(
                loc_name.get()))

        assert "МБ" in size.text or "MB" in size.text

        self.press_back_until_main_page()

    def go_to_map(self, country_name, state_name, loc_name):
        self.try_get(Locator.MENU_BUTTON.get()).click()
        self.try_get(Locator.DOWNLOAD_MAPS.get()).click()
        if country_name:
            logging.info("Trying to find {} folder".format(country_name.get()))
            country, _ = self.try_find_map_with_scroll(country_name.get())
            if country:
                logging.info("Folder {} found.".format(country_name.get()))
                country.click()
                if state_name:
                    logging.info("Trying to find {} folder".format(state_name.get()))
                    state, _ = self.try_find_map_with_scroll(state_name.get())
                    if state:
                        logging.info("Folder {} found.".format(state_name.get()))
                        state.click()
        logging.info("Trying to find city {}".format(loc_name.get()))
        city, _ = self.try_find_map_with_scroll(loc_name.get())


class IosDownloaderSteps(DownloaderSteps, IosSteps):

    def assert_size_and_sublocations(self, country_name, state_name, loc_name):
        self.try_get(Locator.MENU_BUTTON.get()).click()
        sleep(1)
        self.try_get(LocalizedButtons.DOWNLOAD_MAPS.get()).click()
        if country_name:
            country, _ = self.try_find_map_with_scroll(country_name)
            if country:
                sleep(1)
                country.click()
                if state_name:
                    state, _ = self.try_find_map_with_scroll(state_name)
                    if state:
                        sleep(1)
                        state.click()
        city, _ = self.try_find_map_with_scroll(loc_name)

        els = self.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]//*[@type='XCUIElementTypeStaticText']".format(
                loc_name.get()))
        subtitle = els[1].text if len(els) == 4 else ""
        assert len(subtitle.split(",")) <= 3

        size = els[2] if len(els) == 4 or len(els) == 3 else els[1]

        assert "МБ" in size.text or "MB" in size.text

        self.press_back_until_main_page()

    def go_to_map(self, country_name, state_name, loc_name):
        self.try_get(Locator.MENU_BUTTON.get()).click()
        sleep(1)
        self.try_get(LocalizedButtons.DOWNLOAD_MAPS.get()).click()
        if country_name:
            country, _ = self.try_find_map_with_scroll(country_name)
            if country:
                sleep(1)
                country.click()
                if state_name:
                    state, _ = self.try_find_map_with_scroll(state_name)
                    if state:
                        sleep(1)
                        state.click()
        city, _ = self.try_find_map_with_scroll(loc_name)
