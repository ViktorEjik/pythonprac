def sort(arr: list):
    if(len(arr) <= 1):
        return arr
    arr1 = [x for x in arr[1:] if x < arr[0]]
    arr2 = [x for x in arr if x == arr[0]]
    arr3 = [x for x in arr[1:] if x > arr[0]]
    return sort(arr1) + arr2 + sort(arr3)


def main():
    arr = eval(input())

    print(*sort(arr), sep=', ')


if __name__ == '__main__':
    main()
