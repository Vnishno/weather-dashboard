# Open-Meteo API-ს გამოყენება
import asyncio

import aiohttp
import requests

from models import City, WeatherRecord


GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_city(city_name):
    params = {"name": city_name, "count": 1, "language": "ka"}
    response = requests.get(GEO_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    return City(result["name"], result["country"], result["latitude"], result["longitude"])


def weather_params(city):
    return {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }


def make_record(city, current):
    return WeatherRecord(
        city.name,
        city.country,
        current["temperature_2m"],
        current["wind_speed_10m"],
        current["weather_code"],
        current["time"],
    )


def get_weather(city):
    response = requests.get(WEATHER_URL, params=weather_params(city), timeout=10)
    response.raise_for_status()
    data = response.json()
    return make_record(city, data["current"])



async def get_weather_async(session, city):
    async with session.get(WEATHER_URL, params=weather_params(city)) as response:
        response.raise_for_status()
        data = await response.json()
        return make_record(city, data["current"])


async def get_all_weather(cities):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for city in cities:
            tasks.append(get_weather_async(session, city))
        return await asyncio.gather(*tasks, return_exceptions=True)