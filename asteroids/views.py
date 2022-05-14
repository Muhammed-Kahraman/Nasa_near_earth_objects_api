# Importing the necessary libraries.
import datetime
import orjson
import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decouple import config

# Sorting function by closest distance to earth.
def Sort(sub_li):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    sub_li.sort(key=lambda x: x[2])
    return sub_li


# Create your views here.
@api_view(['GET'])
def getDates(request, start_date="", end_date=""):
    # If start_date or end_date is not provided, we are returning the error message.
    if start_date is "" or end_date is "":
        # splitting  the errors more specific way.
        if start_date is "" and end_date is not "":
            return Response("The start date field is a required field! Please fill it out.",
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif start_date is not "" and end_date is "":
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
        all_data = list()
        api_key = config('apiKey')
        date_format = "%Y-%m-%d"

        try:
            # Checking if the start and end date are in valid format.
            start_date = datetime.datetime.strptime(start_date, date_format)
            end_date = datetime.datetime.strptime(end_date, date_format)
            if start_date.day - end_date.day > 7 or start_date.day - end_date.day > 7:
                return Response('The difference between start and end date is cannot be more than 7 '
                                'days',
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            is_valid_date = False

        # if the both date valid then we can proceed.
        if is_valid_date:
            print("Input date is valid ..")
            url_neo_feed = "https://api.nasa.gov/neo/rest/v1/feed?"
            # Creating a cache key and looking for data inside cache memory.
            cache_key = f'nasa_neo_{start_date}_{end_date}'.strip("")
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
            print(json_data['element_count'])

            # Iterating over the dates and add to them a list one by one.
            for date in date_asteroids:
                dates.append(date)

            # Getting the data for each date.
            for date in dates:
                collection = json_data.get('near_earth_objects')
                unsplit_data = collection.get('{}'.format(date))

                # Iterating over the data for getting specific data each asteroid.
                for list_data in unsplit_data:
                    name = list_data.get('name')
                    closes_date = list_data.get('close_approach_data')
                    estimated_diameter = list_data.get('estimated_diameter')
                    estimated_diameter_kilometers = estimated_diameter.get('kilometers')

                    # Iterating over the data for getting more specific data that we wanted.
                    for full_date in closes_date:
                        full_date_object = full_date.get('close_approach_date_full')
                        miss_distance = full_date.get('miss_distance')
                        miss_distance_kilometer = miss_distance.get('kilometers')
                        all_data.append([name_string + name, closes_date_string + full_date_object,
                                         miss_distance_string + " " + miss_distance_kilometer + " km",
                                         estimated_diameter_name, estimated_diameter_kilometers])

            # Checking if the data is empty or not. If empty then return HTTP_404_NOT_FOUND.
            # İf not empty then return HTTP_200_OK
            if all_data is not None:
                sorted_all_data = Sort(all_data)
                return Response(sorted_all_data, status = status.HTTP_200_OK)

            # If data is empty then return HTTP_404_NOT_FOUND.
            else:
                return Response("Oops! Something went wrong. But don't worry we are working on it.",
                                status=status.HTTP_404_NOT_FOUND)

        # If the date is not valid then return HTTP_400_BAD_REQUEST
        else:
            print("The date is not valid.")
            return Response('Incorrect date format it should be YYYY-MM-DD',
                            status=status.HTTP_400_BAD_REQUEST)
