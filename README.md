# Get a city's weather information using a weather forcast API and a forward geocoding API

## Project description

This project gives us a city's temperature and rain rate at the same day by only giving the city's name and corresponding coutry. 


The project uses two functions.



The main function (cityweather) gives the weather information of a city, the date of the day, the hour, the temperature and the rain rate. It only needs the city's name and country. 

It's able to do so by using the other function (cityapi) that takes the city name and country and returns the latitude and langitude of the city. This information is then used by the main function to apoint the city.


- "cityweather" gives the city's eather information by using [Open-Meteo](https://open-meteo.com/en/docs#latitude=34.96&longitude=-5.44&hourly=pressure_msl,visibility), a weather API. This API let's you select a city but instead of using the name of the city, it uses the city's latitude and longitude.

- "cityapi" gives the city's latitude and longitude by giving it the city's name and country by using [API Ninjas](https://api-ninjas.com/api/geocoding), a geocoding API that enables you to convert any city from any country to latitude and longitude coordinates.


