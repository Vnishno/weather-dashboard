import requests

city_name = input("ქალაქის სახელი: ")

try:
    # 1) ქალაქის სახელით კოორდინატებს ვიღებთ
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {"name": city_name, "count": 1, "language": "ka"}

    geo_response = requests.get(geo_url, params=geo_params, timeout=10)
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    city = geo_data["results"][0]

    # 2) კოორდინატებით ამინდს ვიღებთ
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }

    weather_response = requests.get(weather_url, params=weather_params, timeout=10)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    current = weather_data["current"]

    print()
    print(f"{city['name']}, {city['country']}")
    print(f"ტემპერატურა: {current['temperature_2m']}°C")
    print(f"ქარი: {current['wind_speed_10m']} კმ/სთ")
    print(f"ამინდის კოდი: {current['weather_code']}")
    print(f"განახლდა: {current['time']}")

except KeyError:
    print(f"ქალაქი '{city_name}' ვერ მოიძებნა")
except requests.exceptions.ConnectionError:
    print("ინტერნეტთან კავშირი ვერ მოხერხდა")
except requests.exceptions.Timeout:
    print("სერვერმა დიდხანს არ უპასუხა")
except requests.exceptions.HTTPError as e:
    print(f"სერვერმა შეცდომა დააბრუნა: {e}")