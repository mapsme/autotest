import requests
from mapsmefr.utils.tools import get_settings


class TestItem:

    def __init__(self):
        self.id = None
        self.method = None
        self.name = None
        self.type = None
        self.description = None
        self.markers = None
        self.url = "{}/testitem/refresh".format(get_settings('ReportServer', 'host'))

    def update_test(self):
        params = {"name": self.name,
                  "method_name": self.method,
                  "type": self.type,
                  "comment": self.description,
                  "marks": self.markers}
        if self.id:
            params["id"] = self.id
        response = requests.post(self.url, data=params)

        assert response.status_code == 200
