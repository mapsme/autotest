from time import sleep

import pytest
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.steps.locators import LocalizedMapsNames, Locator, LocalizedCategories


@pytest.mark.build_check
class TestDownloadMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main, restart_if_no_zoom):
        pass

    @pytest.fixture
    def restart_if_no_zoom(self, steps, system_steps):
        steps.press_back_until_main_page()
        if not steps.try_get(Locator.ZOOM_IN.get()):
            system_steps.restart_app()
            steps.close_first_time_frame()

    @pytest.mark.name("[Download maps] Загрузка из загрузчика: страна (Андорра)")
    @pytest.mark.base
    def test_download_country_from_my_maps(self, main, steps):
        steps.delete_map(None, None, LocalizedMapsNames.ANDORRA)
        steps.download_map(None, None, LocalizedMapsNames.ANDORRA)
        steps.show_place_on_map(None, None, LocalizedMapsNames.ANDORRA)

    @pytest.mark.name("[Download maps] Загрузка с карты: фрагмент (Тульская область)")
    def test_download_fragment_from_ui(self, main, steps):
        steps.delete_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.TULA)
        steps.search(LocalizedMapsNames.TULA.get())
        steps.choose_first_search_result()

        steps.press_back_until_main_page()

        if not steps.try_get(Locator.ZOOM_IN.get()):
            coord_x = steps.driver.get_window_size()["width"] / 2
            coord_y = steps.driver.get_window_size()["height"] / 2
            TouchAction(steps.driver).tap(None, coord_x, coord_y).perform()
            sleep(1)

        for i in range(8):
            steps.try_get(Locator.ZOOM_IN.get()).click()

        steps.wait_map_download(LocalizedMapsNames.TULA.get())
        steps.press_back_until_main_page()
        steps.show_place_on_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.TULA)

    @pytest.mark.name("[Download maps] Загрузка с карты: страна (Египет)")
    def test_download_country_from_ui(self, main, steps):
        steps.delete_map(None, None, LocalizedMapsNames.EGYPT)
        steps.search(LocalizedMapsNames.EGYPT.get())
        steps.choose_first_search_result(category=LocalizedCategories.COUNTRY.get())

        steps.press_back_until_main_page()

        if not steps.try_get(Locator.ZOOM_IN.get()):
            coord_x = steps.driver.get_window_size()["width"] / 2
            coord_y = steps.driver.get_window_size()["height"] / 2
            TouchAction(steps.driver).tap(None, coord_x, coord_y).perform()

        for i in range(8):
            steps.try_get(Locator.ZOOM_IN.get()).click()

        steps.wait_map_download(LocalizedMapsNames.EGYPT.get())
        steps.press_back_until_main_page()
        steps.show_place_on_map(None, None, LocalizedMapsNames.EGYPT)

    @pytest.mark.name("[Download maps] Загрузка с PP: фрагмент (Владивосток)")
    def test_download_fragment_from_pp(self, main, steps):
        steps.delete_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.PRIMORSKY_KRAI)
        steps.search(LocalizedMapsNames.VLADIVOSTOK.get())
        steps.choose_first_search_result()

        steps.download_map_from_pp()

        steps.press_back_until_main_page()
        steps.show_place_on_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.PRIMORSKY_KRAI)

    @pytest.mark.name("[Download maps] Загрузка с PP: страна (Северная Корея)")
    def test_download_country_from_pp(self, main, steps):
        steps.delete_map(None, None, LocalizedMapsNames.NORTH_KOREA)
        steps.search(LocalizedMapsNames.NORTH_KOREA.get())
        steps.choose_first_search_result()

        steps.download_map_from_pp()

        steps.press_back_until_main_page()
        steps.show_place_on_map(None, None, LocalizedMapsNames.NORTH_KOREA)

    @pytest.mark.name("[Download maps] Загрузка с загрузчика: фрагмент (Алтайский край)")
    def test_download_fragment_from_my_maps(self, main, steps):
        steps.delete_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.ALTAI_KRAI)
        steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.ALTAI_KRAI)
        steps.show_place_on_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.ALTAI_KRAI)

    @pytest.mark.name(
        "[Download maps] Автозагрузка при призумливании к незагруженному фрагменту текущего местоположения")
    def test_auto_download_from_current_location(self, main, steps):
        if not steps.try_get(Locator.ZOOM_IN.get()):
            coord_x = steps.driver.get_window_size()["width"] / 2
            coord_y = steps.driver.get_window_size()["height"] / 2
            TouchAction(steps.driver).tap(None, coord_x, coord_y).perform()

        for i in range(5):
            steps.try_get(Locator.ZOOM_OUT.get()).click()
        steps.delete_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW)
        steps.restart_app()
        if steps.try_get(Locator.GET_POSITION_LIGHT.get()):
            steps.try_get(Locator.GET_POSITION_LIGHT.get()).click()
        for i in range(10):
            steps.try_get(Locator.ZOOM_IN.get()).click()

        steps.wait_map_auto_download(LocalizedMapsNames.MOSCOW.get())
        steps.assert_map_downloaded(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW)

    @pytest.mark.name("[Download maps] Удаление карты в загрузчике (Алтайский край, Северная Корея)")
    def test_delete_from_my_maps(self, main, steps):
        steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.ALTAI_KRAI)
        steps.download_map(None, None, LocalizedMapsNames.NORTH_KOREA)

        steps.delete_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.ALTAI_KRAI)
        steps.delete_map(None, None, LocalizedMapsNames.NORTH_KOREA)

        steps.assert_map_deleted(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.ALTAI_KRAI)
        steps.assert_map_deleted(None, None, LocalizedMapsNames.NORTH_KOREA)
