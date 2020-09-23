import calendar
import json
import logging
import re
from datetime import datetime, timedelta
from time import time, sleep

import pytest
import requests
from mapsmefr.client.booking import Booking
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.base_steps import BookingSteps
from mapsmefr.steps.booking_locators import BookingIosAppLocalizedButtons as ios_locators, \
    BookingAndroidAppLocators as android_locators
from mapsmefr.steps.booking_web_steps import BookingWebSearchForm
from mapsmefr.steps.locators import Locator
from mapsmefr.utils import expected_conditions as EC2
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import is_element_scrolled, get_settings
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, \
    ElementNotVisibleException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.booking
class TestBookingFullMapsme:
    @pytest.yield_fixture
    def main(self, check_appium, driver_booking, testitem_booking, accept_privacy_policy,
             press_back_to_main,
             return_back_to_mapsme,
             switch_to_native):
        yield driver_booking

    @pytest.fixture(scope="class")
    def find_booking_hotels(self):
        host = "https://distribution-xml.booking.com/2.4/json/hotelAvailability"
        now = datetime.now()
        need_date = datetime(now.year, now.month + 1, calendar.monthrange(now.year, now.month + 1)[1])
        need_date_two = (need_date + timedelta(days=1))

        params = {"city_ids": -2960561,
                  "room1": 'A,A',
                  "checkin": need_date.strftime("%Y-%m-%d"),
                  "checkout": need_date_two.strftime("%Y-%m-%d"),
                  "options": "no_cc_filter",
                  "filter": 'free_cancellation',
                  "extras": "hotel_details",
                  "rows": 100}
        resp = requests.get(host, params=params,
                            auth=(get_settings("Tests", "booking_api_user"), get_settings("Tests", "booking_api_pass")))
        result = json.loads(resp.text)["result"]
        hotels = [x["hotel_name"] for x in result]
        logging.info(str(hotels))
        return hotels

    @pytest.fixture(scope="class")
    def find_osm_hotels(self):
        hotels = ["SkyPoint", "Hostel Derevo", "Аэрополис"]
        return hotels

    @pytest.mark.parametrize("button_locator",
                             [pytest.param(Locator.DETAILS_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Booking.com][Browser] Бронирование с кнопки Подробней на Booking.com на Rich PP")),
                              pytest.param(Locator.MORE_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Booking.com][Browser] Бронирование с кнопки Больше на Booking.com на Rich PP")),
                              pytest.param(Locator.MORE_REVIEWS_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Booking.com][Browser] Бронирование с кнопки Больше отзывов на Rich PP"))
                              ])
    def test_browser_booking_rich_pp(self, button_locator, find_booking_hotels, main, download_moscow_map, steps,
                                     b_steps, testitem_booking):
        hotel = None
        result = False
        while not result:
            while True:
                try:
                    hotel = find_booking_hotels.pop()
                    b_steps.search_booking_hotel(hotel)
                    break
                except (TimeoutException, AssertionError):
                    b_steps.press_back_until_main_page()
            sleep(2)
            b_steps.scroll_down(from_el=steps.try_get(Locator.PP_ANCHOR.get()))
            button = b_steps.find_booking_button_on_pp(button_locator)
            assert button
            button.click()
            WebDriverWait(main, 20).until(EC2.web_view_context_enabled())
            contexts = main.contexts
            cons = [x.split("_")[-1] for x in contexts if x != "NATIVE_APP"]
            main.switch_to.context("WEBVIEW_{}".format(cons[-1]))
            WebDriverWait(main, 20).until(EC.url_contains("booking.com"))
            url = main.current_url
            booking = Booking(testitem_booking.id)
            booking.create(hotel, url)
            result = self.browser_steps(booking, hotel)
            booking.result("Booked" if result else "Failure")
            b_steps.switch_to_native()
            b_steps.close_first_time_frame()
            b_steps.press_back_until_main_page()

    @pytest.mark.name("[Booking.com][Browser] Бронирование с кнопки BOOK на Rich PP")
    def test_browser_booking_rich_button(self, find_booking_hotels, main, download_moscow_map, steps, b_steps,
                                         testitem_booking):
        result = False
        while not result:
            hotel = None
            while True:
                try:
                    hotel = find_booking_hotels.pop()
                    b_steps.search_booking_hotel(hotel)
                    break
                except (TimeoutException, AssertionError):
                    b_steps.press_back_until_main_page()
            BottomPanel().book().click()
            WebDriverWait(main, 20).until(EC2.web_view_context_enabled())
            contexts = main.contexts
            cons = [x.split("_")[-1] for x in contexts if x != "NATIVE_APP"]
            main.switch_to.context("WEBVIEW_{}".format(cons[-1]))
            WebDriverWait(main, 20).until(EC.url_contains("booking.com"))
            url = main.current_url
            booking = Booking(testitem_booking.id)
            booking.create(hotel, url)
            result = self.browser_steps(booking, hotel)
            booking.result("Booked" if result else "Failure")
            b_steps.switch_to_native()
            b_steps.close_first_time_frame()
            b_steps.press_back_until_main_page()

    @pytest.mark.name("[Booking.com][Browser] Бронирование с кнопки Booking.com на Poor PP")
    def test_browser_booking_poor_button(self, main, download_moscow_map, steps, b_steps, testitem_booking,
                                         find_osm_hotels):
        result = False
        while not result:
            hotel = None
            while True:
                try:
                    hotel = find_osm_hotels.pop()
                    b_steps.search_osm_hotel(hotel)
                    break
                except (TimeoutException, AssertionError):
                    b_steps.press_back_until_main_page()
            BottomPanel().book().click()
            WebDriverWait(main, 20).until(EC2.web_view_context_enabled())
            contexts = main.contexts
            cons = [x.split("_")[-1] for x in contexts if x != "NATIVE_APP"]
            main.switch_to.context("WEBVIEW_{}".format(cons[-1]))
            WebDriverWait(main, 20).until(EC.url_contains("booking.com"))
            url = main.current_url
            hotel = "SkyPoint"
            booking = Booking(testitem_booking.id)
            booking.create(hotel, url)
            result = self.browser_steps(booking, hotel)
            booking.result("Booked" if result else "Failure")
            b_steps.switch_to_native()
            b_steps.close_first_time_frame()
            b_steps.press_back_until_main_page()

    @pytest.mark.parametrize("button_locator",
                             [pytest.param(Locator.DETAILS_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Booking.com][App] Бронирование с кнопки Подробней на Booking.com на Rich PP")),
                              pytest.param(Locator.MORE_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Booking.com][App] Бронирование с кнопки Больше на Booking.com на Rich PP")),
                              pytest.param(Locator.MORE_REVIEWS_ON_BOOKING,
                                           marks=pytest.mark.name(
                                               "[Booking.com][App] Бронирование с кнопки Больше отзывов на Rich PP"))
                              ])
    def test_app_booking_rich_pp(self, button_locator, find_booking_hotels, main, download_moscow_map, steps, b_steps,
                                 testitem_booking):
        hotel = None
        result = False
        while not result:
            while True:
                try:
                    hotel = find_booking_hotels.pop()
                    b_steps.search_booking_hotel(hotel)
                    break
                except (TimeoutException, AssertionError):
                    b_steps.press_back_until_main_page()
            b_steps.scroll_down()
            button = b_steps.find_booking_button_on_pp(button_locator)
            assert button
            button.click()
            booking = Booking(testitem_booking.id)
            booking.create(hotel, None)
            result = self.app_steps(steps, booking)
            booking.result("Booked" if result else "Failure")
            b_steps.close_first_time_frame()
            b_steps.press_back_until_main_page()

    @pytest.mark.name("[Booking.com][App] Бронирование с кнопки BOOK на Rich PP")
    def test_app_booking_rich_button(self, find_booking_hotels, main, download_moscow_map, steps, b_steps,
                                     testitem_booking):
        hotel = None
        result = False
        while not result:
            while True:
                try:
                    hotel = find_booking_hotels.pop()
                    b_steps.search_booking_hotel(hotel)
                    break
                except (TimeoutException, AssertionError):
                    b_steps.press_back_until_main_page()

            BottomPanel().book().click()
            booking = Booking(testitem_booking.id)
            booking.create(hotel, None)
            result = self.app_steps(steps, booking)
            booking.result("Booked" if result else "Failure")
            b_steps.close_after_booked_window()
            b_steps.close_first_time_frame()
            b_steps.press_back_until_main_page()

    def browser_steps(self, booking, hotel=None):
        driver = WebDriverManager.get_instance().driver
        driver.implicitly_wait(30)
        form = BookingWebSearchForm()

        sleep(10)

        url = driver.current_url
        url = url + "&test=1"
        driver.get(url)
        sleep(10)

        try:
            driver.find_element_by_xpath("//div[@id='sr-header-group-action-icon']").click()
        except:
            pass

        chosen_date = form.checkin_input().get_attribute("value")
        logging.info("Current chosen check-in date: {}".format(chosen_date))
        chosen = datetime.strptime(chosen_date, "%Y-%m-%d")
        if (chosen - datetime.now()).days < 30:
            form.checkin_date().click()
            WebDriverWait(driver, 10) \
                .until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'pikaday-checkin')]")))
            form.datepicker_next_arrow().click()
            form.datepicker_ci_last_day().click()
            chosen_date = form.checkin_input().get_attribute("value")
            logging.info("Current chosen check-in date: {}".format(chosen_date))

        if hotel:
            try:
                driver.find_element_by_xpath("//button[@class='input_clear_button']").click()
                form.direction().send_keys(hotel)
                sleep(1)
            except (ElementNotVisibleException, NoSuchElementException):
                pass
        try:
            form.submit_search().click()
        except (ElementClickInterceptedException, WebDriverException):
            try:
                driver.find_element_by_xpath("//*[@class='alertify-log-close-button']").click()
            except NoSuchElementException:
                pass
            form.submit_search().click()

        logging.info("Clicking search")
        form.wait_search_overlay()

        form.go_to_first_result()
        logging.info("Choosing first search result")

        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                (By.XPATH, "//a[contains(@href, '#availabilityBlock')]")))
        except TimeoutException:
            return False

        form.go_to_variants().click()
        sleep(3)

        try:
            form.free_cancellation().click()
            logging.info("Clicking free cancellation filter")
        except:
            pass

        form.first_book_variant().click()
        logging.info("Selecting first book variant in list")

        form.book().click()
        logging.info("Clicking Reserve")
        form.wait_search_overlay()

        form.book().click()
        logging.info("Clicking Book")
        sleep(5)

        try:
            form.fill_cc_data(
                "4441336954914542")  # todo: generate valid card numbers (mapsmefr/utils/card_number_generator)
        except:
            pass

        form.save_old_bookings()

        try:
            form.book().click()
        except:
            pass

        result = form.wait_booked_stamp()

        if result:
            prog = re.compile(r"[0-9.]+")
            result = prog.search(form.price().text.replace(" ", "").replace(",", ""))
            booking.price = float(result[0])
            booking.reservation_id = form.reservation_id()

        return result

    def app_steps(self, steps, booking):
        if get_settings("System", "platform") == "Android":
            return self.app_steps_android(steps, booking)
        else:
            return self.app_steps_ios(steps, booking)

    def app_steps_android(self, steps, booking):
        if steps.try_get_by_xpath(android_locators.REWIEW_TAB.get()):
            steps.try_get_by_xpath(android_locators.NAVIGATE_UP.get()).click()
        sleep(5)

        try:
            timeout = time() + 30
            while not steps.try_get(android_locators.CHECK_IN.get()):
                steps.scroll_down(small=True)
                if time() > timeout:
                    break
            steps.try_get(android_locators.CHECK_IN.get()).click()
        except Exception as e:
            steps.try_get(android_locators.SELECT_DATE.get()).click()

        now = datetime.now()
        need_date = datetime(now.year, now.month + 1, calendar.monthrange(now.year, now.month + 1)[1])
        need_date_two = (need_date + timedelta(days=1))

        date = None
        while not date:
            date = steps.try_get_by_xpath("//*[@content-desc='{}']".format(need_date_two.strftime("%d %B %Y")))
            if not date:
                steps.scroll_down(small=True)

        day = steps.try_get_by_xpath("//*[@content-desc='{}']".format(need_date.strftime("%d %B %Y")))
        day.click()
        steps.try_get_by_xpath("//*[@content-desc='{}']".format(need_date_two.strftime("%d %B %Y"))).click()
        steps.try_get(android_locators.CALENDAR_CONFIRM.get()).click()

        change_dates = steps.try_get(android_locators.CHANGE_DATES.get())
        if change_dates:
            steps.driver.execute_script("mobile: shell", {'command': "am force-stop com.booking"})
            return False

        try:
            steps.try_get(android_locators.SEARCH.get()).click()
            steps.try_get("com.booking:id/hotel_view_frame").click()
        except:
            pass

        change_dates = steps.try_get(android_locators.CHANGE_DATES.get())
        if change_dates:
            steps.driver.execute_script("mobile: shell", {'command': "am force-stop com.booking"})
            return False
        steps.try_get(android_locators.SELECT_ROOMS.get()).click()
        try:
            steps.try_get(android_locators.FREE_CANCELLATION.get()).click()
            sleep(2)
        except:
            pass

        while not steps.try_get(android_locators.SELECT_ROOM.get()):
            steps.scroll_down(small=True)

        select = steps.try_get(android_locators.SELECT_ROOM.get())
        if not "selected" in select.text:
            steps.try_get(android_locators.SELECT_ROOM.get()).click()
        while steps.try_get(android_locators.RESERVE.get()):
            steps.try_get(android_locators.RESERVE.get()).click()
            if steps.try_get("com.booking:id/message"):
                if "There was a problem" in steps.try_get("com.booking:id/message").text or \
                        "Your selections isn't available" in steps.try_get("com.booking:id/message").text:
                    steps.driver.execute_script("mobile: shell", {'command': "am force-stop com.booking"})
                    pytest.fail("Problems with booking services")
            if steps.try_get(android_locators.CVC_EDIT.get()):
                steps.try_get(android_locators.CVC_EDIT.get()).send_keys("111")
            if steps.try_get(android_locators.OK_BUTTON.get()):
                steps.try_get(android_locators.OK_BUTTON.get()).click()

        result = False
        try:
            WebDriverWait(steps.driver, 20).until(
                EC.visibility_of_element_located((By.ID, android_locators.BOOKING_CONFIRMED.get())))
            result = True
        except TimeoutException:
            result = False

        if result:
            steps.try_get(android_locators.VIEW_CONFIRMATION.get()).click()
            steps.try_get("com.booking:id/posButton").click()
            reservation_number = steps.try_get(android_locators.RESERVATION_NUMBER.get()).text
            booking.reservation_id = reservation_number
            while not steps.try_get("com.booking:id/price_display_value"):
                steps.scroll_down(small=True)
            price = steps.try_get("com.booking:id/price_display_value").text
            prog = re.compile(r"[0-9.]+")
            result = prog.search(price.replace(" ", "").replace(",", ""))
            booking.price = float(result[0])

        steps.driver.execute_script("mobile: shell", {'command': "am force-stop com.booking"})

        return result

    def app_steps_ios(self, steps, booking):

        in_progress = steps.try_get("In progress")
        if in_progress:
            WebDriverWait(steps.driver, 40).until(EC.invisibility_of_element(in_progress))
        first_result = steps.try_get("ai_sr_cell_hotel")
        if first_result:
            first_result.click()
        WebDriverWait(steps.driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[./*[@name='{}']]".format(ios_locators.CHECK_IN.get()))))
        steps.scroll_down(small=True)

        steps.driver.find_element_by_xpath(
            "//*[./*[@name='{}']]/*".format(ios_locators.CHECK_IN.get())).click()

        now = datetime.now()
        need_date = datetime(now.year, now.month + 1, calendar.monthrange(now.year, now.month + 1)[1])
        need_date_two = (need_date + timedelta(days=1))

        timeout = time() + 60
        while not (steps.try_get(need_date_two.strftime("ai_cal_%Y_%m_%d"))
                   and is_element_scrolled(steps.driver, steps.try_get(need_date_two.strftime("ai_cal_%Y_%m_%d")))):
            steps.scroll_down(small=True)
            if time() > timeout:
                steps.driver.find_element_by_id("breadcrumb").click()
                return False

        steps.driver.find_element_by_id(need_date.strftime("ai_cal_%Y_%m_%d")).click()
        steps.driver.find_element_by_id(need_date_two.strftime("ai_cal_%Y_%m_%d")).click()
        steps.driver.find_element_by_id("ai_cal_apply").click()

        steps.scroll_up()

        select_rooms = steps.try_get("ai_pp_select_rooms")
        if not select_rooms:
            steps.driver.find_element_by_id("breadcrumb").click()
            return False

        select_rooms.click()

        try:
            steps.driver.find_element_by_id(ios_locators.FREE_CANCELLATION.get()).click()
        except:
            pass

        try:
            if not is_element_scrolled(steps.driver,
                                       steps.driver.find_element_by_id(ios_locators.SELECT.get())):
                steps.scroll_down(small=True)
            steps.driver.find_element_by_id(ios_locators.SELECT.get()).click()
        except NoSuchElementException:
            pass

        steps.driver.find_element_by_id(ios_locators.RESERVE.get()).click()

        try:
            steps.driver.execute_script('mobile: alert', {'action': 'accept'})
        except:
            pass

        try:
            steps.driver.find_element_by_id(ios_locators.CONTINUE.get()).click()
        except NoSuchElementException:
            pass
        steps.driver.find_element_by_id(ios_locators.NEXT_STEP.get()).click()
        try:
            steps.driver.find_element_by_id(ios_locators.FINAL_STEP.get()).click()
        except NoSuchElementException:
            pass

        try:
            cvc = steps.driver.find_element_by_xpath("//*[@type='XCUIElementTypeTextField']")
            cvc.send_keys("111")
            sleep(1)
            steps.driver.find_element_by_id(ios_locators.DONE.get()).click()
        except WebDriverException:
            done = steps.try_get(ios_locators.DONE.get())
            if done:
                done.click()

        steps.driver.find_element_by_id(ios_locators.BOOK_NOW.get()).click()
        result = False
        try:
            WebDriverWait(steps.driver, 15).until(
                EC.visibility_of_element_located(
                    (By.ID, ios_locators.BOOK_CONFIRMED.get())))
            result = True
        except TimeoutException:
            try:
                steps.driver.execute_script('mobile: alert', {'action': 'accept'})
            except:
                pass
            result = False

        if result:
            reservation_id = steps.driver.find_element_by_xpath(
                "//*[./*[@name='{}']]/*".format(ios_locators.RESERVATION_NUMBER.get())).text
            booking.reservation_id = reservation_id
            price = steps.driver.find_element_by_xpath("//*[./*[@name='Autotest Mapsme']]/*[2]").text
            prog = re.compile(r"[0-9.]+")
            result = prog.search(price.replace(" ", "").replace(",", ""))
            booking.price = float(result[0])

        steps.driver.find_element_by_id("breadcrumb").click()
        return result
