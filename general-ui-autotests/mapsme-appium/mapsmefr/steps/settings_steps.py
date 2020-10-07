import logging
import time
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
            self.scroll_down(small=True)
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
        setting, i = self.try_get_by_text(name, "android:id/title")

        while not setting:
            self.scroll_down(small=True)
            setting, i = self.try_get_by_text(name, "android:id/title")

        setting.click()
        sleep(3)
        self.try_get_by_text(value).click()
        logging.info("Choose settings {} value {}".format(name, value))

    def assert_radio(self, name, value):
        setting, i = self.try_get_by_text(name, "android:id/title")

        while not setting:
            self.scroll_down(small=True)
            setting, i = self.try_get_by_text(name, "android:id/title")

        setting.click()
        sleep(3)

        assert self.try_get_by_text(value).get_attribute("checked") == "true"
        self.driver.back()

    def assert_switch(self, name, value: bool):
        switch = self.try_get_by_xpath(
            "//*[@text='{}']/ancestor::*[@class='android.widget.LinearLayout'][1]//*[@resource-id='{}']".format(name,
                                                                                                                Locator.SWITCH.get()))
        while not switch:
            self.scroll_down(small=True)
            switch = self.try_get_by_xpath(
                "//*[@text='{}']/ancestor::*[@class='android.widget.LinearLayout'][1]//*[@resource-id='{}']"
                    .format(name, Locator.SWITCH.get()))

        on = switch.text.lower()
        cond = (value and on == LocalizedSettings.ON_WITH_DOT.get().lower()) or (
                    (not value) and on == LocalizedSettings.OFF_WITH_DOT.get().lower())
        assert cond

    def off_recent_track(self):
        setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        setting.click()
        off = self.try_get_by_text(LocalizedSettings.ON_WITH_DOT.get())
        if off:
            self.switch_settings(LocalizedSettings.ON_WITH_DOT.get(), False)
        sleep(2)
        self.driver.back()

    def on_recent_track(self):
        setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        setting.click()
        on = self.try_get_by_text(LocalizedSettings.OFF_WITH_DOT.get())
        if on:
            self.switch_settings(LocalizedSettings.OFF_WITH_DOT.get(), True)
            self.driver.back()
            self.choose_radio_settings(LocalizedSettings.RECENT_TRACK.get(), LocalizedSettings.ONE_HOUR.get())
        sleep(2)
        self.driver.back()

    def assert_recent_track_on(self):
        setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        setting.click()
        self.assert_switch(LocalizedSettings.ON_WITH_DOT.get(), True)
        self.driver.back()

    def assert_recent_track_off(self):
        setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.RECENT_TRACK.get())
        setting.click()
        self.assert_switch(LocalizedSettings.OFF_WITH_DOT.get(), False)
        self.driver.back()

    def on_voice_instructions(self):
        setting = self.try_get_by_text(LocalizedSettings.VOICE_INSTRUCTIONS.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.VOICE_INSTRUCTIONS.get())
        setting.click()
        on = self.try_get_by_text(LocalizedSettings.OFF_WITH_DOT.get())
        if on:
            self.switch_settings(LocalizedSettings.OFF_WITH_DOT.get(), True)
        self.choose_radio_settings(LocalizedSettings.VOICE_LANGUAGE.get(), "English")
        sleep(2)
        self.driver.back()

    def off_voice_instructions(self):
        setting = self.try_get_by_text(LocalizedSettings.VOICE_INSTRUCTIONS.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.VOICE_INSTRUCTIONS.get())
        setting.click()
        off = self.try_get_by_text(LocalizedSettings.ON_WITH_DOT.get())
        if off:
            self.switch_settings(LocalizedSettings.ON_WITH_DOT.get(), False)
        sleep(2)
        self.driver.back()

    def assert_voice_instructions_on(self):
        setting = self.try_get_by_text(LocalizedSettings.VOICE_INSTRUCTIONS.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.VOICE_INSTRUCTIONS.get())
        setting.click()
        self.assert_switch(LocalizedSettings.ON_WITH_DOT.get(), True)
        self.driver.back()

    def assert_voice_instructions_off(self):
        setting = self.try_get_by_text(LocalizedSettings.VOICE_INSTRUCTIONS.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.VOICE_INSTRUCTIONS.get())
        setting.click()
        self.assert_switch(LocalizedSettings.OFF_WITH_DOT.get(), False)
        self.driver.back()

    def get_version(self):
        timeout = time.time() + 180
        setting = self.try_get_by_text(LocalizedSettings.ABOUT.get())
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(LocalizedSettings.ABOUT.get())
            if time.time() > timeout:
                break
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

    def scroll_to_setting(self, setting_name):
        timeout = time.time() + 60
        setting = self.try_get_by_text(setting_name)
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_text(setting_name)
            if time.time() > timeout:
                break
        return setting

    def switch_speed_cameras(self, value):
        self.switch_settings(LocalizedSettings.SPEED_CAMERAS.get(), value)

    def assert_speed_cameras(self, value):
        self.assert_switch(LocalizedSettings.SPEED_CAMERAS.get(), value)


