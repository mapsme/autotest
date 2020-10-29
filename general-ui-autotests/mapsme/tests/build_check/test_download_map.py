import logging
import re
from time import sleep

import pytest
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.steps.locators import LocalizedMapsNames, Locator, LocalizedCategories, LocalizedButtons
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mapsmefr.utils import expected_conditions as EC2


@pytest.mark.build_check
@pytest.mark.downloadmap
@pytest.mark.regress1
@pytest.mark.night
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
        steps.choose_first_search_result(category=LocalizedCategories.CITY.get())

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
    def test_auto_download_from_current_location(self, main, steps, system_steps):
        if not steps.try_get(Locator.ZOOM_IN.get()):
            coord_x = steps.driver.get_window_size()["width"] / 2
            coord_y = steps.driver.get_window_size()["height"] / 2
            TouchAction(steps.driver).tap(None, coord_x, coord_y).perform()

        for i in range(5):
            steps.try_get(Locator.ZOOM_OUT.get()).click()
        steps.delete_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW)
        system_steps.restart_app()
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
        steps.download_map(None, None, LocalizedMapsNames.ANDORRA) #TODO delete

        steps.delete_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.ALTAI_KRAI)
        steps.delete_map(None, None, LocalizedMapsNames.NORTH_KOREA)

        steps.assert_map_deleted(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.ALTAI_KRAI)
        steps.assert_map_deleted(None, None, LocalizedMapsNames.NORTH_KOREA)

    @pytest.mark.name("[Download maps] Проверка наличия информации по mwm: название, размер, описание")
    def test_downloader_ui(self, main, steps, downloader_steps):
        steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.VORONEZH)
        steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW)
        steps.download_map(None, None, LocalizedMapsNames.NORTH_KOREA)

        downloader_steps.assert_size_and_sublocations(None, None, LocalizedMapsNames.NORTH_KOREA)
        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.VORONEZH)
        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW)

        if steps.try_get(Locator.GET_POSITION_LIGHT.get()):
            steps.try_get(Locator.GET_POSITION_LIGHT.get()).click()

        for i in range(3):
            steps.try_get(Locator.ZOOM_IN.get()).click()

        assert not steps.try_get("onmap_downloader")

    @pytest.mark.name("[Download maps] Загрузка целой страны с несколькими mwm")
    def test_download_country_several_mwm(self, main, steps, downloader_steps):
        steps.delete_map(None, None, LocalizedMapsNames.IRELAND)
        steps.download_map(None, None, LocalizedMapsNames.IRELAND)  # TODO не скачивается??

        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.CONNACHT)
        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.LEINSTER)
        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.MUNSTER)
        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.ULSTER)

    @pytest.mark.name("[Download maps] Проверка кнопки Загрузить все")
    def test_download_all_button(self, main, steps, downloader_steps):
        steps.delete_map(None, None, LocalizedMapsNames.IRELAND)
        steps.download_map(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.DUBLIN)
        downloader_steps.go_to_map(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.LEINSTER)
        steps.try_get(Locator.PLUS_DOWNLOADER_BUTTON.get()).click()
        assert steps.try_get(Locator.DOWNLOAD_ALL.get())
        #logging.info(steps.driver.page_source) #TODO
        download_all = steps.try_get("Скачать")
        download_all.click()
        WebDriverWait(steps.driver, 60).until(EC2.element_to_be_dissapeared((By.ID, Locator.DOWNLOAD_ALL.get())))
        steps.press_back_until_main_page()
        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.CONNACHT)
        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.MUNSTER)
        downloader_steps.assert_size_and_sublocations(LocalizedMapsNames.IRELAND, None, LocalizedMapsNames.ULSTER)
        steps.delete_map(None, None, LocalizedMapsNames.IRELAND)
        steps.go_to_maps()
        assert steps.try_get_by_text(LocalizedMapsNames.IRELAND.get()) is None

    @pytest.mark.skip(reason="Clean iphone")
    @pytest.mark.name("[Download maps] Проверка отмены загрузки всех карт")
    def test_cancel_download_all(self, main, steps, downloader_steps):
        steps.delete_map(None, None, LocalizedMapsNames.RUSSIA)
        #steps.search(LocalizedMapsNames.MOSCOW.get())
        #steps.choose_first_search_result()
        #steps.download_map_from_pp()
        steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW)
        steps.press_back_until_main_page()
        if get_settings("System", "platform") == "Android":
            self.cancel_download_for_android(steps)
        else:
            self.cancel_download_for_ios(steps)

    def cancel_download_for_android(self, steps):
        steps.try_get(Locator.MENU_BUTTON.get()).click()
        steps.try_get(Locator.DOWNLOAD_MAPS.get()).click()
        russia, num = steps.try_find_map_with_scroll(LocalizedMapsNames.RUSSIA.get())
        steps.driver.find_elements_by_id(Locator.DOWNLOAD_ICON.get())[num].click()
        sleep(7)
        steps.try_get(Locator.IN_PROGRESS.get()).click()
        pattern = r"\d+"
        root = steps.try_get("recycler")
        subtitle = root.find_element_by_xpath(
            ".//*[@class='android.widget.RelativeLayout' and .//*[contains(@resource-id, 'name') and @text='{}']]//*[contains(@resource-id, 'subtitle')]".format(
                LocalizedMapsNames.RUSSIA.get()))

        m = re.findall(pattern, subtitle.text)
        assert int(m[0]) > 1

        russia, num = steps.try_find_map_with_scroll(LocalizedMapsNames.RUSSIA.get())
        steps.driver.find_elements_by_id(Locator.DOWNLOAD_ICON.get())[num].click()
        sleep(7)

        steps.try_get_by_text(LocalizedButtons.CANCELL_ALL.get()).click()

        root = steps.try_get("recycler")
        subtitle = root.find_element_by_xpath(
            ".//*[@class='android.widget.RelativeLayout' and .//*[contains(@resource-id, 'name') and @text='{}']]//*[contains(@resource-id, 'subtitle')]".format(
                LocalizedMapsNames.RUSSIA.get()))

        n = re.findall(pattern, subtitle.text)
        assert int(n[0]) > int(m[0])

    def cancel_download_for_ios(self, steps):
        steps.driver.find_element_by_id(Locator.MENU_BUTTON.get()).click()
        sleep(1)
        steps.driver.find_element_by_id(LocalizedButtons.DOWNLOAD_MAPS.get()).click()
        russia, num = steps.try_find_map_with_scroll(LocalizedMapsNames.RUSSIA)

        check = steps.try_get_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@name='{}' or @name='{}']".format(LocalizedMapsNames.RUSSIA.get(),
                                                                                                      Locator.FOLDER_ICON.get(),
                                                                                                      Locator.DOWNLOADED_ICON.get()))
        TouchAction(steps.driver).long_press(check, duration=2000).wait(500).release().perform()
        up = "ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        low = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        steps.try_get_by_xpath(
            "//*[contains(translate(@name, '{}', '{}'),'{}')]"
                .format(up, low, LocalizedButtons.DOWNLOAD_ALL_BUTTON.get().lower())).click()

        sleep(60)
        steps.try_get(Locator.IN_PROGRESS.get()).click()
        sleep(30)
        pattern = r"\d+"
        els = steps.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]//*[@type='XCUIElementTypeStaticText']".format(
                LocalizedMapsNames.RUSSIA.get()))
        subtitle = els[1]

        m = re.findall(pattern, subtitle.text)
        assert int(m[0]) > 1

        russia, num = steps.try_find_map_with_scroll(LocalizedMapsNames.RUSSIA)
        TouchAction(steps.driver).long_press(steps.driver.find_elements_by_id(Locator.FOLDER_ICON.get())[
                                                 num], duration=2000).wait(500).release().perform()
        steps.try_get_by_xpath(
            "//*[contains(translate(@name, '{}', '{}'),'{}')]"
                .format(up, low, LocalizedButtons.DOWNLOAD_ALL_BUTTON.get().lower())).click()
        sleep(60)

        TouchAction(steps.driver).long_press(steps.try_get(LocalizedMapsNames.RUSSIA.get()), duration=2000).wait(
            500).release().perform()

        steps.try_get_by_text(LocalizedButtons.CANCEL_DOWNLOAD.get()).click()

        sleep(30)

        els = steps.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]//*[@type='XCUIElementTypeStaticText']".format(
                LocalizedMapsNames.RUSSIA.get()))
        subtitle = els[1]

        n = re.findall(pattern, subtitle.text)
        assert int(n[0]) > int(m[0])
