# მონაცემების შენახვა და წაკითხვა JSON ფაილებიდან
import json
import os

from models import City, WeatherRecord


class JsonStorage:
    # მშობელი კლასი - უბრალოდ წერს და კითხულობს JSON ფაილს

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"ფაილი {self.file_path} დაზიანებულია, ვიწყებთ ცარიელი სიით")
            return []

    def save(self, data):
        folder = os.path.dirname(self.file_path)
        os.makedirs(folder, exist_ok=True)

        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"ფაილში შენახვა ვერ მოხერხდა: {e}")


class CityStorage(JsonStorage):
    # შვილი კლასი - ლექსიკონებს City ობიექტებად აქცევს და პირიქით

    def load(self):
        cities = []
        for item in super().load():
            try:
                cities.append(City.from_dict(item))
            except KeyError:
                print("ერთი ქალაქის ჩანაწერი დაზიანებულია და გამოვტოვე")
        return cities

    def save(self, cities):
        data = []
        for city in cities:
            data.append(city.to_dict())
        super().save(data)


class HistoryStorage(JsonStorage):
    # იგივე პრინციპი, ოღონდ WeatherRecord ობიექტებისთვის

    def load(self):
        records = []
        for item in super().load():
            try:
                records.append(WeatherRecord.from_dict(item))
            except KeyError:
                print("ისტორიის ერთი ჩანაწერი დაზიანებულია და გამოვტოვე")
        return records

    def save(self, records):
        data = []
        for record in records:
            data.append(record.to_dict())
        super().save(data)