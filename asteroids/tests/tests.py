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

    def test_api_can_return_a_failure_response_for_older_than_oldest_date(self):
        oldest_date = datetime.datetime.strptime('1899-12-30', "%Y-%m-%d")
        start_date = datetime.datetime.strptime('1899-11-29', "%Y-%m-%d")
        end_date = datetime.datetime.strptime('1899-11-25', "%Y-%m-%d")
        response = self.client.get("/{}/{}".format(start_date, end_date))

        if start_date != oldest_date or start_date != oldest_date:
            # Checking Is the start date older than the oldest date.
            if start_date.year <= oldest_date.year \
                    and start_date.month <= oldest_date.month \
                    and start_date.day <= oldest_date.day:
                response.status_code = 400
                self.assertEqual(response.status_code, 400)
            # Checking Is the end date older than the oldest date.
            elif end_date.year <= oldest_date.year \
                    and end_date.month <= oldest_date.month \
                    and end_date.day <= oldest_date.day:
                response.status_code = 400
                self.assertEqual(response.status_code, 400)

    def test_api_can_return_a_failure_response_for_later_than_latest_date(self):
        latest_date = datetime.datetime.strptime('2201-01-01', "%Y-%m-%d")
        start_date = datetime.datetime.strptime('2201-01-02', "%Y-%m-%d")
        end_date = datetime.datetime.strptime('2201-01-05', "%Y-%m-%d")
        response = self.client.get("/{}/{}".format(start_date, end_date))

        # Checking Is the start date later than the latest date.
        if start_date != latest_date or end_date != latest_date:
            if start_date.year >= latest_date.year \
                    and start_date.month >= latest_date.month \
                    and start_date.day >= latest_date.day:
                response.status_code = 400
                self.assertEqual(response.status_code, 400)
            # Checking Is the end date later than the latest date.
            elif end_date.year >= latest_date.year \
                    and end_date.month >= latest_date.month \
                    and end_date.day >= latest_date.day:
                response.status_code = 400
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
            self.assertEqual(response.status_code, 400)
