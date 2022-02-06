import random

field = [["0"] * 3 for i in range(7)]

def vvod():
    while True:
        a = input('Cделайте свой ход\t').split()
        if len(a) != 2:
            print(" Введите 2 координаты! ")
            continue

        x, y = a

        if not (x.isdigit()) or not (y.isdigit()):
            print(" Введите числа! ")
            continue

        x, y = int(x), int(y)

        if x < 1 or x > 6 or y < 1 or y > 6:
            print('Координаты вне диапозона! Попробуёте ещё раз.')
            continue

        if field[x][y] != "0":
            print(" Клетка занята! ")
            continue

        return x, y


print(vvod())
