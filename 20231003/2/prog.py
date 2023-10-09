def f(a, b):
    numeric = (int, float, complex)
    enum = (list, tuple)
    if isinstance(a, numeric) and isinstance(b, numeric):
        return a - b
    if isinstance(a, enum) and isinstance(b, enum) and type(a) == type(b):
        ans = list()
        for elem in a:
            if elem not in b:
                ans += [elem]
        return type(a)(ans)
    raise ValueError


if __name__ == '__main__':
    inp = eval(input())
    print(f(*inp))
