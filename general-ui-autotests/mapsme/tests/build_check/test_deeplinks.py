from time import sleep
from urllib import parse

import pytest
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.pageobjects.guides_catalog import GuidesCatalog
from mapsmefr.steps.locators import LocalizedMapsNames, LocalizedCategories, Locator, LocalizedButtons
from mapsmefr.steps.locators import PlatformDependantAttributes as attributes
from mapsmefr.utils.tools import get_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.build_check
@pytest.mark.deeplinks
@pytest.mark.releaseonly
class TestDeepLinksWithApp:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, download_moscow_map, press_back_to_main, restart_if_failed):
        pass

    @pytest.fixture
    def delete_guide(self, steps):
        if get_settings("System", "platform") == "IOS":
            BottomPanel().bookmarks().click()
            steps.try_get(LocalizedButtons.GUIDES.get().upper()).click()
            sleep(2)
            while steps.try_get("ic24PxMore"):
                steps.try_get("ic24PxMore").click()
                steps.try_get(LocalizedButtons.DELETE.get()).click()
                sleep(2)

    def create_url(self, base, params):
        return "{}?{}".format(base, parse.urlencode(params))

    @pytest.yield_fixture
    def restart_if_failed(self, request, system_steps, steps):
        yield
        status = True if request.node.rep_setup.passed and request.node.rep_call.passed else False
        if not status:
            system_steps.restart_app()
            steps.close_first_time_frame()
            steps.press_back_until_main_page()

    @pytest.mark.iosonly
    @pytest.mark.name("[Deeplinks] dlink.maps.me/map?")
    def test_deeplink_place_on_map(self, main, steps, system_steps):
        params = (("v", "1"),
                  ("ll", "55.702478,37.551932"),
                  ("n", "Point Name"),
                  ("id", "AnyStringOrEncodedUrl"),
                  ("backurl", "UrlToCallOnBackButton"),
                  ("appname", "TitleToDisplayInNavBar"))
        res = self.create_url("https://dlink.maps.me/map", params)
        system_steps.execute_deeplink_universal(res)
        steps.assert_pp("Point+Name")
        steps.assert_category_on_pp(LocalizedCategories.THEATRE.get())
        assert steps.try_get(Locator.ZOOM_OUT.get())
        assert steps.try_get(Locator.ZOOM_IN.get())

    @pytest.mark.name("[Deeplinks] Диплинк dlink.maps.me/search? поиск в списке")
    def test_deeplink_search_on_list(self, main, steps, system_steps, search_steps):
        steps.wait_map_auto_download(LocalizedMapsNames.MOSCOW.get())
        params = (("query", LocalizedCategories.SIGHTS.get()),
                  ("cll", "55.765601,37.605963"))
        res = self.create_url("https://dlink.maps.me/search", params)

        system_steps.execute_deeplink_universal(res)

        assert steps.try_get_by_xpath(
            "//*[contains(@{},'{}')]".format(attributes.TEXT_VALUE.get(), LocalizedCategories.SIGHTS.get()))

        assert steps.try_get(Locator.SHOW_ON_MAP.get())

        try:
            steps.driver.hide_keyboard()
        except:
            pass

        search_steps.assert_popular_sights_list()

    @pytest.mark.name("[Deeplinks] Диплинк dlink.maps.me/search? поиск на карте")
    def test_deeplink_search_on_map(self, main, steps, system_steps):
        steps.wait_map_auto_download(LocalizedMapsNames.MOSCOW.get())
        params = (("query", LocalizedCategories.SIGHTS.get()),
                  ("cll", "55.765601,37.605963"),
                  ("map", "")
                  )
        res = self.create_url("https://dlink.maps.me/search", params).replace("map=", "map")
        system_steps.execute_deeplink_universal(res)

        assert steps.try_get_by_xpath(
            "//*[contains(@{},'{}')]".format(attributes.TEXT_VALUE.get(), LocalizedCategories.SIGHTS.get()))

        assert steps.try_get(Locator.SHOW_ON_MAP.get()).text in (
        LocalizedButtons.LIST.get(), LocalizedButtons.LIST.get().upper())

        assert steps.try_get(Locator.ZOOM_OUT.get())
        assert steps.try_get(Locator.ZOOM_IN.get())

    @pytest.mark.name("[Deeplinks] Диплинк dlink.maps.me/route?")
    def test_deeplink_route(self, main, steps, r_steps, route_car, system_steps):
        steps.wait_map_auto_download(LocalizedMapsNames.MOSCOW.get())
        params = (
            ("sll", "55.765601,37.605963"),
            ("saddr", "PointA"),
            ("dll", "55.794248,37.553433"),
            ("daddr", "PointB"),
            ("type", "pedestrian")
        )
        res = self.create_url("https://dlink.maps.me/route", params)
        system_steps.execute_deeplink_universal(res)

        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        r_steps.wait_route_start()

        r_steps.assert_route_type(Locator.ROUTING_WALK.get())

        assert steps.try_get(Locator.ZOOM_OUT.get())
        assert steps.try_get(Locator.ZOOM_IN.get())

    @pytest.mark.name("[Deeplinks] Диплинк dlink.maps.me/catalogue?")
    def test_deeplink_catalogue(self, main, steps, delete_guide, system_steps):
        steps.wait_map_auto_download(LocalizedMapsNames.MOSCOW.get())
        params = (
            ("id", "06e2e2b3-2e01-43d2-be15-27e7370ae77b"),
            ("name", "Zagreb - a city of unusual museums and amazing nature scenery"),

        )
        res = self.create_url("https://dlink.maps.me/catalogue", params)
        system_steps.execute_deeplink_universal(res)

        WebDriverWait(steps.driver, 30).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@text='{0}' or @name='{0}']".format(LocalizedButtons.GUIDE_DOWNLOADED.get()))))

        steps.try_get(Locator.NOT_NOW.get()).click()

        try:
            GuidesCatalog().close().click()
        except:
            pass

    @pytest.mark.webview
    @pytest.mark.name("[Deeplinks] Диплинк dlink.maps.me/guides_page?")
    def test_deeplink_guides_page(self, main, steps, system_steps):
        steps.wait_map_auto_download(LocalizedMapsNames.MOSCOW.get())
        params = (
            ("url", "search/?tag=24&city=4611686018695784240"),
        )
        res = self.create_url("https://dlink.maps.me/guides_page", params)
        system_steps.execute_deeplink_universal(res)
        sleep(10)

        guides_page = GuidesCatalog()

        assert guides_page.navigation_bar_title()
        assert guides_page.filter_by_city().get_attribute(
            attributes.TEXT_VALUE.get()) == LocalizedMapsNames.AMSTERDAM.get()
        assert guides_page.filter_by_tag().get_attribute(attributes.TEXT_VALUE.get()) == LocalizedCategories.FOOD.get()

        guides_page.close()

    @pytest.mark.name("[Deeplinks] Диплинк через onelink на бесплатный маршрут с установленным ранее приложением")
    def test_deeplink_onelink_catalogue(self, main, steps, delete_guide, system_steps):
        steps.wait_map_auto_download(LocalizedMapsNames.MOSCOW.get())
        params = (
            ("pid", "mapsme_app"),
            ("is_retargeting", "true"),
            ("af_dp",
             "https://dlink.maps.me/catalogue?id=06e2e2b3-2e01-43d2-be15-27e7370ae77b&name=Zagreb+-+a+city+of+unusual+museums+and+amazing+nature+scenery"),
        )
        res = self.create_url("https://mapsme.onelink.me/LBgk", params)
        system_steps.execute_onelink_deeplink(res)

        WebDriverWait(steps.driver, 30).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@text='{0}' or @name='{0}']".format(LocalizedButtons.GUIDE_DOWNLOADED.get()))))

        steps.try_get(Locator.NOT_NOW.get()).click()

        try:
            GuidesCatalog().close().click()
        except:
            pass

    @pytest.mark.webview
    @pytest.mark.name("[Deeplinks] Диплинк через onelink на страницу в каталоге с установленным ранее приложением")
    def test_deeplink_onelink_guides_page(self, main, steps, system_steps):
        steps.wait_map_auto_download(LocalizedMapsNames.MOSCOW.get())
        params = (
            ("pid", "mapsme_app"),
            ("is_retargeting", "true"),
            ("af_dp", "https://dlink.maps.me/guides_page?url=search%2F%3Fcity%3D4611686018695784240%26tag%3D24"),
        )
        res = self.create_url("https://mapsme.onelink.me/LBgk", params)
        system_steps.execute_onelink_deeplink(res)
        sleep(10)

        guides_page = GuidesCatalog()

        assert guides_page.navigation_bar_title()
        assert guides_page.filter_by_city().get_attribute(
            attributes.TEXT_VALUE.get()) == LocalizedMapsNames.AMSTERDAM.get()
        assert guides_page.filter_by_tag().get_attribute(attributes.TEXT_VALUE.get()) == LocalizedCategories.FOOD.get()

        guides_page.close()
