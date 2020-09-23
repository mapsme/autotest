from enum import Enum

from mapsmefr.pageobjects.switch import switch
from mapsmefr.steps.locators import Locator, LocalizedButtons
from mapsmefr.utils import expected_conditions as EC2
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings
from selenium.webdriver.support.wait import WebDriverWait


class GuidesCatalogLocators(Enum):
    GUIDES_CATALOG = {"ru": "Каталог путеводителей", "en": "Guides catalog"}
    TRY = {"ru": "Попробовать"}

    def get(self):
        return self.value[get_settings("Android", "locale")]


class GuidesCatalog:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    def switch_to_webview(self):
        WebDriverWait(self.driver, 20).until(EC2.web_view_context_enabled())
        contexts = self.driver.contexts
        cons = [x.split("_")[-1] for x in contexts if x != "NATIVE_APP"]
        self.driver.switch_to.context("WEBVIEW_{}".format(cons[-1]))

    def switch_to_native(self):
        pass

    @switch("native")
    def navigation_bar_title(self):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_id(GuidesCatalogLocators.GUIDES_CATALOG.get())
        else:
            return self.driver.find_element_by_xpath(
                "//*[contains(@text, '{}')]".format(GuidesCatalogLocators.GUIDES_CATALOG.get()))

    @switch("native")
    def close(self):
        if get_settings("System", "platform") == "IOS":
            return self.driver.find_element_by_id(Locator.DONE.get())
        else:
            return self.driver.find_element_by_id("close")

    @switch("web")
    def guide_title(self):
        return self.driver.find_element_by_xpath("//div[contains(@class, 'page__name')]")

    @switch("web")
    def guide_author(self):
        return self.driver.find_element_by_xpath("//a[contains(@class, 'page__author')]")

    @switch("web")
    def check_price_button(self):
        return self.driver.find_element_by_xpath("//a[contains(@class, 'ga_check-price_top')]")

    @switch("web")
    def breadcrumbs_active_item(self):
        return self.driver.find_element_by_xpath("//*[contains(@class, 'breadcrumbs__item_active')]")

    @switch("web")
    def see_all(self):
        if self.driver.context != "NATIVE_APP":
            return self.driver.find_element_by_xpath("//*[contains(@class, 'ga_see-all')]")
        else:
            if get_settings("System", "platform") == "IOS":
                return self.driver.find_element_by_id(LocalizedButtons.SEE_ALL.get())
            else:
                return self.driver.find_element_by_xpath("//*[@text='{}']".format(LocalizedButtons.SEE_ALL.get()))

    @switch("web")
    def filter_by_city(self):
        if self.driver.context != "NATIVE_APP":
            return self.driver.find_element_by_xpath("//input[@name='city']/preceding-sibling::div/input")
        else:
            if get_settings("System", "platform") == "IOS":
                return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeTextField'][1]")
            else:
                return self.driver.find_element_by_xpath("//*[@class='android.widget.EditText'][1]")

    @switch("web")
    def filter_by_tag(self):
        if self.driver.context != "NATIVE_APP":
            return self.driver.find_element_by_xpath("//input[@name='q']")
        else:
            if get_settings("System", "platform") == "IOS":
                return self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeTextField']")[1]
            else:
                return self.driver.find_elements_by_xpath("//*[@class='android.widget.EditText']")[1]

    @switch("web")
    def try_subscription(self):
        if self.driver.context != "NATIVE_APP":
            if self.driver.find_element_by_xpath("(//span[text()='{}'])".format(GuidesCatalogLocators.TRY.get())):
                self.driver.switch_to.context("NATIVE_APP")
                return self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeLink']")
            return self.driver.find_element_by_xpath("(//span[text()='{}'])|(//*[@class='billboard__image'])"
                                                     .format(GuidesCatalogLocators.TRY.get()))
        else:
            pass

    @switch("web")
    def search_result_dropdown(self, name):
        if self.driver.context != "NATIVE_APP":
            return self.driver.find_element_by_xpath(
                "//span[@class='input__item-name-inner' and text()='{}']".format(name))
        else:
            pass

    @switch("web")
    def clear_search(self):
        if self.driver.context != "NATIVE_APP":
            return self.driver.find_element_by_xpath("//*[contains(@class,'input__action')]")
        else:
            pass

    @switch("web")
    def subscribe_result_banner(self):
        if self.driver.context != "NATIVE_APP":
            return self.driver.find_element_by_xpath("//a[contains(@href, 'subscribe')]")
