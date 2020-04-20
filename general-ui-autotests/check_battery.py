import json

import requests

if __name__ == "__main__":
    after_result = requests.get("http://autotest.mapsme.cloud.devmail.ru/device", params={"status": "Active"})
    after_devices = json.loads(after_result.text)
    first = True
    for ad in after_devices:
        if ad["battery_level"] is not None and 0 < ad["battery_level"] < 30:
            with open("battery.txt", "a") as f:
                if first:
                    f.write("Battery level too low:\n")
                    first = False
                f.write("\t{}: {}%\n".format(ad["name"], ad["battery_level"]))
