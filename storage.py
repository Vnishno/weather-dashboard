# მონაცემების შენახვა და წაკითხვა JSON ფაილებიდან
import json
import os

from models import City, WeatherRecord


# JsonStorage - მშობელი კლასი, უბრალოდ წერს და კითხულობს JSON ფაილს
# ობიექტების შესახებ არაფერი იცის, მხოლოდ სიებთან და ლექსიკონებთან მუშაობს
class JsonStorage:

    # ფაილის მისამართი გარედან გადაეცემა, რომ ერთი კლასი ნებისმიერ ფაილთან იმუშაოს
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        # პირველ გაშვებაზე ფაილი ჯერ არ არსებობს - ცარიელი სია ბრუნდება
        if not os.path.exists(self.file_path):
            return []

        # with - ფაილი ავტომატურად იხურება, "r" - წაკითხვა
        # encoding="utf-8" - ქართული ასოები სწორად რომ წაიკითხოს
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        # JSONDecodeError - ფაილი დაზიანებულია (არასწორი JSON), პროგრამა არ ჩერდება
        except json.JSONDecodeError:
            print(f"ფაილი {self.file_path} დაზიანებულია, ვიწყებთ ცარიელი სიით")
            return []

    def save(self, data):
        # data ფოლდერი თუ არ არსებობს, იქმნება. exist_ok=True - თუ არსებობს, შეცდომა არ ამოვარდეს
        folder = os.path.dirname(self.file_path)
        os.makedirs(folder, exist_ok=True)

        # "w" - ჩაწერა (ძველი შიგთავსი იშლება და სრული სია თავიდან იწერება)
        # ensure_ascii=False - ქართული ქართულად ჩაიწეროს და არა თ კოდებად
        # indent=4 - ფაილი ლამაზად, შეწევით ჩაიწეროს
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        # OSError - ფაილში ჩაწერის პრობლემა (წვდომა არ არის, დისკი სავსეა და ა.შ.)
        except OSError as e:
            print(f"ფაილში შენახვა ვერ მოხერხდა: {e}")


# CityStorage - JsonStorage-ის შვილი კლასი (მემკვიდრეობა)
# load და save თავიდანაა დაწერილი: ფაილთან მუშაობას super()-ით მშობელს ანდობს,
# თავად კი ლექსიკონებს City ობიექტებად აქცევს და პირიქით
class CityStorage(JsonStorage):

    def load(self):
        cities = []
        # super().load() - მშობლის load, რომელიც ფაილიდან ლექსიკონების სიას აბრუნებს
        for item in super().load():
            # KeyError - თუ ჩანაწერს რომელიმე ველი აკლია, მხოლოდ ის გამოიტოვება, დანარჩენი ჩაიტვირთება
            try:
                cities.append(City.from_dict(item))
            except KeyError:
                print("ერთი ქალაქის ჩანაწერი დაზიანებულია და გამოვტოვე")
        return cities

    def save(self, cities):
        # ჯერ ყველა City ობიექტი ლექსიკონად, მერე ფაილში ჩაწერა მშობლის save-ით
        data = []
        for city in cities:
            data.append(city.to_dict())
        super().save(data)


# HistoryStorage - იგივე პრინციპი, ოღონდ WeatherRecord ობიექტებისთვის
class HistoryStorage(JsonStorage):

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
