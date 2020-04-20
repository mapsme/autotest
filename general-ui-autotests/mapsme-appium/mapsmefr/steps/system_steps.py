import logging
from time import sleep

from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.steps.locators import IOSOnlySystemLocators, LocalizedButtons
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings


class SystemSteps:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    @staticmethod
    def get():
        if get_settings("System", "platform") == "Android":
            return AndroidSystemSteps()
        else:
            return IosSystemSteps()

    def execute_deeplink(self, deeplink):
        pass

    def execute_deeplink_universal(self, deeplink):
        pass

    def execute_onelink_deeplink(self, deeplink):
        pass

    def restart_app(self):
        pass

    def start_mail_app(self):
        pass


class AndroidSystemSteps(SystemSteps):

    def execute_deeplink(self, deeplink):
        self.driver.execute_script("mobile: shell",
                                   {'command': "am force-stop {}".format(get_settings("Android", "package"))})
        self.driver.execute_script("mobile:deepLink", {
            "url": deeplink,
            "package": get_settings("Android", "package")})

    def execute_deeplink_universal(self, deeplink):
        self.execute_deeplink(deeplink)

    def execute_onelink_deeplink(self, deeplink):
        self.driver.execute_script("mobile: shell",
                                   {'command': "am force-stop {}".format(get_settings("Android", "package"))})
        self.driver.execute_script("mobile:deepLink", {
            "url": deeplink,
            "package": "com.android.chrome"})

        sleep(10)
        self.driver.execute_script("mobile: shell",
                                   {'command': "am force-stop com.android.chrome"})

    def restart_app(self):
        self.driver.execute_script("mobile: shell",
                                   {'command': "am force-stop {}".format(get_settings("Android", "package"))})
        sleep(10)
        self.driver.execute_script("mobile: shell", {
            'command': "am start {}/com.mapswithme.maps.SplashActivity".format(get_settings("Android", "package"))})
        sleep(5)

    def start_mail_app(self):
        self.driver.execute_script("mobile: shell",
                                   {'command': "am force-stop com.google.android.gm"})
        sleep(5)

        self.driver.execute_script("mobile: shell", {
            'command': "am start com.google.android.gm/com.google.android.gm.ui.MailActivityGmail"})


class IosSystemSteps(SystemSteps):

    def execute_deeplink_universal(self, deeplink):
        self.driver.execute_script("mobile: terminateApp", {"bundleId": "com.apple.mobilenotes"})
        sleep(3)

        self.driver.execute_script("mobile: launchApp",
                                   {"bundleId": "com.apple.mobilenotes"})

        self.driver.find_element_by_id(IOSOnlySystemLocators.NEW_NOTE.get()).click()
        self.driver.find_element_by_id(IOSOnlySystemLocators.NOTE_FIELD.get()).send_keys(deeplink)
        self.driver.find_element_by_id(LocalizedButtons.DONE.get()).click()

        sleep(3)

        loc = self.driver.find_element_by_xpath("//*[@type='XCUIElementTypeLink']").location
        TouchAction(self.driver).press(x=loc["x"] + 20, y=loc["y"] + 20).release().perform()

    def execute_deeplink(self, deeplink):
        driver = WebDriverManager.get_instance().driver
        logging.info("Terminating Safari")
        driver.execute_script("mobile: terminateApp", {"bundleId": "com.apple.mobilesafari"})
        logging.info("Terminating mapsme")
        driver.execute_script("mobile: terminateApp", {"bundleId": get_settings("Android", "package")})

        sleep(3)

        logging.info("Executing deeplink: {}".format(deeplink))

        driver.execute_script("mobile: launchApp",
                              {"bundleId": "com.apple.mobilesafari", "arguments": ["-U", deeplink]})

        driver.find_element_by_id(LocalizedButtons.OPEN.get()).click()

    def execute_onelink_deeplink(self, deeplink):
        self.execute_deeplink_universal(deeplink)

    def restart_app(self):
        logging.info("Terminate app")
        self.driver.execute_script("mobile: terminateApp", {"bundleId": get_settings("Android", "package")})
        sleep(5)
        logging.info("Activate app")
        self.driver.execute_script("mobile: activateApp", {"bundleId": get_settings("Android", "package")})
        sleep(5)

    def start_mail_app(self):
        self.driver.execute_script("mobile: terminateApp", {"bundleId": "com.apple.mobilemail"})
        sleep(5)
        self.driver.execute_script("mobile: launchApp", {"bundleId": "com.apple.mobilemail"})
