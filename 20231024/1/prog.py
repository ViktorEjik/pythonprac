def fib(n, m):
    f_1 = 1
    f_2 = 1
    while n >= 0:
        if f_1 >= m:
            yield f_1
            n -= 1
        x = f_2 + f_1
        f_1, f_2 = f_2, x

import sys
exec(sys.stdin.read())
