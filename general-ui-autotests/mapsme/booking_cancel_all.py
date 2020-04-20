import argparse
import json
import platform
from os.path import realpath, dirname, join
from time import sleep

import requests
from mapsmefr.utils.tools import get_settings
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-bn", "--build_number")
    parser.add_argument("-ht", "--host", default="http://autotest.mapsme.cloud.devmail.ru/beta")
    args = vars(parser.parse_args())
    return args


class BookingCanceller:

    def __init__(self):
        self.driver = self.init_driver()
        self.session = None
        self.bookings = []
        self.host = None
        self.cookies = None

    def init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        # options.add_argument("--kiosk") for debug with no-headless mode
        options.add_argument("--no-sandbox")
        chrome = "chromedriver"
        if platform.system() == "Linux":
            chrome += "_linux"
        driver = webdriver.Chrome(join(dirname(realpath(__file__)), chrome), options=options)
        driver.set_window_size(2560, 1600)
        driver.implicitly_wait(30)
        return driver

    def get_all_booked_hotels(self):
        response = requests.get("{}/testresult".format(self.host), params={"session_id": self.session})
        tests = json.loads(response.text)
        test_ids = [x["id"] for x in tests]
        for test_id in test_ids:
            response = requests.get("{}/booking".format(self.host), params={"test_result_id": test_id})
            books = json.loads(response.text)
            for b in books:
                if b["status"] == "Booked":
                    self.bookings.append(b)

    def sign_in(self):
        self.driver.find_element_by_xpath("//input[@id='username']").send_keys(get_settings("Tests", "booking_user"))
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        self.driver.find_element_by_xpath("//input[@id='password']").send_keys(get_settings("Tests", "booking_pass"))
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(@class,'user_name_block')]")))

    def cancel(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'modal-wrapper')]")))
            self.driver.refresh()
        except:
            pass

        self.driver.find_element_by_xpath("//a[contains(@class,'mb-cancel')]").click()
        sleep(1)
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='personal_reasons_trip_called_off']")))

        except TimeoutException:
            self.driver.find_element_by_xpath("//button[@class='modal-mask-closeBtn']").click()
            sleep(1)
            self.driver.find_element_by_xpath("//a[contains(@class,'mb-cancel')]").click()
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@id='personal_reasons_trip_called_off']")))

        self.driver.find_element_by_xpath("//input[@id='personal_reasons_trip_called_off']").click()
        sleep(2)

        for cookie in self.cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)

        print(self.driver.get_cookies())
        cs = self.driver.find_element_by_xpath("//*[@id='cancel_sure']")
        cs.click()
        WebDriverWait(self.driver, 60).until(EC.staleness_of(cs))

        try:
            ok = self.driver.find_element_by_xpath("//input[@class='MyBookingOptionsSaveChanges']")
            ok.click()
            WebDriverWait(self.driver, 20).until(EC.staleness_of(ok))
            self.driver.find_element_by_xpath("//li[@id='current_account']/a").click()
            self.sign_in()
            self.cookies = self.driver.get_cookies()
        except:
            pass

        self.driver.find_element_by_xpath("//div[@class='mb-back']/a").click()

        try:
            self.sign_in()
            self.cookies = self.driver.get_cookies()
        except:
            pass

        sleep(5)

    def cancel_by_session(self):
        try:
            self.driver.get("https://www.booking.com")
            self.driver.find_element_by_xpath("//li[@id='current_account']/a").click()
            self.sign_in()

            self.cookies = self.driver.get_cookies()

            self.driver.get("https://secure.booking.com/myreservations.ru.html")

            for booking in self.bookings:
                try:
                    need_booking = self.driver.find_element_by_xpath(
                        """//div[contains(@class,'mytrips-item') 
                            and contains(@class,'bui-card') 
                            and not(.//div[contains(@class,'mytrips-item__status--cancelled')]) 
                            and .//span[text()='{}']]""".format(booking["name"]))
                    self.driver.get(need_booking.find_element_by_xpath(
                        ".//div[contains(@class,'mytrips-item__name')]/a").get_attribute("href"))
                    self.cancel()


                except Exception as e:
                    print("Cannot find hotel '{}' in list".format(booking))
                    print(str(e))

        except Exception as e:
            self.driver.save_screenshot("error.png")
            print(str(e))
        finally:
            self.driver.quit()

    def cancel_all(self):
        try:
            self.driver.get("https://www.booking.com")
            self.driver.find_element_by_xpath("//li[@id='current_account']/a").click()
            self.sign_in()

            self.cookies = self.driver.get_cookies()

            self.driver.get("https://secure.booking.com/myreservations.ru.html")

            bookings = self.driver.find_elements_by_xpath(
                "//div[contains(@class,'bui-card mtr-two-column-card') and not(.//div[text()='Canceled'])]")
            for i, _ in enumerate(bookings):
                self.driver.get(
                    self.driver.find_element_by_xpath(
                        "//div[contains(@class,'bui-list__description')]/a[contains(@class,'mtr-action-link')]").get_attribute(
                        "href"))
                self.cancel()

            cancelled_bookings = self.driver.find_elements_by_xpath(
                "//div[@class='js-booking_block' and ./div[contains(@class,'mb-block--cancelled')]]")

            for i, _ in enumerate(cancelled_bookings):
                sleep(1)
                try:
                    self.driver.find_element_by_xpath("//a[contains(@href,'remove_booking')]").click()
                except:
                    print("no delete from list button!")
                sleep(2)
        except Exception as e:
            self.driver.save_screenshot("error.png")
            print(str(e))
        finally:
            self.driver.quit()

        # self.driver.save_screenshot("file.png")


if __name__ == '__main__':
    args = arg_parser()
    booking_canceller = BookingCanceller()
    booking_canceller.host = args["host"]
    if args["build_number"]:
        session_id = requests.get("{}/session".format(args["host"]), {"jenkins_job": args["build_number"]}).text
        booking_canceller.session = session_id
        booking_canceller.get_all_booked_hotels()
        booking_canceller.cancel_by_session()
    else:
        booking_canceller.cancel_all()
