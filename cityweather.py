import requests
from datetime import date
from datetime import datetime
from datetime import timezone
from cityapi import getLatLong


def get_city_weather(city :str, country :str):
    '''
    This functions returns today's date. The city's temperature and the ammount of rain falling.
    input: city : str , country : str
    output : str

    '''
    resultat = getLatLong(city=city, country=country)
    latitude = resultat[0]
    longitude = resultat[1]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,rain"

    r = requests.get(url)
    data = r.json()

    data_date = data["hourly"]["time"][0]
    data_temp = data["hourly"]["temperature_2m"][0]
    data_temp_celisius = data["hourly_units"]["temperature_2m"]
    data_rain = data["hourly"]["rain"][0]

    return f"Today is {data_date}, it's {data_temp} {data_temp_celisius} in {city},{country}. And it's raining {data_rain} mm."


if __name__ == "__main__":

    resultat = get_city_weather(city="Paris", country="France")
    print(resultat)
