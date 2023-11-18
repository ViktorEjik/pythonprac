from string import ascii_lowercase


class Alpha:
    __slots__ = list('abcdefghijklmnopqrstuvwxyz')
    
    def __init__(self, *args, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __str__(self):
        s = str()
        for key in self.__slots__:
            try:
                s += f'{key}: {getattr(self, key)}, '
            except:
                pass
        return s[:-2]


class AlphaQ:
    def __init__(self, *args, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __getattr__(self, __name: str):
        if __name in self.__dict__ and __name in ascii_lowercase:
            return self.__dict__[__name]
        raise AttributeError
    
    def __str__(self):
        s = str()
        for key in ascii_lowercase:
            try:
                s += f'{key}: {getattr(self, key)}, '
            except:
                pass
        return s[:-2]

import sys
exec(sys.stdin.read())
