from entity import Monster
import exeptions

MAP_LENGTH = 10


class Map:
    def __init__(self) -> None:
        self.map = [[None for _ in range(MAP_LENGTH)] for _ in range(MAP_LENGTH)]
    
    def set_evant(self, position, evant):
        x, y = position
        flag = self.map[x][y] is not None
        self.map[x][y] = evant
        if flag:
            raise exeptions.ReplaseMonster
    
    def get_evant(self, position):
        x, y = position
        return self.map[x][y]
    
    def is_evant(self, position):
        x, y = position
        return self.map[x][y] is not None


class Game:
    
    def __init__(self, map, player) -> None:
        self.map = map
        self.player = player
    
    def addmon(self, position, name, hellow):
        monster = Monster(name, hellow)
        try:
            monster = Monster(name, hellow)
            self.map.set_evant(position, monster)
        except exeptions.UnknownMonster as err:
            raise err
        except exeptions.ReplaseMonster as err:
            raise err
        except Exception:
            raise exeptions.IncorectArgument
    
    def go_to(self, orientation):
        self.player.move(orientation)
        pos = self.player.position
        res = [pos, None]
        if self.map.is_evant(pos):
            res[1] = self.map.get_evant(pos).boo()
        return res
    

