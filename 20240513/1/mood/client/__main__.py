"""Start client of net game."""

import sys
import socket
import threading
import time

from .client import CMD_Game, msg_sendreciever

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
elif flag and sys.argv[4] == '--file':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        with open(sys.argv[5]) as file:
            name = sys.argv[5].split('/')[-1].split('.')[0]
            s.sendall((name+'\n').encode())
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
        s.sendall((name+'\n').encode())
        connect_ans = int(s.recv(1024).rstrip().decode())

        if not connect_ans:
            cli = CMD_Game(s, name)
            request = threading.Thread(target=msg_sendreciever, args=(cli, cli.socket))
            request.start()
            cli.cmdloop()
        else:
            print(f'Can`t connect with {name}')
