"""Start client of net game."""

import sys
import socket
import threading

from .client import CMD_Game, msg_sendreciever


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
