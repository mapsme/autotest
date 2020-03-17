import csv
import time
from os.path import join, dirname, realpath

import pytest
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.locators import LocalizedMapsNames, LocalizedButtons, Locator, LocalizedSettings, \
    LocalizedCategories
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestRoutingMapsme:

    @pytest.fixture(scope="class")
    def download_maps(self, request, steps):
        if request.config.getoption("--clean-device") == "true":
            steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW, LocalizedMapsNames.VORONEZH,
                               LocalizedMapsNames.LIPETSK, LocalizedMapsNames.MOSCOW_OBLAST, LocalizedMapsNames.TULA)

    @pytest.yield_fixture()
    def turn_off_wifi(self, request, driver):
        if request.config.getoption("--clean-device") == "true":
            if get_settings("System", "platform") == "Android":
                try:
                    driver.set_network_connection(0)
                except:
                    driver.set_network_connection(1)
                yield
                try:
                    driver.set_network_connection(2)
                except:
                    driver.execute_script("mobile: shell", {'command': "am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings"})
                    time.sleep(1)
                    driver.execute_script("mobile: shell", {'command': "input keyevent 19"})
                    time.sleep(1)
                    driver.execute_script("mobile: shell", {'command': "input keyevent 23"})

            else:
                actions = TouchAction(driver)
                x = driver.get_window_size()['width'] / 2
                y_top = driver.get_window_size()['height']
                y_bot = driver.get_window_size()['height'] * 0.2
                actions.press(None, x, y_top).wait(500).move_to(None, x, y_bot).release().perform()
                wifi = driver.find_element_by_id("Wi-Fi")
                val = wifi.get_attribute("value")
                if val == "1":
                    wifi.click()
                    time.sleep(5)
                actions.press(None, x, driver.get_window_size()['height'] * 0.5).wait(500).move_to(None, x,
                                                                                                 y_top).release().perform()
                yield
                actions = TouchAction(driver)
                x = driver.get_window_size()['width'] / 2
                y_top = driver.get_window_size()['height']
                y_bot = driver.get_window_size()['height'] * 0.2
                actions.press(None, x, y_top).wait(500).move_to(None, x, y_bot).release().perform()
                wifi = driver.find_element_by_id("Wi-Fi")
                val = wifi.get_attribute("value")
                if val == "0":
                    wifi.click()
                    time.sleep(5)
                actions.press(None, x, driver.get_window_size()['height'] * 0.5).wait(500).move_to(None, x,
                                                                                                   y_top).release().perform()
        else:
            yield

    @pytest.fixture(scope="class")
    def force_stop(self):
        try:
            WebDriverManager.get_instance().driver.execute_script("mobile: shell", {
                "command": "am force-stop {}".format(get_settings("Android", "package"))})
            WebDriverManager.get_instance().driver.execute_script("mobile: shell", {
                'command': "am start {}/com.mapswithme.maps.SplashActivity".format(get_settings("Android", "package"))})
        except:
            pass

    @pytest.yield_fixture()
    def stop_routing(self, steps):
        yield
        steps.stop_routing()

    @pytest.fixture()
    def vulkan(self, steps):
        steps.search("?vulkan")
        WebDriverManager.get_instance().driver.execute_script("mobile: shell", {
            "command": "am force-stop {}".format(get_settings("Android", "package"))})
        WebDriverManager.get_instance().driver.execute_script("mobile: shell", {
            'command': "am start {}/com.mapswithme.maps.SplashActivity".format(get_settings("Android", "package"))})

    @pytest.fixture()
    def gl(self, steps):
        steps.search("?gl")
        WebDriverManager.get_instance().driver.execute_script("mobile: shell", {
            "command": "am force-stop {}".format(get_settings("Android", "package"))})
        WebDriverManager.get_instance().driver.execute_script("mobile: shell", {
            'command': "am start {}/com.mapswithme.maps.SplashActivity".format(get_settings("Android", "package"))})

    @pytest.fixture
    def main(self, testitem, check_diff, lockito, download_maps, press_back_to_main, um24c, memory_script):
        pass

    @pytest.yield_fixture()
    def off_3d(self, steps, settings_steps):
        settings_steps.open_settings()
        settings_steps.switch_settings(LocalizedSettings.ON_3D.get(), False)
        steps.press_back_until_main_page()
        yield
        steps.press_back_until_main_page()
        settings_steps.open_settings()
        settings_steps.switch_settings(LocalizedSettings.ON_3D.get(), True)
        steps.press_back_until_main_page()


    @pytest.yield_fixture()
    def off_perspective(self, steps, settings_steps):
        settings_steps.open_settings()
        settings_steps.switch_settings(LocalizedSettings.PERSPECTIVE.get(), False)
        steps.press_back_until_main_page()
        yield
        steps.press_back_until_main_page()
        settings_steps.open_settings()
        settings_steps.switch_settings(LocalizedSettings.PERSPECTIVE.get(), True)
        steps.press_back_until_main_page()

    @pytest.yield_fixture()
    def off_autozoom(self, steps, settings_steps):
        settings_steps.open_settings()
        settings_steps.switch_settings(LocalizedSettings.AUTO_ZOOM.get(), False)
        steps.press_back_until_main_page()
        yield
        steps.press_back_until_main_page()
        settings_steps.open_settings()
        settings_steps.switch_settings(LocalizedSettings.AUTO_ZOOM.get(), True)
        steps.press_back_until_main_page()

    @pytest.yield_fixture()
    def set_nightmode(self, steps, settings_steps):
        settings_steps.open_settings()
        settings_steps.choose_radio_settings(LocalizedSettings.NIGHT_MODE.get(), LocalizedSettings.ON.get())
        steps.press_back_until_main_page()
        yield
        steps.press_back_until_main_page()
        settings_steps.open_settings()
        settings_steps.choose_radio_settings(LocalizedSettings.NIGHT_MODE.get(), LocalizedSettings.AUTOMATICALLY.get())
        steps.press_back_until_main_page()

    def test_routing_auto_mode(self, main, steps, stop_routing):
        """ Москва - Воронеж:
            ночной режим - авто
            перспективный вид = да
            3D здания - да
            cпидкамеры - авто
            автозум - да
        """
        if get_settings("System", 'platform') == 'Android':
            self.android(steps)
        else:
            self.ios(steps)

    def test_routing_without_3d(self, main, steps, off_3d, stop_routing):
        if get_settings("System", 'platform') == 'Android':
            self.android(steps)
        else:
            self.ios(steps)

    def test_routing_without_perspective(self, main, steps, off_perspective, stop_routing):
        if get_settings("System", 'platform') == 'Android':
            self.android(steps)
        else:
            self.ios(steps)

    def test_routing_without_autozoom(self, main, steps, off_autozoom, stop_routing):
        if get_settings("System", 'platform') == 'Android':
            self.android(steps)
        else:
            self.ios(steps)

    def test_routing_with_night_mode(self, main, steps, set_nightmode, stop_routing):
        if get_settings("System", 'platform') == 'Android':
            self.android(steps)
        else:
            self.ios(steps)

    @pytest.mark.androidonly
    def test_routing_opengl(self, main, turn_off_wifi, gl, steps):
        self.android(steps)

    @pytest.mark.androidonly
    def test_routing_vulcan(self, main, turn_off_wifi, vulkan, steps):
        self.android(steps)

    def android(self, steps):
        panel = BottomPanel()
        steps.search("Воронеж")
        steps.choose_first_search_result()
        panel.to().click()

        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        WebDriverWait(WebDriverManager.get_instance().driver, 30).until(
            EC.visibility_of_element_located((By.ID, Locator.TIME.get())))

        start = steps.try_get_by_text(LocalizedButtons.START.get())
        start.click()

        time_in_minutes = get_settings('Tests', 'routing_time')
        timeout = time.time() + 60 * int(time_in_minutes)
        while time.time() <= timeout:
            time.sleep(60)
            try:
                WebDriverManager.get_instance().driver.location
            except:
                pass

    def ios(self, steps):
        panel = BottomPanel()
        steps.search("Воронеж")
        steps.choose_first_search_result(LocalizedCategories.CITY.get())
        panel.to().click()

        WebDriverWait(WebDriverManager.get_instance().driver, 60).until(
            EC.visibility_of_element_located((By.ID, Locator.START.get())))
        start = steps.try_get(Locator.START.get())
        start.click()

        el = steps.try_get(Locator.ACCEPT_BUTTON.get())
        if el:
            el.click()

        time_in_minutes = get_settings('Tests', 'routing_time')
        timeout = time.time() + 60 * int(time_in_minutes)

        with open(join(dirname(realpath(__file__)).split('mapsme')[0], 'coords.csv'), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                WebDriverManager.get_instance().driver.set_location(row[0], row[1], row[2])
                time.sleep(1)
                if time.time() > timeout:
                    break
