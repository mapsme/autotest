import json
import logging
import time
from datetime import datetime
from os import makedirs, remove, system
from os.path import isdir, isfile, exists

import pytest
import requests
from mapsmefr.client.session import Session
from mapsmefr.steps.fixtures import unlock
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import set_settings, get_settings
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException


class TestMonkeyAndroidMapsme:
    count_crashes = 0
    crashes = []

    @pytest.yield_fixture(scope="session")
    def session(self, request):
        session = Session()
        session.create("monkey", request.config.getoption("--build-number"), request.config.getoption("--device-id"),
                       request.config.getoption("--session-info"))
        logging.info("==============================================================================================")
        logging.info(
            "SESSION LINK:    {}#!/top/session.monkey?id={}".format(get_settings("ReportServer", "host"), session.id))
        logging.info("==============================================================================================")
        yield session
        status = "Failed" if request.node.testsfailed > 0 else "Passed"
        session.complete(status)

    @pytest.yield_fixture(scope='session')
    def driver(self, request):
        unlock(request.config.getoption("--device-id"))
        driver = WebDriverManager.get_instance().driver
        driver.implicitly_wait(30)
        platform = WebDriverManager.get_instance().device.platform
        set_settings("System", "platform", platform)
        result = driver.execute_script("mobile: shell", {'command': "dumpsys window windows | grep -E 'mCurrentFocus'"})
        locale = driver.execute_script("mobile: shell", {'command': "getprop persist.sys.locale"})
        app_package = result.split("/")[0].split(" ")[-1]
        set_settings("Android", "package", app_package)
        set_settings("Android", "locale", locale.split("-")[0])
        yield driver
        try:
            WebDriverManager.destroy()
        except (InvalidSessionIdException, WebDriverException):
            logging.info("Session deleted by timeout")

    @pytest.yield_fixture()
    def config(self, request):
        yield {"device": request.config.getoption("--device-id"),
               "time": int(request.config.getoption("--monkey-time")),
               "version": request.config.getoption("--apk-version"),
               "type": request.config.getoption("--apk-type")
               }

    def test_monkey(self, clean_device, driver, session, accept_privacy_policy, config):
        with open("crashes-{}.txt".format(config["type"]), "w+") as f:
            f.write("Found crashes:\n")
        logging.info("{} Monkey test start at device {}".format(datetime.now(), config["device"]))
        startTime = time.time()
        finTime = startTime + config["time"]
        while time.time() < finTime:
            self.start_test1(session.id, config["device"], 1000, config["version"])
        self.analyze_crashes(config["type"])
        logging.info("{} Done".format(datetime.now()))
        self.get_crashes_stats(session.id, config["type"])

    def start_test1(self, session_id, devID, acts, appVer):
        fnm = time.time()
        fn = "{}.txt".format(fnm)
        self.start_monkey(devID, fn, acts, appVer)
        is_crash = self.analyze_monkey_log(fnm, devID, appVer)
        if is_crash:
            self.count_crashes += 1
            logging.error("{} Crash #{}".format(datetime.now(), self.count_crashes))
            self.send_crash(session_id, len(self.crashes), self.crashes[-1])

    def start_monkey(self, devID, out_file, acts, appVer):
        if isdir("logs/{}/{}".format(appVer, devID)) == False:
            makedirs("logs/{}/{}".format(appVer, devID))
        if isfile("logs/{}/{}/{}".format(appVer, devID, out_file)) == True:
            remove("logs/{}/{}/{}".format(appVer, devID, out_file))
        pack_name = get_settings("Android", "package")
        system("adb -s {} shell monkey -p {} -v --pct-syskeys 0 {} > logs/{}/{}/{} 2>&1".format(devID, pack_name,
                                                                                                acts, appVer,
                                                                                                devID,
                                                                                                out_file))

    def analyze_monkey_log(self, n, devID, appVer):
        pos = None
        f = "logs/{}/{}/{}.txt".format(appVer, devID, n)
        if exists(f):
            with open(f, 'r') as s:
                lines = s.readlines(-1)
                for p, line in enumerate(lines):
                    if '// CRASH: com.mapswithme' in line:
                        pos = p
                if pos:
                    tmp_crash = ["===== Monkey crash start at {}, iteration #{} =====\n".format(devID, n)]
                    for line in lines[pos:]:
                        tmp_crash.append(line)
                    tmp_crash.append("===== Monkey crash end at {}, iteration #{} =====\n".format(devID, n))
                    self.crashes.append(tmp_crash)
        return pos is not None

    def analyze_crashes(self, type):
        if len(self.crashes) > 0:
            for i, items in enumerate(self.crashes):
                log = ["\n",
                       "======================================\n",
                       "============= Crash # {} =============\n".format(i + 1),
                       "======================================\n\t"]
                log.extend(items)
                current_crash = "\t".join(log)
                logging.info(current_crash)
                with open("crashes-{}.txt".format(type), "a") as f:
                    f.write(current_crash)


        else:
            logging.info("No crashes found")
            with open("crashes-{}.txt".format(type), "a") as f:
                f.write("\tNo crashes found")

    def send_crash(self, session_id, num, text):
        err_text = "".join(text).split("** Monkey aborted due to error.")[0]
        if "backtrace" in err_text:
            err_text = err_text.split("backtrace:\n")[-1]
        else:
            err_text = err_text.split("Build Time:")[-1].split("\n", 1)[-1]
        params = {"session_id": session_id,
                  "crash_number": num,
                  "full_crash_text": "<br>".join(text),
                  "error_text": err_text}
        try:
            resp = requests.post("{}/monkeycrash".format(get_settings("ReportServer", "host")), data=params)
            if resp.status_code != 200:
                logging.error("something went wrong!!!")
                logging.info(str(params))
                logging.info(resp.status_code)
                logging.info(resp.text)
        except:
            logging.error("something went wrong!!!")

    def get_crashes_stats(self, session_id, type):
        params = {"session_id": session_id}
        resp = requests.get("{}/monkey/sessionstats".format(get_settings("ReportServer", "host")), params=params)
        with open("crashes-stats-{}.json".format(type), "a") as f:
            data = json.loads(resp.text)
            data["url"] = "{}/#!/top/session.monkey?id={}".format(get_settings("ReportServer", "host"), session_id)
            f.write(json.dumps(data))
