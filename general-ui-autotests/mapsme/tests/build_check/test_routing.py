import csv
import logging
import time
from os.path import join, dirname, realpath
from time import sleep

import pytest
from PIL import Image
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.locators import LocalizedButtons, Locator, LocalizedMapsNames, LocalizedCategories
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.regress1
class TestRoutingMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main, route_car):
        pass

    @pytest.yield_fixture
    def route_car(self, steps):
        if steps.try_get(LocalizedButtons.CANCELLATION.get()):
            steps.try_get(LocalizedButtons.CANCELLATION.get()).click()
        if steps.try_get_by_text(LocalizedButtons.OK.get()):
            steps.try_get_by_text(LocalizedButtons.OK.get()).click()
        if steps.try_get(Locator.ROUTING_CAR.get()):
            steps.try_get(Locator.ROUTING_CAR.get()).click()
            sleep(2)
        yield
        if steps.try_get(LocalizedButtons.CANCELLATION.get()):
            steps.try_get(LocalizedButtons.CANCELLATION.get()).click()
        if steps.try_get(Locator.ROUTING_CAR.get()):
            steps.try_get(Locator.ROUTING_CAR.get()).click()
            sleep(2)

    @pytest.mark.skip
    @pytest.mark.name(
        "[Routing][Car]Проверка выбора финиша выбором букмарки (кнопка слева) и на PP нажатием на кнопку Route To")
    def test_auto_routing_bookmark(self, main, download_moscow_map, steps, r_steps, bookmark_steps):
        panel = BottomPanel()
        bookmark_steps.delete_all_groups()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), "проспект Мира, 78")
        bookmark_name = "проспект Мира, 78"
        bookmark_steps.create_bookmark(bookmark_name)
        panel.bookmarks().click()
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        bookmark = bookmark_steps.try_find_bookmark_with_scroll(bookmark_name)
        sleep(1)
        bookmark.click()
        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        r_steps.wait_route_start()

    @pytest.mark.skip
    @pytest.mark.name(
        "[Routing][Walk]Проверка выбора финиша выбором букмарки (кнопка слева) и на PP нажатием на кнопку Route To")
    def test_walk_routing_bookmark(self, main, download_moscow_map, steps, r_steps, bookmark_steps):
        panel = BottomPanel()
        bookmark_steps.delete_all_groups()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), "проспект Мира, 78")
        bookmark_name = "проспект Мира, 78"
        bookmark_steps.create_bookmark(bookmark_name)
        steps.search("метро Алексеевская")

        steps.choose_first_search_result()
        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        steps.try_get(Locator.ROUTING_WALK.get()).click()
        r_steps.wait_route_start()
        steps.press_back_until_main_page()
        panel.bookmarks().click()
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        bookmark = bookmark_steps.try_find_bookmark_with_scroll(bookmark_name)
        sleep(1)
        bookmark.click()
        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        r_steps.wait_route_start()
        assert not steps.try_get(Locator.ROUTING_WALK.get())

    @pytest.mark.skip
    @pytest.mark.name(
        "[Routing][Bike]Проверка выбора финиша выбором букмарки (кнопка слева) и на PP нажатием на кнопку Route To")
    def test_bike_routing_bookmark(self, main, download_moscow_map, steps, r_steps, bookmark_steps):
        panel = BottomPanel()
        bookmark_steps.delete_all_groups()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), "проспект Мира, 78")
        bookmark_name = "проспект Мира, 78"
        bookmark_steps.create_bookmark(bookmark_name)
        steps.search("метро Алексеевская")

        steps.choose_first_search_result()
        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        steps.try_get(Locator.ROUTING_BIKE.get()).click()
        r_steps.wait_route_start()
        steps.press_back_until_main_page()
        panel.bookmarks().click()
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        bookmark = bookmark_steps.try_find_bookmark_with_scroll(bookmark_name)
        sleep(1)
        bookmark.click()
        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        r_steps.wait_route_start()
        assert not steps.try_get(Locator.ROUTING_BIKE.get())

    @pytest.mark.skip
    @pytest.mark.build_check
    @pytest.mark.name("[Routing][Car] My position авто с 3 промежуточными точками и несколькими mwm и началом движения")
    def test_routing_auto(self, main, download_moscow_map, steps, r_steps):
        """ Текущее местоположение -> метро Сокол -> метро Беляево -> Сергиев-Посад -> метро Алексеевская """
        steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW)
        panel = BottomPanel()
        steps.search("метро Алексеевская")
        steps.choose_first_search_result()

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.search("метро Сокол")
        steps.choose_first_search_result()

        r_steps.click_add_stop()

        steps.search("метро Беляево")
        steps.choose_first_search_result()

        r_steps.click_add_stop()

        steps.search("Сергиев-Посад")
        steps.choose_first_search_result()
        r_steps.click_add_stop()

        r_steps.download_additional_maps()
        r_steps.wait_route_start()

    @pytest.mark.build_check
    @pytest.mark.name(
        "[Routing][Bike] My position вело с 3 промежуточными точками и несколькими mwm и началом движения")
    def test_routing_bike(self, main, download_moscow_map, steps, r_steps):
        """ Текущее местоположение -> метро Сокол -> метро Беляево -> Сергиев-Посад -> метро Алексеевская """
        panel = BottomPanel()
        steps.search("метро Алексеевская")
        steps.choose_first_search_result()

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.search("метро Сокол")
        steps.choose_first_search_result()

        r_steps.click_add_stop()

        steps.search("метро Беляево")
        steps.choose_first_search_result()

        r_steps.click_add_stop()

        steps.search("Сергиев-Посад")
        steps.choose_first_search_result()
        r_steps.click_add_stop()

        r_steps.download_additional_maps()

        steps.try_get(Locator.ROUTING_BIKE.get()).click()
        r_steps.wait_route_start()

    @pytest.mark.build_check
    @pytest.mark.name(
        "[Routing][Walk] My position пеший с 3 промежуточными точками и несколькими mwm и началом движения")
    def test_routing_walk(self, main, download_moscow_map, steps, r_steps):
        """ Текущее местоположение -> метро Сокол -> метро Беляево -> Сергиев-Посад -> метро Алексеевская """
        panel = BottomPanel()
        steps.search("метро Алексеевская")
        steps.choose_first_search_result()

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.search("метро Сокол")
        steps.choose_first_search_result()

        r_steps.click_add_stop()
        r_steps.wait_route_start()

        steps.search("метро Беляево")
        steps.choose_first_search_result()

        r_steps.click_add_stop()
        r_steps.wait_route_start()

        steps.search("Сергиев-Посад")
        steps.choose_first_search_result()
        r_steps.click_add_stop()

        r_steps.download_additional_maps()
        r_steps.wait_route_start()

        steps.try_get(Locator.ROUTING_WALK.get()).click()
        r_steps.wait_route_start()

    @pytest.mark.build_check
    @pytest.mark.name("[Routing][Subway] P2P общественный внутри mwm с метро (Динамо - Технопарк)")
    def test_routing_metro_one_map(self, main, download_moscow_map, steps, r_steps):
        """ Метро Динамо -> метро Технопарк """
        panel = BottomPanel()
        steps.search("метро Динамо")
        steps.choose_first_search_result()

        panel.route_from().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("метро Технопарк", click_search_button=False)
        steps.choose_first_search_result()
        r_steps.wait_route_start()

        steps.try_get(Locator.ROUTING_METRO.get()).click()

        r_steps.wait_metro_panel()

        steps.press_back_until_main_page()

        steps.search("метро Динамо")
        steps.choose_first_search_result()

        panel.route_from().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("метро Технопарк", click_search_button=False)
        steps.choose_first_search_result()
        r_steps.wait_metro_panel()

    @pytest.mark.build_check
    @pytest.mark.name("[Routing][Subway] P2P общественный между mwm с и без метро (Динамо - Чехов)")
    def test_routing_metro_two_maps(self, main, download_moscow_map, steps, r_steps):
        """ Метро Динамо -> Чехов. Ожидается ошибка построения маршрута
        https://testrail.corp.mail.ru/index.php?/tests/view/36653589"""
        panel = BottomPanel()
        steps.search("метро Динамо")
        steps.choose_first_search_result()

        panel.route_from().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()

        steps.search("Чехов", click_search_button=False)
        steps.choose_first_search_result()

        r_steps.download_additional_maps()

        steps.try_get(Locator.ROUTING_METRO.get()).click()
        r_steps.wait_route_too_long()

    @pytest.mark.build_check
    @pytest.mark.name("[Routing][Taxi] P2P такси")
    def test_routing_taxi_p2p(self, main, download_moscow_map, steps, r_steps):
        """Метро Строгино -> метро Алексеевская"""
        panel = BottomPanel()
        steps.search("метро Строгино")
        steps.choose_first_search_result()

        sleep(1)
        panel.route_from().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("метро Алексеевская", click_search_button=False)
        steps.choose_first_search_result()

        sleep(2)
        steps.try_get(Locator.ROUTING_TAXI.get()).click()
        r_steps.wait_taxi_panel()
        r_steps.assert_taxi_install_button()

    @pytest.mark.build_check
    @pytest.mark.name("[Routing][Taxi] My position Такси с PP сюда с определённым местоположением")
    def test_routing_taxi_route_to(self, main, download_moscow_map, steps, r_steps):
        """Текущее местоположение -> метро Алексеевская"""
        panel = BottomPanel()
        steps.search("метро Алексеевская")
        steps.choose_first_search_result()

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        sleep(2)
        steps.try_get(Locator.ROUTING_TAXI.get()).click()
        r_steps.wait_taxi_panel()

    @pytest.mark.build_check
    @pytest.mark.name(
        "[Routing][Car-Taxi] Сохранение промежуточных точек при переходе из авто в такси и с возвратом обратно")
    def test_routing_auto_taxi_back(self, main, download_moscow_map, steps, r_steps, search_steps):
        """Метро Динамо -> метро Сокол ->  метро Беляево -> метро Алексеевская
        https://testrail.corp.mail.ru/index.php?/tests/view/36653927"""
        panel = BottomPanel()
        points = []
        if get_settings("System", "platform") == "Android":
            points = ["метро Сокол", "метро Беляево"]
        steps.search("метро Динамо")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        panel.route_from().click()

        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("метро Алексеевская", click_search_button=False)
        points.append(search_steps.get_first_search_name())
        steps.choose_first_search_result()
        sleep(1)

        steps.search("метро Сокол")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())
        r_steps.click_add_stop()

        sleep(1)

        steps.search("метро Беляево")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())
        r_steps.click_add_stop()

        r_steps.wait_route_start()

        sleep(1)
        steps.try_get(Locator.ROUTING_TAXI.get()).click()

        r_steps.wait_taxi_panel()

        steps.try_get(Locator.ROUTING_CAR.get()).click()

        r_steps.assert_route_points(2, True, *points)

    @pytest.mark.name(
        "[Routing][Bike-Taxi] Сохранение промежуточных точек при переходе из вело в такси и с возвратом обратно")
    def test_routing_bike_taxi_back(self, main, download_moscow_map, steps, r_steps, search_steps):
        """Метро Динамо -> метро Сокол ->  метро Беляево -> метро Алексеевская"""
        panel = BottomPanel()
        points = []
        if get_settings("System", "platform") == "Android":
            points = ["метро Сокол", "метро Беляево"]
        steps.search("метро Динамо")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        panel.route_from().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("метро Алексеевская", click_search_button=False)
        points.append(search_steps.get_first_search_name())
        steps.choose_first_search_result()

        steps.search("метро Сокол")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        r_steps.click_add_stop()

        steps.search("метро Беляево")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        r_steps.click_add_stop()

        steps.try_get(Locator.ROUTING_BIKE.get()).click()

        r_steps.wait_route_start()

        sleep(1)
        steps.try_get(Locator.ROUTING_TAXI.get()).click()
        r_steps.wait_taxi_panel()

        steps.try_get(Locator.ROUTING_BIKE.get()).click()
        r_steps.wait_route_start()

        r_steps.assert_route_points(2, True, *points)

    @pytest.mark.name(
        "[Routing][Walk-Taxi] Сохранение промежуточных точек при переходе из пешего в такси и с возвратом обратно")
    def test_routing_walk_taxi_back(self, main, download_moscow_map, steps, r_steps, search_steps):
        """Метро Динамо -> метро Сокол ->  метро Беляево -> метро Алексеевская"""
        panel = BottomPanel()
        points = []
        if get_settings("System", "platform") == "Android":
            points = ["метро Сокол", "метро Беляево"]
        steps.search("метро Динамо")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        panel.route_from().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("метро Алексеевская", click_search_button=False)
        points.append(search_steps.get_first_search_name())
        steps.choose_first_search_result()

        steps.search("метро Сокол")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        r_steps.click_add_stop()

        sleep(1)

        steps.search("метро Беляево")

        sleep(1)

        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        r_steps.click_add_stop()

        steps.try_get(Locator.ROUTING_WALK.get()).click()

        r_steps.wait_route_start()

        sleep(1)
        steps.try_get(Locator.ROUTING_TAXI.get()).click()
        r_steps.wait_taxi_panel()

        steps.try_get(Locator.ROUTING_WALK.get()).click()

        r_steps.wait_route_start()

        r_steps.assert_route_points(2, True, *points)

    @pytest.mark.name(
        "[Routing][Subway-Taxi] Сохранение промежуточных точек при переходе из общественного транспорта в такси и с возвратом обратно")
    def test_routing_metro_taxi_back(self, main, download_moscow_map, steps, r_steps, search_steps):
        """Метро Динамо -> метро Парк Победы ->  метро Строгино -> метро Алексеевская"""
        panel = BottomPanel()
        points = []
        if get_settings("System", "platform") == "Android":
            points = ["метро Парк Победы", "метро Строгино"]
        steps.search("метро Динамо")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        panel.route_from().click()

        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("метро Алексеевская", click_search_button=False)
        points.append(search_steps.get_first_search_name())

        sleep(1)
        steps.choose_first_search_result()

        steps.search("метро Парк Победы")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        r_steps.click_add_stop()

        steps.search("метро Строгино")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        r_steps.click_add_stop()

        steps.try_get(Locator.ROUTING_METRO.get()).click()

        r_steps.wait_metro_panel()

        r_steps.assert_route_points(2, True, *points)

        sleep(1)
        steps.try_get(Locator.ROUTING_TAXI.get()).click()
        r_steps.wait_taxi_panel()

        steps.try_get(Locator.ROUTING_METRO.get()).click()

        r_steps.wait_metro_panel()

        r_steps.assert_route_points(2, True, *points)

    @pytest.mark.name("[Routing][ios only] Планировщик маршрута")
    @pytest.mark.iosonly
    @pytest.mark.build_check
    def test_route_manager(self, main, download_moscow_map, steps, r_steps, search_steps):
        """Метро Динамо -> метро Парк Победы ->  метро Строгино -> метро Алексеевская"""
        panel = BottomPanel()
        points = []
        steps.search("метро Динамо")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        panel.route_from().click()

        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("метро Алексеевская", click_search_button=False)
        points.append(search_steps.get_first_search_name())

        sleep(1)
        steps.choose_first_search_result()

        steps.search("метро Парк Победы")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        r_steps.click_add_stop()

        steps.search("метро Строгино")
        steps.choose_first_search_result()
        points.append(steps.pp_get_title())

        r_steps.click_add_stop()

        steps.try_get(LocalizedButtons.MANAGE_ROUTE.get()).click()

        stop_a = steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']")[1]
        stop_a_name = stop_a.find_element_by_xpath("./*[@type='XCUIElementTypeStaticText']").text
        coords_a = stop_a.find_elements_by_xpath("./*[@type='XCUIElementTypeImage']")[1].location

        stop_start = steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']")[0]
        stop_start_name = stop_start.find_element_by_xpath("./*[@type='XCUIElementTypeStaticText']").text

        stop_b = steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']")[2]
        stop_b_name = stop_b.find_element_by_xpath("./*[@type='XCUIElementTypeStaticText']").text

        stop_finish = steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']")[3]
        stop_finish_name = stop_finish.find_element_by_xpath("./*[@type='XCUIElementTypeStaticText']").text
        coords_finish = stop_finish.find_elements_by_xpath("./*[@type='XCUIElementTypeImage']")[1].location

        actions = TouchAction(steps.driver)

        try:
            actions.press(None, coords_a["x"], coords_a["y"]) \
                .wait(4000).move_to(None, coords_finish["x"],
                                    coords_finish["y"]).release().perform()
        except WebDriverException:
            pass

        steps.try_get(LocalizedButtons.PLAN.get()).click()
        sleep(5)

        steps.try_get(LocalizedButtons.MANAGE_ROUTE.get()).click()

        stop_start = steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']")[0]
        assert stop_start_name == stop_start.find_element_by_xpath("./*[@type='XCUIElementTypeStaticText']").text

        stop_a = steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']")[1]
        assert stop_b_name == stop_a.find_element_by_xpath("./*[@type='XCUIElementTypeStaticText']").text

        stop_b = steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']")[2]
        assert stop_finish_name == stop_b.find_element_by_xpath("./*[@type='XCUIElementTypeStaticText']").text

        stop_finish = steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']")[3]
        assert stop_a_name == stop_finish.find_element_by_xpath("./*[@type='XCUIElementTypeStaticText']").text

    @pytest.mark.name("[Routing][Car] Проверка ограничения на максимальное количество промежуточных точек (3 шт)")
    def test_routing_auto_stops_limit(self, main, steps, r_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653637"""
        panel = BottomPanel()
        steps.search("метро Алексеевская")
        steps.choose_first_search_result()

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.search("метро Сокол")
        steps.choose_first_search_result()

        panel.add_stop().click()

        steps.search("метро Беляево")
        steps.choose_first_search_result()

        panel.add_stop().click()

        steps.search("метро Тульская")
        steps.choose_first_search_result()
        panel.add_stop().click()

        steps.search("метро Сокольники")
        steps.choose_first_search_result()

        assert panel.add_stop() is None

    @pytest.mark.name("[Routing][Walk] Проверка ограничения на максимальное количество промежуточных точек (3 шт)")
    def test_routing_walk_stops_limit(self, main, steps, r_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653637"""
        panel = BottomPanel()
        steps.search("метро Алексеевская")
        steps.choose_first_search_result()

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.try_get(Locator.ROUTING_WALK.get()).click()

        steps.search("метро Сокол")
        steps.choose_first_search_result()

        panel.add_stop().click()

        steps.search("метро Беляево")
        steps.choose_first_search_result()

        panel.add_stop().click()

        steps.search("метро Тульская")
        steps.choose_first_search_result()
        panel.add_stop().click()

        r_steps.wait_route_start()

        steps.search("метро Сокольники")
        steps.choose_first_search_result()
        assert panel.add_stop() is None

    @pytest.mark.name("[Routing][Bike] Проверка ограничения на максимальное количество промежуточных точек (3 шт)")
    def test_routing_bike_stops_limit(self, main, steps, r_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653637"""
        panel = BottomPanel()
        steps.search("метро Алексеевская")
        steps.choose_first_search_result()

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        steps.try_get(Locator.ROUTING_BIKE.get()).click()

        steps.search("метро Сокол")
        steps.choose_first_search_result()

        panel.add_stop().click()

        steps.search("метро Беляево")
        steps.choose_first_search_result()

        panel.add_stop().click()

        steps.search("метро Тульская")
        steps.choose_first_search_result()
        panel.add_stop().click()

        r_steps.wait_route_start()

        steps.search("метро Сокольники")
        steps.choose_first_search_result()
        assert panel.add_stop() is None

    @pytest.mark.name("[Routing][Car] Грунтовые и платные дороги")
    def test_routing_pay_and_bad_roads_only_auto(self, main, steps, r_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653881"""
        steps.download_map(LocalizedMapsNames.GREAT_BRITAIN, None, LocalizedMapsNames.LONDON)
        panel = BottomPanel()
        steps.search("метро Алексеевская")
        steps.choose_first_search_result()

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        r_steps.wait_route_start()

        assert steps.try_get(Locator.DRIVING_OPTIONS.get()) is None or steps.try_get(
            Locator.DRIVING_OPTIONS.get()).get_attribute("visible") == 'false'

        steps.press_back_until_main_page()
        steps.search("Compton Park")
        steps.choose_first_search_result(category=LocalizedCategories.PARK.get())

        panel.route_from().click()
        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("Errol Street", click_search_button=False)
        steps.choose_first_search_result()
        r_steps.wait_route_start()
        steps.try_get(Locator.DRIVING_OPTIONS.get()).click()
        sleep(2)
        steps.driver.back()

        steps.try_get(Locator.ROUTING_BIKE.get()).click()
        r_steps.wait_route_start()
        assert steps.try_get(Locator.DRIVING_OPTIONS.get()) is None or steps.try_get(
            Locator.DRIVING_OPTIONS.get()).get_attribute("visible") == 'false'

        steps.try_get(Locator.ROUTING_WALK.get()).click()
        r_steps.wait_route_start()
        assert steps.try_get(Locator.DRIVING_OPTIONS.get()) is None or steps.try_get(
            Locator.DRIVING_OPTIONS.get()).get_attribute("visible") == 'false'

        steps.try_get(Locator.ROUTING_METRO.get()).click()
        r_steps.wait_metro_panel()
        assert steps.try_get(Locator.DRIVING_OPTIONS.get()) is None or steps.try_get(
            Locator.DRIVING_OPTIONS.get()).get_attribute("visible") == 'false'

        steps.try_get(Locator.ROUTING_TAXI.get()).click()
        r_steps.wait_taxi_panel()
        assert steps.try_get(Locator.DRIVING_OPTIONS.get()) is None or steps.try_get(
            Locator.DRIVING_OPTIONS.get()).get_attribute("visible") == 'false'

    @pytest.mark.name("[Routing][Car] Платные дороги")
    def test_toll_roads(self, main, steps, r_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653882
        https://testrail.corp.mail.ru/index.php?/tests/view/36653900"""
        panel = BottomPanel()
        steps.search("Воронеж")
        steps.choose_first_search_result(category=LocalizedCategories.CITY.get())

        panel.to().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()

        r_steps.download_additional_maps()
        r_steps.wait_route_start()
        steps.try_get(Locator.ZOOM_IN.get()).click()

        assert steps.try_get(Locator.DRIVING_OPTIONS.get())
        sleep(5)

        filename = "toll_road.png"
        steps.driver.get_screenshot_as_file(filename)
        coor = self.get_coords_proportions(filename)
        TouchAction(steps.driver).tap(x=round(coor[0] * steps.driver.get_window_size()["width"]),
                                      y=round(coor[1] * steps.driver.get_window_size()["height"])).perform()

        assert steps.try_get_by_text(LocalizedButtons.AVOID_TOLL_ROADS.get())
        assert steps.try_get_by_text(LocalizedButtons.TOLL_ROAD.get(), strict=False)

    @pytest.mark.name("[Routing][Car] Грунтовые дороги")
    def test_unpaved_roads(self, main, steps, r_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653901"""
        steps.download_map(LocalizedMapsNames.SPAIN, None, LocalizedMapsNames.SEVILLE)
        panel = BottomPanel()
        steps.press_back_until_main_page()
        steps.search("P.N. Los Alcornocales")
        steps.choose_first_search_result()

        panel.route_from().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("Sierra de Ojen", click_search_button=False)
        steps.choose_first_search_result()

        r_steps.download_additional_maps()
        r_steps.wait_route_start()
        steps.try_get(Locator.ZOOM_IN.get()).click()

        assert steps.try_get(Locator.DRIVING_OPTIONS.get())
        sleep(5)

        filename = "unpaved_road.png"
        steps.driver.get_screenshot_as_file(filename)
        coor = self.get_coords_proportions(filename)
        TouchAction(steps.driver).tap(x=round(coor[0] * steps.driver.get_window_size()["width"]),
                                      y=round(coor[1] * steps.driver.get_window_size()["height"])).perform()

        assert steps.try_get_by_text(LocalizedButtons.AVOID_UNPAVED_ROADS.get())
        assert steps.try_get_by_text(LocalizedButtons.UNPAVED_ROAD.get(), strict=False)

    @pytest.mark.name("[Routing][Car] Паромные переправы")
    def test_ferry_roads(self, main, steps, r_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653902"""
        steps.download_map(LocalizedMapsNames.ITALY, None, LocalizedMapsNames.SICILY)
        panel = BottomPanel()
        steps.press_back_until_main_page()
        steps.search("Cascate Cataolo")
        steps.choose_first_search_result()

        panel.route_from().click()
        el = steps.try_get_by_text(LocalizedButtons.ACCEPT.get())
        if el:
            el.click()
        steps.try_get(Locator.ROUTING_CHOOSE_POINT.get()).click()
        steps.search("Vulcano Porto", click_search_button=False)
        steps.choose_first_search_result()

        r_steps.download_additional_maps()
        r_steps.wait_route_start()
        steps.try_get(Locator.ZOOM_IN.get()).click()

        assert steps.try_get(Locator.DRIVING_OPTIONS.get())
        sleep(5)

        filename = "ferry_road.png"
        steps.driver.get_screenshot_as_file(filename)
        coor = self.get_coords_proportions(filename)
        logging.info(str(coor))
        TouchAction(steps.driver).tap(x=round(coor[0] * steps.driver.get_window_size()["width"]) + 10,
                                      y=round(coor[1] * steps.driver.get_window_size()["height"]) + 10).perform()

        assert steps.try_get_by_text(LocalizedButtons.AVOID_FERRY_ROADS.get())
        assert steps.try_get_by_text(LocalizedButtons.FERRY_ROAD.get(), strict=False)

    def get_coords(self, filename):
        img = Image.open(filename)
        img = img.convert("RGB")

        width, height = img.size

        rg = None

        for i in range(width):
            for j in range(height):
                x = img.getpixel((i, j))
                if rg != x:
                    rg = x

                if rg[1] < 60 and rg[2] < 60 and rg[0] > 200:
                    if i > 200 and j > 100:
                        return i, j

    def get_coords_proportions(self, filename, number=1):
        img = Image.open(filename)
        img = img.convert("RGB")

        width, height = img.size

        rg = None
        n = 1

        for i in range(width):
            for j in range(height):
                x = img.getpixel((i, j))
                if rg != x:
                    rg = x

                if rg[1] < 60 and rg[2] < 60 and rg[0] > 200:
                    if i > 200 and j > 100:
                        if n == number:
                            return i / width, j / height
                        n = n + 1

    @pytest.mark.name("[Routing][Subway] Проверка отображения слоя метро на карте")
    def test_metro_layer(self, main, steps):
        steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.CHELYABINSK)
        steps.search("Red square")
        steps.choose_first_search_result()
        steps.press_back_until_main_page()
        for i in range(5):
            steps.try_get(Locator.ZOOM_OUT.get()).click()
            sleep(1)
        filename = "subway1.png"
        steps.driver.get_screenshot_as_file(filename)
        sleep(1)
        assert self.assert_get_coords_subway(filename, False)
        steps.try_get(Locator.MAP_LAYERS.get()).click()
        subway = steps.try_get_by_xpath(
            "//*[@class='android.widget.LinearLayout' and ./*[@text='{}']]/*[@class='android.widget.ImageButton']".format(
                LocalizedButtons.SUBWAY.get())) or \
                 steps.try_get_by_text(LocalizedButtons.SUBWAY.get()).click()
        subway.click()
        TouchAction(steps.driver).tap(x=100, y=100).perform()
        sleep(10)
        # click to empty space to close
        # zoom out 5 times

        filename = "subway.png"
        steps.driver.get_screenshot_as_file(filename)
        assert self.assert_get_coords_subway(filename, True)

        steps.try_get(Locator.MAP_LAYERS.get()).click()
        sleep(3)
        filename = "subway2.png"
        steps.driver.get_screenshot_as_file(filename)
        assert self.assert_get_coords_subway(filename, False)

        steps.search(LocalizedMapsNames.CHELYABINSK.get())
        steps.choose_first_search_result(category=LocalizedCategories.CAPITAL.get())
        steps.press_back_until_main_page()
        steps.try_get(Locator.ZOOM_IN.get()).click()
        steps.try_get(Locator.MAP_LAYERS.get()).click()
        subway = steps.try_get_by_xpath(
            "//*[@class='android.widget.LinearLayout' and ./*[@text='{}']]/*[@class='android.widget.ImageButton']".format(
                LocalizedButtons.SUBWAY.get())) or \
                 steps.try_get_by_text(LocalizedButtons.SUBWAY.get()).click()
        subway.click()
        assert steps.try_get_by_text("Subway map is unavailable")  # Subway map is unavailable Карта метро недоступна
        subway.click()
        TouchAction(steps.driver).tap(x=100, y=100).perform()

    def assert_get_coords_subway(self, filename, show):
        pass
        img = Image.open(filename)
        img = img.convert("RGB")

        width, height = img.size

        rg = None
        n = 1

        green = False
        light_green = False
        blue = False
        purple = False
        brown = False

        for i in range(width):
            for j in range(height):
                x = img.getpixel((i, j))
                if rg != x:
                    rg = x

                    if rg[0] > 30 and rg[0] < 35 and rg[1] > 95 and rg[1] < 105 and rg[2] > 30 and rg[2] < 40:
                        green = True
                    if rg[0] > 200 and rg[0] < 210 and rg[1] > 220 and rg[1] < 230 and rg[2] > 120 and rg[2] < 130:
                        light_green = True

                    if rg[0] > 20 and rg[0] < 35 and rg[1] > 70 and rg[1] < 90 and rg[2] > 180 and rg[2] < 205:
                        blue = True

                    if rg[0] > 195 and rg[0] < 205 and rg[1] > 65 and rg[1] < 75 and rg[2] > 180 and rg[2] < 190:
                        logging.info("purple: {}".format(x))
                        purple = True

                    if rg[0] > 90 and rg[0] < 110 and rg[1] > 60 and rg[1] < 75 and rg[2] > 50 and rg[2] < 80:
                        brown = True

        if show:
            return green and light_green and blue and purple and brown
        else:
            return not (green and light_green and brown and blue and purple)
