# pylint: disable=missing-docstring, fixme

import sys
import urllib.parse
import requests

BASE_URI = "https://www.metaweather.com"


def search_city(query):
    # TODO: Look for a given city and disambiguate between several candidates. Return one city (or None)
    url = BASE_URI + "/api/location/search/?query=" + query
    response = requests.get(url).json()
    try:
        city = response[0]
        print(f"{city})")
        #print(f"{city['title']}: {city['woeid']} ({city['latt_long']})")
    except IndexError:
        print(f"Sorry, MetaWeather does not know abour {query}...")


def weather_forecast(woeid):
    # TODO: Return a 5-element list of weather forecast for a given woeid
    pass


def main():
    query = input("City?\n> ")
    city = search_city(query)
    # TODO: Display weather forecast for a given city


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
