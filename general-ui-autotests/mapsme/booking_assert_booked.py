import argparse
import json

import requests


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-bn", "--build_number", required=True)
    parser.add_argument("-ht", "--host", default="http://autotest.mapsme.cloud.devmail.ru/beta")
    parser.add_argument("-s", "--status", help="booked or cancelled")
    parser.add_argument("-u", "--user", required=True)
    parser.add_argument("-p", "--password", required=True)
    args = vars(parser.parse_args())
    return args


class BookingAsserter:

    def __init__(self, session_id):
        self.session = session_id
        self.bookings = []
        self.platform = None
        self.status = None
        self.host = None

    def get_all_booked_hotels(self):
        session_info = json.loads(requests.get("{}/session/{}".format(self.host, self.session)).text)
        platform = json.loads(requests.get("{}/device/{}".format(self.host, session_info["device_id"])).text)[
            "platform_name"]
        self.platform = platform
        response = requests.get("{}/testresult".format(self.host), params={"session_id": self.session})
        tests = json.loads(response.text)
        test_ids = [x["id"] for x in tests]
        for test_id in test_ids:
            response = requests.get("{}/booking".format(self.host), params={"test_result_id": test_id})
            books = json.loads(response.text)
            for b in books:
                if b["status"] == "Booked":
                    self.bookings.append(b)

    def get_today_bookings(self):
        host = "https://secure-distribution-xml.booking.com/2.4/json/bookingDetails"
        for booking in self.bookings:
            params = {"reservation_id": booking["reservation_id"].replace(".", "")}
            resp = requests.post(host, data=params, auth=(arg_parser()["user"], arg_parser()["password"]))
            result = json.loads(resp.text)["result"]
            need = result[0]
            print(str(need))
            aid = 1595466
            if self.platform == "IOS":
                aid = 1595464
            try:
                assert need["status"] == self.status
                assert need["guest_name"] == "Autotest Mapsme"
                assert need["affiliate_id"] == aid
                assert need["price_local"] == booking["price"]
            except AssertionError:
                with open("booking_check.txt", "a") as f:
                    f.write("Test failed:\n\tBooking # {}, hotel '{}'\n\t".format(
                        booking["reservation_id"].replace(".", ""), booking["name"]) +
                            "Expected status: {}, real status: {}\n\t".format(self.status, need["status"]) +
                            "Expected affiliate id: {}, real affiliate id: {}\n\t".format(aid, need["affiliate_id"]) +
                            "Expected price: {}, real price: {}\n\t".format(booking["price"], need["price_local"]))


if __name__ == '__main__':
    args = arg_parser()
    session_id = requests.get("{}/session".format(args["host"]), {"jenkins_job": args["build_number"]}).text
    asserter = BookingAsserter(session_id)
    asserter.status = args["status"]
    asserter.host = args["host"]
    asserter.get_all_booked_hotels()
    asserter.get_today_bookings()
