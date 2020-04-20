from time import sleep

import pytest
from PIL import Image
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.locators import LocalizedButtons, Locator, LocalizedMapsNames, LocalizedCategories, \
    LocalizedSettings
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import WebDriverException


@pytest.mark.regress1
class TestSettingsMapsme:

    @pytest.fixture
    def main(self, testitem, press_back_to_main):
        pass

    @pytest.yield_fixture
    def set_main_settings(self, settings_steps, steps):
        yield
        steps.press_back_until_main_page()
        settings_steps.open_settings()
        settings_steps.choose_radio_settings(LocalizedSettings.MEASUREMENT_UNITS.get(),
                                             LocalizedSettings.KILOMETERS.get())
        settings_steps.switch_settings(LocalizedSettings.ZOOM_BUTTONS.get(), True)
        settings_steps.switch_settings(LocalizedSettings.ON_3D.get(), True)
        settings_steps.switch_settings(LocalizedSettings.AUTO_DOWNLOAD.get(), True,
                                       alt=LocalizedSettings.DISABLE_AUTODOWNLOAD.get())
        settings_steps.switch_settings(LocalizedSettings.BOOKMARK_BACKUP.get(), False)
        settings_steps.switch_settings(LocalizedSettings.INSREASE_FONT.get(), False)
        settings_steps.switch_settings(LocalizedSettings.LATIN.get(), True)
        settings_steps.off_recent_track()
        settings_steps.switch_settings(LocalizedSettings.STATISTIC.get(), True)
        # settings_steps.switch_settings(LocalizedSettings.GOOGLE_PLAY_SERVICES.get(), True)
        settings_steps.choose_radio_settings(LocalizedSettings.POWER_SAVING_MODE.get(),
                                             LocalizedSettings.NEVER.get())
        settings_steps.choose_radio_settings(LocalizedSettings.NIGHT_MODE.get(), LocalizedSettings.AUTOMATICALLY.get())
        settings_steps.switch_settings(LocalizedSettings.PERSPECTIVE.get(), True)
        settings_steps.switch_settings(LocalizedSettings.AUTO_ZOOM.get(), True)
        settings_steps.switch_speed_cameras(LocalizedSettings.AUTO.get())
        steps.press_back_until_main_page()

    def test_settings_saving(self, main, steps, settings_steps, system_steps, set_main_settings):
        settings_steps.open_settings()
        settings_steps.choose_radio_settings(LocalizedSettings.MEASUREMENT_UNITS.get(), LocalizedSettings.MILES.get())
        settings_steps.switch_settings(LocalizedSettings.ZOOM_BUTTONS.get(), False)
        settings_steps.switch_settings(LocalizedSettings.ON_3D.get(), False)
        settings_steps.switch_settings(LocalizedSettings.AUTO_DOWNLOAD.get(), False,
                                       alt=LocalizedSettings.DISABLE_AUTODOWNLOAD.get())
        settings_steps.switch_settings(LocalizedSettings.BOOKMARK_BACKUP.get(), True)
        settings_steps.switch_settings(LocalizedSettings.INSREASE_FONT.get(), True)
        settings_steps.switch_settings(LocalizedSettings.LATIN.get(), False)
        settings_steps.on_recent_track()
        settings_steps.switch_settings(LocalizedSettings.STATISTIC.get(), False)
        #settings_steps.switch_settings(LocalizedSettings.GOOGLE_PLAY_SERVICES.get(), False)
        settings_steps.choose_radio_settings(LocalizedSettings.MOBILE_INTERNET.get(),
                                             LocalizedSettings.ALWAYS_ASK.get())
        settings_steps.choose_radio_settings(LocalizedSettings.POWER_SAVING_MODE.get(),
                                             LocalizedSettings.AUTOMATIC.get())
        settings_steps.choose_radio_settings(LocalizedSettings.NIGHT_MODE.get(), LocalizedSettings.OFF.get())
        settings_steps.switch_settings(LocalizedSettings.PERSPECTIVE.get(), False)
        settings_steps.switch_settings(LocalizedSettings.AUTO_ZOOM.get(), False)
        settings_steps.switch_speed_cameras(LocalizedSettings.NEVER.get())

        steps.press_back_until_main_page()
        system_steps.restart_app()

        settings_steps.open_settings()
        settings_steps.assert_radio(LocalizedSettings.MEASUREMENT_UNITS.get(), LocalizedSettings.MILES.get())
        #settings_steps.assert_switch(LocalizedSettings.ZOOM_BUTTONS.get(), False)
        settings_steps.assert_switch(LocalizedSettings.ON_3D.get(), False)
        settings_steps.assert_switch(LocalizedSettings.AUTO_DOWNLOAD.get(), False,
                                     alt=LocalizedSettings.DISABLE_AUTODOWNLOAD.get())
        settings_steps.assert_switch(LocalizedSettings.BOOKMARK_BACKUP.get(), True)
        settings_steps.assert_switch(LocalizedSettings.INSREASE_FONT.get(), True)
        settings_steps.assert_switch(LocalizedSettings.LATIN.get(), False)

        settings_steps.assert_recent_track_on()

        settings_steps.assert_switch(LocalizedSettings.STATISTIC.get(), False)
        #settings_steps.assert_switch(LocalizedSettings.GOOGLE_PLAY_SERVICES.get(), False)
        settings_steps.assert_radio(LocalizedSettings.MOBILE_INTERNET.get(),
                                    LocalizedSettings.ALWAYS_ASK.get())
        settings_steps.assert_radio(LocalizedSettings.POWER_SAVING_MODE.get(),
                                    LocalizedSettings.AUTOMATIC.get())
        settings_steps.assert_radio(LocalizedSettings.NIGHT_MODE.get(), LocalizedSettings.OFF.get())
        settings_steps.assert_switch(LocalizedSettings.PERSPECTIVE.get(), False)
        settings_steps.assert_switch(LocalizedSettings.AUTO_ZOOM.get(), False)

        settings_steps.assert_speed_cameras(LocalizedSettings.NEVER.get())

        settings_steps.off_voice_instructions()
        settings_steps.assert_voice_instructions_off()
