from functools import wraps

import pytest
from mapsmefr.utils.driver import WebDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from mapsmefr.utils import expected_conditions as EC2


def switch(context_type):
    if context_type not in ("native", "web"):
        raise Exception("Context type must be native or web")

    def switch_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if context_type == "native":
                driver = WebDriverManager.get_instance().driver
                if driver.context != "NATIVE_APP":
                    driver.switch_to.context("NATIVE_APP")
            else:
                driver = WebDriverManager.get_instance().driver
                if driver.context == "NATIVE_APP":
                    try:
                        WebDriverWait(driver, 20).until(EC2.web_view_context_enabled())
                        contexts = driver.contexts
                        cons = [x.split("_")[-1] for x in contexts if x != "NATIVE_APP" and "chrome" not in x]
                        if len(cons) > 0:
                            driver.switch_to.context("WEBVIEW_{}".format(cons[-1]))
                    except TimeoutException:
                        pass

            return func(*args, **kwargs)

        return wrapper

    return switch_wrapper
