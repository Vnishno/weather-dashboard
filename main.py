# Weather Dashboard - მთავარი ფაილი, მენიუ
import asyncio
import time

import requests

from api_client import get_city, get_weather, get_all_weather
from storage import CityStorage, HistoryStorage

city_storage = CityStorage("data/cities.json")
history_storage = HistoryStorage("data/history.json")

def check_weather(history):
    city_name = input("ქალაქის სახელი: ")

    try:
        city = get_city(city_name)
        record = get_weather(city)
        print()
        print(record)
        history.append(record)
        history_storage.save(history)

    except KeyError:
        print(f"ქალაქი '{city_name}' ვერ მოიძებნა")
    except requests.exceptions.ConnectionError:
        print("ინტერნეტთან კავშირი ვერ მოხერხდა")
    except requests.exceptions.Timeout:
        print("სერვერმა დიდხანს არ უპასუხა")
    except requests.exceptions.HTTPError as e:
        print(f"სერვერმა შეცდომა დააბრუნა: {e}")



def weather_for_my_cities(cities, history):
    if not cities:
        print("სია ცარიელია. ჯერ ქალაქი დაამატე (პუნქტი 3).")
        return

    start = time.time()

    results = asyncio.run(get_all_weather(cities))

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            print(f"\n{city} - ამინდი ვერ მივიღე")
        else:
            print()
            print(result)
            history.append(result)

    history_storage.save(history)
    print(f"\n(დრო: {time.time() - start:.2f} წამი)")


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
    city_storage.save(cities)
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
    city_storage.save(cities)
    print(f"{removed} წაიშალა სიიდან") 



def show_history(history):
    if not history:
        print("ისტორია ჯერ ცარიელია")
        return

    search = input("ქალაქის სახელი (ყველასთვის დააჭირე Enter): ").strip().lower()

    found = []
    for record in history:
        if search in record.city_name.lower():
            found.append(record)

    if not found:
        print("ამ ქალაქზე ჩანაწერი ვერ მოიძებნა")
        return

    print(f"\nნაპოვნია {len(found)} ჩანაწერი (ვაჩვენებ ბოლო 20-ს):")
    for record in found[-20:]:
        print(record.short_info())

def show_menu():
    print("\n----- Weather Dashboard -----")
    print("1. ქალაქის ამინდის ნახვა")
    print("2. ჩემი ქალაქების ამინდი (ყველა ერთად)")
    print("3. ქალაქის დამატება სიაში")
    print("4. ქალაქის წაშლა სიიდან")
    print("5. ჩემი ქალაქების სია")
    print("6. ამინდის ისტორია")
    print("0. გასვლა")


def main():
    cities = city_storage.load()
    history = history_storage.load()
    while True:
        show_menu()
        choice = input("აირჩიე: ").strip()

        if choice == "1":
            check_weather(history)
        elif choice == "2":
            weather_for_my_cities(cities, history)
        elif choice == "3":
            add_city(cities)
        elif choice == "4":
            remove_city(cities)
        elif choice == "5":
            show_cities(cities)
        elif choice == "6":
            show_history(history)
        elif choice == "0":
            print("თქვენ გახვედით მენიუდან!")
            break
        else:
            print("ასეთი პუნქტი არ არსებობს, სცადე თავიდან")


if __name__ == "__main__":
    main()