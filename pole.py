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
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other): # Метод для сравнения координат
        return self.x == other.x and self.y == other.y

    def __repr__(self): # Метод вывода координат поля
        return f"Dot({self.x}, {self.y})"


class Ship:  # Родительский класс кораблей
    def __init__(self, n_dot, l, position):
        self.n_dot = n_dot  # Начальная точка коробля
        self.l = l # Длина коробля
        self.position = position # Положение коробля вертикаль/горизонталь
        self.live = l # Жизнь коробля

    @property
    def dots(self): # Метот возврата точек корабля (свойство)
        ship_dots = []
        for i in range(self.l):
            cor_x = self.n_dot.x
            cor_y = self.n_dot.y
            if self.position == 0:
                cor_x += i
            elif self.position == 1:
                cor_y += i
            ship_dots.append(Dot(cor_x, cor_y))

        return ship_dots

    def shooten(self, shot):
        return  shot in self.dots

    def zam(self):
        raise NotImplementedError()


class Board:  # Класс поля
    def __init__(self, hid = False, pole = 6):
        self.pole = pole
        self.ships = [] # Хранение кораблей
        self.busy = [] # Хранение занятых точек
        self.hid = hid
        self.fild = [["0"] * pole for _ in range(pole)]
        self.count = 0

    def __str__(self): # Метод формирования поля
        raz = ""
        raz += "      1 | 2 | 3 | 4 | 5 | 6 |"
        for i, j in enumerate(self.fild):
            raz += f"\n  {i + 1} | " + " | " .join(j) + " |"
        if self.hid:
            raz = raz.replace("■", "0")
        return raz

    def out(self, d): # Метод проверки точки за пределами доски
        return not((0 <= d.x < self.pole) and (0 <= d.y < self.pole))

    def add_ship(self, ship): # Метод добавления корабля на поле
        for d in ship.dots:
            if self.out(d) or d in self.busy: # Точка корабля не выходит за границы и не  занята
                raise BoardWrongShipException()
        for d in ship.dots: # Замена точки корабля на символ
            self.fild[d.x][d.y] = "■"

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, tor = False): # Метод обвода контура корабля
        cont = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0 , 1),
                (1, -1), (1, 0), (1, 1)
                ]

        for d in ship.dots: # Определяем точки коробля
            for dx, dy in cont: # Провереем координаты вонтура для точки коробля
                cor = Dot(d.x + dx, d.y + dy) # Смещаем коордитаты точки коробля
                if not(self.out(cor)) and cor not in self.busy: # Точка не выходит за грацъницы поля и не занята
                    if tor:
                        self.fild[cor.x][cor.y] = "."
                    self.busy.append(cor)

    def shot(self, d):
        if self.out(d): # Выстрел не выходит за пределы поля
            raise BoardOutException()

        if d in self.busy: # Проверки клетки на повтор
            raise  BoardUsedException()

        self.busy.append(d)

        for ship in self.ships: # Проверка из списка кораблей
            if d in ship.dots:
                ship.live -= 1
                self.fild[d.x][d.y] = "x"
                if ship.live == 0:
                    self.count += 1
                    self.contour(ship, tor = True)
                    print('Корабль утонул!')
                    return False
                else:
                    print('Корабль ранен')
                    return True

        self.fild[d.x][d.y] = 'T' # Описание промаха
        print("Мимо!")
        return False

    def begin(self): # Очистка точек поля
        self.busy = []


class Player: # Основной класс игрока
    def __init__(self, board, enemy):
        self.board = board # Доска игрока
        self.enemy = enemy # Сторона игры

    def ask(self): # Метод который "спрашивает" игрока, в какую клетку он делает выстрел
       raise NotImplementedError() # Определяется у потомков класса

    def move(self): # Метод который делает ход в игре
       while True:
           try:
               target = self.ask() # Выбираем цель
               repeat = self.enemy.shot(target) # Производим выстрел
               return repeat
           except BoardException as e:
               print(e)

class User(Player): # Класс пользователя
    def ask(self):

        while True:
            coord = input("Ваш ход: ").split()
            if len(coord) != 2:
                print("Введите две координаты")
                continue

            x, y = coord

            if not(x.isdigit()) or not(y.isdigit()):
                print("Введите числа")
                continue
            x, y = int(x), int(y)

            return  (Dot(x-1, y-1))

class AI(Player): # Класс компьютера
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return  d


class Game: # Класс игры
    def gen_board(self):
        klass_ship = [3, 2, 2, 1, 1, 1, 1]
        board = Board(pole = self.pole)
        shag = 0
        for l in klass_ship:
            while True:
                shag += 1
                if shag > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.pole), randint(0, self.pole)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.gen_board()
        return board

    def __init__(self, pole=6):
        self.pole = pole
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")


    @staticmethod
    def vstack(s1, s2): # Метод вывода полей рядом
        s1 = s1.split("\n")
        s2 = s2.split("\n")
        maxlen = max(map(len, s1))
        result = ""
        for line1, line2 in zip(s1, s2):
            result += f"{line1:{maxlen}}\t\t{line2}\n"
        return result

    def loop(self): #Цикл выполнения игры
        num = 0
        while True:
            user_output = "\t\tДоска пользователя:\n\n" + str(self.us.board)
            ai_output = "\tДоска пользователя:\n\n" + str(self.ai.board)
            print("-" * 70)
            print(Game.vstack(user_output, ai_output))
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()
# выполнение запуска происходит через game.py
