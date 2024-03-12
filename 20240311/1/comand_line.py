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
        # addmon dragon hp 999 coords 6 9 hello "Who goes there?"

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
        

    def do_EOF(self, args):
        return True
    
    def emptyline(self) -> bool:
        pass
