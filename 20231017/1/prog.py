def main():
    s = input().lower()
    set_pars = set()
    for i in range(len(s) - 1):
        if not (s[i].isalpha() and s[i + 1].isalpha()):
            continue
        par = s[i], s[i+1]
        if par not in set_pars:
            set_pars.add(par)
    print(len(set_pars))


if __name__ == '__main__':
    main()
