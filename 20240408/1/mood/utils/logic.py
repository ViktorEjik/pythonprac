"""Base logic and map module."""

from cowsay import list_cows

from ..data import cows
from .exeptions import (ReplaseMonster, MonsterRIP,
                        NOMonster, UnknownMonster,
                        IncorectArgument, NONamedMonster,
                        PlayerExist)
from .entity import Monster, Player
from random import randrange, choice
import asyncio

MAP_LENGTH = 10


class Map:
    """Interfase to create and manipulate evants on map."""

    def __init__(self) -> None:
        """Initiolase game map."""
        self.map: list[None | Monster] = [
            [None for _ in range(MAP_LENGTH)] for _ in range(MAP_LENGTH)
        ]
        self.monsters = list()

    def set_evant(self, position: tuple[int, int], evant: Monster | None):
        """Set evant on map position."""
        x, y = position
        flag = bool(self.map[x][y])
        self.map[x][y] = evant
        self.monsters.append((x, y, evant))
        if flag:
            raise ReplaseMonster

    def get_evant(self, position: tuple[int, int]) -> Monster:
        """Return ivent on map position."""
        x, y = position
        return self.map[x][y]
    
    def del_monster(self, position: tuple[int, int]):
        if not self.is_evant(position):
            return
        x, y = position
        self.monsters = list(filter(lambda z: z != (x, y, self.map[x][y]), self.monsters))
        self.map[x][y] = None
        

    def is_evant(self, position: tuple[int, int]) -> bool:
        """Return True if on position in map has ivent."""
        x, y = position
        return self.map[x][y] is not None
    
    def move_evant(self, now, new):
        self.map[new[0]][new[1]] = self.map[now[0]][now[1]].copy()
        self.del_monster(now)
        self.monsters.append((new[0], new[1], self.map[new[0]][new[1]]))
        for i in range(MAP_LENGTH):
            print(self.map[i])


class Game:
    """Base logic of game."""
    
    orient = {
        (0, 1): 'down',
        (1, 0): 'right',
        (0, -1): 'up',
        (-1, 0): 'left',
    }

    name_of_monster: list[str] = list_cows() + list(cows.cow_dict)

    def __init__(self, map: Map, player: Player, sleep:int=30) -> None:
        """Initiolased map and player list, with admin."""
        self.map = map
        self.adm = player
        self.pl_list:dict[str: Player] = dict()
        self.t_sleep = sleep

    def addmon(self,
               position: tuple[int, int],
               name: str,
               hellow: str,
               hp: int):
        """Add named monster on map."""
        try:
            monster = Monster(name, hellow, hp)
            self.map.set_evant(position, monster)
        except UnknownMonster as err:
            raise err
        except ReplaseMonster as err:
            raise err
        except Exception:
            raise IncorectArgument

    def attack(
        self,
        player: Player,
        name: str,
        weapon='sword'
    ) -> tuple[int, str, int]:
        """Attack nemed monster with one of weapon (sword, spean, axe)."""
        play_pos = player.position
        monster = self.map.get_evant(play_pos)
        if not monster:
            raise NOMonster

        if name != monster.name:
            raise NONamedMonster

        weapon = player.attack_with(weapon)
        dmg = monster.healing(weapon.damage)

        if not monster:
            self.map.del_monster(play_pos)
            raise MonsterRIP(dmg=dmg, name=monster.name)
        return dmg, monster.name, monster.hp

    def go_to(
        self,
        orientation: str,
        player: Player
    ) -> tuple[tuple[int, int], str | None]:
        """Move player on one of 4 orientation (left, right, up, down) on one position."""
        player.move(orientation)
        pos = player.position
        res = (pos,)
        if self.map.is_evant(pos):
            res += (str(self.map.get_evant(pos)), )
        else:
            res += (None,)
        return res

    def add_new_player(self, player_name: str) -> Player:
        """Add new connected player."""
        if player_name in self.pl_list:
            raise PlayerExist
        self.pl_list[player_name] = Player(player_name)
        return self.pl_list[player_name]

    def del_player(self, player: Player) -> None:
        """Delate disconnected player."""
        del self.pl_list[player.name]

    async def wandering_monster(self, flag, clients):
        
        if not flag:
            print('wandering_monster off')
            return
        print('wandering_monster on, sleep =', self.t_sleep)
        while True:
            if not self.map.monsters:
                await asyncio.sleep(self.t_sleep)
                continue
            while True:
                i = randrange(0, len(self.map.monsters))
                x, y, monster = self.map.monsters.pop(i)
                dx, dy = choice([(0,1), (1, 0), (0, -1), (-1, 0)])
                if self.map.is_evant(((x + dx) % MAP_LENGTH, (y+dy) % MAP_LENGTH)):
                    continue
                break
            new = ((x + dx) % MAP_LENGTH, (y+dy) % MAP_LENGTH)
            self.map.move_evant((x, y), new)
            for client in clients:
                await clients[client].put(
                    f'{monster.name} moved one cell {self.orient[(dx, dy)]}'
                    +'\n'
                )
                if self.pl_list[client.name].position == new:
                    await clients[client].put(str(monster)+'\n')
            print(f'Monster from ({x, y}) move to {new}')
            await asyncio.sleep(self.t_sleep)
        
