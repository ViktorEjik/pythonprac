def main():
    n = int(input())
    for i in range(n, n + 3):
        print(f'{i} * {n} = {i*n} {i} * {n + 1} = {i * (n+1)} {i} * {n+2} = {i * (n+2)}')


if __name__ == '__main__':
    main()
