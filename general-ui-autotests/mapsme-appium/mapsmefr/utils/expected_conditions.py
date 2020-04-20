from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.expected_conditions import _find_element


class web_view_context_enabled(object):

    def __call__(self, driver):
        try:
            cont = driver.contexts
            return len(cont) > 1
        except WebDriverException:
            return False


class element_to_be_dissapeared(object):

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            _find_element(driver, self.locator)
            return False
        except (NoSuchElementException, WebDriverException):
            return True


class presence_one_of_elements_located(object):
    def __init__(self, *locators):
        self.locators = locators

    def __call__(self, driver):
        for locator in self.locators:
            try:
                _find_element(driver, locator)
                return True
            except (NoSuchElementException, WebDriverException):
                pass
        else:
            return False
