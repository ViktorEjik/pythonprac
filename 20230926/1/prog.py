def main():
    mat = list()
    while s := input():
        mat.append(list(eval(s)))
    
    l = len(mat[0])
    res = [[0 for _ in range(l)] for _ in range(l)]
    
    
    
    for i in range(l):
        for j in range(l):
            for k in range(len(mat[0])):
                res[i][j] += mat[i][k] * mat[l + k][j]
    
    for i in range(l):
        print(*res[i], sep=',')



if __name__ == '__main__':
    main()

