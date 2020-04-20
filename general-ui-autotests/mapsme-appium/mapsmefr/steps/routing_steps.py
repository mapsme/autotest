import string

from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.base_steps import AndroidSteps, IosSteps
from mapsmefr.steps.locators import LocalizedButtons, Locator
from mapsmefr.utils import expected_conditions as EC2
from mapsmefr.utils.driver import WebDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class RoutingSteps:

    def __init__(self):
        super().__init__()

    @staticmethod
    def get():
        if WebDriverManager.get_instance().device.platform == "Android":
            return AndroidRoutingSteps()
        else:
            return IosRoutingSteps()

    def assert_route_points(self, count, p2p=True, *points):
        pass

    def wait_taxi_panel(self):
        pass

    def wait_metro_panel(self):
        pass

    def download_additional_maps(self):
        pass

    def wait_route_start(self):
        pass

    def wait_route_too_long(self):
        pass

    def assert_taxi_install_button(self):
        pass

    def assert_route_type(self, route_type):
        pass


class AndroidRoutingSteps(RoutingSteps, AndroidSteps):
    def assert_route_points(self, count, p2p=True, *points):
        panel = BottomPanel()
        for point in [x for x in points if x is not None]:
            self.search(point)
            self.choose_first_search_result()
            assert panel.delete()
            el = self.driver.find_element_by_id(Locator.PP_ANCHOR.get())
            self.scroll_up(from_el=el)

    def wait_taxi_panel(self):
        WebDriverWait(self.driver, 180).until(EC2.presence_one_of_elements_located(
            (By.XPATH, "//*[@text='{}']".format(LocalizedButtons.TAXI_NOT_FOUND.get())),
            (By.XPATH, "//*[@text='{}']".format(LocalizedButtons.TAXI_NOT_AVAILABLE.get())),
            (By.ID, Locator.TAXI_VEZET.get())))

    def wait_metro_panel(self):
        WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.ID, Locator.ROUTE_METRO.get())))

    def assert_taxi_install_button(self):
        assert self.try_get_by_text(LocalizedButtons.INSTALL_BUTTON.get())

    def download_additional_maps(self):
        download = self.try_get_by_text(LocalizedButtons.DOWNLOAD_NOW_BUTTON.get())
        if download:
            download.click()
            in_progress = self.try_get(Locator.IN_PROGRESS_WHEEL.get())
            if in_progress:
                WebDriverWait(self.driver, 180).until(
                    EC2.element_to_be_dissapeared((By.ID, Locator.IN_PROGRESS_WHEEL.get())))

    def wait_route_start(self):
        timeout = 180
        if WebDriverManager.get_instance().device.platform_version <= "7.0":
            timeout = 300
        WebDriverWait(WebDriverManager.get_instance().driver, timeout).until(
            EC.visibility_of_element_located((By.ID, Locator.TIME.get())))

    def wait_route_too_long(self):
        WebDriverWait(self.driver, 60).until(
            EC2.presence_one_of_elements_located(
                (By.XPATH, "//*[@text='{}']".format(LocalizedButtons.ROUTE_TOO_LONG.get())),
                (By.XPATH, "//*[@text='{}']".format(LocalizedButtons.ROUTE_TO_TRANSPORT_TOO_LONG.get())),
                (By.XPATH, "//*[@text='{}']".format(LocalizedButtons.ROUTE_CLOSER.get()))))
        ok = self.try_get_by_text(LocalizedButtons.CANCELLATION.get()) or self.try_get_by_text(
            LocalizedButtons.OK.get())
        ok.click()

    def assert_route_type(self, route_type):
        assert self.try_get(route_type).get_attribute("checked") == "true"


class IosRoutingSteps(RoutingSteps, IosSteps):
    def assert_route_points(self, count, p2p=True, *points):
        metro = self.try_get(Locator.ROUTING_METRO.get())
        if metro:
            self.try_get(LocalizedButtons.MANAGE_ROUTE.get()).click()
            for point in points:
                assert self.try_get(point)
        else:
            if WebDriverManager.get_instance().device.platform_version >= "13":
                els = self.driver.find_elements_by_xpath(
                    "//*[@type='XCUIElementTypeCollectionView']/*[@type='XCUIElementTypeCell']")
                assert len(els) >= count * 4 + 3  # (count + 2) + count*2 + (count + 1)
            else:
                assert self.try_get(Locator.ROUTE_METRO.get())
                route_stop = "ic_route_manager_stop_{}"
                alphabet = string.ascii_lowercase
                for i in range(count):
                    assert self.try_get(route_stop.format(alphabet[i]))

    def wait_taxi_panel(self):
        WebDriverWait(self.driver, 180).until(EC2.presence_one_of_elements_located(
            (By.ID, Locator.TAXI_VEZET.get()), (By.ID, LocalizedButtons.TAXI_NOT_FOUND.get()),
            (By.ID, LocalizedButtons.TAXI_NOT_AVAILABLE.get())))

    def wait_metro_panel(self):
        WebDriverWait(self.driver, 180).until(EC2.element_to_be_dissapeared((By.ID, Locator.ROUTING_METRO.get())))
        if WebDriverManager.get_instance().device.platform_version >= "13":
            els = self.driver.find_elements_by_xpath(
                "//*[@type='XCUIElementTypeCollectionView']/*[@type='XCUIElementTypeCell']")
            assert len(els) >= 3
        else:
            WebDriverWait(self.driver, 180).until(
                EC.presence_of_element_located((By.ID, Locator.ROUTE_METRO.get())))

    def download_additional_maps(self):
        download = self.try_get(Locator.DOWNLOAD_NOW_BUTTON.get())
        if download:
            download.click()
            in_progress = self.try_get(Locator.IN_PROGRESS_WHEEL.get())
            if in_progress:
                WebDriverWait(self.driver, 180).until(
                    EC2.element_to_be_dissapeared((By.ID, Locator.IN_PROGRESS_WHEEL.get())))

    def wait_route_start(self):
        WebDriverWait(self.driver, 180).until(
            EC.visibility_of_element_located((By.ID, Locator.START.get())))

    def wait_route_too_long(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, LocalizedButtons.ROUTE_PLANNING_FAILED.get())))
        WebDriverWait(self.driver, 60).until(
            EC2.presence_one_of_elements_located((By.ID, LocalizedButtons.ROUTE_TOO_LONG.get()),
                                                 (By.ID, LocalizedButtons.ROUTE_TO_TRANSPORT_TOO_LONG.get()),
                                                 (By.ID, LocalizedButtons.ROUTE_CLOSER.get())))
        self.try_get(Locator.SEND.get()).click()

    def assert_taxi_install_button(self):
        assert self.try_get(LocalizedButtons.INSTALL_BUTTON.get())

    def assert_route_type(self, route_type):
        assert not self.try_get(route_type)
