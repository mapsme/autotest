from time import sleep

import pytest
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.fixtures import execute_adb_command
from mapsmefr.steps.locators import LocalizedButtons, Locator, LocalizedSettings
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings


@pytest.mark.build_check
@pytest.mark.taxi
class TestTaxiMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main):
        pass

    @pytest.fixture
    def uninstall_taxi(self):
        execute_adb_command("adb -s {} shell pm uninstall {}".format(WebDriverManager.get_instance().device.device_id,
                                                                     get_settings("Tests", "partner_taxi")))

    @pytest.mark.name("Проверка перехода в приложение заказа такси")
    def test_taxi_not_installed(self, main, uninstall_taxi, steps, r_steps, system_steps):
        steps.search("Кунцевская")
        steps.choose_first_search_result()
        BottomPanel().to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        sleep(2)
        steps.try_get(Locator.ROUTING_TAXI.get()).click()
        assert steps.try_get(Locator.TAXI_VEZET.get())
        assert steps.try_get_by_text(LocalizedButtons.INSTALL_BUTTON.get())
        steps.try_get_by_text(LocalizedButtons.INSTALL_BUTTON.get()).click()

        if steps.try_get_by_text("Google Play", strict=False):
            steps.try_get_by_text("Google Play", strict=False).click()
            if steps.try_get_by_text(LocalizedSettings.ALWAYS.get()):
                steps.try_get_by_text(LocalizedSettings.ALWAYS.get()).click()

        sleep(3)
        steps.try_get_by_text(LocalizedButtons.INSTALL_BUTTON.get()).click()
        sleep(15)
        system_steps.restart_app()

        steps.press_back_until_main_page()

        steps.search("Кунцевская")
        steps.choose_first_search_result()
        BottomPanel().to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        sleep(2)
        steps.try_get(Locator.ROUTING_TAXI.get()).click()
        assert steps.try_get(Locator.TAXI_VEZET.get())
        assert steps.try_get_by_text(LocalizedButtons.ORDER_TAXI.get())
        steps.try_get_by_text(LocalizedButtons.ORDER_TAXI.get()).click()
        sleep(5)
        r_steps.assert_taxi_opened()
        r_steps.terminate_taxi_app()
