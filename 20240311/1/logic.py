import exeptions
from entity import Monster, Player

MAP_LENGTH = 10


class Map:
    def __init__(self) -> None:
        self.map = [
            [None for _ in range(MAP_LENGTH)] for _ in range(MAP_LENGTH)
        ]

    def set_evant(self, position: tuple[int, int], evant):
        x, y = position
        flag = self.map[x][y] is not None
        self.map[x][y] = evant
        if flag:
            raise exeptions.ReplaseMonster

    def get_evant(self, position: tuple[int, int]):
        x, y = position
        return self.map[x][y]

    def is_evant(self, position: tuple[int, int]):
        x, y = position
        return self.map[x][y] is not None


class Game:

    def __init__(self, map: Map, player: Player) -> None:
        self.map = map
        self.player = player

    def addmon(self,
               position: tuple[int, int],
               name: str,
               hellow: str,
               hp: int):
        try:
            monster = Monster(name, hellow, hp)
            self.map.set_evant(position, monster)
        except exeptions.UnknownMonster as err:
            raise err
        except exeptions.ReplaseMonster as err:
            raise err
        except Exception:
            raise exeptions.IncorectArgument

    def go_to(self, orientation: str):
        self.player.move(orientation)
        pos = self.player.position
        res = [pos, None]
        if self.map.is_evant(pos):
            res[1] = self.map.get_evant(pos).boo()
        return res
