import requests


def getLatLong(city:str, country:str):
    '''
    This function returns latitude and longitude 
    input : city : str , country : str
    output : list
    '''
    response = requests.get(
        url=f"https://api.api-ninjas.com/v1/geocoding?city={city}&country={country}",
        headers={"X-Api-Key": "Put your NinjasAPI key here"},
    )

    data_city = response.json()

    latitude = data_city[0]["latitude"]
    longitude = data_city[0]["longitude"]
    return [latitude, longitude]
