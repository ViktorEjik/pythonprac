import cmd
import shlex

import exeptions
from entity import Player
from logic import Game, Map

class CMD_Game(cmd.Cmd):
    
    def __init__(self,
                 completekey: str = "tab",
                 stdin = None,
                 stdout = None,
                 game: Game | None = None) -> None:
        # Создание новой игры
        if not game:
            game = Game(Map(), Player())
        self.game = game
        super().__init__(completekey, stdin, stdout)
    
    prompt = 'MUD-> '

    @staticmethod
    def print_pos(res):
        print(f'Moved to ({res[0][0]}, {res[0][1]})')
        if res[1]:
            print(res[1])
    
    def do_left(self, args):
        if args:
            print('Invalid command')
        res = self.game.go_to('left')
        self.print_pos(res)

    def do_right(self, args):
        if args:
            print('Invalid command')
        res = self.game.go_to('right')
        self.print_pos(res)
    
    def do_up(self, args):
        if args:
            print('Invalid command')
        res = self.game.go_to('up')
        self.print_pos(res)

    def do_down(self, args):
        if args:
            print('Invalid command')
        res = self.game.go_to('down')
        self.print_pos(res)
    
    def do_addmon(self, args):
        try:
            args = shlex.split(args)
            args.insert(0, 'name')
            monster = dict()
            i = 0
            if any(x not in args for x in ['hello', 'hp', 'coords']):
                raise exeptions.IncorectArgument
            while i < len(args):
                match args[i]:
                    case 'name' | 'hello':
                        monster[args[i]] = args[i+1]
                        i += 2
                    case 'hp':
                        monster[args[i]] = int(args[i+1])
                        i += 2
                    case 'coords':
                        monster[args[i]] = int(args[i+1]), int(args[i+2])
                        i += 3
                    case _:
                        raise exeptions.IncorectArgument
        except exeptions.IncorectArgument:
            print('Invalid command')
            return
        except ValueError:
            print('Invalid arguments')
            return
        except IndexError:
            print('Invalid arguments')
            return

        ans = (
            f'Added monster {monster["name"]} to'
            f'{monster["coords"]} saying {monster["hello"]}'
        )

        try:
            self.game.addmon(
                monster['coords'], monster["name"],
                monster['hello'], monster['hp']
            )
        except exeptions.UnknownMonster:
            print('Cannot add unknown monster')
            return
        except exeptions.ReplaseMonster:
            ans += '\nReplaced the old monster'
        except exeptions.IncorectArgument:
            print('Invalid arguments')
            return
        print(ans)

    
    def complete_addmon(self, text, line, begidx, endidx):
        if all(x not in line for x in ['hello', 'hp', 'coords']):
            return [c for c in self.game.name_of_monster if c.startswith(text)]


    def do_attack(self, args):
        res = 'Attacked {name}, damage {dmg} hp'
        args = shlex.split(args)
        if not args or len(args) not in [1, 3]:
            print('Invalid arguments')
            return
        name, args = args[0], args[1:]
        if args and (args[0] != 'with' or len(args) != 2):
            print('Invalid arguments')
            return
        try:
            if args:
                dmg = self.game.attack(name=name, weapon=args[1])
            else:
                dmg = self.game.attack(name=name)

        except exeptions.MonsterRIP as err:
            print(res.format(name=err.name, dmg=err.dmg))
            print(f'{err.name} died')
            return
        except exeptions.NOMonster:
            print('No monster here')
            return
        except exeptions.NONamedMonster:
            print(f'No {name} here')
            return
        except exeptions.NOWepon:
            print('Unknown weapon')
            return


        print(res.format(name=dmg[1], dmg=dmg[0]))
        print(f'{dmg[1]} now has {dmg[2]}')

    def complete_attack(self, text, line, begidx, endidx):
        if 'with' in line:
            return [c for c in self.game.player.inventory.keys() if c.startswith(text)]
        return [c for c in self.game.name_of_monster if c.startswith(text)]


    def do_EOF(self, args):
        return True
    
    def emptyline(self) -> bool:
        pass
