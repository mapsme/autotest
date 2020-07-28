import logging
import subprocess
from os import system
from time import sleep

import pytest
from mapsmefr.client.appium_check import AppiumServer
from mapsmefr.client.device import Device
from mapsmefr.client.test_result import TestResult
from mapsmefr.steps.base_steps import BaseSteps
from mapsmefr.steps.locators import LocalizedButtons, Locator, LocalizedMapsNames
from mapsmefr.steps.routing_steps import RoutingSteps
from mapsmefr.steps.search_steps import SearchSteps
from mapsmefr.steps.settings_steps import SettingsSteps
from mapsmefr.steps.system_steps import SystemSteps
from mapsmefr.steps.bookmark_steps import BookmarkSteps
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import set_settings, get_settings


def pytest_addoption(parser):
    logging.info("adding pytest options")
    parser.addoption("--device-id", action="store", help="device name")
    parser.addoption("--apk-name", action="store", default="mapsme.ipa")
    parser.addoption("--build-number", action="store", default="0")
    parser.addoption("--session-info", action="store", default='{"name":"","build_number":"","url":"","started_by":""}')
    parser.addoption("--report-host", action="store", default="http://autotest.mapsme.cloud.devmail.ru")
    parser.addoption("--refresh-tests", action="store", default="false")
    parser.addoption("--booking-tests", action="store", default="false")  # todo
    parser.addoption("--skip-webview", action="store_true", default=False)

    # monkey ones
    parser.addoption("--monkey-time", action="store", default="3600")
    parser.addoption("--apk-version", action="store")
    parser.addoption("--apk-type", action="store")
    parser.addoption("--clean-device", action="store", default="false")
    parser.addoption("--clean-data", action="store", default="true")

    # hardware
    parser.addoption("--is-power", action="store_true", default=False)
    parser.addoption("--is-memory", action="store_true", default=False)
    parser.addoption("--is-standart", action="store_true", default=False)
    parser.addoption("--simulator", action="store_true", default=False)
    parser.addoption("--time", action="store", default="10", help='routing time in minutes')


