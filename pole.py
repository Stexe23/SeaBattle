# Создаём классы
class Dot:  # Класс точек на поле
    pass


class Board:  # Класс поля
    pass


class Ship:  # Родительский класс кораблей
    def ship(self, dlina, n_dot, position, live):
        self.dlina = dlina
        self.n_dot = n_dot
        self.position = position
        self.live = live

    def get_dots(self):
        return self.dlina


class Linkor(Ship):  # Класс корабля на четыре клетки поля
    pass


class Kreiser(Ship): # Класс корабля на две клетки поля
    pass


class Esminec(Ship): # Клас корабля на одну клетку поля
    pass
