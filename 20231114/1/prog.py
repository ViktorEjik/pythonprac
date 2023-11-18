def objcount(cls):
    class new_cls(cls):
        counter = 0
        
        def __init__(self, *args, **kwargs):
            type(self).counter += 1
            super().__init__(*args, **kwargs)
        
        def __del__(self):
            type(self).counter -= 1
            try:
                super().__del__()
            except AttributeError:
                pass

    return new_cls


import sys
exec(sys.stdin.read())

