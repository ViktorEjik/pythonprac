class MonsterRIP(Exception):
    def __init__(self, dmg: int, name: str, *args: object) -> None:
        super().__init__(*args)
        self.dmg = dmg
        self.name = name


class NOWepon(Exception):
    pass


class NOMonster(Exception):
    pass


class ReplaseMonster(Exception):
    pass


class IncorectArgument(Exception):
    pass


class UnknownMonster(Exception):
    pass
