import logging
from time import sleep

from mapsmefr.steps.base_steps import CommonSteps, check_not_crash, screenshotwrap
from mapsmefr.steps.locators import Locator, LocalizedButtons, LocalizedSettings
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SettingsSteps(CommonSteps):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get():
        if WebDriverManager.get_instance().device.platform == "Android":
            return AndroidSettingsSteps()
        else:
            return IosSettingsSteps()

    def open_settings(self):
        pass

    def switch_settings(self, name, value: bool):
        pass

    def choose_radio_settings(self, name, value):
        pass

    def off_recent_track(self):
        pass

    def on_recent_track(self):
        pass

    def get_version(self):
        pass


class AndroidSettingsSteps(SettingsSteps):

    @check_not_crash
    @screenshotwrap("Открыть настройки")
    def open_settings(self):
        self._wait_in_progress()
        self.driver.find_element_by_id(Locator.MENU_BUTTON.get()).click()
        self.driver.find_element_by_id(Locator.SETTINGS.get()).click()

    @check_not_crash
    @screenshotwrap("Переключить настройку")
    def switch_settings(self, name, value: bool):
        switch = self.try_get_by_xpath(
            "//*[@text='{}']/ancestor::*[@class='android.widget.LinearLayout'][1]//*[@resource-id='{}']".format(name,
                                                                                                                Locator.SWITCH.get()))
        while not switch:
            self.scroll_down()
            switch = self.try_get_by_xpath(
                "//*[@text='{}']/ancestor::*[@class='android.widget.LinearLayout'][1]//*[@resource-id='{}']"
                    .format(name, Locator.SWITCH.get()))

        on = switch.text.lower()
        if on == LocalizedSettings.ON_WITH_DOT.get().lower() and not value:
            switch.click()
        if on == LocalizedSettings.OFF_WITH_DOT.get().lower() and value:
            switch.click()
        logging.info("Switch settings {} to state {}".format(name, value))

    @screenshotwrap("Переключить настройку")
    def choose_radio_settings(self, name, value):
        setting = self.try_get_by_text(name)

        while not setting:
            self.scroll_down()
            setting = self.try_get_by_text(name)

        setting.click()
        self.try_get_by_text(value).click()
        logging.info("Choose settings {} value {}".format(name, value))

    def off_recent_track(self):
        setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        setting.click()
        off = self.try_get_by_text(LocalizedSettings.ON_WITH_DOT.get())
        if off:
            self.switch_settings(LocalizedSettings.ON_WITH_DOT.get(), False)

    def on_recent_track(self):
        setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        setting.click()
        on = self.try_get_by_text(LocalizedSettings.OFF_WITH_DOT.get())
        if on:
            self.switch_settings(LocalizedSettings.OFF_WITH_DOT.get(), True)
        self.try_get_by_text(LocalizedSettings.ONE_HOUR.get()).click()

    def get_version(self):
        setting = self.try_get_by_text(LocalizedSettings.ABOUT.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.ABOUT.get())
        setting.click()
        return self.try_get("version").text

    @check_not_crash
    def _wait_in_progress(self):
        try:
            in_progress = self.driver.find_element_by_id(Locator.IN_PROGRESS.get())
            WebDriverWait(self.driver, 150).until(EC.staleness_of(in_progress))
        except NoSuchElementException as nse:
            pass

    def login_osm(self):
        self.try_get(Locator.LOGIN_OSM.get()).click()
        self.try_get(Locator.OSM_USERNAME_FIELD.get()).send_keys(get_settings("Tests", "osm_user"))
        self.try_get(Locator.OSM_PASSWORD_FIELD.get()).send_keys(get_settings("Tests", "osm_pass"))
        self.try_get(Locator.ENTER_OSM_BUTTON.get()).click()


class IosSettingsSteps(SettingsSteps):

    @screenshotwrap("Открыть настройки")
    def open_settings(self):
        self.driver.find_element_by_id(Locator.MENU_BUTTON.get()).click()
        sleep(1)
        self.driver.find_element_by_id(LocalizedButtons.SETTINGS.get()).click()

    @check_not_crash
    @screenshotwrap("Переключить настройку")
    def switch_settings(self, name, value: bool):
        switch = self.try_get_by_xpath("//*[@type='XCUIElementTypeSwitch' and @name='{}']".format(name))
        while not switch:
            self.scroll_down()
            switch = self.try_get_by_xpath("//*[@type='XCUIElementTypeSwitch' and @name='{}']".format(name))

        on = switch.text
        if on == "1" and not value:
            switch.click()
        if on == "0" and value:
            switch.click()
        logging.info("Switch settings {} to state {}".format(name, value))

    @check_not_crash
    @screenshotwrap("Переключить настройку")
    def choose_radio_settings(self, name, value):
        setting = self.try_get_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(name))

        while not (setting and setting.get_attribute("visible") == "true"):
            self.scroll_down()
            setting = self.try_get_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(name))

        # выглядит как набор нелогичных костылей
        # и это нормально
        # потому что это IOS

        sleep(3)
        setting.click()
        sleep(1)
        try:
            loc = setting.location
            if not (loc["x"] == 0 and loc["y"] == 0):
                setting.click()
        except WebDriverException:
            pass

        sleep(1)
        val = self.try_get(value)
        val.click()
        sleep(1)
        self.try_get(LocalizedButtons.BACK.get()).click()
        logging.info("Choose settings {} value {}".format(name, value))

    def get_version(self):
        setting = self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(LocalizedSettings.ABOUT.get()))

        while not (setting and setting.get_attribute("visible") == "true"):
            self.scroll_down()
            setting = self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(LocalizedSettings.ABOUT.get()))

        setting.click()

        return self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeStaticText' and contains(@value,'Version') or contains(@value,'Версия')]").text
