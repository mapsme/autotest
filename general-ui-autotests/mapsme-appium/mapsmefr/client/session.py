import json
import logging
from datetime import datetime

import requests
from mapsmefr.client.device import Device
from mapsmefr.utils.tools import get_settings


class Session:

    def __init__(self):
        self.id = None
        self.build_number = None
        self.device_id = None
        self.time_start = None
        self.time_end = None
        self.caused_by = None
        self.upstream_job = None
        self.upstream_build_number = None
        self.upstream_url = None
        self.type = None
        self.test_count = None
        self.release_id = None
        self.url = "{}/session".format(get_settings('ReportServer', 'host'))

    def create(self, type, build_number=0, device_id=None, options=None):
        logging.info("session opts: {}".format(options))

        info = json.loads(options)
        self.type = type
        self.build_number = build_number
        self.device_id = Device.init_device(device_id).id
        self.time_start = datetime.now()
        self.caused_by = info["started_by"]
        self.upstream_job = info["name"]
        self.upstream_build_number = info["build_number"]
        self.upstream_url = info["url"]
        params = {"build_number": self.build_number,
                  "time_start": self.time_start,
                  "time_end": self.time_end,
                  "device_id": self.device_id,
                  "type": self.type,
                  "caused_by": info["started_by"],
                  "upstream_job": info["name"],
                  "upstream_build_number": info["build_number"],
                  "upstream_url": info["url"],
                  "jenkins_job": info["jenkins_job"] if "jenkins_job" in info else None,
                  "release": info["release"] if "release" in info else None,
                  "release_type": info["release_type"] if "release_type" in info else None,
                  "test_count": self.test_count
                  }
        responce = requests.post(self.url, data=params)
        self.id = int(responce.text)
        with open("session.txt", "w") as f:
            f.write("{}#!/top/session.hardware?id={}".format(get_settings('ReportServer', 'host'), self.id))

    def update_release(self, full_version):
        resp = requests.post("{}/{}".format(self.url, self.id), data={"version": full_version})
        self.release_id = json.loads(resp.text)["release_id"]

    def complete(self, status):
        self.time_end = datetime.now()
        params = {"time_end": self.time_end,
                  "status": status}
        requests.post("{}/{}".format(self.url, self.id), data=params)


class PytestMarkers():

    def __init__(self):
        self.url = "{}/markers".format(get_settings('ReportServer', 'host'))

    def update(self, markers):
        params = {"markers": json.dumps(list(markers))}
        requests.post("{}".format(self.url), data=params)
