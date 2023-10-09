def main():
    a, b = eval(input())
    print([x for x in range(a, b) if all([x % i != 0 for i in range(2, x // 2 + 1)])])


if __name__ == '__main__':
    main()
