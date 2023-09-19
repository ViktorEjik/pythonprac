def main():
    a, b, c = eval(input())
    print((a > 0 and b > 0 and c > 0) and max(a, b, c) < a + b + c - max(a, b, c))


if __name__ == '__main__':
    main()
