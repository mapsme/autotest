import json

import requests
from mapsmefr.utils.tools import get_settings


class JenkinsMapsme:

    def __init__(self):
        self.host = get_settings("Jenkins", "jenkins_url")
        self.user = get_settings("Jenkins", "jenkins_user")
        self.token = get_settings("Jenkins", "jenkins_token")
        self.session = None
        self.crumbs = None

    def get_session(self):
        if not self.session:
            self.session = requests.session()
            self.session.auth = (self.user, self.token)
            resp = self.session.get("{}/crumbIssuer/api/json".format(self.host))
            self.crumbs = json.loads(resp.text)["crumb"]
        return self.session

    def um24c_start(self, host, test_item):
        params = {"host": host,
                  "test_item": str(test_item)}
        response = self.get_session().post("{}/job/autotest-launcher/buildWithParameters"
                                           .format(self.host), data={"Jenkins-Crumb": self.crumbs, "token": self.token,
                                                                     "JOBNAME": "test-ios/um24c-start",
                                                                     "PARAMETERS": json.dumps(params)})
        return response.status_code == 201

    def um24c_kill(self):
        response = self.get_session().post("{}/job/autotest-launcher/buildWithParameters"
                                           .format(self.host), data={"Jenkins-Crumb": self.crumbs, "token": self.token,
                                                                     "JOBNAME": "test-ios/um24c-kill"})
        return response.status_code == 201
