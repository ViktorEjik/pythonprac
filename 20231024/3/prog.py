from itertools import *
print(*sorted(list(filter(lambda x: x[x.find('TOR') + 1:].find('TOR') > -1 , (''.join(x) for x in product('TOR', repeat=int(input())))))), sep =', ')

