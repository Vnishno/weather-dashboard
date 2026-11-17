# ქალაქების სიის მართვა (encapsulation)
# სია კლასის შიგნით არის დამალული და მისი შეცვლა მხოლოდ add_city და remove_city მეთოდებით შეიძლება,
# რომლებიც ყველაფერს ამოწმებენ და ცვლილებას ავტომატურად ინახავენ ფაილში


class CityManager:
    def __init__(self, storage):
        # __ - private ატრიბუტი, კლასის გარედან პირდაპირ წვდომა არ შეიძლება
        self.__storage = storage
        self.__cities = storage.load()

    # @property - სიის წაკითხვა გარედან შეიძლება (manager.cities),
    # მაგრამ ბრუნდება ასლი (copy), რომ გარედან append-ით ნამდვილი სია ვერ შეიცვალოს
    @property
    def cities(self):
        return self.__cities.copy()

    def add_city(self, city):
        # ერთი და იგივე ქალაქი ორჯერ ვერ დაემატება
        for saved_city in self.__cities:
            if saved_city.name == city.name:
                return False

        self.__cities.append(city)
        self.__storage.save(self.__cities)
        return True

    def remove_city(self, number):
        # ნომრის შემოწმება - 0 რომ ჩაიწეროს, pop(-1) ბოლო ქალაქს წაშლიდა
        if number < 1 or number > len(self.__cities):
            return None

        # number - 1, რადგან მომხმარებელი 1-დან ითვლის, Python კი 0-დან
        removed = self.__cities.pop(number - 1)
        self.__storage.save(self.__cities)
        return removed
