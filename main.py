import requests


GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_city(city_name):
    params = {"name": city_name, "count": 1, "language": "ka"}
    response = requests.get(GEO_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["results"][0]


def get_weather(city):
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }
    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["current"]


def show_weather(city, current):
    print()
    print(f"{city['name']}, {city['country']}")
    print(f"ტემპერატურა: {current['temperature_2m']}°C")
    print(f"ქარი: {current['wind_speed_10m']} კმ/სთ")
    print(f"ამინდის კოდი: {current['weather_code']}")
    print(f"განახლდა: {current['time']}")


def check_weather():
    city_name = input("ქალაქის სახელი: ")

    try:
        city = get_city(city_name)
        current = get_weather(city)
        show_weather(city, current)

    except KeyError:
        print(f"ქალაქი '{city_name}' ვერ მოიძებნა")
    except requests.exceptions.ConnectionError:
        print("ინტერნეტთან კავშირი ვერ მოხერხდა")
    except requests.exceptions.Timeout:
        print("სერვერმა დიდხანს არ უპასუხა")
    except requests.exceptions.HTTPError as e:
        print(f"სერვერმა შეცდომა დააბრუნა: {e}")

        

def show_menu():
    print("\n----- Weather Dashboard -----")
    print("1. ქალაქის ამინდის ნახვა")
    print("0. გასვლა")


def main():
    while True:
        show_menu()
        choice = input("აირჩიე: ").strip()

        if choice == "1":
            check_weather()
        elif choice == "0":
            print("ნახვამდის!")
            break
        else:
            print("ასეთი პუნქტი არ არსებობს, სცადე თავიდან")


if __name__ == "__main__":
    main()