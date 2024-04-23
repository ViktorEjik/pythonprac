import unittest
import socket
import multiprocessing
import time

from mood.server.server import start
from mood.client import CMD_Game


class TestRoot(unittest.TestCase):

    def test_creating_monster(self):
        proc = multiprocessing.Process(target=start)
        proc.start()
        time.sleep(1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 1337))
            s.sendall(('test\n').encode())
            connect_ans = int(s.recv(1024).rstrip().decode())
            tst = CMD_Game(s, 'test')
            tst.prompt = ''

            tst.do_addmon("milk coords 0 0 hp 19 hello 'U'")
            expected_response = 'Added monster milk to (0, 0) saying "U"'
            self.assertEqual(s.recv(1024).rstrip().decode(), expected_response)

        proc.terminate()

    def test_move_to_monster(self):
        proc = multiprocessing.Process(target=start)
        proc.start()
        time.sleep(1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 1337))
            s.sendall(('test\n').encode())
            connect_ans = int(s.recv(1024).rstrip().decode())
            tst = CMD_Game(s, 'test')
            tst.prompt = ''

            tst.do_addmon("default coords 1 0 hp 19 hello 'u'")
            response = s.recv(1024).rstrip().decode()
            tst.do_right('')

            with open('./test/move_monster.test', 'r') as f:
                expected_response = f.read()
            self.assertEqual(s.recv(1024).rstrip().decode(), expected_response)

        proc.terminate()

    def test_attack_monster(self):
        proc = multiprocessing.Process(target=start)
        proc.start()
        time.sleep(1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 1337))
            s.sendall(('test\n').encode())
            connect_ans = int(s.recv(1024).rstrip().decode())
            tst = CMD_Game(s, 'test')
            tst.do_addmon("milk coords 0 0 hp 19 hello 'U'")
            response = s.recv(1024).rstrip().decode()

            tst.do_attack("milk with spear")
            response = s.recv(1024).rstrip().decode()
            expected_response = 'Attacked milk, damage 15 hps\nmilk now has 4 hps'
            self.assertEqual(response, expected_response)

        proc.terminate()