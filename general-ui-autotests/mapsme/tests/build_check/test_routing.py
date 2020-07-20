from time import sleep

import pytest
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.locators import LocalizedButtons, Locator, LocalizedMapsNames
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.build_check
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

    @pytest.mark.name("[Routing] P2P авто с 3 промежуточными точками и несколькими mwm и началом движения")
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

    @pytest.mark.name("[Routing] P2P вело с 3 промежуточными точками и несколькими mwm и началом движения")
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

    @pytest.mark.name("[Routing] P2P пеший с 3 промежуточными точками и несколькими mwm и началом движения")
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

    @pytest.mark.name("[Routing] P2P общественный внутри mwm с метро (Динамо - Технопарк)")
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

    @pytest.mark.name("[Routing] P2P общественный между mwm с и без метро (Динамо - Чехов)")
    def test_routing_metro_two_maps(self, main, download_moscow_map, steps, r_steps):
        """ Метро Динамо -> Чехов. Ожидается ошибка построения маршрута"""
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

    @pytest.mark.name("[Routing] P2P такси")
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

    @pytest.mark.name("[Routing] Такси с PP сюда с определённым местоположением")
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

    @pytest.mark.name("[Routing] Сохранение промежуточных точек при переходе из авто в такси и с возвратом обратно")
    def test_routing_auto_taxi_back(self, main, download_moscow_map, steps, r_steps, search_steps):
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

    @pytest.mark.name("[Routing] Сохранение промежуточных точек при переходе из вело в такси и с возвратом обратно")
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

    @pytest.mark.name("[Routing] Сохранение промежуточных точек при переходе из пешего в такси и с возвратом обратно")
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
        "[Routing] Сохранение промежуточных точек при переходе из общественного транспорта в такси и с возвратом обратно")
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

    @pytest.mark.name("[Routing] Планировщик маршрута")
    @pytest.mark.iosonly
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
