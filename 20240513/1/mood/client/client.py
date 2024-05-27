"""Client comand line."""

import cmd
import shlex
import readline
import sys
import socket
import threading
import time

from ..utils.exeptions import IncorectArgument


def msg_sendreciever(client, socket):
    """Print message from server to cli."""
    while response := socket.recv(2048).rstrip().decode():
        print(f"\n{response}\n{client.prompt}{readline.get_line_buffer()}", end="", flush=True)


class CMD_Game(cmd.Cmd):
    """Comand line to communikate with server."""

    def __init__(self,
                 socket,
                 name,
                 completekey: str = "tab",
                 stdin=None,
                 stdout=None,
                 ) -> None:
        """Init comand line."""
        self.socket = socket
        if not stdin:
            socket.sendall('cows\n'.encode())
            self.name_of_monster = eval(socket.recv(1024).rstrip().decode())
            socket.sendall('invent\n'.encode())
            self.player_inventory = eval(socket.recv(1024).rstrip().decode())

        self.prompt = f'MUD({name})-> '
        self.intro = (
            '<<< Welcome to Python-MUD 0.1 >>>\n'
            'Type help or ? to list commands.\n'
        )
        super().__init__(completekey, stdin, stdout)

    def print_pos(self, orient):
        """Send server signal to move player on orientatuion."""
        self.socket.sendall(f'{orient}\n'.encode())

    def do_locale(self, locale):
        """Set locale"""
        self.socket.sendall(('locale ' + locale + '\n').encode())

    def do_online(self, *args):
        self.socket.sendall('online\n'.encode())

    def do_movemonsters(self, args):
        """On/Off move monsters"""
        if args == 'on':
            self.socket.sendall(('movemonsters on\n').encode())
        elif args == 'off':
            self.socket.sendall(('movemonsters off\n').encode())
        else:
            print('Invalid argument')

    def do_sayall(self, args):
        """Use it to chat with another player."""
        self.socket.sendall(('sayall ' + args + '\n').encode())

    def do_left(self, args):
        """Move one ciels left."""
        if args:
            print('Invalid command')
            return
        self.print_pos('left')

    def do_right(self, args):
        """Move one ciels right."""
        if args:
            print('Invalid command')
            return
        self.print_pos('right')

    def do_up(self, args):
        """Move one ciels up."""
        if args:
            print('Invalid command')
            return
        self.print_pos('up')

    def do_down(self, args):
        """Move one ciels down."""
        if args:
            print('Invalid command')
            return
        self.print_pos('down')

    def do_addmon(self, args):
        """
        Add monster on map.

            addmon <name> coords <x> <y> hp <hp> hello '<hellow>'
            name: name of monster,
            x, y: int position of monster,
            hp: int count of hit point,
            hello: hellow frase.
        """
        try:
            args = shlex.split(args)
            args.insert(0, 'name')
            monster = dict()
            i = 0
            if any(x not in args for x in ['hello', 'hp', 'coords']):
                raise IncorectArgument
            while i < len(args):
                match args[i]:
                    case 'name' | 'hello':
                        monster[args[i]] = args[i + 1]
                        i += 2
                    case 'hp':
                        monster[args[i]] = int(args[i + 1])
                        i += 2
                    case 'coords':
                        monster[args[i]] = int(args[i + 1]), int(args[i + 2])
                        i += 3
                    case _:
                        raise IncorectArgument

        except IncorectArgument:
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

    def complete_addmon(self, text, line, begidx, endidx):
        """Auto complit addmon comand."""
        if all(x not in line for x in ['hello', 'hp', 'coords']):
            return [c for c in self.name_of_monster if c.startswith(text)]

    def do_attack(self, args):
        """
        Attack monster in position.

            attack <monster_name> with <weapon>
                monster_name: name of monster, witch you will attack,
                weapon: one of sword, spaer, axe
        """
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

    def complete_attack(self, text, line, begidx, endidx):
        """Auto complite attack comand."""
        if 'with' in line:
            return [
                c for c
                in self.player_inventory
                if c.startswith(text)
            ]
        return [c for c in self.name_of_monster if c.startswith(text)]

    def do_me(self, *args):
        """Print iformation of you person."""
        self.socket.sendall('me\n'.encode())

    def do_exit(self, args):
        """Exit of geme."""
        self.socket.sendall('drp\n'.encode())
        return True

    def do_EOF(self, args):
        """Write ctrl+d to close the game."""
        self.socket.sendall('drp\n'.encode())
        return True

    def emptyline(self) -> bool:
        """Nead to write empty line."""
        pass


def run_client():
    flag = False
    if sys.argv[1] == '--host_port':
        host = sys.argv[2]
        port = int(sys.argv[3])
        flag = True
    else:
        host = "localhost"
        port = 1337
    if sys.argv[1] == '--file' and not flag:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 1337))

            with open(sys.argv[2]) as file:
                name = sys.argv[2].split('.')[0]
                s.sendall((name + '\n').encode())
                connect_ans = int(s.recv(1024).rstrip().decode())

                if not connect_ans:
                    scr = CMD_Game(s, stdin=file, name=name)
                    request = threading.Thread(target=msg_sendreciever, args=(scr, scr.socket))
                    request.start()

                    scr.prompt = ''
                    scr.use_rawinput = False
                    scr.emptyline = lambda x: True
                    scr.cmdloop()
                else:
                    print(f'Can`t connect with {name}')
    elif flag and sys.argv[4] == '--file':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            with open(sys.argv[5]) as file:
                name = sys.argv[5].split('/')[-1].split('.')[0]
                s.sendall((name + '\n').encode())
                time.sleep(0.5)
                connect_ans = int(s.recv(1024).rstrip().decode())

                if not connect_ans:
                    scr = CMD_Game(s, stdin=file, name=name)
                    request = threading.Thread(target=msg_sendreciever, args=(scr, scr.socket))
                    request.start()

                    scr.prompt = ''
                    scr.use_rawinput = False
                    scr.emptyline = lambda x: True
                    scr.cmdloop()
                    time.sleep(1)
                else:
                    print(f'Can`t connect with {name}')
    else:
        if flag:
            name = sys.argv[4]
        else:
            name = sys.argv[1]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall((name + '\n').encode())
            connect_ans = int(s.recv(1024).rstrip().decode())

            if not connect_ans:
                cli = CMD_Game(s, name)
                request = threading.Thread(target=msg_sendreciever, args=(cli, cli.socket))
                request.start()
                cli.cmdloop()
            else:
                print(f'Can`t connect with {name}')
