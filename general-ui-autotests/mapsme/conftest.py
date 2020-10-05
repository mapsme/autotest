import base64
import json
from datetime import datetime
from os import walk
from os.path import realpath, join, dirname
from subprocess import PIPE

import requests
from mapsmefr.client.session import Session, PytestMarkers
from mapsmefr.client.test_item import TestItem
from mapsmefr.client.test_result import TestResult
from mapsmefr.steps.fixtures import *
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings, set_settings


@pytest.yield_fixture(scope='session')
def driver_booking(request, session_booking):
    driver = WebDriverManager.get_instance().driver
    driver.implicitly_wait(10)
    platform = WebDriverManager.get_instance().device.platform

    if platform == "Android":
        result = driver.execute_script("mobile: shell", {'command': "dumpsys window windows | grep -E 'mCurrentFocus'"})
        locale = driver.execute_script("mobile: shell", {'command': "getprop persist.sys.locale"})
        app_package = result.split("/")[0].split(" ")[-1]
        set_settings("Android", "package", app_package)
        set_settings("Android", "locale", locale.split("-")[0])
    else:
        locale = subprocess.run(["ideviceinfo -u {} -q com.apple.international -k Locale"
                                .format(WebDriverManager.get_instance().device.udid)],
                                shell=True, stdout=PIPE, stderr=PIPE).stdout
        set_settings("Android", "locale", locale.decode().split("_")[0])

    set_settings("System", "platform", platform)
    yield driver
    WebDriverManager.destroy()


@pytest.yield_fixture(scope="session")
def session(request):
    session = Session()
    count = len([item for item in request.node.items])
    session.test_count = count
    session.create("ui", request.config.getoption("--build-number"), request.config.getoption("--device-id"),
                   request.config.getoption("--session-info"))
    yield session
    status = "Failed" if request.node.testsfailed > 0 else "Passed"
    session.complete(status)


@pytest.yield_fixture(scope="session")
def session_booking(request):
    session = Session()
    session.create("booking", request.config.getoption("--build-number"), request.config.getoption("--device-id"),
                   request.config.getoption("--session-info"))
    yield session
    status = "Failed" if request.node.testsfailed > 0 else "Passed"
    session.complete(status)


@pytest.yield_fixture(scope="function")
def testitem(request, session):
    test = TestResult()
    test.start(session.id, request.node.name)
    yield test
    status = "Failed"
    if request.node.rep_setup.passed and request.node.rep_call.passed:
        status = "Passed"
    if request.node.rep_setup.skipped:
        status = "Skipped"

    test.result(status)


@pytest.yield_fixture(scope="function")
def testitem_booking(request, session_booking):
    test = TestResult()
    test.start(session_booking.id, request.node.name)
    yield test
    status = "Passed" if request.node.rep_setup.passed and request.node.rep_call.passed else "Failed"
    test.result(status)


@pytest.fixture(scope="function", autouse=True)
def activate_app_if_crashed(steps):
    """Костыльная обработка крешей
    todo проверено только на ios"""
    logging.info("Check if app was crashed")
    if get_settings("System", "platform") == "IOS":
        try:
            cur_app = WebDriverManager.get_instance().driver.find_element_by_xpath(
                "//*[@type='XCUIElementTypeApplication']").text
            logging.info("current focus: {}".format(cur_app))
            if "maps.me" not in cur_app:
                logging.info("executing mobile:activateApp for {}".format(get_settings("Android", "package")))
                WebDriverManager.get_instance().driver.execute_script("mobile:activateApp",
                                                                      {"bundleId": get_settings("Android", "package")})
        except Exception as e:
            logging.info("executing mobile:activateApp for {}".format(get_settings("Android", "package")))
            WebDriverManager.get_instance().driver.execute_script("mobile:activateApp",
                                                                  {"bundleId": get_settings("Android", "package")})
    else:
        cur_focus = WebDriverManager.get_instance().driver.execute_script("mobile: shell", {
            'command': "dumpsys window windows | grep -E 'mObscuringWindow|mHoldScreenWindow|mCurrentFocus'"})
        if not get_settings("Android", "package") in cur_focus or "Application Error" in cur_focus:
            if "LauncherActivity" in cur_focus or "mCurrentFocus=null" in cur_focus:
                pass
            else:
                WebDriverManager.get_instance().driver.execute_script("mobile: shell", {
                    'command': "am start {}/com.mapswithme.maps.SplashActivity"
                                                                      .format(get_settings("Android", "package"))})
    steps.close_first_time_frame()


def pytest_configure(config):
    set_settings("ReportServer", "host", config.getoption("--report-host"))


@pytest.fixture(scope="session", autouse=True)
def refresh_tests(request):
    if request.config.getoption("--refresh-tests") == "true":
        session = request.node
        markers_set = set()
        system_markers = ("name", "parametrize", "skip")
        for item in session.items:
            markers = [mark for mark in item.iter_markers(name="name")]
            name = item.name
            doc = item.getparent(pytest.Class).obj.__dict__[name.split("[")[0]].__doc__
            if len(markers) > 0:
                all_markers = [mark.name for mark in item.iter_markers() if mark.name not in system_markers]
                markers_set.update(all_markers)
                test = TestItem()
                test.name = markers[0].kwargs["name"] if "name" in markers[0].kwargs else markers[0].args[0]
                test.scenario = markers[0].kwargs["scenario"] if "scenario" in markers[0].kwargs else None
                test.method = name
                test.type = "booking" if "[Booking.com]" in test.name else "ui"
                if len(all_markers) > 0:
                    test.markers = json.dumps(all_markers)
                if doc:
                    test.description = doc
                test.update_test()
        PytestMarkers().update(markers_set)
        pytest.skip("skipping all the tests")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    pytest_html = item.config.pluginmanager.getplugin('html')

    extra = getattr(rep, 'extra', [])
    if rep.when == 'call' or rep.when == 'setup':
        xfail = hasattr(rep, 'wasxfail')
        if (rep.skipped and xfail) or (rep.failed and not xfail):
            path = dirname(realpath(__file__)).split('mapsme')[0]
            filename = join(path, item.name + ".png")
            screencap = WebDriverManager.get_instance().driver.get_screenshot_as_base64()
            image_64_decode = base64.b64decode(screencap)
            log = "<br>".join([rep.longrepr.reprcrash.message] + rep.longrepr.reprtraceback.reprentries[0].lines)
            with open(filename, 'wb') as ff:
                ff.write(image_64_decode)
            test_r = None
            try:
                with open("testresult.txt", "r") as f:
                    test_r = f.read()

                params = {"test_result": test_r,
                          "log": "Error:<br> {}".format(log),
                          "file": screencap,
                          "timestamp": datetime.now(),
                          "is_fail": True,
                          "before": True}
                resp = requests.post("{}/testlog".format(get_settings("ReportServer", "host")), data=params)
            except FileNotFoundError:
                logging.info("TESTRESULT.TXT is NOT FOUND")

            extra.append(pytest_html.extras.image(item.name + ".png"))
        rep.extra = extra


def get_screenshot(filename):
    try:
        WebDriverManager.get_instance().driver.get_screenshot_as_file(filename)
        return True
    except Exception:
        logging.warning("Error while making screenshot!")
        return False
