from io import StringIO

from cowsay import cowsay, list_cows, read_dot_cow

import cows
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
    def position(self, pos: tuple[int, int]):
        self._position = pos

    def move(self, orientation: str):
        self.position = (
            (self.position[0] + self.orient[orientation][0]) % MAP_LENGTH,
            (self.position[1] + self.orient[orientation][1]) % MAP_LENGTH
        )


class Monster:
    def __init__(self, name: str, hellow: str, hp: int) -> None:
        self.hellow = hellow
        if (name not in list_cows()) and (name not in cows.cow_dict):
            raise exeptions.UnknownMonster
        self.name = name
        self.hp = hp

    def boo(self):
        try:
            return cowsay(message=self.hellow, cow=self.name)
        except Exception:
            cow = read_dot_cow(StringIO(cows.cow_dict[self.name]))
            return cowsay(message=self.hellow, cowfile=cow)
