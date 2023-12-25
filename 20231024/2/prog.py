from itertools import islice


def slide(seq, n):
    k = 0
    x = True
    while k < len(seq):
        x = islice(seq, k, k+n)
        k += 1
        yield from x


import sys
exec(sys.stdin.read())
