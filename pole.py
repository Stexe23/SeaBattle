# Создаём классы
class Dot:  # Класс точек на поле
    def __init__(self, ix, iy, d):
        self.ix = ix
        self.iy = iy
        self.d = d


class Board:  # Класс поля
    def __init__(self, pole, ship_, hid, ship_live):
        self.pole = pole
        self.ship_ = ship_
        self.hid = bool(hid)
        self.ship_live = ship_live

    def get_add_ship(self):
        pass

    def get_contour(self):
        pass


class Ship:  # Родительский класс кораблей
    def __init__(self, dlina, n_dot, position, live):
        self.dlina = dlina
        self.n_dot = n_dot
        self.position = position
        self.live = live

    def get_dots(self):
        return self.dlina

    def get_dots(self):
        pass




class Linkor(Ship):  # Класс корабля на четыре клетки поля
    pass


class Kreiser(Ship): # Класс корабля на две клетки поля
    pass


class Esminec(Ship): # Клас корабля на одну клетку поля
    pass
