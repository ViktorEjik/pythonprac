from typing import Any
from pprint import pprint

class Omnibus:
    d = dict()
    
    def __init__(self) -> None:
        self.attr = list()
    
    def __setattr__(self, __name, __value) -> None:
        if '__' in __name:
            pass
        if __name != 'attr':
            
            if __name in self.attr:
                return
            
            try:
                Omnibus.d[__name] +=1
            except:
                Omnibus.d[__name] = 1
            self.attr.append(__name)
        else:
            object.__setattr__(self, __name, __value)
    
    def __getattr__(self, __name: str) -> Any:
        if __name in self.attr:
            return Omnibus.d[__name]
    
    def __delattr__(self, __name: str) -> None:
        if __name not in self.attr:
            return
        self.attr.remove(__name)
        Omnibus.d[__name] -= 1


import sys
exec(sys.stdin.read())

