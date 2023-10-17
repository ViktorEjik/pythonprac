def main():
    import timeit
    print(timeit.Timer('-'.join(map(str, range(100)))).autorange())



if __name__ == '__main__':
    main()
