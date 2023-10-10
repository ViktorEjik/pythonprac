from decimal import *


def esum(N, one):
    prod = one
    sum = one
    for i in range(2, N+1):
        prod *= type(one)(i)
        sum += one/prod
    return sum

print(esum(20, Decimal(1)))
    
