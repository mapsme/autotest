import json
import logging
import platform
import socket
import subprocess
from os.path import join, dirname, realpath
from subprocess import PIPE

import pytest
import requests
from mapsmefr.utils.tools import get_settings, set_settings


class Device:

    def __init__(self, info):
        self.id = info['id']
        self.name = info['device_id'] if pytest.config.getoption("--simulator") else info["name"]
        self.device_id = "emulator-5554" if pytest.config.getoption("--simulator") else info['device_id']
        self.udid = info['udid']
        self.platform = info['platform_name']
        self.platform_version = info['platform_version']
        self.status = info['status']
        self._server_url = info["server_url"]
        self.emulator = pytest.config.getoption("--simulator")

    @staticmethod
    def init_device(device_id):
        host = get_settings('ReportServer', 'host')
        response = requests.get("{}/device/{}".format(host, device_id))
        info = json.loads(response.text)
        info["server_url"] = host
        if info['platform_name'] == 'Android':
            return AndroidDevice(info)
        else:
            return IOSDevice(info)

    def get_capabilities(self):
        pass

    def check_active(self):
        pass

    def reboot(self):
        pass


class AndroidDevice(Device):

    def __init__(self, info):
        super().__init__(info)

    def get_capabilities(self):
        apk_path = "{}/{}".format(pytest.config.rootdir.dirname, pytest.config.getoption("--apk-name"))
        automation = 'UIAutomator2' if float(self.platform_version) >= 5.0 else "UiAutomator"

        caps = {
            # 'app': apk_path,
            'newCommandTimeout': 900,
            'autoGrantPermissions': True,
            'automationName': automation,
            'platformName': self.platform,
            'platformVersion': self.platform_version,
            'deviceName': self.device_id,
            'udid': self.device_id,
            'systemPort': find_open_port(),
            'chromedriverUseSystemExecutable': True,
            'showChromedriverLog': True
            # 'normalizeTagNames': True,
            # "unlockType": "pin",
            # "unlockKey": "0000"

            # 'chromedriverExecutable': '/usr/local/lib/node_modules/appium-chromedriver/chromedriver/mac/chromedriver'
        }

        if self.emulator:
            caps["avd"] = self.name

        if not self.emulator:
            chrome_ver = subprocess.run(
                ["adb -s {} shell dumpsys package com.android.chrome | grep versionName".format(self.device_id)],
                shell=True,
                stdout=PIPE, stderr=PIPE)
            res = [x.decode() for x in chrome_ver.stdout.split(b'\n') if x.strip() != b'']
            ver = res[0].split("=")[1].rsplit(".", 2)[0]
            platf = "linux" if platform.system() == "Linux" else "mac"

            logging.info("CHROMEDRIVER VERSION: {}".format(ver))

            chromedriver = join(pytest.config.rootdir.strpath, "chromedriver_dir",
                                "chromedriver_{}_{}".format(ver, platf))

            caps['chromedriverExecutable'] = chromedriver

        if pytest.config.getoption("--booking-tests") == 'true':
            caps['chromeOptions'] = {"androidPackage": "com.android.chrome"}

        if pytest.config.getoption("--apk-name") in ("beta", "debug", "release"):
            bn = pytest.config.getoption("--apk-name")
            num = ".{}".format(bn) if bn != "release" else ""
            caps['appPackage'] = "com.mapswithme.maps.pro{}".format(num)
            caps['appActivity'] = "com.mapswithme.maps.SplashActivity"
        else:
            caps["app"] = apk_path

        return caps

    def check_active(self):
        if self.emulator:
            return True
        else:
            res = subprocess.run(["adb devices -l | awk 'NR > 1 {print $1}'"], shell=True, stdout=PIPE, stderr=PIPE)
            active_devices = [x.decode() for x in res.stdout.split(b'\n') if x != b'']
            requests.post("{}/refresh".format(self._server_url),
                          data={"active_devices": json.dumps(active_devices), "platform_name": self.platform})
            if self.device_id in active_devices:
                return True
            else:
                return False

    def reboot(self):
        subprocess.run(["adb -s {} reboot".format(self.device_id)], shell=True, stdout=PIPE, stderr=PIPE)


class IOSDevice(Device):

    def __init__(self, info):
        super().__init__(info)

    def get_capabilities(self):
        app_path = "{}/{}".format(pytest.config.rootdir.dirname, pytest.config.getoption("--apk-name"))
        caps = {
            # "noReset": True,
            # "fullReset": False,
            "browserName": "",
            "showXcodeLog": False,
            "xcodeOrgId": "3T6FSDE8C7",
            "xcodeSigningId": "iPhone Developer",
            'automationName': 'XCUITest',
            'newCommandTimeout': 900,
            "useNewWDA": True,
            "wdaLocalPort": find_open_port(),
            "waitForQuiescence": False,
            'platformName': self.platform,
            'platformVersion': self.platform_version,
            'deviceName': self.device_id,
            'udid': self.udid,
            # 'startIWDP': True,
            'webkitResponseTimeout': 30000,
            "language": "ru",
            "locale": "ru",
            "safariLogAllCommunication": True,
            "webviewConnectTimeout": 10000,
            "includeSafariInWebviews": True,
            # "fullContextList": True

        }

        set_settings("Android", "package", "com.my.maps-beta-enterprise")

        if pytest.config.getoption("--apk-name") in ("beta", "debug", "release"):
            bn = pytest.config.getoption("--apk-name")
            caps["bundleId"] = "com.my.maps-beta-enterprise" if bn == "beta" else "com.mapswithme.full"
            set_settings("Android", "package", caps["bundleId"])
        else:
            #if "Release" in pytest.config.getoption("--apk-name"):
            #    set_settings("Android", "package", "com.mapswithme.full")
            caps["app"] = app_path

        return caps

    def check_active(self):
        if not self.emulator:
            res = subprocess.run(["idevice_id -l"], shell=True, stdout=PIPE, stderr=PIPE)
            active_devices = [x.decode() for x in res.stdout.split(b'\n') if x != b'']
            logging.info("udid: {}, active={}".format(self.udid, active_devices))
            requests.post("{}/refresh".format(self._server_url),
                          data={"active_devices": json.dumps(active_devices), "platform_name": self.platform})
            if self.udid in active_devices:
                return True
            else:
                return False
        else:
            return True

    def reboot(self):
        subprocess.run(["idevicediagnostics -u {} restart".format(self.udid)], shell=True, stdout=PIPE, stderr=PIPE)


def find_open_port():
    for port in range(8200, 8299):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(('', port))
                return port
            except OSError:
                pass
