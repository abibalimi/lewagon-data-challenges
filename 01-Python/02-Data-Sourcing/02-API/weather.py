# pylint: disable=missing-docstring, fixme

import sys
import requests

BASE_URI = "https://www.metaweather.com"
DEGREE_SIGN = u"\N{DEGREE SIGN}"


def search_city(query):
    # TODO: Look for a given city and disambiguate between several candidates.
    # Return one city (or None)
    url = BASE_URI + "/api/location/search/?query=" + query
    response = requests.get(url).json()
    try:
        city = response[0]
        #print(f"{city})")
        #print(f"{city['title']}: {city['woeid']} ({city['latt_long']})")
        print(f"Here is the weather in {city['title']}")
        return city
    except IndexError:
        print(f"Sorry, MetaWeather does not know abour {query}...")
        return None


def weather_forecast(woeid):
    #import pdb; pdb.set_trace()
    # TODO: Return a 5-element list of weather forecast for a given woeid
    url = f"{BASE_URI}/api/location/{woeid}"
    response = requests.get(url).json()
    return response['consolidated_weather']


def main():
    query = input("City?\n> ")
    if query:
        city = search_city(query)
        # TODO: Display weather forecast for a given city
        if city:
            woeid = city['woeid']
            forecasts = weather_forecast(woeid)
            for forecast in forecasts[0:5]:
                print(f"{forecast['applicable_date']}: {forecast['weather_state_name']}"
                      f" {round(forecast['max_temp'], 1)}{DEGREE_SIGN}C")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
