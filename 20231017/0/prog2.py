s = input()
x, y = eval(input())

print(eval(s, {'x': x, 'y': y}))
print(eval(s, {'x': y, 'y': x}))

