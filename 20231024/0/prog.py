def walk2d():
    point = 0, 0
    # dx, dy = yield 'start'
    while (delta := yield point):
        point = point[0] + delta[0], point[1] + delta[1]


def main():
    w = walk2d()
    w.send(None)
    print(w.send((1, 1)))
    print(w.send((2, 0)))
    print(w.send((-2, -3)))


if __name__ == '__main__':
    main()
