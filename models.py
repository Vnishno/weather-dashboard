# მოდელები - ქალაქის და ამინდის ჩანაწერის კლასები
from datetime import datetime

# Open-Meteo ამინდს ტექსტით არ აბრუნებს, მხოლოდ რიცხვითი კოდით (WMO სტანდარტი)
# ეს ლექსიკონი კოდს ქართულ ტექსტად თარგმნის (კოდები Open-Meteo-ს დოკუმენტაციიდანაა)
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



# City - ქალაქის სახელი, ქვეყანა და კოორდინატები
class City:
    # __init__ - ობიექტის შექმნისას ავტომატურად ეშვება და ველებს ავსებს
    def __init__(self, name, country, latitude, longitude):
        self.name = name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    # to_dict - ობიექტი ლექსიკონად, რადგან JSON-ში ობიექტის პირდაპირ ჩაწერა შეუძლებელია
    def to_dict(self):
        return {
            "name": self.name,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    # from_dict - პირიქით, ფაილიდან წაკითხული ლექსიკონიდან City ობიექტის შექმნა
    # @classmethod - ობიექტი ჯერ არ არსებობს, ამიტომ კლასზე იძახება: City.from_dict(...), cls = City
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["country"], data["latitude"], data["longitude"])
    # __str__ - როგორ გამოჩნდეს ობიექტი print()-ის დროს
    def __str__(self):
        return f"{self.name}, {self.country}"


# WeatherRecord - ერთი ამინდის ჩანაწერი (ეკრანზე საჩვენებლად და ისტორიაში შესანახად)
class WeatherRecord:
    def __init__(self, city_name, country, temperature, wind_speed, weather_code, time, saved_at=None):
        self.city_name = city_name
        self.country = country
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.weather_code = weather_code
        # time - API-დან მოსული დრო, როდის განახლდა ეს მონაცემი (დაახლოებით ყოველ 15 წუთში)
        self.time = time
        # saved_at - როდის შემოწმდა ამინდი. ახალ ჩანაწერზე ახლანდელი დრო იწერება,
        # ფაილიდან ჩატვირთვისას კი ძველი დრო რჩება (or - თუ saved_at None-ია, აიღებს მარჯვენა მხარეს)
        self.saved_at = saved_at or datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "city_name": self.city_name,
            "country": self.country,
            "temperature": self.temperature,
            "wind_speed": self.wind_speed,
            "weather_code": self.weather_code,
            "time": self.time,
            "saved_at": self.saved_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["city_name"],
            data["country"],
            data["temperature"],
            data["wind_speed"],
            data["weather_code"],
            data["time"],
            data["saved_at"],
        )

    # short_info - ისტორიაში ერთ ხაზად გამოსაჩენად
    # :<12 და :>5 - სვეტების გასწორება, რომ ცხრილივით ლამაზად გამოჩნდეს
    def short_info(self):
        return f"{self.saved_at} | {self.city_name:<12} | {self.temperature:>5}°C | {self.description}"
    
    # @property - მეთოდი, რომელიც ფრჩხილების გარეშე იკითხება (record.description)
    # .get() - თუ კოდი ლექსიკონში არ არის, KeyError-ის ნაცვლად "უცნობი ამინდი" დაბრუნდება
    @property
    def description(self):
        return WEATHER_CODES.get(self.weather_code, "უცნობი ამინდი")

    # \n - ახალ ხაზზე გადასვლა, replace('T', ' ') - "2026-11-17T16:00" ხდება "2026-11-17 16:00"
    def __str__(self):
        return (
            f"{self.city_name}, {self.country}\n"
            f"   ტემპერატურა: {self.temperature}°C\n"
            f"   ქარი: {self.wind_speed} კმ/სთ\n"
            f"   ამინდი: {self.description}\n"
            f"   განახლდა: {self.time.replace('T', ' ')}"
        )
