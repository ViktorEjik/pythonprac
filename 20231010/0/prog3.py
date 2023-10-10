from math import sin

def scale(a, b, A, B, x):
    return (x-a)*(B-A) / (b - a) + A

scr = [['.' for _ in range(30)]for _ in range(30)] 

for i in range(30):
    x = scale(0, 30, -5, 5, i)
    y = sin(x)
    y = scale(-1, 1, 29, 0, y)
    print(len(scr), len(scr[0]))
    scr[i][int(y)] = '*'

print('\n'.join([''.join(s) for s in scr]))
