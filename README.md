# Weather Dashboard

კონსოლური აპლიკაცია, რომელიც ქალაქების ამინდს Open-Meteo API-დან იღებს.

## შესაძლებლობები
- ქალაქის ამინდის ნახვა (ტემპერატურა, ქარი, ამინდის აღწერა)
- ჩემი ქალაქების ამინდი ერთდროულად (async, aiohttp)
- ქალაქების სიის მართვა - დამატება, წაშლა, ნახვა
- ამინდის ისტორია და ძებნა ქალაქის მიხედვით
- მონაცემები ინახება JSON ფაილებში

## ფაილები
- `main.py` - მენიუ
- `api_client.py` - API-სთან მუშაობა
- `models.py` - City და WeatherRecord კლასები
- `storage.py` - JSON ფაილებში შენახვა (JsonStorage → CityStorage, HistoryStorage)
- `city_manager.py` - ქალაქების სიის მართვა
- `decorators.py` - timer და retry დეკორატორები

## გაშვება
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```