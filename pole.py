from random import randint

# Создаём классы
# Классы исключений
class BoardException(Exception): # Основной клас исключения
    pass

class BoardOutException(BoardException): # Исключение выхода за поле
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException): # Исключение повторного выстрела
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException): # Исключение ошибки корабля на поле
    pass

# Основные классы
class Dot:  # Класс точек на поле
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.d = d

    def __eq__(self, other): # Метод для сравнения координат
        return self.x == other.x and self.y == other.y

    def __repr__(self): # Метод вывода координат поля
        return f"Dot({self.x}, {self.y})"


class Board:  # Класс поля
    def __init__(self, pole = 6, hid = False):
        self.pole = pole
        self.ships = [] # Хранение кораблей
        self.busy = [] # Хранение занятых точек
        self.hid = hid
        self.fild = [["0"] * pole for _ in range(pole)]

    def __str__(self): # Метод формирования поля
        raz = ""
        raz += "\t| 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, j in enumerate(self.fild):
            raz += f"\n  {i + 1} | " + " | " .join(j) + " |"
        if self.hid:
            raz = raz.replace("■", "0")
        return raz

    def out(self, d): # Метод проверки точки за пределами доски
        return not((0 <= d.x <= self.pole) and (0 <= d.y <= self.pole))

    def add_ship(self, ship): # Метод добавления корабля на поле
        for d in ship.dots:
            if self.out(d) or d in self.busy: # Точка кораюля не выходит за границы и не  занята
                raise BoardWrongShipException()
        for d in ship.dots: # Замена точки корабля на символ
            self.fild[d.x][d.y] = "■"

    def contour(self, ship_cont, tor =False): # Метод обвода контура корабля
        cont = [(-1, -1), (-1, 0), (-1, 1), # Координаты контура
                ( 0, -1), ( 0, 0), ( 0, 1),
                ( 1, -1), ( 1, 0), ( 1, 1)]

        for d in ship_cont.dots: # Определяем точки коробля
            for dx, dy in cont: # Провереем координаты вонтура для точки коробля
                cor = Dot(d.x + dx, d.y + dy) # Смещаем коордитаты точки коробля
                if not(self.out(cor) and cor not in self.busy): # Точка не выходит за грацъницы и не занята
                    if tor:
                        self.fild[cor.x][cor.y] = "."
                    self.busy.append(cor)

                self.ships.append(ship_cont)
                self.contour(ship_cont)



class Ship:  # Родительский класс кораблей
    def __init__(self, n_dot, dlina, position):
        self.dlina = dlina
        self.n_dot = n_dot
        self.position = position
        self.live = dlina

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.n_dot):
            cor_x = self.dlina.x
            cor_y = self.dlina.y
            if self.position == 0:
                cor_x += i
            if self.position == 1:
                cor_y += i
            ship_dots.append(Dot(cor_x, cor_y))

        return ship_dots





class Linkor(Ship):  # Класс корабля на четыре клетки поля
    pass


class Kreiser(Ship): # Класс корабля на две клетки поля
    pass


class Esminec(Ship): # Клас корабля на одну клетку поля
    pass


b = Board()
print(b)