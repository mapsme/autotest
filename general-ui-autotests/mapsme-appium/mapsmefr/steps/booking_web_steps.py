import logging
from time import sleep

from mapsmefr.utils.driver import WebDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BookingWebSearchForm:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    def form(self):
        return self.driver.find_element_by_xpath("//form[@id='form_search_location']")

    def direction(self):
        return self.driver.find_element_by_xpath("//*[@id='input_destination']")

    def checkin_date(self):
        return self.driver.find_element_by_xpath("//div[@id='ci_date']")

    def checkin_input(self):
        return self.driver.find_element_by_xpath("//input[@id='ci_date_input']")

    def checkout_date(self):
        return self.driver.find_element_by_xpath("//div[@id='co_date']")

    def submit_search(self):
        return self.driver.find_element_by_xpath("//button[@id='submit_search']")

    def datepicker_ci_selected(self):
        return self.driver.find_element_by_xpath("//td[contains(@class, 'is-selected')]")

    def datepicker_ci_last_day(self):
        return [x for x in self.driver.find_elements_by_xpath(
            "//div[contains(@class, 'pikaday-checkin')]//button[@class='pika-button pika-day']") if x.text != ''][-1]

    def datepicker_next_arrow(self):
        return self.driver.find_element_by_xpath("//button[contains(@class, 'pika-next')]")

    def book(self):
        return self.driver.find_element_by_xpath("//button[@name='book']")

    def price(self):
        return self.driver.find_element_by_id("cost_with_addons")

    def free_cancellation(self):
        return self.driver.find_element_by_xpath("//*[@data-filter-key='cancellation']")

    def go_to_variants(self):
        return self.driver.find_element_by_xpath("//a[contains(@href, '#availabilityBlock')]")

    def first_book_variant(self):
        return [x for x in self.driver.find_elements_by_xpath(
            "//button[contains(@class, 'js-rt_select_btn') or contains(@class, 'rt_select_btn')]") if x.text != ''][0]

    def wait_search_overlay(self):
        try:
            search_overlay = self.driver.find_element_by_xpath(
                "//div[contains(@class, 'search_overlay')]")
            WebDriverWait(self.driver, 20).until(EC.staleness_of(search_overlay))
        except (NoSuchElementException, TimeoutException):
            pass

    def fill_cc_data(self, cc_number):
        card = [cc_number[:4], cc_number[4:8], cc_number[8:12], cc_number[12:]]
        for c in card:
            self.driver.find_element_by_xpath("//input[@id='cc_number']").send_keys(c)
            sleep(1)

        logging.info("CC number: {}".format(cc_number))

        self.driver.find_element_by_xpath("//input[@id='cc_expiry_date']").send_keys(
            "01")
        sleep(1)
        self.driver.find_element_by_xpath("//input[@id='cc_expiry_date']").send_keys(
            "25")
        sleep(1)
        logging.info("CC expiry date: 01/25")

        try:
            self.driver.find_element_by_xpath("//input[contains(@id, 'cc_cvc')]").send_keys("111")
            logging.info("CVC code: 111")
        except:
            logging.info("No field for cvc code")

    def go_to_first_result(self):
        variant = self.driver.find_element_by_xpath("//div[@data-block='results']//ol[@id='sr']//a")
        link = variant.get_attribute("href")
        self.driver.get(link)

    def wait_booked_stamp(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='booked-stamp']")))
            return True
        except TimeoutException:
            logging.info("Booked stamp didn't appear")  # security issue
            return False

    def reservation_id(self):
        return self.driver.find_element_by_xpath("//td[contains(@class, 'pb-bui-booking-ref__value-bn')]").text

    def save_old_bookings(self):
        try:
            self.driver.find_element_by_xpath("//label[contains(@class,'book_and_cancel-confirm_label')]").click()
        except:
            pass
