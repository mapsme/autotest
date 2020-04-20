import logging
from datetime import datetime, timedelta
from urllib import parse

import pytest
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.pageobjects.booking_filter_page import SearchFilter
from mapsmefr.steps.base_steps import BookingSteps
from mapsmefr.steps.locators import LocalizedCategories, Locator, LocalizedButtons, BookingButtons
from mapsmefr.utils import expected_conditions as EC2
from mapsmefr.utils.tools import get_settings
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.build_check
class TestBookingOnlyUiMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main):
        pass

    @pytest.yield_fixture(scope="class")
    def b_steps(self):
        yield BookingSteps.get()

    @pytest.mark.name("[Hotels] Поиск по категории 'Отели', отображение кнопки фильтра")
    def test_search_hotels_category_filter(self, main, steps):
        steps.click_search_button()
        steps.click_categories()
        steps.choose_category_in_list(LocalizedCategories.HOTELS.get())

        assert steps.try_get(Locator.HOTEL_FILTER.get())
        assert steps.try_get(LocalizedButtons.HOTEL_FILTER.get()) or steps.try_get_by_text(
            LocalizedButtons.HOTEL_FILTER.get())

    @pytest.mark.releaseonly
    @pytest.mark.name("[Hotels] Отображение компонентов Rich PP (галерея, описание, удобства, отзывы) для Аэрополиса")
    def test_hotel_rich_pp_booking(self, main, download_moscow_map, b_steps):
        b_steps.search_booking_hotel(LocalizedButtons.AEROPOLIS_NAME.get())
        b_steps.scroll_down(from_el=b_steps.try_get(Locator.PP_ANCHOR.get()))
        b_steps.assert_hotel_description()
        b_steps.assert_booking_buttons_on_rich_pp()
        bad_reviews = b_steps.driver.find_elements_by_id(Locator.HOTEL_BAD_REVIEW.get())
        good_reviews = b_steps.driver.find_elements_by_id(Locator.HOTEL_GOOD_REVIEW.get())
        assert len(bad_reviews) + len(good_reviews) > 0
        assert b_steps.try_get(Locator.TAXI_VEZET.get()) or b_steps.try_get(Locator.HOTEL_PP_TAXI_VEZET.get())

    @pytest.mark.name(
        "[Hotels] Поиск списком с применением фильтра онлайн - подстветка только отелей, удовлетворяющих требованиям по дате")
    def test_hotel_online_filter_list_dates(self, main, b_steps):
        b_steps.click_search_button()
        b_steps.click_categories()
        b_steps.choose_category_in_list(LocalizedCategories.HOTELS.get())
        b_steps.try_get(Locator.HOTEL_FILTER.get()).click()
        s_filter = SearchFilter()
        s_filter.check_in().click()

        when = datetime.now() + timedelta(days=31)

        if get_settings("System", "platform") == "IOS":
            from mapsmefr.pageobjects.calendar import IosSystemCalendar as calendar
        else:
            from mapsmefr.pageobjects.calendar import AndroidSystemCalendar as calendar

        calend = calendar()
        calend.choose_date(when)
        calend.click_done()

        s_filter.search_button().click()

        b_steps.assert_available_hotels_in_search()

    @pytest.mark.name("[Hotels] UI фильтра (даты, рейтинг, ценовая категория, тип; применить и сбросить)")
    def test_ui_hotel_filter(self, main, download_moscow_map, b_steps):
        b_steps.click_search_button()
        b_steps.click_categories()
        b_steps.choose_category_in_list(LocalizedCategories.HOTELS.get())
        b_steps.try_get(Locator.HOTEL_FILTER.get()).click()
        s_filter = SearchFilter()
        assert s_filter.check_in()
        assert s_filter.check_out()
        assert s_filter.price_high()
        assert s_filter.price_medium()
        assert s_filter.price_low()
        assert s_filter.rating_any()
        assert s_filter.rating_good()
        assert s_filter.rating_very_good()
        assert s_filter.rating_excellent()

        types = [BookingButtons.HOSTEL, BookingButtons.HOTEL, BookingButtons.APARTMENTS, BookingButtons.CAMPING,
                 BookingButtons.CHALET, BookingButtons.GUEST_HOUSE, BookingButtons.RESORT, BookingButtons.MOTEL]

        for t in types:
            assert s_filter.type(t.get())

        s_filter.rating_very_good().click()
        s_filter.search_button().click()

        b_steps.assert_filtered_hotels(rating=8.0)

        b_steps.try_get(Locator.HOTEL_FILTER.get()).click()
        s_filter.rating_excellent().click()
        s_filter.price_medium().click()
        s_filter.search_button().click()

        b_steps.assert_filtered_hotels(rating=9.0, price_category="$$")

        b_steps.try_get(Locator.HOTEL_FILTER.get()).click()
        s_filter.price_medium().click()
        s_filter.price_high().click()
        s_filter.type(BookingButtons.APARTMENTS.get()).click()
        s_filter.search_button().click()

        b_steps.assert_filtered_hotels(rating=9.0, price_category="$$$", type=BookingButtons.APARTMENTS.get())

        b_steps.try_get(Locator.HOTEL_FILTER_CLEAR.get()).click()

        b_steps.assert_hotel_filter_cleared(BookingButtons.APARTMENTS.get())

    @pytest.mark.webview
    @pytest.mark.releaseonly
    @pytest.mark.parametrize("button_locator",
                             [pytest.param(Locator.DETAILS_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Проверка aid] Бронирование отеля с кнопки Подробней на Booking.com на Rich PP")),
                              pytest.param(Locator.MORE_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Проверка aid] Бронирование с кнопки Больше на Booking.com на Rich PP")),
                              pytest.param(Locator.MORE_REVIEWS_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Проверка aid] Бронирование с кнопки Больше отзывов на Rich PP"))
                              ])
    def test_hotels_aid_browser_rich_pp(self, button_locator, main, download_moscow_map, b_steps, return_back_to_mapsme,
                                        switch_to_native):
        b_steps.search_booking_hotel(LocalizedButtons.AEROPOLIS_NAME.get())
        b_steps.scroll_down(from_el=b_steps.try_get(Locator.PP_ANCHOR.get()))
        button = b_steps.find_booking_button_on_pp(button_locator)
        assert button
        button.click()
        WebDriverWait(b_steps.driver, 20).until(EC2.web_view_context_enabled())
        contexts = b_steps.driver.contexts
        cons = [x.split("_")[-1] for x in contexts if x != "NATIVE_APP"]
        b_steps.driver.switch_to.context("WEBVIEW_{}".format(cons[-1]))
        WebDriverWait(b_steps.driver, 20).until(EC.url_contains("booking.com"))
        url = b_steps.driver.current_url
        url_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        logging.info(str(url_params))
        aid = url_params["aid"]
        if get_settings("System", "Platform") == "Android":
            assert aid == "1595466"
        else:
            assert aid == "1595464"
        b_steps.switch_to_native()
        b_steps.close_first_time_frame()
        b_steps.press_back_until_main_page()

    @pytest.mark.webview
    @pytest.mark.name("[Проверка aid] Бронирование с кнопки BOOK на Rich PP")
    def test_hotels_aid_browser_rich_button(self, main, download_moscow_map, b_steps, return_back_to_mapsme,
                                            switch_to_native):
        b_steps.search_booking_hotel(LocalizedButtons.AEROPOLIS_NAME.get())
        BottomPanel().book().click()
        WebDriverWait(b_steps.driver, 20).until(EC2.web_view_context_enabled())
        contexts = b_steps.driver.contexts
        cons = [x.split("_")[-1] for x in contexts if x != "NATIVE_APP"]
        b_steps.driver.switch_to.context("WEBVIEW_{}".format(cons[-1]))
        WebDriverWait(b_steps.driver, 20).until(EC.url_contains("booking.com"))
        url = b_steps.driver.current_url
        url_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        logging.info(str(url_params))
        aid = url_params["aid"]
        if get_settings("System", "Platform") == "Android":
            assert aid == "1595466"
        else:
            assert aid == "1595464"
        b_steps.switch_to_native()
        b_steps.close_first_time_frame()
        b_steps.press_back_until_main_page()

    @pytest.mark.webview
    @pytest.mark.name("[Проверка aid] Бронирование с кнопки BOOK на Poor PP")
    def test_hotels_aid_browser_poor_button(self, main, download_moscow_map, b_steps, return_back_to_mapsme,
                                            switch_to_native):
        b_steps.search_osm_hotel("Аэрополис")
        BottomPanel().book().click()
        WebDriverWait(b_steps.driver, 20).until(EC2.web_view_context_enabled())
        contexts = b_steps.driver.contexts
        cons = [x.split("_")[-1] for x in contexts if x != "NATIVE_APP"]
        b_steps.driver.switch_to.context("WEBVIEW_{}".format(cons[-1]))
        WebDriverWait(b_steps.driver, 20).until(EC.url_contains("booking.com"))
        url = b_steps.driver.current_url
        url_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        logging.info(str(url_params))
        aid = url_params["aid"]
        if get_settings("System", "Platform") == "Android":
            assert aid == "1595466"
        else:
            assert aid == "1595464"
        b_steps.switch_to_native()
        b_steps.close_first_time_frame()
        b_steps.press_back_until_main_page()
