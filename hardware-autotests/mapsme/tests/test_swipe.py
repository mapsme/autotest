import logging
import random
import time

import pytest
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.steps.locators import LocalizedMapsNames, Locator
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings


class TestSwipeMapsme:

    @pytest.fixture(scope="class")
    def download_maps(self, request, steps):
        if request.config.getoption("--clean-device") == "true":
            steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW, LocalizedMapsNames.VORONEZH,
                               LocalizedMapsNames.LIPETSK, LocalizedMapsNames.MOSCOW_OBLAST, LocalizedMapsNames.TULA,
                               LocalizedMapsNames.NOVGOROD, LocalizedMapsNames.TVER, LocalizedMapsNames.YAROSLAVL)

    def test_swipe_map_randomly(self, testitem, check_diff, download_maps, um24c, memory_script, steps):
        time_in_minutes = get_settings('Tests', 'routing_time')
        timeout = time.time() + 60 * int(time_in_minutes)

        driver = WebDriverManager.get_instance().driver
        driver.implicitly_wait(0.5)
        actions = TouchAction(driver)
        win_size = driver.get_window_size()
        min_x = 100
        max_x = win_size["width"] - 100
        min_y = 100
        max_y = win_size["height"] - 100

        while time.time() <= timeout:
            random_x_1 = random.randint(min_x, max_x)
            random_y_1 = random.randint(min_y, max_y)

            random_x_2 = random.randint(min_x, max_x)
            random_y_2 = random.randint(min_y, max_y)

            actions.press(None, random_x_1, random_y_1).wait(500).move_to(None, random_x_2,
                                                                          random_y_2).release().perform()
            logging.info("Swipe from ({},{}) to ({},{})".format(random_x_1, random_y_1, random_x_2, random_y_2))

            download_map = steps.try_get(Locator.DOWNLOAD_MAP_BUTTON.get())
            if download_map:
                position = steps.try_get(Locator.GET_POSITION_LIGHT.get())
                if not position:
                    actions.tap(x=200, y=200).perform()
                    time.sleep(1)
                steps.try_get(Locator.GET_POSITION_LIGHT.get()).click()
                time.sleep(1)
            anchor = steps.try_get(Locator.PP_ANCHOR.get())
            if anchor:
                steps.scroll_up(from_el=anchor)
