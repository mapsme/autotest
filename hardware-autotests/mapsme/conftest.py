import csv

import requests
from mapsmefr.client.jenkins import JenkinsMapsme
from mapsmefr.client.session import Session
from mapsmefr.client.test_result import TestResult
from mapsmefr.steps.fixtures import *
from os.path import dirname, realpath, join


@pytest.yield_fixture(scope="session")
def session(request):
    session = Session()
    session.create("hardware", request.config.getoption("--build-number"), request.config.getoption("--device-id"),
                   request.config.getoption("--session-info"))
    yield session
    status = "Failed" if request.node.testsfailed > 0 else "Passed"
    session.complete(status)


@pytest.yield_fixture(scope="class")
def lockito(request, driver):
    if get_settings("System", "platform") == "Android":
        driver.execute_script("mobile: shell", {'command': "am force-stop fr.dvilleneuve.lockito"})
        driver.execute_script("mobile: shell", {'command': "am start fr.dvilleneuve.lockito/.ui.SplashscreenActivity"})
        driver.implicitly_wait(120)
        driver.find_element_by_xpath("//*[@text='Москва-Воронеж']").click()

        driver.find_element_by_id("fr.dvilleneuve.lockito:id/playStopButton").click()
        driver.execute_script("mobile: shell", {
            'command': "am start {}/com.mapswithme.maps.SplashActivity".format(get_settings("Android", "package"))})
        driver.implicitly_wait(10)
        yield
        try:
            driver.execute_script("mobile: shell", {'command': "am force-stop fr.dvilleneuve.lockito"})
        except Exception as e:
            logging.error("{}".format(e))
    else:
        with open(join(dirname(realpath(__file__)).split('mapsme')[0], 'coords.csv'), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            row = next(spamreader)
            driver.set_location(row[0], row[1], row[2])
        yield
        with open(join(dirname(realpath(__file__)).split('mapsme')[0], 'coords.csv'), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            row = next(spamreader)
            driver.set_location(row[0], row[1], row[2])


@pytest.yield_fixture(scope="function")
def testitem(request, session):
    test = TestResult()
    test.is_memory = request.config.getoption("--is-memory")
    test.is_power = request.config.getoption("--is-power")
    test.is_standart = request.config.getoption("--is-standart")
    test.start(session.id, request.node.name)
    yield test
    status = "Failed"
    if hasattr(request.node, "rep_setup") and hasattr(request.node, "rep_call"):
        if request.node.rep_call.passed and request.node.rep_setup.passed:
            status = "Passed"
    test.result(status)


@pytest.yield_fixture
def um24c(request, testitem):
    host = get_settings('ReportServer', 'host')
    if get_settings("System", "platform") == "Android":
        if request.config.getoption("--is-power"):
            dir = dirname(realpath(__file__)).split('mapsme')[0]
            res = subprocess.Popen(
                ["{}um24c/app.js -a 00:BA:60:0A:05:59 -t {} -p -s {}".format(dir, testitem.id, host)],
                shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        yield
        if request.config.getoption("--is-power"):
            subprocess.Popen(["kill -9 {}".format(res.pid)], shell=True)
            subprocess.Popen(["kill -9 {}".format(res.pid + 1)], shell=True)
    else:
        if request.config.getoption("--is-power"):
            result = JenkinsMapsme().um24c_start(host, testitem.id)
            assert result, "Something went wrong in jenkins"
        yield
        if request.config.getoption("--is-power"):
            result = JenkinsMapsme().um24c_kill()
            assert result, "Something went wrong in jenkins"


@pytest.yield_fixture(scope="function")
def memory_script(request, testitem):
    host = get_settings('ReportServer', 'host')
    if get_settings("System", "platform") == "Android":
        if request.config.getoption("--is-memory"):
            dir = dirname(realpath(__file__)).split('mapsme')[0]
            res = subprocess.Popen(
                ["python3 {}mapsme/meminfo_android.py -t {} -s {} -d {} -p {}".format(dir, testitem.id, host,
                                                                                      WebDriverManager.get_instance().device.device_id,
                                                                                      get_settings("Android",
                                                                                                   "package"))],
                shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        yield
        if request.config.getoption("--is-memory"):
            subprocess.Popen(["kill -9 {}".format(res.pid)], shell=True)
    else:
        yield


@pytest.yield_fixture()
def check_diff(request, session, testitem):
    try:
        logging.info("Check if standart for this test, device and release exists")
        host = get_settings('ReportServer', 'host')
        params = {"test_item_method": testitem.test_item_method, "device_id": session.device_id,
                  "release_id": session.release_id, "metric_type": "power"}
        if not request.config.getoption("--is-standart"):
            logging.info("Not a standart")
            res = requests.get("{}/standart/check".format(host), params=params)
            if res.status_code != 200:
                pytest.fail("Something went wrong during check")
                logging.info(str(res.text))
            if res.text == 'false':
                pytest.fail(
                    "There are no standart metrics for test item '{}', device '{}'".format(testitem.test_item_method,
                                                                                           WebDriverManager.get_instance().device.name))
    except Exception as e:
        print(e)
    yield
    logging.info("Check diff")
    host = get_settings('ReportServer', 'host')
    params = {"chosen": testitem.id, "device_id": session.device_id, "release_id": session.release_id,
              "test_item_method": testitem.test_item_method}
    logging.info("params: {}".format(str(params)))
    if not request.config.getoption("--is-standart"):
        logging.info("Not a standart")
        if testitem.is_power:
            res = requests.get("{}/diff/power".format(host), params=params)
            logging.info("It is power test")
            if res.status_code != 200:
                pytest.fail(
                    "Something went wrong during comparing power results, please check if you have standart for this test/device")
            logging.info("Diff is {}%".format(res.text))
            if int(res.text) > 10:
                pytest.fail("An average charge difference between current test and standart is {}%".format(res.text))
        if testitem.is_memory:
            res = requests.get("{}/diff/memory".format(host), params=params)
            logging.info("It is memory test")
            if res.status_code != 200:
                pytest.fail(
                    "Something went wrong during comparing memory results, please check if you have standart for this test/device")
            logging.info("Diff is {}%".format(res.text))
            if int(res.text) > 10:
                pytest.fail("An average memory difference between current test and standart is {}%".format(res.text))


def pytest_configure(config):
    set_settings("ReportServer", "host", config.getoption("--report-host"))


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
            result = get_screenshot(filename)
            if result:
                extra.append(pytest_html.extras.image(item.name + ".png"))
        rep.extra = extra


def get_screenshot(filename):
    try:
        WebDriverManager.get_instance().driver.get_screenshot_as_file(filename)
        return True
    except Exception:
        logging.warning("Error while making screenshot!")
        return False
