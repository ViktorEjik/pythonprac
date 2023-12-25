class Maze:
    def __init__(self, n) -> None:
        self.n = n
        self.img = [
            ['█' for _ in range(2*self.n + 1)] for _ in range(2*self.n + 1)
        ]
        for i in range(1, 2*self.n + 1, 2):
            for j in range(1, 2*self.n + 1, 2):
                self.img[i][j] = '·'
    
    def __setitem__(self, __index, __value):
        start = __index[0], __index[1].start
        finish = __index[1].stop, __index[2]
        if start[0] == finish[0]:
            
            for i in range(start[1]*2 + 1, finish[1]*2 + 1, 2):
                self.img[i + 1][start[0]*2 + 1] = __value
            for i in range(finish[1]*2 + 1, start[1]*2 + 1, 2):
                self.img[i + 1][start[0]*2 + 1] = __value

        elif start[1] == start[1]:

            for i in range(start[0]*2 + 1, finish[0]*2 + 1, 2):
                self.img[start[1]*2 + 1][i + 1] = __value
            for i in range(finish[0]*2 + 1, start[0]*2 + 1, 2):
                self.img[start[1]*2 + 1][i + 1] = __value
                
    def __getitem__(self, __index):
        start = __index[0] * 2 + 1, __index[1].start * 2 + 1
        finish = __index[1].stop * 2 + 1, __index[2] * 2 + 1
        valid = set((start,))
        while True:
            new_valid = set() | valid
            for now in valid:
                if self.img[now[1]][now[0] + 1] == '·':
                    new_valid.add((now[0] + 2, now[1]))
                if self.img[now[1]][now[0] - 1] == '·':
                    new_valid.add((now[0] - 2, now[1]))
                if self.img[now[1] + 1][now[0]] == '·':
                    new_valid.add((now[0], now[1] + 2))
                if self.img[now[1] - 1][now[0]] == '·':
                    new_valid.add((now[0], now[1] - 2))
            if new_valid == valid:
                break
            valid = new_valid
        return finish in valid
    
    def __str__(self) -> str:
        strs = list()
        for s in self.img:
            strs.append(''.join(s))
        return '\n'.join(s for s in strs)


import sys
exec(sys.stdin.read())
        