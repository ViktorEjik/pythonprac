from cowsay import cowsay, list_cows
import exeptions


MAP_LENGTH = 10

class Player:
    orient = {
        'left': (-1, 0),
        'right': (1, 0),
        'up': (0, -1),
        'down': (0, 1)
    }
    
    
    def __init__(self) -> None:
        self._position = (0, 0)

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, pos):
        self._position = pos
    
    def move(self, orientation):
        self.position = (
            (self.position[0] + self.orient[orientation][0]) % MAP_LENGTH,
            (self.position[1] + self.orient[orientation][1]) % MAP_LENGTH
        )

class Monster:
    def __init__(self, name, hellow) -> None:
        self.hellow = hellow
        self.name = name
    
    def boo(self):
        return cowsay(message=self.hellow, cow=self.name)
