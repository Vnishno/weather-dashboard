# მოდელები - ქალაქის და ამინდის ჩანაწერის კლასები
from datetime import datetime

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
    def __init__(self, city_name, country, temperature, wind_speed, weather_code, time, saved_at=None):
        self.city_name = city_name
        self.country = country
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.weather_code = weather_code
        self.time = time
        # თუ ფაილიდან ვტვირთავთ, saved_at უკვე გვაქვს, თუ არა - ახლანდელ დროს ვწერთ
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

    def short_info(self):
        # ისტორიაში ერთ ხაზად გამოსაჩენად
        return f"{self.saved_at} | {self.city_name:<12} | {self.temperature:>5}°C | {self.description}"
    
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