def execute_adb_command(command):
    try:
        logging.info('\tTrying to execute command "{}"'.format(command))
        return subprocess.run([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    except Exception as e:
        logging.warning('\tError while executing command: {}'.format(e))


def unlock(device):
    if "iphone" not in device.lower():
        commands = []
        result = execute_adb_command("adb -s {} shell wm size".format(device))
        logging.info("result {}".format(result))
        size = result.decode().split(" ")[-1].replace("\n", "")
        logging.info("Screen size: {}".format(size))
        x = size.split("x")[0]
        y = size.split("x")[1]
        res1 = execute_adb_command("adb -s {} shell dumpsys power | grep 'mHoldingWakeLockSuspendBlocker'"
                                   .format(device)).decode().split("=")[-1].replace("\n", "").replace("\r", "")
        logging.info("Result: {}".format(res1))
        res2 = execute_adb_command("adb -s {} shell dumpsys power | grep 'mHoldingDisplaySuspendBlocker'"
                                   .format(device)).decode().split("=")[-1].replace("\n", "").replace("\r", "")
        logging.info("Result: {}".format(res2))
        if (res1 == "false" or res1 == "true") and res2 == "false":
            commands = ["adb -s {} shell input keyevent 26".format(device),
                        "adb -s {} shell input swipe {} {} {} {}".
                            format(device, round(int(x) / 4 * 3), round(int(y) / 4 * 3), round(int(x) / 4),
                                   round(int(y) / 4)),
                        "adb -s {} shell input text 0000".format(device),
                        "adb -s {} shell input keyevent 66".format(device)]
        if res1 == "false" and res2 == "true":
            commands = ["adb -s {} shell input swipe 400 1000 200 400",
                        "adb -s {} shell input text 0000",
                        "adb -s {} shell input keyevent 66"]

        for command in commands:
            execute_adb_command(command)


@pytest.yield_fixture(scope='session')
def driver(request, session):
    logging.info("[session] starting driver")
    if not request.config.getoption("--simulator"):
        unlock(request.config.getoption("--device-id"))
    driver = WebDriverManager.get_instance().driver
    driver.implicitly_wait(10)
    platform = WebDriverManager.get_instance().device.platform

    if platform == "Android":
        result = driver.execute_script("mobile: shell", {
            'command': "dumpsys window windows | grep -E 'mObscuringWindow|mHoldScreenWindow|mCurrentFocus' | grep -E 'mapswithme'"})
        locale = driver.execute_script("mobile: shell", {'command': "getprop persist.sys.locale"})
        if locale == "\n":
            locale = "en-US"
        app_package = result.split("/")[0].split(" ")[-1]
        set_settings("Android", "package", app_package)
        set_settings("Android", "locale", locale.split("-")[0])
    else:
        if WebDriverManager.get_instance().device.emulator:
            locale = b'en_US'
        else:
            locale = subprocess.run(["ideviceinfo -u {} -q com.apple.international -k Locale"
                                    .format(WebDriverManager.get_instance().device.udid)],
                                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        set_settings("Android", "locale", locale.decode().split("_")[0])
        # ideviceinstaller -U <UUID> -l | grep maps.me

    set_settings("Tests", "routing_time", request.config.getoption("--time"))
    set_settings("System", "platform", platform)
    yield driver
    WebDriverManager.destroy()


@pytest.fixture(scope="session", autouse=True)
def clean_device(request):
    logging.info("[session] cleaning device")
    commands = []
    device = Device.init_device(request.config.getoption("--device-id"))

    if device.platform == "Android":
        if request.config.getoption("--clean-device") == "true":
            logging.info("Cleaning device")
            commands.append("adb -s {} shell pm uninstall com.mapswithme.maps.pro".format(device.device_id))
            commands.append("adb -s {} shell pm uninstall com.mapswithme.maps.pro.beta".format(device.device_id))
            commands.append("adb -s {} shell pm uninstall com.mapswithme.maps.pro.debug".format(device.device_id))
            commands.append("adb -s {} shell pm uninstall io.appium.uiautomator2.server".format(device.device_id))
            commands.append("adb -s {} shell pm uninstall io.appium.uiautomator2.server.test".format(device.device_id))
            commands.append("adb -s {} shell pm uninstall io.appium.settings".format(device.device_id))

        if request.config.getoption("--clean-data") == "true":
            logging.info("Cleaning data on device")
            commands.append("adb -s {} shell rm -rf /storage/emulated/0/MapsWithMe".format(device.device_id))
            commands.append("adb -s {} shell rm -rf /storage/sdcard0/MapsWithMe".format(device.device_id))
    else:
        if request.config.getoption("--clean-device") == "true" and device.emulator is True:
            commands.append("ios-deploy -i {} -1 com.mapswithme.full -9".format(device.udid))
            commands.append("ios-deploy -i {} -1 com.my.maps-beta-enterprise -9".format(device.udid))
            commands.append("ios-deploy -i {} -1 com.facebook.wda.runner -9".format(device.udid))
            commands.append("ios-deploy -i {} -1 com.facebook.wda.lib -9".format(device.udid))

    for command in commands:
        try:
            logging.info('\tTrying to execute command "{}"'.format(command))
            system(command)
        except Exception as e:
            logging.warning('\tError while executing command: {}'.format(e))


@pytest.fixture(scope="session")
def check_appium():
    logging.info("[session] check appium")
    server = AppiumServer()
    if not server.check_if_connected():
        server.connect()
    if not server.check_if_okay():
        server.restart()


@pytest.fixture(scope="session")
def steps(driver):
    try:
        logging.info("[session] base steps")
        return BaseSteps.get()
    except Exception as e:
        print(e)


@pytest.fixture(scope="session")
def r_steps(driver):
    logging.info("[session] routing steps")
    return RoutingSteps.get()


@pytest.fixture(scope="session")
def system_steps(driver):
    logging.info("[session] system steps")
    return SystemSteps.get()


@pytest.fixture(scope="session")
def search_steps(driver):
    logging.info("[session] search steps")
    return SearchSteps.get()


@pytest.fixture(scope="session")
def settings_steps(driver):
    logging.info("[session] settings steps")
    return SettingsSteps.get()


@pytest.fixture(scope="session")
def bookmark_steps():
    logging.info("[session] bookmark steps")
    return BookmarkSteps.get()


@pytest.yield_fixture
def route_car(steps):
    yield
    if steps.try_get(LocalizedButtons.CANCELLATION.get()):
        steps.try_get(LocalizedButtons.CANCELLATION.get()).click()
    if steps.try_get(Locator.ROUTING_CAR.get()):
        steps.try_get(Locator.ROUTING_CAR.get()).click()
        sleep(2)


@pytest.fixture(scope="session")
def accept_privacy_policy(steps):
    logging.info("[session] accept privacy policy")
    steps.accept_privacy_policy()
    steps.close_first_time_frame()


@pytest.fixture
def download_moscow_map(steps):
    steps.download_map(LocalizedMapsNames.RUSSIA, None, LocalizedMapsNames.MOSCOW)


@pytest.yield_fixture
def press_back_to_main(steps):
    yield
    steps.press_back_until_main_page()


@pytest.yield_fixture
def switch_to_native(b_steps):
    if get_settings("System", "platform") == "IOS":
        WebDriverManager.get_instance().driver.execute_script("mobile: terminateApp",
                                                              {"bundleId": 'com.apple.mobilesafari'})
    yield
    b_steps.switch_to_native()


@pytest.yield_fixture
def return_back_to_mapsme(steps):
    yield
    driver = WebDriverManager.get_instance().driver
    try:
        if get_settings("System", "platform") == "Android":
            driver.execute_script("mobile: shell", {
                'command': "am start {}/com.mapswithme.maps.SplashActivity".format(get_settings("Android", "package"))})
            steps.close_first_time_frame()
        else:
            driver.execute_script("mobile: activateApp", {"bundleId": 'com.my.maps-beta-enterprise'})
            steps.close_first_time_frame()
    except:
        pass


@pytest.fixture
def emulate_location_moscow(driver):
    if get_settings("System", "platform") == "Android":
        pass
    else:
        if not WebDriverManager.get_instance().device.emulator:
            system("idevicelocation -u {} 55.758769 37.621199".format(WebDriverManager.get_instance().device.udid))
        else:
            WebDriverManager.get_instance().driver.set_location(55.758769, 37.621199, 0)
        # driver.set_location(55.758769, 37.621199, 0)


@pytest.fixture(scope="session")
def get_version(request, session, steps, settings_steps):
    logging.info("[session] get_version")
    steps.press_back_until_main_page()
    if steps.try_get_by_text(LocalizedButtons.STOP.get()):
        steps.try_get_by_text(LocalizedButtons.STOP.get()).click()
    settings_steps.open_settings()
    version = settings_steps.get_version().split(" ", 1)[1]
    session.update_release(version)
    steps.press_back_until_main_page()


@pytest.fixture(scope="session", autouse=True)
def session_fixtures(request, check_appium, driver, accept_privacy_policy, get_version):
    pass


def pytest_runtest_setup(item):
    if item.config.getoption("--refresh-tests") == "false":
        markers_android = [mark for mark in item.iter_markers(name="androidonly")]
        markers_ios = [mark for mark in item.iter_markers(name="iosonly")]
        markers_release = [mark for mark in item.iter_markers(name="releaseonly")]
        if len(markers_android) > 0:
            platform = Device.init_device(item.config.getoption("--device-id")).platform
            if platform == "IOS":
                session = item._request.getfixturevalue('session')
                test = TestResult()
                test.start(session.id, item.name)
                test.result("Skipped")
                pytest.skip("test can be run in Android only")
        if len(markers_ios) > 0:
            platform = Device.init_device(item.config.getoption("--device-id")).platform
            if platform == "Android":
                session = item._request.getfixturevalue('session')
                test = TestResult()
                test.start(session.id, item.name)
                test.result("Skipped")
                pytest.skip("test can be run in IOS only")
        if len(markers_release) > 0:
            if item.config.getoption("--apk-name") != "release":
                session = item._request.getfixturevalue('session')
                test = TestResult()
                test.start(session.id, item.name)
                test.result("Skipped")
                pytest.skip("test can be run in release version only")
        if item.config.getoption("--skip-webview") is True:
            markers = [mark for mark in item.iter_markers(name="webview")]
            if len(markers) > 0:
                session = item._request.getfixturevalue('session')
                test = TestResult()
                test.start(session.id, item.name)
                test.result("Skipped")
                pytest.skip("skipping webview tests")
