from time import sleep, time

import pytest
from mapsmefr.steps.locators import LocalizedMapsNames, Locator, LocalizedButtons
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestSearchMapsme:

    @pytest.fixture(scope="class")
    def maps(self):
        return [
            {"country": LocalizedMapsNames.CZECH, "state": None, "city": LocalizedMapsNames.PRAGUE},
            {"country": LocalizedMapsNames.RUSSIA, "state": None, "city": LocalizedMapsNames.MOSCOW},
            {"country": LocalizedMapsNames.CHINA, "state": None, "city": LocalizedMapsNames.HEBEI},
            {"country": LocalizedMapsNames.GERMANY, "state": None, "city": LocalizedMapsNames.HAMBURG},
            {"country": LocalizedMapsNames.ARGENTINA, "state": None, "city": LocalizedMapsNames.BUENOS_AIRES}
        ]

    @pytest.fixture(scope="class")
    def download_maps(self, request, steps, maps):
        if request.config.getoption("--clean-device") == "true":
            for map in maps:
                steps.download_map(map["country"], map["state"], map["city"])

    def test_random_search(self, testitem, check_diff, download_maps, maps, um24c, memory_script, steps):
        time_in_minutes = get_settings('Tests', 'routing_time')
        big_timeout = time() + 60 * int(time_in_minutes)

        self.click_search(steps)
        self.click_categories(steps)

        all_categories = self.collect_categories(steps)

        steps.press_back_until_main_page()
        for map in maps:
            if time() > big_timeout:
                break
            steps.show_place_on_map(map["country"], map["state"], map["city"])
            sleep(1)

            for category in all_categories:
                if time() > big_timeout:
                    break
                self.click_search(steps)
                self.click_categories(steps)

                self.find_category_in_list(steps, category)

                steps.try_get(Locator.SHOW_ON_MAP.get()).click()

                for _ in range(5):
                    steps.try_get(Locator.ZOOM_IN.get()).click()
                    sleep(1)

                for _ in range(5):
                    steps.try_get(Locator.ZOOM_OUT.get()).click()
                    sleep(1)

                steps.try_get(Locator.SHOW_ON_MAP.get()).click()

                steps.press_back_until_main_page()

    def click_search(self, steps):
        steps.try_get(Locator.SEARCH_BUTTON.get()).click()
        sleep(2)
        WebDriverManager.get_instance().driver.hide_keyboard()

    def click_categories(self, steps):
        categories = steps.try_get_by_text(text=LocalizedButtons.SEARCH_CATEGORIES_TAB.get())
        if not categories:
            categories = steps.try_get(LocalizedButtons.SEARCH_CATEGORIES_TAB.get())
        categories.click()

    def collect_categories(self, steps):
        if get_settings("System", "platform") == "Android":
            return self.collect_categories_android(steps)
        else:
            return self.collect_categories_ios(steps)

    def collect_categories_android(self, steps):
        all_categories = set()
        for _ in range(3):
            categories = WebDriverManager.get_instance().driver.find_elements_by_xpath(
                "//*[@class='android.support.v7.widget.RecyclerView']/*")
            all_categories.update([x.text for x in categories])
            steps.scroll_down()
        return all_categories

    def collect_categories_ios(self, steps):
        all_categories = set()
        for _ in range(2):
            categories = WebDriverManager.get_instance().driver.find_elements_by_xpath(
                "//*[@type='XCUIElementTypeTable']//*[@type='XCUIElementTypeStaticText']")
            all_categories.update([x.text for x in categories])
            steps.scroll_down()
        return all_categories

    def find_category_in_list(self, steps, category_name):
        if get_settings("System", "platform") == "Android":
            return self.find_category_in_list_android(steps, category_name)
        else:
            return self.find_category_in_list_ios(steps, category_name)

    def find_category_in_list_android(self, steps, category_name):
        driver = WebDriverManager.get_instance().driver
        cat = steps.try_get_by_text(text=category_name)
        old_page_elements = [x.text for x in driver.find_elements_by_xpath("//*[@class='android.widget.TextView']")]
        new_page_elements = []
        timeout = time() + 60
        while not cat and old_page_elements != new_page_elements:
            old_page_elements = new_page_elements
            steps.scroll_down(small=True)
            cat = steps.try_get_by_text(text=category_name)
            new_page_elements = [x.text for x in driver.find_elements_by_xpath("//*[@class='android.widget.TextView']")]
            if time() > timeout:
                break
        steps.try_get_by_text(text=category_name).click()
        try:
            in_progress = driver.find_element_by_id(Locator.SEARCH_PROGRESS.get())
            WebDriverWait(driver, 120).until(EC.staleness_of(in_progress))
        except NoSuchElementException as nse:
            pass

    def find_category_in_list_ios(self, steps, category_name):
        driver = WebDriverManager.get_instance().driver
        cat = steps.try_get(category_name)
        old_page_elements = [x.text for x in driver.find_elements_by_xpath("//*[@type='XCUIElementTypeStaticText']")]
        new_page_elements = []
        timeout = time() + 60
        while not (cat and cat.get_attribute("visible") == 'true') and old_page_elements != new_page_elements:
            old_page_elements = new_page_elements
            steps.scroll_down(small=True)
            cat = steps.try_get(category_name)
            new_page_elements = [x.text for x in
                                 driver.find_elements_by_xpath("//*[@type='XCUIElementTypeStaticText']")]
            if time() > timeout:
                break
        sleep(1)
        steps.try_get(category_name).click()
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, Locator.SHOW_ON_MAP.get())))
        except TimeoutException as nse:
            steps.try_get(category_name).click()
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, Locator.SHOW_ON_MAP.get())))
