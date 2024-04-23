"""Start client of net game."""

import sys
import socket
import threading

from .client import CMD_Game, msg_sendreciever


if sys.argv[1] == '--file':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 1337))

        with open(sys.argv[2]) as file:
            name = sys.argv[2].split('.')[0]
            s.sendall((name+'\n').encode())
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

else:
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
