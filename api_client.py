# Open-Meteo API-ს გამოყენება
# ქალაქის მოძებნა და ამინდის მიღება
import asyncio

import aiohttp
import requests

from models import City, WeatherRecord
from decorators import retry


# GEO_URL - ქალაქის სახელით კოორდინატების მიღება
# WEATHER_URL - კოორდინატებით ამინდის მიღება
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# retry - თუ ინტერნეტი წამით გაითიშა, პროგრამა პირდაპირ არ ჩავარდეს და 3-ჯერ სცადოს
@retry(times=3, delay=1)
def get_city(city_name):
    # language=ka - ქალაქის და ქვეყნის სახელი ქართულად დაბრუნდეს
    params = {"name": city_name, "count": 1, "language": "ka"}
    # timeout=10 - თუ სერვერი 10 წამში არ პასუხობს, ლოდინი წყდება
    response = requests.get(GEO_URL, params=params, timeout=10)
    # raise_for_status - თუ სტატუსი 200 არ არის (მაგ. 404, 500), ამოვარდება HTTPError
    response.raise_for_status()
    data = response.json()
    # თუ ქალაქი ვერ მოიძებნა, პასუხში "results" არ არის და ამოვარდება KeyError (main.py-ში იჭერს)
    result = data["results"][0]
    # პასუხიდან საჭიროა მხოლოდ 4 ველი, მათით იქმნება City ობიექტი
    return City(result["name"], result["country"], result["latitude"], result["longitude"])


# weather_params და make_record - ცალკე ფუნქციებია, რადგან ორივე ვერსიას (ჩვეულებრივს და async-ს)
# სჭირდება და ასე კოდი არ მეორდება
def weather_params(city):
    return {
        "latitude": city.latitude,
        "longitude": city.longitude,
        # current - ახლანდელი ამინდიდან მხოლოდ ტემპერატურა, ქარი და ამინდის კოდი
        "current": "temperature_2m,wind_speed_10m,weather_code",
        # timezone=auto - დრო ქალაქის ადგილობრივი დროით დაბრუნდეს და არა GMT-ით
        "timezone": "auto",
    }


# API-ს პასუხიდან და ქალაქის ობიექტიდან WeatherRecord ობიექტის აწყობა
def make_record(city, current):
    return WeatherRecord(
        city.name,
        city.country,
        current["temperature_2m"],
        current["wind_speed_10m"],
        current["weather_code"],
        current["time"],
    )

# get_weather - ერთი ქალაქის ამინდი, ჩვეულებრივი requests-ით
@retry(times=3, delay=1)
def get_weather(city):
    response = requests.get(WEATHER_URL, params=weather_params(city), timeout=10)
    response.raise_for_status()
    data = response.json()
    return make_record(city, data["current"])



# async ნაწილი - ყველა ქალაქის ამინდი ერთდროულად.
# requests async-ს ვერ აკეთებს, ამიტომ აქ aiohttp გამოიყენება
async def get_weather_async(session, city):
    # session გარედან მოდის, რომ ყველა მოთხოვნამ ერთი კავშირი გამოიყენოს
    async with session.get(WEATHER_URL, params=weather_params(city)) as response:
        response.raise_for_status()
        # await - პასუხის ლოდინი, ამ დროს სხვა ქალაქების მოთხოვნებიც მუშაობს
        data = await response.json()
        return make_record(city, data["current"])


async def get_all_weather(cities):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # tasks - ყველა ქალაქის "დავალება" გროვდება სიაში, ამ ეტაპზე ჯერ არაფერი იგზავნება
        tasks = []
        for city in cities:
            tasks.append(get_weather_async(session, city))
        # gather - ყველა მოთხოვნა ერთდროულად იგზავნება (6 ქალაქზე ~2 წამის ნაცვლად ~0.7 წამი)
        # return_exceptions=True - თუ ერთი ქალაქი ჩავარდა, დანარჩენები მაინც დაბრუნდება,
        # ჩავარდნილის ადგილას იქნება შეცდომის ობიექტი (main.py-ში isinstance-ით მოწმდება)
        return await asyncio.gather(*tasks, return_exceptions=True)
