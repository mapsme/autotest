import json
import logging

import requests
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from falcon.models import Devices

logger = logging.getLogger(__name__)


class Jenkins:
    def __init__(self):
        self.host = "https://client.jenkins.mapsme.devmail.ru/jenkins"
        self.user = "kkravchuk"
        self.token = "1136c9dd0f242f7c5f62bff76fbc974e21"
        self.session = None
        self.crumbs = None

    def get_session(self):
        if not self.session:
            self.session = requests.session()
            self.session.auth = (self.user, self.token)
            resp = self.session.get("{}/crumbIssuer/api/json".format(self.host))
            logger.debug(resp.text)
            self.crumbs = json.loads(resp.text)["crumb"]
        return self.session

    def android_ui_start(self, device_id, test_items, build_number, **kwargs):
        params = {"build_number": build_number,
                  "DEVICE_NAME": device_id,
                  "mark": str(test_items)}
        if build_number in ("beta", "debug", "release"):
            params["clean_device"] = False
        else:
            params["clean_device"] = True
        params.update(**kwargs)
        response = self.get_session().post("{}/job/autotest-launcher/buildWithParameters"
                                           .format(self.host), data={"Jenkins-Crumb": self.crumbs, "token": self.token,
                                                                     "JOBNAME": "test-android/ui-test-android",
                                                                     "PARAMETERS": json.dumps(params)})
        logger.debug(response.text)
        logger.debug(response.status_code)
        return response.status_code == 201

    def ios_ui_start(self, device_id, test_items, build_number, **kwargs):
        params = {"build_number": build_number,
                  "DEVICE_NAME": device_id,
                  "mark": str(test_items)}
        if build_number in ("beta", "debug", "release"):
            params["clean_device"] = False
        else:
            params["clean_device"] = True
        params.update(**kwargs)
        response = self.get_session().post("{}/job/autotest-launcher/buildWithParameters"
                                           .format(self.host), data={"Jenkins-Crumb": self.crumbs,"token": self.token,
                                                                     "JOBNAME": "test-ios/ui-test-ios",
                                                                     "PARAMETERS": json.dumps(params)})
        return response.status_code == 201

    def check_device(self, node):
        params = {"node": node}
        response = self.get_session().post("{}/job/autotest-launcher/buildWithParameters"
                                .format(self.host), data={"Jenkins-Crumb": self.crumbs, "token": self.token,
                                                          "JOBNAME": "at-infrastructure/check-devices-status",
                                                          "PARAMETERS": json.dumps(params)})
        return response.status_code == 201

    def kill_appium_session(self, device_id, node):
        params = {"device_id": device_id,
                  "node": node}
        response = self.get_session().post("{}/job/autotest-launcher/buildWithParameters"
                                           .format(self.host), data={"Jenkins-Crumb": self.crumbs, "token": self.token,
                                                                     "JOBNAME": "at-infrastructure/kill-appium-session",
                                                                     "PARAMETERS": json.dumps(params)})
        return response.status_code == 201


@require_POST
def start_build_check(request):
    device_id = request.POST["device_id"]
    build_number = request.POST["build_number"]
    device_platform = request.POST["device_platform"]
    skip_webview = True if request.POST["skip_webview"] == "1" else False
    if device_platform == "Android":
        result = Jenkins().android_ui_start(device_id, "build_check", build_number, EXCLUDE_WEBVIEW=skip_webview)
    else:
        result = Jenkins().ios_ui_start(device_id, "build_check", build_number, EXCLUDE_WEBVIEW=skip_webview)
    if result:
        return JsonResponse({})
    return JsonResponse({"error": "something went wrong on jenkins side"}, status=500)


@require_POST
def device_refresh(request):
    jenkins = Jenkins()
    result1 = jenkins.check_device("autotest")
    result2 = jenkins.check_device("naboo")

    if result1 and result2:
        return JsonResponse({})
    return JsonResponse({"error": "something went wrong on jenkins side"}, status=500)


@require_POST
def kill_appium_session(request, id):
    jenkins = Jenkins()
    device = Devices.objects.get(id=id)
    if device.platform_name == "Android":
       node = "autotest"
       device_id = device.devive_id
    else:
        node = "naboo"
        device_id = device.udid
    result = jenkins.kill_appium_session(device_id, node)
    if result:
        return JsonResponse({})
    return JsonResponse({"error": "something went wrong on jenkins side"}, status=500)


