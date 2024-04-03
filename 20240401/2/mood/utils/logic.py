"""Base logic and map module."""

from cowsay import list_cows

from ..data import cows
from .exeptions import (ReplaseMonster, MonsterRIP,
                        NOMonster, UnknownMonster,
                        IncorectArgument, NONamedMonster,
                        PlayerExist)
from .entity import Monster, Player

MAP_LENGTH = 10


class Map:
    """Interfase to create and manipulate evants on map."""

    def __init__(self) -> None:
        """Initiolase game map."""
        self.map = [
            [None for _ in range(MAP_LENGTH)] for _ in range(MAP_LENGTH)
        ]

    def set_evant(self, position: tuple[int, int], evant: Monster | None):
        """Set evant on map position."""
        x, y = position
        flag = bool(self.map[x][y])
        self.map[x][y] = evant
        if flag:
            raise ReplaseMonster

    def get_evant(self, position: tuple[int, int]) -> Monster:
        """Return ivent on map position."""
        x, y = position
        return self.map[x][y]

    def is_evant(self, position: tuple[int, int]) -> bool:
        """Return True if on position in map has ivent."""
        x, y = position
        return self.map[x][y] is not None


class Game:
    """Base logic of game."""

    name_of_monster: list[str] = list_cows() + list(cows.cow_dict)

    def __init__(self, map: Map, player: Player) -> None:
        """Initiolased map and player list, with admin."""
        self.map = map
        self.adm = player
        self.pl_list = dict()

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
            self.map.set_evant(play_pos, None)
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
