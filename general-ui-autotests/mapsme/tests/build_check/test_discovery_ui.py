from time import sleep

import pytest
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.pageobjects.booking_filter_page import SearchFilter
from mapsmefr.pageobjects.discovery_page import DiscoveryPage
from mapsmefr.pageobjects.guides_catalog import GuidesCatalog
from mapsmefr.steps.base_steps import BookingSteps
from mapsmefr.steps.locators import LocalizedCategories, Locator, LocalizedButtons, LocalizedMapsNames
from mapsmefr.steps.locators import PlatformDependantAttributes as attributes
from mapsmefr.steps.routing_steps import RoutingSteps


@pytest.mark.build_check
@pytest.mark.discovery
@pytest.mark.regress1
@pytest.mark.night
class TestDiscoveryMapsme:

    @pytest.fixture
    def main(self, emulate_location_moscow, testitem, press_back_to_main, switch_to_native):
        pass

    @pytest.yield_fixture(scope="class")
    def b_steps(self):
        yield BookingSteps.get()

    @pytest.mark.releaseonly
    @pytest.mark.name("[Discovery] Отели: карточки, оценка, переход к PP, построение маршрута по 'Сюда', фильтр")
    def test_discovery_hotels(self, main, download_moscow_map, steps, b_steps):
        panel = BottomPanel()
        panel.discovery().click()
        page = DiscoveryPage()
        steps.scroll_down()
        hotel_name = page.first_hotel_name().text
        hotel_type = page.first_hotel_type().text
        steps.scroll_down()
        page.first_hotel_type().click()
        steps.assert_pp(hotel_name)
        steps.assert_category_on_pp(hotel_type)
        b_steps.scroll_down(from_el=b_steps.try_get(Locator.PP_ANCHOR.get()))
        assert b_steps.find_booking_button_on_pp(Locator.DETAILS_ON_BOOKING)
        steps.press_back_until_main_page()

        panel.discovery().click()
        steps.scroll_down()
        page.first_hotel_route_to().click()

        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        RoutingSteps().get().wait_route_start()

        steps.press_back_until_main_page()

        panel.discovery().click()
        steps.scroll_down()
        coord_y = page.first_hotel_name().location["y"]
        page.slide_left(coord_y, 3)
        page.click_more(coord_y)

        assert SearchFilter().check_out()

    @pytest.mark.name("[Discovery] Достопримечательности: карточка, популярность, построение маршрута по 'Сюда', поиск")
    def test_discovery_attractions(self, main, download_moscow_map, steps):
        panel = BottomPanel()
        panel.discovery().click()
        page = DiscoveryPage()
        sleep(5)

        attr_name = page.first_attraction_name().text
        attr_type = page.first_attraction_type().text

        assert page.first_attraction_popular()

        page.first_attraction_name().click()
        steps.assert_pp(attr_name)
        steps.assert_category_on_pp(attr_type)

        assert steps.try_get_by_text(LocalizedButtons.LEAVE_A_REVIEW.get(), strict=False) or steps.try_get_by_text(
            LocalizedButtons.LEAVE_A_REVIEW.get().upper(), strict=False)

        steps.press_back_until_main_page()

        try:
            BottomPanel().to()
            actions = TouchAction(steps.driver)
            coord_x = steps.driver.get_window_size()['width'] * 0.5
            coord_y = steps.driver.get_window_size()['height'] * 0.5
            actions.tap(None, coord_x, coord_y).perform()
            sleep(1)
            steps.press_back_until_main_page()
        except:
            pass

        panel.discovery().click()
        page.first_attraction_route_to().click()

        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        RoutingSteps().get().wait_route_start()

        steps.press_back_until_main_page()

        panel.discovery().click()
        coord_y = page.first_attraction_name().location["y"]
        page.slide_left(coord_y, 3)
        page.click_more(coord_y)

        assert steps.try_get_by_xpath(
            "//*[contains(@{},'{}')]".format(attributes.TEXT_VALUE.get(), LocalizedCategories.SIGHTS.get()))

    @pytest.mark.name("[Discovery] Перекусить: карточка, популярность, построение маршрута по 'Сюда', поиск")
    def test_discovery_eat_and_drink(self, main, download_moscow_map, steps, b_steps):
        panel = BottomPanel()

        panel.discovery().click()
        steps.scroll_down()
        page = DiscoveryPage()
        steps.scroll_down(small=True)
        sleep(2)

        eat_name = page.first_eat_name().text
        eat_type = page.first_eat_type().text

        assert page.first_eat_popular()

        page.first_eat_name().click()
        b_steps.scroll_down(from_el=b_steps.try_get(Locator.PP_ANCHOR.get()))

        steps.assert_pp(eat_name)
        steps.assert_category_on_pp(eat_type)

        assert steps.try_get_by_text(LocalizedButtons.LEAVE_A_REVIEW.get(), strict=False) or steps.try_get_by_text(
            LocalizedButtons.LEAVE_A_REVIEW.get().upper(), strict=False)

        steps.press_back_until_main_page()

        panel.discovery().click()
        steps.scroll_down()
        sleep(5)
        r_to = page.first_eat_route_to()
        sleep(1)
        r_to.click()

        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        RoutingSteps().get().wait_route_start()

        steps.press_back_until_main_page()

        panel.discovery().click()
        steps.scroll_down()
        sleep(5)
        coord_y = page.first_eat_name().location["y"]
        page.slide_left(coord_y, 3)
        page.click_more(coord_y)

        assert steps.try_get_by_xpath(
            "//*[contains(@{},'{}')]".format(attributes.TEXT_VALUE.get(), LocalizedCategories.WHERE_TO_EAT.get()))

    # i know this test is ugly af but i can't do anything with that at this point :(
    @pytest.mark.webview
    @pytest.mark.releaseonly
    @pytest.mark.name("[Discovery] Гиды: карточка, переход на профиль, переход по 'Ещё'")
    def test_discovery_guides(self, main, download_moscow_map, steps):
        panel = BottomPanel()
        panel.discovery().click()
        page = DiscoveryPage()
        sleep(5)

        guide_name = page.first_guide_name().text
        guide_type = page.first_guide_type().text
        page.first_guide_name().click()

        guides_page = GuidesCatalog()

        assert guides_page.navigation_bar_title()
        if len([x for x in steps.driver.contexts if x != "NATIVE_APP" and "chrome" not in x]) > 0:
            assert guides_page.guide_title().text == guide_name
            assert guides_page.guide_author().text == guide_type
        else:
            sleep(3)
            assert steps.try_get_by_text(guide_name)
            sleep(3)
            assert steps.try_get_by_text(guide_type, strict=False)

        guides_page.close().click()
        steps.press_back_until_main_page()

        panel.discovery().click()
        sleep(5)

        coord_y = page.first_guide_name().location["y"]
        page.slide_left(coord_y, 3)
        page.click_more(coord_y)

        assert guides_page.navigation_bar_title()
        if len([x for x in steps.driver.contexts if x != "NATIVE_APP" and "chrome" not in x]) > 0:
            assert guides_page.breadcrumbs_active_item().text == LocalizedMapsNames.MOSCOW.get()
        assert guides_page.see_all()

        guides_page.close().click()
