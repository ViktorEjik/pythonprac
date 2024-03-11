import cmd

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
        

    def do_EOF(self, args):
        return True
    
    def emptyline(self) -> bool:
        pass
