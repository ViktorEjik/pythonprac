from math import inf


class A(Exception):
    pass


class B(A):
    pass


class C(B):
    pass


def div_ad(a, b):
    try: 
        return a/b
    except ZeroDivisionError:
        return inf


def main():
    for a, b in [(10,5), (1,0), (5, 6)]:
        print(div_ad(a, b))



if __name__ == '__main__':
    main()

