def main():
    while s := input():
        if s == '13':
            break
        elif int(s) % 2 == 0:
            print(s)
    else:
        print('Не ввели 13')


if __name__ == '__main__':
    main()
