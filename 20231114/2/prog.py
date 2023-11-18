class Num:
    def __get__(self, obj, objtype=None):
        if '_num' in dir(obj):
            return obj._num
        return 0
    
    def __set__(self, obj, value):
        if 'real' in dir(value):
            obj._num = value
        elif '__len__' in dir(value):
            obj._num = len(value)

import sys
exec(sys.stdin.read())
       