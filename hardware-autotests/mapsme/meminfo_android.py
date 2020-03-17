import argparse
import time
from datetime import datetime
from subprocess import run, PIPE

import requests


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--testid", help="Test result id", required=True)
    parser.add_argument("-s", "--server", help="Host", required=True)
    parser.add_argument("-d", "--device", help="Device", required=True)
    parser.add_argument("-p", "--package", help="Package", required=True)
    args = vars(parser.parse_args())
    return args


if __name__ == '__main__':
    args = arg_parser()
    test = args["testid"]
    host = args["server"]
    device = args["device"]
    package = args["package"]
    print(str(args))
    while True:
        inf = run(["adb -s {} shell dumpsys meminfo {}".format(device, package)], shell=True, stdout=PIPE, stderr=PIPE)
        mem = 0
        timestamp = None
        for line in inf.stdout.decode().split("\n"):
            if "TOTAL" in line:
                mem = int(line.split()[1])
                timestamp = datetime.now().timestamp()
                break

        try:
            response = requests.post("{}/meminfo".format(host),
                                     data={"record_timestamp": timestamp,
                                             "total_memory_in_bytes": mem,
                                             "test_result_id": test})
            if response.status_code != 200:
                print(response.text)
        except:
            print("something went wrong")
        time.sleep(5)
