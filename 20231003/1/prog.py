def Pareto(*args):
    ans = list()
    a = args[0]
    for i in range(len(a)):
        flag = list()
        for j in range(len(a)):
            if i!=j:
                if (a[i][0] > (a[j][0]) or (a[i][1]) > (a[j][1])
                    or (a[i][0] >= a[j][0] and a[i][1] > a[j][1])):
                    flag.append(True)
                else:
                    flag.append(False)
        if all(flag):
            ans.append(a[i])
    print(tuple(ans))

Pareto(eval(input()))