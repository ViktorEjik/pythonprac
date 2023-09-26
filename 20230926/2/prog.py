def main():
    key = lambda x: (x**2) % 100
    arr = list(eval(input()))

    for i in range(len(arr)-1):
        for j in range(len(arr)-i-1):
            if key(arr[j]) > key(arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    print(arr)


if __name__ == '__main__':
    main()
