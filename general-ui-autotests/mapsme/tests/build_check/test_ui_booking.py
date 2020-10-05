import logging
from datetime import datetime, timedelta
from time import sleep
from urllib import parse

import pytest
from PIL import Image
from appium.webdriver import WebElement
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.pageobjects.booking_filter_page import SearchFilter
from mapsmefr.steps.base_steps import BookingSteps
from mapsmefr.steps.locators import LocalizedCategories, Locator, LocalizedButtons, BookingButtons
from mapsmefr.utils import expected_conditions as EC2
from mapsmefr.utils.tools import get_settings
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.build_check
@pytest.mark.booking_ui
class TestBookingOnlyUiMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main):
        pass

    @pytest.yield_fixture(scope="class")
    def b_steps(self):
        yield BookingSteps.get()

    @pytest.mark.skip
    @pytest.mark.name("[Hotels] Поиск по категории 'Отели', отображение кнопки фильтра")
    def test_search_hotels_category_filter(self, main, steps):
        steps.click_search_button()
        steps.click_categories()
        steps.choose_category_in_list(LocalizedCategories.HOTEL.get())

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

    @pytest.mark.skip
    @pytest.mark.name(
        "[Hotels] Поиск списком с применением фильтра онлайн - подстветка только отелей, удовлетворяющих требованиям по дате")
    def test_hotel_online_filter_list_dates(self, main, b_steps):
        b_steps.click_search_button()
        b_steps.click_categories()
        b_steps.choose_category_in_list(LocalizedCategories.HOTEL.get())
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
        sleep(5)
        if b_steps.try_get(LocalizedButtons.SEARCH.get()):
            b_steps.try_get(LocalizedButtons.SEARCH.get()).click()
        sleep(5)

        s_filter.search_button().click()
        sleep(5)
        b_steps.assert_available_hotels_in_search()

    @pytest.mark.name("[Hotels] UI фильтра (даты, рейтинг, ценовая категория, тип; применить и сбросить)")
    def test_ui_hotel_filter(self, main, b_steps):
        b_steps.click_search_button()
        b_steps.click_categories()
        b_steps.choose_category_in_list(LocalizedCategories.HOTEL.get())
        b_steps.try_get(Locator.HOTEL_FILTER.get()).click()
        s_filter = SearchFilter()
        assert s_filter.reset_button()
        assert s_filter.check_in()
        assert s_filter.check_out()
        assert s_filter.price_high()
        assert s_filter.price_medium()
        assert s_filter.price_low()
        assert s_filter.rating_any()
        assert s_filter.rating_good()
        assert s_filter.rating_very_good()
        assert s_filter.rating_excellent()
        assert s_filter.type(BookingButtons.HOSTEL.get()).location["y"] > s_filter.price_high().location["y"] > \
               s_filter.rating_any().location["y"] > s_filter.check_in().location["y"]

        self.assert_blue_rating(s_filter)
        self.assert_blue_price(s_filter)

        # TODO написать метод для каждого поля, напимер для рейтинга - что можно выбрать только один. делать скриншот элемента и проверять на синий цвет

        types = [BookingButtons.HOSTEL, BookingButtons.HOTEL, BookingButtons.APARTMENTS, BookingButtons.CAMPING,
                 BookingButtons.CHALET, BookingButtons.GUEST_HOUSE, BookingButtons.RESORT, BookingButtons.MOTEL]

        for t in types:
            assert s_filter.type(t.get())

        self.assert_blue_type(s_filter)

        s_filter.rating_very_good().click()
        s_filter.search_button().click()
        sleep(5)
        b_steps.assert_filtered_hotels(rating=8.0)

        b_steps.try_get(Locator.HOTEL_FILTER.get()).click()
        s_filter.rating_excellent().click()
        s_filter.price_medium().click()
        s_filter.search_button().click()
        sleep(5)
        b_steps.assert_filtered_hotels(rating=9.0, price_category="$$")

        b_steps.try_get(Locator.HOTEL_FILTER.get()).click()
        s_filter.price_medium().click()
        s_filter.price_high().click()
        s_filter.type(BookingButtons.APARTMENTS.get()).click()
        s_filter.search_button().click()
        sleep(5)
        b_steps.assert_filtered_hotels(rating=9.0, price_category="$$$", type=BookingButtons.APARTMENTS.get())

        b_steps.try_get(Locator.HOTEL_FILTER_CLEAR.get()).click()

        sleep(5)

        b_steps.assert_hotel_filter_cleared(BookingButtons.APARTMENTS.get())

    def assert_blue_price(self, s_filter):
        s_filter.price_high().click()
        s_filter.price_medium().click()

        s_filter.price_high().screenshot("high.png")
        s_filter.price_medium().screenshot("medium.png")
        sleep(10)

        assert self.get_coords("high.png")
        assert self.get_coords("medium.png")

        s_filter.price_high().click()
        s_filter.price_medium().click()

        s_filter.price_high().screenshot("high.png")
        s_filter.price_medium().screenshot("medium.png")
        sleep(10)

        assert not self.get_coords("high.png")
        assert not self.get_coords("medium.png")

    def assert_blue_rating(self, s_filter):
        s_filter.rating_good().click()
        s_filter.rating_very_good().click()

        s_filter.rating_any().screenshot("any.png")
        s_filter.rating_good().screenshot("good.png")
        s_filter.rating_very_good().screenshot("verygood.png")
        sleep(10)

        assert self.get_coords("verygood.png")
        assert not self.get_coords("any.png")
        assert not self.get_coords("good.png")

    def assert_blue_type(self, s_filter):
        s_filter.type(BookingButtons.GUEST_HOUSE.get()).click()
        s_filter.type(BookingButtons.RESORT.get()).click()

        s_filter.type(BookingButtons.GUEST_HOUSE.get()).screenshot("guest.png")
        s_filter.type(BookingButtons.RESORT.get()).screenshot("resort.png")
        sleep(10)
        assert self.get_coords("guest.png")
        assert self.get_coords("resort.png")

        s_filter.type(BookingButtons.GUEST_HOUSE.get()).click()
        s_filter.type(BookingButtons.RESORT.get()).click()

        s_filter.type(BookingButtons.GUEST_HOUSE.get()).screenshot("guest.png")
        s_filter.type(BookingButtons.RESORT.get()).screenshot("resort.png")
        sleep(10)

        assert not self.get_coords("guest.png")
        assert not self.get_coords("resort.png")

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
                if rg == (23, 135, 219) or rg == (28, 147, 237):
                    # android if rg == (36, 156, 242):
                    return True


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

    def test_booking_menu_button(self, main, steps):
        steps.try_get(Locator.MENU_BUTTON.get()).click()
        assert steps.try_get_by_text(BookingButtons.BOOKING_MENU_BTN.get())
