class Unded(Exception):
    pass


class Skeleton(Unded):
    pass


class Zombie(Unded):
    pass


class Ghoul(Unded):
    pass


def necro(a):
    if a % 3 == 0:
        raise Skeleton()
    elif a % 3 == 1:
        raise Zombie()
    else:
        raise Ghoul()


def main():
    x, y = eval(input())
    for i in range(x, y):
        try:
            necro(i)
        except Skeleton:
            print('Skeleton')
        except Zombie:
            print('Zombie')
        except Unded:
            print('Generic Undead')


if __name__ == '__main__':
    main()
