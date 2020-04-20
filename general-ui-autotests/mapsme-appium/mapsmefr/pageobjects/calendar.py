from babel.dates import format_date
from mapsmefr.steps.locators import LocalizedButtons
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings


class IosSystemCalendar:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    def choose_date(self, when):
        when_day = format_date(when, "dd")
        when_month = format_date(when, "MMMM", get_settings("Android", "locale"))
        when_year = format_date(when, "yyyy")

        self.choose_day(when_day)
        self.choose_month(when_month)
        self.choose_year(when_year)

    def choose_month(self, month):
        wheels = [x.text for x in self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypePickerWheel']")]
        need_wheel_index = 1
        for i, wheel in enumerate(wheels):
            try:
                val = int(wheel)
            except ValueError:
                need_wheel_index = i + 1
                break
        wheel = self.driver.find_element_by_xpath(
            "//*[@type='XCUIElementTypePickerWheel'][{}]".format(need_wheel_index))
        wheel.send_keys(month)

    def choose_day(self, day):
        wheels = [x.text for x in self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypePickerWheel']")]
        need_wheel_index = 1
        for i, wheel in enumerate(wheels):
            try:
                val = int(wheel)
                if val <= 31:
                    need_wheel_index = i + 1
                    break
            except ValueError:
                pass
        wheel = self.driver.find_element_by_xpath(
            "//*[@type='XCUIElementTypePickerWheel'][{}]".format(need_wheel_index))
        wheel.send_keys(day)

    def choose_year(self, year):
        wheels = [x.text for x in self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypePickerWheel']")]
        need_wheel_index = 1
        for i, wheel in enumerate(wheels):
            try:
                val = int(wheel)
                if val > 31:
                    need_wheel_index = i + 1
                    break
            except ValueError:
                pass

        wheel = self.driver.find_element_by_xpath(
            "//*[@type='XCUIElementTypePickerWheel'][{}]".format(need_wheel_index))
        wheel.send_keys(year)

    def click_done(self):
        self.driver.find_element_by_id(LocalizedButtons.DONE.get()).click()


class AndroidSystemCalendar:
    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    def choose_month(self, month):
        pass

    def choose_day(self, day):
        pass

    def choose_date(self, when):
        when_date = format_date(when, "dd MMMM yyyy", get_settings("Android", "locale"))
        need = self.driver.find_elements_by_xpath(
            "//*[@class='android.view.View' and @content-desc='{}']".format(when_date))

        while len(need) == 0:
            self.driver.find_element_by_id("android:id/next").click()
            need = self.driver.find_elements_by_xpath(
                "//*[@class='android.view.View' and @content-desc='{}']".format(when_date))

        self.driver.find_element_by_xpath(
            "//*[@class='android.view.View' and @content-desc='{}']".format(when_date)).click()

    def choose_year(self, year):
        pass

    def click_done(self):
        self.driver.find_element_by_id("android:id/button1").click()
