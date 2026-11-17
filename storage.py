# ქალაქების შენახვა და წაკითხვა JSON ფაილიდან
import json
import os

from models import City

CITIES_FILE = "data/cities.json"


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
