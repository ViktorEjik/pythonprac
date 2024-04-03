"""Module contains all exceptions."""


class MonsterRIP(Exception):
    """Raised if monster died."""

    def __init__(self, dmg: int, name: str, *args: object) -> None:
        """Init exception."""
        super().__init__(*args)
        self.dmg = dmg
        self.name = name


class PlayerExist(Exception):
    """Raised if a player with an already registered name tries to join."""

    pass


class NOWepon(Exception):
    """Raised if player try to attack monster with nonexistent weapons."""

    pass


class NOMonster(Exception):
    """Rised if no monster in this position."""

    pass


class NONamedMonster(Exception):
    """Raised if player try to attack monster with name is different from the true."""

    pass


class ReplaseMonster(Exception):
    """Rised if new monster replase old."""

    pass


class IncorectArgument(Exception):
    """Rised if use incorect argument."""

    pass


class UnknownMonster(Exception):
    """Rised if use anknown monster."""

    pass
