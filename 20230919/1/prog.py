def main():
    num = int(input())
    A = '+' if num % 2 == 0 and num % 25 == 0 else '-'
    B = '+' if num % 2 != 0 and num % 25 == 0 else '-'
    C = '+' if num % 8 == 0 else '-'
    print(f'A {A} B {B} C {C}')


if __name__ == '__main__':
    main()
