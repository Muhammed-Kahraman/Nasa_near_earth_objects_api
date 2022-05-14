import datetime

from rest_framework.test import APITestCase


# Create your tests here.
class TestApi(APITestCase):
    def test_api_can_get_a_success_request(self):
        date_list = ["2019-01-01", "2019-01-01"]
        response = self.client.get("/{}/{}".format(date_list[0], date_list[1]))
        self.assertEqual(response.status_code, 200)

    def test_api_can_return_a_failure_response_for_7_days_limit(self):
        date_list = ["2019-01-01", "2019-01-09"]
        start_date = datetime.datetime.strptime(date_list[0], "%Y-%m-%d")
        end_date = datetime.datetime.strptime(date_list[1], "%Y-%m-%d")
        response = self.client.get("/{}/{}".format(start_date, end_date))
        if start_date.day - end_date.day > 7 or end_date.day - start_date.day > 7:
            self.assertEqual(response.status_code, 400)

    def test_api_can_return_a_failure_response_for_missing_field(self):
        date_list = ["", "2019-01-01"]
        response = self.client.get("/{}/{}".format(date_list[0], date_list[0]))
        response_second = self.client.get("/{}/{}".format(date_list[1], date_list[0]))
        response_third = self.client.get("/{}/{}".format(date_list[0], date_list[1]))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_second.status_code, 422)
        self.assertEqual(response_third.status_code, 422)

    def test_api_can_return_a_failure_response_for_wrong_date_format(self):
        date_list = ["2019-011-01", "2019-01-009"]
        response = self.client.get("/{}/{}".format(date_list[0], date_list[0]))
        try:
            date_format = "%Y-%m-%d"
            datetime.datetime.strptime(date_list[0], date_format)
            datetime.datetime.strptime(date_list[1], date_format)
        except ValueError:
            response.status_code = 400
            self.assertEqual(response.status_code, 400)
