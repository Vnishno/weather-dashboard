# ქალაქების სიის მართვა (encapsulation)


class CityManager:
    def __init__(self, storage):
        # __ ნიშნავს private-ს - კლასის გარედან პირდაპირ ვერ მიწვდებიან
        self.__storage = storage
        self.__cities = storage.load()

    @property
    def cities(self):
        # სიის ასლს ვაბრუნებთ, რომ გარედან append-ით ვერ შეცვალონ
        return self.__cities.copy()

    def add_city(self, city):
        for saved_city in self.__cities:
            if saved_city.name == city.name:
                return False

        self.__cities.append(city)
        self.__storage.save(self.__cities)
        return True

    def remove_city(self, number):
        if number < 1 or number > len(self.__cities):
            return None

        removed = self.__cities.pop(number - 1)
        self.__storage.save(self.__cities)
        return removed