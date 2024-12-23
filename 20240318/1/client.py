import cmd
import shlex
import socket

import exeptions
from entity import Print_Monster


class CMD_Game(cmd.Cmd):

    def __init__(self,
                 socket,
                 completekey: str = "tab",
                 stdin=None,
                 stdout=None,
                 ) -> None:

        self.socket = socket
        socket.sendall('cows\n'.encode())
        self.name_of_monster = eval(socket.recv(1024).rstrip().decode())
        socket.sendall('invent\n'.encode())
        self.player_inventory = eval(socket.recv(1024).rstrip().decode())
        super().__init__(completekey, stdin, stdout)

    prompt = 'MUD-> '

    def print_pos(self, orient):
        self.socket.sendall(f'{orient}\n'.encode())
        response = self.socket.recv(1024).rstrip().decode().split('\\')
        pos = response[0]
        print(f'Moved to ({pos})')
        if len(response) > 1:
            name, hellow = shlex.split(response[1])
            print(Print_Monster(name, hellow))

    def do_left(self, args):
        if args:
            print('Invalid command')
            return
        self.print_pos('left')

    def do_right(self, args):
        if args:
            print('Invalid command')
            return
        self.print_pos('right')

    def do_up(self, args):
        if args:
            print('Invalid command')
            return
        self.print_pos('up')

    def do_down(self, args):
        if args:
            print('Invalid command')
            return
        self.print_pos('down')

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
                    case 'name' | 'hello' | 'hp':
                        monster[args[i]] = args[i+1]
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
        monster['hello'] = '"' + monster['hello'] + '"'
        self.socket.sendall(
            (
                f"addmon {monster['name']} {monster['coords'][0]} "
                f"{monster['coords'][1]} {monster['hello']} "
                f"{monster['hp']}\n"
            ).encode()
        )

        response = self.socket.recv(1024).rstrip().decode()

        if response == '0':
            print(
                f'Added monster {monster["name"]} to '
                f'{monster["coords"]} saying {monster["hello"]}'
            )
        elif response == '1':
            print(
                f'Added monster {monster["name"]} to'
                f'{monster["coords"]} saying {monster["hello"]}'
                '\nReplaced the old monster'
            )
        elif response == '2':
            print('Cannot add unknown monster')

    def complete_addmon(self, text, line, begidx, endidx):
        if all(x not in line for x in ['hello', 'hp', 'coords']):
            return [c for c in self.name_of_monster if c.startswith(text)]

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

        self.socket.sendall(
            f'attack {name} { args[1] if args else "sword"}\n'.encode()
        )
        state, *dmg = shlex.split(self.socket.recv(1024).rstrip().decode())

        if state == '0':
            print(res.format(name=name, dmg=dmg[0]))
            print(f'{name} now has {dmg[1]}')
        elif state == '1':
            print(res.format(name=name, dmg=dmg[0]))
            print(f'{name} died')
        elif state == '2':
            print('No monster here')
        elif state == '3':
            print(f'No {name} here')
        elif state == '4':
            print('Unknown weapon')

    def complete_attack(self, text, line, begidx, endidx):
        if 'with' in line:
            return [
                c for c
                in self.player_inventory
                if c.startswith(text)
            ]
        return [c for c in self.game.name_of_monster if c.startswith(text)]

    def do_EOF(self, args):
        return True

    def emptyline(self) -> bool:
        pass


if __name__ == '__main__':
    host = "localhost"
    port = 1337
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        cli = CMD_Game(s).cmdloop()
