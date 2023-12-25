from itertools import combinations


class Triangle:
    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.S = 0.5 * abs((a[0]-c[0])*(b[1]-c[1]) - (b[0] - c[0])*(a[1] - c[1]))
    
    def __abs__(self):
        return self.S
    
    def __bool__(self):
        return self.S != 0
    
    def __gt__(self, obj):
        return self.__abs__() > obj.__abs__()
    
    def is_in_sqere(self, dot):
        return (
            min(self.a[0], self.b[0], self.c[0]) <= dot[0] <= max(self.a[0], self.b[0], self.c[0])
            and min(self.a[1], self.b[1], self.c[1]) <= dot[1] <= max(self.a[1], self.b[1], self.c[1])
        )
    
    def is_in_triandle(self, dot):
        if not self.is_in_sqere(dot):
            return False
        if any(map(lambda x: x == dot, (self.a, self.b, self.c))):
            return True
        k = lambda a, b: (a[1] - b[1])/(a[0]-b[0])
        f = lambda a, b: a[1] - k(a, b) * a[0]
        # y = k*x + f
        l = lambda tup: tup[2][1] <= k(tup[0], tup[1]) * tup[2][0] + f(tup[0], tup[1])
        flags = sum(map(l, ((self.a, self.b, dot), (self.a, self.c, dot), (self.b, self.c, dot))))
        return True if flags == 2 else False
    
    def __contains__(self, obj):
        if self.__abs__() < obj.__abs__():
            return False
        if obj.__abs__() == 0:
            return True
        return all(map(self.is_in_triandle, (obj.a, obj.b, obj.c)))
    
    @staticmethod
    def check_conv(a, b, c, d):
        x1_1, y1_1 = a
        x1_2, y1_2 = b
        x2_1, y2_1 = c
        x2_2, y2_2 = d

        A1 = y1_1 - y1_2
        B1 = x1_2 - x1_1
        C1 = x1_1*y1_2 - x1_2*y1_1
        A2 = y2_1 - y2_2
        B2 = x2_2 - x2_1
        C2 = x2_1*y2_2 - x2_2*y2_1
        
        if B1*A2 - B2*A1 and A1:
            y = (C2*A1 - C1*A2) / (B1*A2 - B2*A1)
            x = (-C1 - B1*y) / A1
        elif B1*A2 - B2*A1 and A2:
            y = (C2*A1 - C1*A2) / (B1*A2 - B2*A1)
            x = (-C2 - B2*y) / A2
        else: return False
        
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2): return True
        else: return False

        
    
    def __and__(self, obj):
        if self.__abs__() == 0 or obj.__abs__() == 0:
            return False
        if (
            any(map(self.is_in_triandle, (obj.a, obj.b, obj.c)))
            or any(map(obj.is_in_triandle, (self.a, self.b, self.c)))
        ): return True

        for tup1 in combinations((self.a, self.b, self.c), 2):
            for tup2 in combinations((obj.a, obj.b, obj.c), 2):
                if self.check_conv(*tup1, *tup2):
                    return True
        return False

import sys
exec(sys.stdin.read())
