from cowsay import list_cows

import cows
import exeptions
from entity import Monster, Player

MAP_LENGTH = 10


class Map:
    def __init__(self) -> None:
        self.map = [
            [None for _ in range(MAP_LENGTH)] for _ in range(MAP_LENGTH)
        ]

    def set_evant(self, position: tuple[int, int], evant: Monster | None):
        x, y = position
        flag = bool(self.map[x][y])
        self.map[x][y] = evant
        if flag:
            raise exeptions.ReplaseMonster

    def get_evant(self, position: tuple[int, int]) -> Monster:
        x, y = position
        return self.map[x][y]

    def is_evant(self, position: tuple[int, int]) -> bool:
        x, y = position
        return self.map[x][y] is not None


class Game:
    name_of_monster: list[str] = list_cows() + list(cows.cow_dict)

    def __init__(self, map: Map, player: Player) -> None:
        self.map = map
        self.adm = player
        self.pl_list = dict()

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

    def attack(
        self,
        player: Player,
        name: str,
        weapon='sword'
    ) -> tuple[int, str, int]:
        play_pos = player.position
        monster = self.map.get_evant(play_pos)
        if not monster:
            raise exeptions.NOMonster

        if name != monster.name:
            raise exeptions.NONamedMonster

        weapon = player.attack_with(weapon)
        dmg = monster.healing(weapon.damage)

        if not monster:
            self.map.set_evant(play_pos, None)
            raise exeptions.MonsterRIP(dmg=dmg, name=monster.name)
        return dmg, monster.name, monster.hp

    def go_to(
        self,
        orientation: str,
        player: Player
    ) -> tuple[tuple[int, int], str | None]:

        player.move(orientation)
        pos = player.position
        res = (pos,)
        if self.map.is_evant(pos):
            res += (str(self.map.get_evant(pos)), )
        else:
            res += (None,)
        return res

    def add_new_player(self, player_name: str) -> Player:
        if player_name in self.pl_list:
            raise exeptions.PlayerExist
        self.pl_list[player_name] = Player(player_name)
        return self.pl_list[player_name]

    def del_player(self, player: Player) -> None:
        del self.pl_list[player.name]
