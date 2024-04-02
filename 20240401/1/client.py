import cmd
import shlex
import socket
import sys
import readline
import threading

import exeptions


def msg_sendreciever(client, socket):
    while response := socket.recv(1024).rstrip().decode():
        print(f"\n{response}\n{client.prompt}{readline.get_line_buffer()}", end="", flush=True)


class CMD_Game(cmd.Cmd):

    def __init__(self,
                 socket,
                 name,
                 completekey: str = "tab",
                 stdin=None,
                 stdout=None,
                 ) -> None:
        self.socket = socket
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
        self.socket.sendall(f'{orient}\n'.encode())

    def do_sayall(self, args):
        self.socket.sendall(('sayall ' + args + '\n').encode())

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

    def complete_addmon(self, text, line, begidx, endidx):
        if all(x not in line for x in ['hello', 'hp', 'coords']):
            return [c for c in self.name_of_monster if c.startswith(text)]

    def do_attack(self, args):

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
        if 'with' in line:
            return [
                c for c
                in self.player_inventory
                if c.startswith(text)
            ]
        return [c for c in self.name_of_monster if c.startswith(text)]

    def do_me(self, *args):
        self.socket.sendall('me\n'.encode())

    def do_exit(self, args):
        self.socket.sendall('drp\n'.encode())
        return True

    def do_EOF(self, args):
        self.socket.sendall('drp\n'.encode())
        return True

    def emptyline(self) -> bool:
        pass


if __name__ == '__main__':
    host = "localhost"
    port = 1337
    name = sys.argv[1]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall((name+'\n').encode())
        connect_ans = int(s.recv(1024).rstrip().decode())

        if not connect_ans:
            cli = CMD_Game(s, name)
            request = threading.Thread(target=msg_sendreciever, args=(cli, cli.socket))
            request.start()
            cli.cmdloop()
            request
        else:
            print(f'Can`t connect with {name}')
