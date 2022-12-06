import requests
import emoji
from code_dict import code_dict


def get_lat_long(city: str, country: str):
    """
    This function returns latitude and longitude
    input : city : str , country : str
    output : list
    """
    response = requests.get(
        url=f"https://api.api-ninjas.com/v1/geocoding?city={city}&country={country}",
        headers={"X-Api-Key": "write your NinjasAPI key here"},
    )

    data_city = response.json()

    return [round(data_city[0]["latitude"], 2), round(data_city[0]["longitude"], 2)]


def get_city_weather(city: str, country: str):
    """
    This functions returns today's date. The city's temperature and the amount of rain falling.
    input: city : str , country : str
    output : json object

    """
    result = get_lat_long(city=city, country=country)

    url = f"https://api.open-meteo.com/v1/forecast?latitude={result[0]}&longitude={result[1]}&hourly=temperature_2m,relativehumidity_2m,precipitation,rain,snowfall,snow_depth,weathercode,visibility,windspeed_10m&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&timezone=auto"

    response = requests.get(url)
    data = response.json()

    return data


def get_weather_description(chosen_key: str):
    """
    Function that sends weather message given a key
    Input: chosen_key: str
    Output: key value(message)
    """
    return code_dict[chosen_key]


def send_sms(message: str, phone_number: str):
    '''
    Function that sends an sms text using a SMS sender API.
    Input : message : str , phone_number:str
    Output : Status of post-call
    '''
    request = requests.post(
        "https://textbelt.com/text",
        {
            "phone": phone_number,
            "message": message,
            "key": "textbelt_test",
        },
    )

    print(request.json())


def weather_notifier(city: str, country: str, phone_number: str):

    data = get_city_weather(city=city, country=country)

    
    data_date = data["hourly"]["time"][0]

    dates = data_date.split("T")

    
    data_sunrise = data["daily"]["sunrise"][0]
    sunrises = data_sunrise.split("T")

    
    data_sunset = data["daily"]["sunset"][0]
    sunsets = data_sunset.split("T")

    message_to_send = f"""
    
    Today is {dates[0]} {dates[1]} {data["timezone_abbreviation"]} in {city}, {country}. \n
    Right now :  The temperature  is {data["hourly"]["temperature_2m"][0]} {data["hourly_units"]["temperature_2m"]}. \n
    It's raining {data["hourly"]["rain"][0]} {data["hourly_units"]["rain"]} with {data["hourly"]["precipitation"][0]} {data["hourly_units"]["precipitation"]} precipitation
    
    and snow is at {data["hourly"]["snowfall"][0]} {data["hourly_units"]["snowfall"]} with a depth of {data["hourly"]["snow_depth"][0]} { data["hourly_units"]["snow_depth"]}.
    \n
    The visibility is to {data["hourly"]["visibility"][0]} {data["hourly_units"]["visibility"]}. The Humidity is near {data["hourly"]["relativehumidity_2m"][0]} {data["hourly_units"]["relativehumidity_2m"]}. \n
    The wind on average is at {data["hourly"]["windspeed_10m"][0]} {data["hourly_units"]["windspeed_10m"]} going a direction of {data["daily"]["winddirection_10m_dominant"][0]} { data["daily_units"]["winddirection_10m_dominant"]}.\n

    Throughout the day  : The maximum temperature is up to {data["daily"]["temperature_2m_max"][0]} {data["daily_units"]["temperature_2m_max"]} and minimum temperature 
    is down to {data["daily"]["temperature_2m_min"][0]} {data["daily_units"]["temperature_2m_min"]}. \n

    Today's sunrise was at {sunrises[1]} {data["timezone_abbreviation"]} and the sunset is at {sunsets[1]} {data["timezone_abbreviation"]}. \n
    
    Overall, It can be described by : \n 
    {get_weather_description(chosen_key=str(data["hourly"]["weathercode"][0]))}.

    Thank you for using our servive ! \n
    Have a safe day.\n
    {emoji.emojize(":grinning_face_with_big_eyes:")}

    
    """

    print(message_to_send)

    send_sms(message=message_to_send, phone_number=phone_number)
