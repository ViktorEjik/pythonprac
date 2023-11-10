#   Написать программу, которая заставляет человека вводить координаты вершин треугольника в формате (x1, y1), (x2, y2), (x3, y3),
# до тех пор, пока это не окажутся координаты вершин треугольника в указанном формате, а потом выводит его площадь с точностью до сотой.
#   Если формат ввода неправильный, программа вместо площади выводит «Invalid input»,
# а если формат условно правильный, но площадь его нулевая или вычислить её нельзя, потому что введены вообще не числа — «Not a triangle».
#   Диагностика ввода и расчет площади производится в функции triangleSquare, которая:
#       1) получает на вход входную строку программы
#       2) преобразует строку в координаты вершин: (x1, y1), (x2, y2), (x3, y3) = eval(inStr)
#       3) при преобразовании ловит все исключения, и при любом перехваченном исключении формирует исключение InvalidInput (этот класс нужно определить)
#       4) если ввод корректен, выполняет проверку на то, что координаты - корректны для треугольника; в случае некорректности 
#           формирует исключение BadTriangle (этот класс нужно определить)
#       5) если координаты корректны, то вычисляет и возвращает площадь
#   При вызове функции triangleSquare в основном коде программы ловятся исключения InvalidInput и BadTriangle,
# и в блоках их обработки выдается соответствующая диагностика
#   Вывод площади выполняется в блоке else

# Написать тесты:
# на неправильный формат
# на не-треугольник

class InvalidInput(Exception):
    def __str__(self) -> str:
        return 'Invalid input'


class BadTriangle(Exception):
    def __str__(self) -> str:
        return 'Not a triangle'


def triangleSquare(inStr):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(inStr)
    except Exception:
        raise InvalidInput()
    try:
        sqere = 0.5 * abs((x1-x3)*(y2-y3) - (x2 - x3)*(y1 - y3))
    except Exception:
        raise BadTriangle()
    if sqere == 0:
        raise BadTriangle()
    return sqere


def main():
    flag = True
    while flag:
        inStr = input()
        try:
            res = triangleSquare(inStr)
        except (InvalidInput, BadTriangle) as error:
            print(error)
        else:
            print(f'{res:.2f}')
            flag = False

if __name__ == '__main__':
    main()
