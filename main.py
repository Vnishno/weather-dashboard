# Weather Dashboard - მთავარი ფაილი
# მენიუ და მომხმარებელთან ურთიერთობა (input / print)
import asyncio

import requests

from api_client import get_city, get_weather, get_all_weather
from storage import CityStorage, HistoryStorage
from city_manager import CityManager
from decorators import timer

# ორი ცალკე ფაილი - ერთი ქალაქების სიისთვის, მეორე ამინდის ისტორიისთვის
city_storage = CityStorage("data/cities.json")
history_storage = HistoryStorage("data/history.json")

# მენიუს 1-ლი პუნქტი - ერთი ქალაქის ამინდი
def check_weather(history):
    city_name = input("ქალაქის სახელი: ")

    try:
        city = get_city(city_name)
        record = get_weather(city)
        print()
        # print(record) - ავტომატურად იძახებს WeatherRecord-ის __str__ მეთოდს
        print(record)
        # ახალი ჩანაწერი ემატება ისტორიას და მაშინვე ინახება ფაილში
        history.append(record)
        history_storage.save(history)

    # KeyError - ქალაქი ვერ მოიძებნა (API-ს პასუხში "results" არ არის)
    except KeyError:
        print(f"ქალაქი '{city_name}' ვერ მოიძებნა")
    # ConnectionError - ინტერნეტი არ არის (retry 3-ჯერ ცდის და მერე მოდის აქ)
    except requests.exceptions.ConnectionError:
        print("ინტერნეტთან კავშირი ვერ მოხერხდა")
    # Timeout - სერვერი 10 წამში არ პასუხობს
    except requests.exceptions.Timeout:
        print("სერვერმა დიდხანს არ უპასუხა")
    # HTTPError - სერვერმა შეცდომის სტატუსი დააბრუნა (raise_for_status აგდებს)
    except requests.exceptions.HTTPError as e:
        print(f"სერვერმა შეცდომა დააბრუნა: {e}")


# მენიუს მე-2 პუნქტი - ყველა შენახული ქალაქის ამინდი ერთდროულად
# @timer - ზომავს რამდენი დრო დასჭირდა (async-ის სისწრაფის საჩვენებლად)
@timer
def weather_for_my_cities(cities, history):
    if not cities:
        print("სია ცარიელია. ჯერ ქალაქი დაამატე (პუნქტი 3).")
        return

    # asyncio.run - ჩვეულებრივი ფუნქციიდან async ფუნქციის გაშვება
    results = asyncio.run(get_all_weather(cities))

    # zip - ქალაქები და შედეგები წყვილ-წყვილად (gather შედეგებს იმავე რიგით აბრუნებს)
    for city, result in zip(cities, results):
        # isinstance - თუ შედეგი შეცდომის ობიექტია, ამ ქალაქის ამინდი ვერ მივიღეთ
        if isinstance(result, Exception):
            print(f"\n{city} - ამინდი ვერ მივიღე")
        else:
            print()
            print(result)
            history.append(result)

    # ფაილში ინახება ერთხელ, ციკლის შემდეგ და არა ყოველ ქალაქზე
    history_storage.save(history)


# მენიუს მე-3 პუნქტი - ქალაქის დამატება სიაში
def add_city(manager):
    city_name = input("რომელი ქალაქი დავამატო? ")

    try:
        city = get_city(city_name)
    except KeyError:
        print(f"ქალაქი '{city_name}' ვერ მოიძებნა")
        return
    # RequestException - ConnectionError, Timeout და HTTPError-ის მშობელი, ერთად იჭერს სამივეს
    except requests.exceptions.RequestException:
        print("API-სთან დაკავშირება ვერ მოხერხდა")
        return

    # add_city აბრუნებს True-ს თუ დაემატა, False-ს თუ ეს ქალაქი უკვე სიაშია
    if manager.add_city(city):
        print(f"{city} დაემატა სიაში")
    else:
        print(f"{city.name} უკვე სიაშია")


# მენიუს მე-5 პუნქტი - ქალაქების სია ნომრებით
def show_cities(cities):
    if not cities:
        print("სია ცარიელია")
        return

    # enumerate - სიის ელემენტები ნომრებთან ერთად, start=1 რომ ნუმერაცია 1-დან დაიწყოს
    for number, city in enumerate(cities, start=1):
        print(f"{number}. {city}")


# მენიუს მე-4 პუნქტი - ქალაქის წაშლა ნომრით
def remove_city(manager):
    show_cities(manager.cities)
    if not manager.cities:
        return

    # ValueError - თუ რიცხვის ნაცვლად ტექსტი ჩაიწერა
    try:
        number = int(input("რომელი ნომერი წავშალო? "))
    except ValueError:
        print("ნომერი უნდა იყოს მთელი რიცხვი")
        return

    # remove_city აბრუნებს None-ს თუ ასეთი ნომერი არ არსებობს
    removed = manager.remove_city(number)
    if removed is None:
        print(f"ასეთი ნომერი სიაში არ არის (1-{len(manager.cities)})")
    else:
        print(f"{removed} წაიშალა სიიდან")



# მენიუს მე-6 პუნქტი - ისტორიის ნახვა, ქალაქის მიხედვით ძებნით
def show_history(history):
    if not history:
        print("ისტორია ჯერ ცარიელია")
        return

    # lower() - რომ დიდი და პატარა ასოები ერთნაირად მოიძებნოს
    search = input("ქალაქის სახელი (ყველასთვის დააჭირე Enter): ").strip().lower()

    # ცარიელი ტექსტი ("") ყველა სახელში "შედის", ამიტომ Enter-ზე ყველა ჩანაწერი მოიძებნება
    found = []
    for record in history:
        if search in record.city_name.lower():
            found.append(record)

    if not found:
        print("ამ ქალაქზე ჩანაწერი ვერ მოიძებნა")
        return

    # found[-20:] - მხოლოდ ბოლო 20 ჩანაწერი, რომ ეკრანი არ გადაივსოს
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
    # პროგრამის გაშვებისას ქალაქები და ისტორია იტვირთება ფაილებიდან
    manager = CityManager(city_storage)
    history = history_storage.load()
    # while True - მენიუ მეორდება სანამ მომხმარებელი 0-ს არ აირჩევს
    while True:
        show_menu()
        # strip() - შემთხვევით დაწერილი ჰარები იშლება
        choice = input("აირჩიე: ").strip()

        if choice == "1":
            check_weather(history)
        elif choice == "2":
            weather_for_my_cities(manager.cities, history)
        elif choice == "3":
            add_city(manager)
        elif choice == "4":
            remove_city(manager)
        elif choice == "5":
            show_cities(manager.cities)
        elif choice == "6":
            show_history(history)
        elif choice == "0":
            print("თქვენ გახვედით მენიუდან!")
            # break - while True ციკლიდან გამოსვლა
            break
        else:
            print("ასეთი პუნქტი არ არსებობს, სცადე თავიდან")


# main() ეშვება მხოლოდ მაშინ, როცა ეს ფაილი პირდაპირ ეშვება (python main.py),
# import-ის დროს კი არა
if __name__ == "__main__":
    main()
