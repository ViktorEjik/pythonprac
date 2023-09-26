def main():
    l = eval(input())
    for elem in l:
        if elem % 2 == 1:
            print(elem)
            break
    else:
        print(l[-1])


if __name__ == '__name__':
    main()
