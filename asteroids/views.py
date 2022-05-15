# Importing the necessary libraries.
import datetime
from pprint import pprint

import orjson
import requests
from decouple import config
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Sorting function by closest distance to earth.
def Sort(sub_li):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    sub_li.sort(key=lambda x: x.get('miss_distance_km'))
    return sub_li


# Create your views here.
@api_view(['GET'])
def getDates(request, start_date="", end_date=""):
    # If start_date or end_date is not provided, we are returning the error message.
    if start_date == "" or end_date == "":
        # splitting  the errors more specific way.
        if start_date == "" and end_date != "":
            return Response("The start date field is a required field! Please fill it out.",
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif start_date != "" and end_date == "":
            return Response("The end date field is a required field! Please fill it out.",
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response("The start date and end date fields are required fields! Please fill it out.",
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # If start date or end date not empty then we can proceed to check the dates are valid or not.
    else:
        # Defining variable we need in the future.
        is_valid_date = True
        name_string = "Name: "
        closes_date_string = 'Close_approach_date_full: '
        estimated_diameter_name = 'Estimated_diameter (km):'
        miss_distance_string = 'Miss_distance:'
        dates = []
        all_data = []
        api_key = config('apiKey')
        date_format = "%Y-%m-%d"
        oldest_date_contains_data = datetime.datetime.strptime('1899-12-30', date_format)
        latest_date_contains_data = datetime.datetime.strptime('2201-01-01', date_format)
        try:
            # Checking if the start and end date are in valid format.
            start_date = datetime.datetime.strptime(start_date, date_format)
            end_date = datetime.datetime.strptime(end_date, date_format)
            if start_date.day - end_date.day > 7 or start_date.day - end_date.day > 7:
                return Response('The difference between start and end date is cannot be more than 7 '
                                'days',
                                status=status.HTTP_400_BAD_REQUEST)

            # Checking start date or end date not equals the oldest date.
            if start_date != oldest_date_contains_data or end_date != oldest_date_contains_data:

                # Checking Is the start date older than the oldest date.
                if start_date.year <= oldest_date_contains_data.year \
                        and start_date.month <= oldest_date_contains_data.month \
                        and start_date.day <= oldest_date_contains_data.day:

                    return Response("The oldest date that contains data 1899-12-30."
                                    " You can't go back any further than that date. ",
                                    status=status.HTTP_400_BAD_REQUEST)

                # Checking Is the end date older than the oldest date.
                elif end_date.year <= oldest_date_contains_data.year \
                        and end_date.month <= oldest_date_contains_data.month \
                        and end_date.day <= oldest_date_contains_data.day:

                    return Response("The oldest date that contains data 1899-12-30."
                                    " You can't go back any further than that date. ",
                                    status=status.HTTP_400_BAD_REQUEST)

                # Checking Is the start date later than the latest date.
                if start_date != latest_date_contains_data or end_date != latest_date_contains_data:
                    if start_date.year >= latest_date_contains_data.year \
                            and start_date.month >= latest_date_contains_data.month \
                            and start_date.day >= latest_date_contains_data.day:
                        return Response("The latest date that contains data 2201-01-01."
                                        "You can't go any further than that date. (For now)",
                                        status=status.HTTP_400_BAD_REQUEST)

                    # Checking Is the end date later than the latest date.
                    elif end_date.year >= latest_date_contains_data.year \
                            and end_date.month >= latest_date_contains_data.month \
                            and end_date.day >= latest_date_contains_data.day:
                        return Response("The latest date that contains data 2201-01-01."
                                        "You can't go any further than that date. (For now)",
                                        status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            is_valid_date = False

        # if the both date valid then we can proceed.
        if is_valid_date:
            url_neo_feed = "https://api.nasa.gov/neo/rest/v1/feed?"
            # Creating a cache key and looking for data inside cache memory.
            cache_key = f'nasa_neo_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}'
            json_data = cache.get(cache_key)
            # If data is not found in cache then we are making a new request to the API.
            if not json_data:
                response = requests.get(url_neo_feed, params={
                    'api_key': api_key,
                    'start_date': start_date,
                    'end_date': end_date
                })
                response.raise_for_status()
                json_data = orjson.loads(response.text)

            # After getting the data from the API we are storing it in cache memory.
            cache.set(cache_key, json_data, timeout=4000)
            date_asteroids = json_data['near_earth_objects']

            # Iterating over the dates and add to them a list one by one.
            for date in date_asteroids:
                dates.append(date)

            # Getting the data for each date.
            for date in dates:
                collection = json_data.get('near_earth_objects')
                unsplit_data = collection.get('{}'.format(date))
                day_list = []
                # Iterating over the data for getting specific data each asteroid.
                for list_data in unsplit_data:
                    name = list_data.get('name')
                    closes_date = list_data.get('close_approach_data')
                    estimated_diameter = list_data.get('estimated_diameter')
                    estimated_diameter_kilometers = estimated_diameter.get('kilometers')
                    json_dict =  {
                        'name': name,
                        'closest_date': closes_date[0].get('close_approach_date_full'),
                        'miss_distance_km' : closes_date[0].get('miss_distance').get('kilometers'),
                        'estimated_diameter_km': estimated_diameter_kilometers
                    }
                    all_data.append(json_dict)

            # Checking if the data is empty or not. If empty then return HTTP_404_NOT_FOUND.
            # İf not empty then return HTTP_200_OK
            if all_data is not None:
                sorted_all_data = Sort(all_data)
                return Response(sorted_all_data, status=status.HTTP_200_OK)

            # If data is empty then return HTTP_404_NOT_FOUND.
            else:
                return Response("Oops! Something went wrong. But don't worry we are working on it.",
                                status=status.HTTP_404_NOT_FOUND)

        # If the date is not valid then return HTTP_400_BAD_REQUEST
        else:
            return Response('Incorrect date format it should be YYYY-MM-DD',
                            status=status.HTTP_400_BAD_REQUEST)
