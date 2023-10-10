from fractions import Fraction
from decimal import Decimal


def multiplier(x, y, Tupe=float):
    return Tupe(x) * Tupe(y)


def main():
    print(multiplier('1.1', '1.2', float))
    print(multiplier(1.1, 1.2, Decimal))
    print(multiplier('1/6', '2/3', Fraction))


if __name__ == '__main__':
    main()
