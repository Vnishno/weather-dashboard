import json
import os
import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
CITIES_FILE = "data/cities.json"

WEATHER_CODES = {
    0: "მოწმენდილი ცა",
    1: "ძირითადად მოწმენდილი",
    2: "ნაწილობრივ მოღრუბლული",
    3: "მოღრუბლული",
    45: "ნისლი",
    48: "ნისლი და თრთვილი",
    51: "მსუბუქი ჟინჟღლი",
    53: "ჟინჟღლი",
    55: "ძლიერი ჟინჟღლი",
    56: "ყინვიანი ჟინჟღლი",
    57: "ძლიერი ყინვიანი ჟინჟღლი",
    61: "მსუბუქი წვიმა",
    63: "წვიმა",
    65: "ძლიერი წვიმა",
    66: "ყინვიანი წვიმა",
    67: "ძლიერი ყინვიანი წვიმა",
    71: "მსუბუქი თოვლი",
    73: "თოვლი",
    75: "ძლიერი თოვლი",
    77: "თოვლის მარცვლები",
    80: "მსუბუქი თავსხმა",
    81: "თავსხმა",
    82: "ძლიერი თავსხმა",
    85: "თოვლჭყაპი",
    86: "ძლიერი თოვლჭყაპი",
    95: "ჭექა-ქუხილი",
    96: "ჭექა-ქუხილი სეტყვით",
    99: "ძლიერი ჭექა-ქუხილი სეტყვით",
}



class City:
    def __init__(self, name, country, latitude, longitude):
        self.name = name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "name": self.name,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["country"], data["latitude"], data["longitude"])
    def __str__(self):
        return f"{self.name}, {self.country}"


class WeatherRecord:
    def __init__(self, city_name, country, temperature, wind_speed, weather_code, time):
        self.city_name = city_name
        self.country = country
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.weather_code = weather_code
        self.time = time

    @property
    def description(self):
        return WEATHER_CODES.get(self.weather_code, "უცნობი ამინდი")

    def __str__(self):
        return (
            f"{self.city_name}, {self.country}\n"
            f"   ტემპერატურა: {self.temperature}°C\n"
            f"   ქარი: {self.wind_speed} კმ/სთ\n"
            f"   ამინდი: {self.description}\n"
            f"   განახლდა: {self.time.replace('T', ' ')}"
        )

def get_city(city_name):
    params = {"name": city_name, "count": 1, "language": "ka"}
    response = requests.get(GEO_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    return City(result["name"], result["country"], result["latitude"], result["longitude"])


def get_weather(city):
    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }
    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data["current"]
    return WeatherRecord(
        city.name,
        city.country,
        current["temperature_2m"],
        current["wind_speed_10m"],
        current["weather_code"],
        current["time"],
    )



def load_cities():
    # პირველ გაშვებაზე ფაილი ჯერ არ არსებობს
    if not os.path.exists(CITIES_FILE):
        return []

    try:
        with open(CITIES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("ქალაქების ფაილი დაზიანებულია, ვიწყებთ ცარიელი სიით")
        return []

    cities = []
    for item in data:
        try:
            cities.append(City.from_dict(item))
        except KeyError:
            print("ერთი ქალაქის ჩანაწერი დაზიანებულია და გამოვტოვე")
    return cities


def save_cities(cities):
    data = []
    for city in cities:
        data.append(city.to_dict())

    os.makedirs("data", exist_ok=True)
    try:
        with open(CITIES_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"ფაილში შენახვა ვერ მოხერხდა: {e}")

def check_weather():
    city_name = input("ქალაქის სახელი: ")

    try:
        city = get_city(city_name)
        record = get_weather(city)
        print()
        print(record)

    except KeyError:
        print(f"ქალაქი '{city_name}' ვერ მოიძებნა")
    except requests.exceptions.ConnectionError:
        print("ინტერნეტთან კავშირი ვერ მოხერხდა")
    except requests.exceptions.Timeout:
        print("სერვერმა დიდხანს არ უპასუხა")
    except requests.exceptions.HTTPError as e:
        print(f"სერვერმა შეცდომა დააბრუნა: {e}")




def add_city(cities):
    city_name = input("რომელი ქალაქი დავამატო? ")

    try:
        city = get_city(city_name)
    except KeyError:
        print(f"ქალაქი '{city_name}' ვერ მოიძებნა")
        return
    except requests.exceptions.RequestException:
        print("API-სთან დაკავშირება ვერ მოხერხდა")
        return

    # ერთი ქალაქი ორჯერ რომ არ დაემატოს
    for saved_city in cities:
        if saved_city.name == city.name:
            print(f"{city.name} უკვე სიაშია")
            return

    cities.append(city)
    save_cities(cities)
    print(f"{city} დაემატა სიაში")


def show_cities(cities):
    if not cities:
        print("სია ცარიელია")
        return

    for number, city in enumerate(cities, start=1):
        print(f"{number}. {city}")


def remove_city(cities):
    show_cities(cities)
    if not cities:
        return

    try:
        number = int(input("რომელი ნომერი წავშალო? "))
    except ValueError:
        print("ნომერი უნდა იყოს მთელი რიცხვი")
        return

    if number < 1 or number > len(cities):
        print(f"ასეთი ნომერი სიაში არ არის (1-{len(cities)})")
        return

    removed = cities.pop(number - 1)
    save_cities(cities)
    print(f"{removed} წაიშალა სიიდან") 

def show_menu():
    print("\n----- Weather Dashboard -----")
    print("1. ქალაქის ამინდის ნახვა")
    print("3. ქალაქის დამატება სიაში")
    print("4. ქალაქის წაშლა სიიდან")
    print("5. ჩემი ქალაქების სია")
    print("0. გასვლა")


def main():
    cities = load_cities()
    while True:
        show_menu()
        choice = input("აირჩიე: ").strip()

        if choice == "1":
            check_weather()
        elif choice == "3":
            add_city(cities)
        elif choice == "4":
            remove_city(cities)
        elif choice == "5":
            show_cities(cities)
        elif choice == "0":
            print("ნახვამდის!")
            break
        else:
            print("ასეთი პუნქტი არ არსებობს, სცადე თავიდან")


if __name__ == "__main__":
    main()