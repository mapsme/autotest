import logging
from enum import Enum
from time import sleep

from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.steps.locators import LocalizedButtons, BookingButtons, Locator
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import WebDriverException


class DiscoveryPage:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    def first_hotel_type(self, ind=1):
        types = [BookingButtons.HOSTEL.get(), BookingButtons.HOTEL.get(), BookingButtons.APARTMENTS.get(),
                 BookingButtons.CAMPING.get(), BookingButtons.CHALET.get(), BookingButtons.GUEST_HOUSE.get(),
                 BookingButtons.RESORT.get(), BookingButtons.MOTEL.get()]
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.HOTEL_BOOKING.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeStaticText' and (@name='{}')][{}]".format("' or @name='".join(types), ind))
        else:
            return self.driver.find_element_by_id("hotels").find_elements_by_id("subtitle")[ind - 1]

    def first_hotel_name(self, ind=1):
        if get_settings("System", "platform") == "IOS":
            logging.info("{}".format("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]"
                                     .format(LocalizedButtons.HOTEL_BOOKING.get().upper())))
            # logging.info(self.driver.page_source)
            els = self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*".format(
                LocalizedButtons.HOTEL_BOOKING.get().upper()))
            while els[0].tag_name == 'XCUIElementTypeAny':
                els = self.driver.find_elements_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*".format(
                        LocalizedButtons.HOTEL_BOOKING.get().upper()))
            types = [BookingButtons.HOSTEL.get(), BookingButtons.HOTEL.get(), BookingButtons.APARTMENTS.get(),
                     BookingButtons.CAMPING.get(), BookingButtons.CHALET.get(), BookingButtons.GUEST_HOUSE.get(),
                     BookingButtons.RESORT.get(), BookingButtons.MOTEL.get()]
            need = None
            index = None
            cur_ind = 0
            if els[0].tag_name == 'XCUIElementTypeAny':
                els = self.driver.find_elements_by_xpath(
                    "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*".format(
                        LocalizedButtons.HOTEL_BOOKING.get().upper()))
            for i, el in enumerate(els):
                if el.text in types:
                    need = el
                    index = i
                    cur_ind = cur_ind + 1
                    if cur_ind == ind:
                        break
            else:
                assert False, "No hotels on discovery page!"

            return els[index - 1]
        else:
            return self.driver.find_element_by_id("hotels").find_elements_by_id("title")[ind - 1]

    def first_attraction_name(self, ind=1):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.ATTRACTIONS.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeStaticText'][{}]".format(ind))
        else:
            return self.driver.find_element_by_id("attractions").find_elements_by_id("title")[ind - 1]

    def first_attraction_type(self, ind=1):
        if get_settings("System", "platform") == "IOS":
            els = self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*".format(
                LocalizedButtons.ATTRACTIONS.get().upper()))

            index = None

            name = self.first_attraction_name().text
            for i, el in enumerate(els):
                if el.text == name:
                    index = i
                    break
            else:
                assert False, "No attractions on discovery page!"

            return els[index + 1]

        else:
            return self.driver.find_element_by_id("attractions").find_elements_by_id("subtitle")[ind - 1]

    def first_eat_name(self, ind=1):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.EAT_AND_DRINK.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeStaticText'][{}]".format(ind))
        else:
            return self.driver.find_element_by_id("food").find_elements_by_id("title")[ind - 1]

    def first_eat_type(self, ind=1):
        if get_settings("System", "platform") == "IOS":
            els = self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*".format(
                LocalizedButtons.EAT_AND_DRINK.get().upper()))

            index = None

            name = self.first_eat_name().text
            for i, el in enumerate(els):
                if el.text == name:
                    index = i
                    break
            else:
                assert False, "No eat and drinks on discovery page!"

            return els[index + 1]
        else:
            return self.driver.find_element_by_id("food").find_elements_by_id("subtitle")[ind - 1]

    def first_guide_name(self, ind=1):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.GUIDES.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeStaticText'][{}]".format(ind))
        else:
            return self.driver.find_element_by_id("catalog_promo_recycler").find_elements_by_id("title")[ind - 1]

    def first_guide_type(self, ind=1):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.GUIDES.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeStaticText'][{}]".format(ind * 2))
        else:
            return self.driver.find_element_by_id("catalog_promo_recycler").find_elements_by_id("subtitle")[ind - 1]

    def first_guide_details(self):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.GUIDES.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeButton'and (@name='{}')]".format(LocalizedButtons.DETAILS.get()))
        else:
            return self.driver.find_element_by_id("catalog_promo_recycler").find_element_by_id("button")

    def first_hotel_route_to(self):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.HOTEL_BOOKING.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeButton' and (@name='{}')]".format(LocalizedButtons.TO.get()))
        else:
            return self.driver.find_element_by_id("hotels").find_element_by_id("button")

    def first_attraction_route_to(self):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.ATTRACTIONS.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeButton' and (@name='{}')]".format(LocalizedButtons.TO.get()))
        else:
            return self.driver.find_element_by_id("attractions").find_element_by_id("button")

    def first_eat_route_to(self):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.EAT_AND_DRINK.get().upper())).find_element_by_xpath(
                "./*[@type='XCUIElementTypeButton' and (@name='{}')]".format(LocalizedButtons.TO.get()))
        else:
            return self.driver.find_element_by_id("food").find_element_by_id("button")

    def first_attraction_popular(self):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.ATTRACTIONS.get().upper())).find_element_by_id(Locator.POPULAR.get())
        else:
            return self.driver.find_element_by_id("attractions").find_element_by_id(Locator.POPULAR.get())

    def first_eat_popular(self):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]".format(
                LocalizedButtons.EAT_AND_DRINK.get().upper())).find_element_by_id(Locator.POPULAR.get())
        else:
            return self.driver.find_element_by_id("food").find_element_by_id(Locator.POPULAR.get())

    def slide_left(self, coord_y, times):
        for _ in range(times):
            coords_x_from = self.driver.get_window_size()['width'] * 0.8
            coords_x_to = self.driver.get_window_size()['width'] * 0.2
            actions = TouchAction(
                self.driver)  # да, тут нужно создавать объет заново, потому что после первого эксепшона все летит к чертям
            try:
                actions.press(None, coords_x_from, coord_y) \
                    .wait(4000).move_to(None, coords_x_to,
                                        coord_y).release().perform().release().perform()
            except WebDriverException:
                pass

        sleep(5)

    def click_more(self, coord_y):
        actions = TouchAction(self.driver)
        coord_x = self.driver.get_window_size()['width'] * 0.8
        actions.tap(None, coord_x, coord_y).perform()
