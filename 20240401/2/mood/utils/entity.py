"""Module contains all play entitys."""

import abc
from io import StringIO

from cowsay import cowsay, list_cows, read_dot_cow

from ..data import cows
from .exeptions import NOWepon, UnknownMonster

MAP_LENGTH = 10


class Wepon(abc.ABC):
    """Baseic class to cteate weapon."""

    damage: int


class Sword(Wepon):
    """Criate sword for player."""

    damage = 10


class Spear(Wepon):
    """Criate speare for player."""

    damage = 15


class Axe(Wepon):
    """Criate axe for player."""

    damage = 20


class Player:
    """Provide the interfase to create and manipylate player on a map."""

    orient = {
        'left': (-1, 0),
        'right': (1, 0),
        'up': (0, -1),
        'down': (0, 1)
    }

    inventory = {
        'sword': Sword(),
        'axe': Axe(),
        'spear': Spear()
    }

    def __init__(self, name) -> None:
        """Init player."""
        self._position = (0, 0)
        self.name = name

    @property
    def position(self) -> tuple[int, int]:
        """Get player position."""
        return self._position

    @position.setter
    def position(self, pos: tuple[int, int]):
        """Set player position."""
        self._position = pos

    def move(self, orientation: str):
        """Move pelayer to one cels on orientation."""
        self.position = (
            (self.position[0] + self.orient[orientation][0]) % MAP_LENGTH,
            (self.position[1] + self.orient[orientation][1]) % MAP_LENGTH
        )

    def attack_with(self, weapon: str) -> Wepon:
        """Count damege with weapon."""
        if weapon in self.inventory:
            return self.inventory.get(weapon)
        raise NOWepon

    def __str__(self) -> str:
        """Representetion of player."""
        ans = (
            f'\tname: {self.name}\n'
            f'\tinventnory: {list(self.inventory.keys())}\n'
            f'\tpos: {self.position}'
        )
        return ans


class Print_Monster:
    """Interfase to print monster."""

    def __init__(self, name: str, hellow: str) -> None:
        """Init monster."""
        self.hellow = hellow
        if (name not in list_cows()) and (name not in cows.cow_dict):
            raise UnknownMonster
        self.name = name

    def __str__(self) -> str:
        """Use it to print moster."""
        try:
            return cowsay(message=self.hellow, cow=self.name)
        except Exception:
            cow = read_dot_cow(StringIO(cows.cow_dict[self.name]))
            return cowsay(message=self.hellow, cowfile=cow)


class Monster(Print_Monster):
    """Use it to create and damege monster."""

    def __init__(self, name: str, hellow: str, hp: int) -> None:
        """Initiate monster."""
        super().__init__(name, hellow)
        self.hp = hp

    def __bool__(self):
        """Return false if monster dead."""
        return self.hp > 0

    def healing(self, hp: int) -> int:
        """Interfase to damage and heal monsters."""
        if hp <= self.hp:
            self.hp -= hp
            return hp
        old = self.hp
        self.hp = 0
        return old