class IosSettingsSteps(SettingsSteps):

    @screenshotwrap("Открыть настройки")
    def open_settings(self):
        self.driver.find_element_by_id(Locator.MENU_BUTTON.get()).click()
        sleep(1)
        self.driver.find_element_by_id(LocalizedButtons.SETTINGS.get()).click()

    @check_not_crash
    @screenshotwrap("Переключить настройку")
    def switch_settings(self, name, value: bool, alt=None):
        timeout = time.time() + 60
        if alt:
            switch = self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeSwitch' and (@name='{}' or @name='{}')]".format(name, alt)) or self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[(@name='{}' or @name='{}')]]/*[@type='XCUIElementTypeSwitch']".format(name, alt))
            while not (switch and switch.get_attribute("visible") == "true"):
                self.scroll_down()
                switch = self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeSwitch' and (@name='{}' or @name='{}')]".format(name, alt)) or self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[(@name='{}' or @name='{}')]]/*[@type='XCUIElementTypeSwitch']".format(name, alt))
                if time.time() > timeout:
                    break
        else:
            switch = self.try_get_by_xpath("//*[@type='XCUIElementTypeSwitch' and @name='{}']".format(name)) or self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@type='XCUIElementTypeSwitch']".format(name))
            while not (switch and switch.get_attribute("visible") == "true"):
                self.scroll_down()
                switch = self.try_get_by_xpath("//*[@type='XCUIElementTypeSwitch' and @name='{}']".format(name)) or self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@type='XCUIElementTypeSwitch']".format(name))
                if time.time() > timeout:
                    break

        on = switch.text
        if on == "1" and not value:
            switch.click()
        if on == "0" and value:
            switch.click()
        logging.info("Switch settings {} to state {}".format(name, value))

    def scroll_to_setting(self, setting_name):
        timeout = time.time() + 60
        setting = self.try_get_by_xpath("//*[@type='XCUIElementTypeSwitch' and @name='{}']".format(setting_name))
        while not (setting and setting.get_attribute("visible") == "true"):
            self.scroll_down(small=True)
            setting = self.try_get_by_xpath("//*[@type='XCUIElementTypeSwitch' and @name='{}']".format(setting_name))
            if time.time() > timeout:
                break
        return setting

    @check_not_crash
    @screenshotwrap("Переключить настройку")
    def choose_radio_settings(self, name, value, alt=None):
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
        if alt:
            val = self.try_get(value) or self.try_get(alt)
        else:
            val = self.try_get(value)
        val.click()
        sleep(1)
        self.try_get(LocalizedButtons.SETTINGS.get()).click()
        logging.info("Choose settings {} value {}".format(name, value))

    def get_version(self):
        timeout = time.time() + 60
        setting = self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(LocalizedSettings.ABOUT.get()))

        while not (setting and setting.get_attribute("visible") == "true"):
            self.scroll_down()
            setting = self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(LocalizedSettings.ABOUT.get()))
            if time.time() > timeout:
                break

        setting.click()

        return self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeStaticText' and contains(@value,'Version') or contains(@value,'Версия')]").text

    def login_osm(self):
        self.try_get(Locator.LOGIN_OSM.get()).click()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").send_keys(get_settings("Tests", "osm_user"))
        self.try_get_by_xpath("//*[@type='XCUIElementTypeSecureTextField']").send_keys(
            get_settings("Tests", "osm_pass"))
        self.try_get(LocalizedButtons.LOG_IN_BTN.get()).click()

    def assert_radio(self, name, value):
        settings = self.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@type='XCUIElementTypeStaticText']".format(name))

        while len(settings) == 0:
            self.scroll_down(small=True)
            settings = self.driver.find_elements_by_xpath(
                "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@type='XCUIElementTypeStaticText']".format(
                    name))

        setting = settings[1]

        assert setting.text == value

    def assert_switch(self, name, value: bool, alt=None):
        timeout = time.time() + 60
        if alt:
            switch = self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeSwitch' and (@name='{}' or @name='{}')]".format(name, alt)) or self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[(@name='{}' or @name='{}')]]/*[@type='XCUIElementTypeSwitch']".format(
                        name, alt))
            while not (switch and switch.get_attribute("visible") == "true"):
                self.scroll_down()
                switch = self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeSwitch' and (@name='{}' or @name='{}')]".format(name,
                                                                                               alt)) or self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[(@name='{}' or @name='{}')]]/*[@type='XCUIElementTypeSwitch']".format(
                        name, alt))
                if time.time() > timeout:
                    break
        else:
            switch = self.try_get_by_xpath("//*[@type='XCUIElementTypeSwitch' and @name='{}']".format(name)) or self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@type='XCUIElementTypeSwitch']".format(
                        name))
            while not (switch and switch.get_attribute("visible") == "true"):
                self.scroll_down()
                switch = self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeSwitch' and @name='{}']".format(name)) or self.try_get_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@type='XCUIElementTypeSwitch']".format(
                        name))
                if time.time() > timeout:
                    break

        on = switch.text.lower()
        cond = (value and on == '1') or ((not value) and on == '0')
        assert cond

    def off_voice_instructions(self):
        setting = self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(LocalizedSettings.VOICE_INSTRUCTIONS.get()))
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                    LocalizedSettings.VOICE_INSTRUCTIONS.get()))
        setting.click()
        self.switch_settings(LocalizedSettings.VOICE_INSTRUCTIONS.get(), False)
        sleep(1)
        self.try_get(LocalizedButtons.SETTINGS.get()).click()

    def on_voice_instructions(self):
        setting = self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(LocalizedSettings.VOICE_INSTRUCTIONS.get()))
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                    LocalizedSettings.VOICE_INSTRUCTIONS.get()))
        setting.click()
        self.switch_settings(LocalizedSettings.VOICE_INSTRUCTIONS.get(), True)
        sleep(1)
        self.try_get(LocalizedButtons.SETTINGS.get()).click()

    def assert_voice_instructions_on(self):
        self.assert_radio(LocalizedSettings.VOICE_INSTRUCTIONS.get(), LocalizedSettings.ON_WITH_DOT.get())

    def assert_voice_instructions_off(self):
        self.assert_radio(LocalizedSettings.VOICE_INSTRUCTIONS.get(), LocalizedSettings.OFF_WITH_DOT.get())

    def assert_speed_cameras(self, value):
        setting = self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(LocalizedSettings.VOICE_INSTRUCTIONS.get()))
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                    LocalizedSettings.VOICE_INSTRUCTIONS.get()))
        setting.click()
        assert self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@name='checkmark']".format(value))
        self.try_get(LocalizedButtons.SETTINGS.get()).click()

    def switch_speed_cameras(self, value):
        setting = self.try_get_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(LocalizedSettings.VOICE_INSTRUCTIONS.get()))
        while not setting:
            self.scroll_down(small=True)
            setting = self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                    LocalizedSettings.VOICE_INSTRUCTIONS.get()))
        setting.click()
        self.switch_settings(LocalizedSettings.VOICE_INSTRUCTIONS.get(), True)
        val = self.try_get(value)
        val.click()
        sleep(1)
        self.try_get(LocalizedButtons.SETTINGS.get()).click()

    def off_recent_track(self):
        self.choose_radio_settings(LocalizedSettings.RECENT_TRACK.get(), LocalizedSettings.OFF.get(),
                                   alt=LocalizedSettings.RU_OFF.get())

    def on_recent_track(self, ):
        self.choose_radio_settings(LocalizedSettings.RECENT_TRACK.get(), LocalizedSettings.ONE_HOUR.get())

    def assert_recent_track_on(self):
        self.assert_radio(LocalizedSettings.RECENT_TRACK.get(), LocalizedSettings.ONE_HOUR.get())

    def assert_recent_track_off(self):
        self.assert_radio(LocalizedSettings.RECENT_TRACK.get(), LocalizedSettings.OFF.get())
