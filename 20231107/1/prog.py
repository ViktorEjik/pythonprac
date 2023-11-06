from collections import UserString
# Написать класс DivStr (унаследованный от collections.UserString), в котором:
#   1) Добавлена возможность заведения пустой строки без параметров — DivStr()
#   2) Добавлена операция a // n — возвращается итератор из n подстрок одинакового наибольшего размера, на которые можно разбить исходную строку
#   3) Добавлена операция a % n — возвращается «остаток от деления», хвостик, который надо приписать к a // n, чтобы получилась вся строка (возможно, пустой)

class DivStr(UserString):
    def __init__(self, seq: object = None) -> None:
        if seq is None:
            seq = ''
        super().__init__(seq)
    
    def __floordiv__(self, other):
        seg_len = len(self) // other
        for i in range(0, len(self), seg_len):
            if i + seg_len <= len(self):
                yield self[i:i+seg_len]
    
    def __mod__(self, other):
        mod = len(self) % other
        return self[len(self) - mod:]

if __name__ == '__main__':
    a = DivStr("XcDfQWEasdERTdfgRTY")
    print(*(a // 4))
    print(a % 4)
    print(* a % 10 // 3)
    print(a.lower() % 3)
    print(* a[1:7] // 3)
    print(a % 5 + DivStr() + a % 6)
