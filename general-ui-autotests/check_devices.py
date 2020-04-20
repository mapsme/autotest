import argparse
import json
from subprocess import PIPE, run

import requests


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--platform", help="Android or ios", required=True)
    parser.add_argument("-s", "--server", help="Server host", required=False)
    args = vars(parser.parse_args())
    return args


def check_devices(before_devices, after_devices):
    changes_active = after_devices - before_devices
    changes_disabled = before_devices - after_devices
    if len(changes_active) > 0:
        with open("changes.txt", "a") as f:
            f.write("New active devices:\n")
            for ca in changes_active:
                f.write("\t{}\n".format(ca))
            f.write("\n")
    if len(changes_disabled) > 0:
        with open("changes.txt", "a") as f:
            f.write("Devices were disabled:\n")
            for cd in changes_disabled:
                f.write("\t{}\n".format(cd))
            f.write("\n")


if __name__ == "__main__":
    args = arg_parser()
    url = args["server"] if args["server"] is not None else "http://autotest.mapsme.cloud.devmail.ru"
    before_result = requests.get("{}/device".format(url), params={"status": "Active"})
    before_devices = json.loads(before_result.text)
    if args["platform"] == "Android":
        res = run(["adb devices -l | awk 'NR > 1 {print $1\" \"$2}'"], shell=True, stdout=PIPE, stderr=PIPE)
        result = [x.decode() for x in res.stdout.split(b'\n') if x.strip() != b'']
        active_devices = []
        for device in result:
            if device.split()[1] == "device":
                battery_res = run(["adb -s {} shell dumpsys battery | grep level | awk '{{print $2}}'".format(device.split()[0])], shell=True, stdout=PIPE, stderr=PIPE)
                active_devices.append({"name": device.split()[0], "battery": battery_res.stdout.decode().split("\n")[0].split("\r")[0]})
        requests.post("{}/refresh".format(url),
                      data={"active_devices": json.dumps(active_devices), "platform_name": "Android"})
    else:
        res = run(["idevice_id -l"], shell=True, stdout=PIPE, stderr=PIPE)
        result = [x.decode() for x in res.stdout.split(b'\n') if x != b'']
        active_devices = []
        for device in result:
            battery_res = run(
                ["ideviceinfo -u {} -q com.apple.mobile.battery -k BatteryCurrentCapacity".format(device.split()[0])],
                shell=True, stdout=PIPE, stderr=PIPE)
            active_devices.append({"name": device.split()[0], "battery": battery_res.stdout.decode().split("\n")[0].split("\r")[0]})
        requests.post("{}/refresh".format(url),
                      data={"active_devices": json.dumps(active_devices), "platform_name": "IOS"})
    after_result = requests.get("{}/device".format(url), params={"status": "Active"})
    after_devices = json.loads(after_result.text)

    check_devices(set([x["name"] for x in before_devices]), set([x["name"] for x in after_devices]))



