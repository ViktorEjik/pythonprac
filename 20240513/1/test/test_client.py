import unittest
from unittest.mock import MagicMock
import shlex
import cowsay
import threading
import time
import io

from mood.utils.entity import Monster, Sword, Spear, Axe
from mood.client import CMD_Game
from mood.utils import exeptions 

res = []

MAP_LENGTH = 10

orient = {
        'left': (-1, 0),
        'right': (1, 0),
        'up': (0, -1),
        'down': (0, 1)
    }

custom_monster = cowsay.read_dot_cow(io.StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""))

addmon_errors = {
    '1' : 'Invalid arguments (count of elements)',
    '2' : 'Invalid arguments (type of name)',
    '3' : 'Cannot add unknown monster',
    '4' : 'Invalid arguments (type of message)',
    '5' : 'Invalid arguments (type of hp)',
    '6' : 'Invalid arguments (value of hp)',
    '7' : 'Invalid arguments (type of coord x)',
    '8' : 'Invalid arguments (value of coord x)',
    '9' : 'Invalid arguments (type of coord y',
    '10': 'Invalid arguments (value of coord y)'
}

inventory = {
        'sword': Sword(),
        'axe': Axe(),
        'spear': Spear()
    }

class MyMock(MagicMock):
    def key(self, position):
        return position[1] * self.field_size + position[0]

    def move(self, orientation):
        response = []

        self.position = (
            (self.position[0] + orient[orientation][0]) % MAP_LENGTH,
            (self.position[1] + orient[orientation][1]) % MAP_LENGTH
        )

        response.append(f'Moved to {self.position[0], self.position[1]}')
        if self.monsters.get(self.position, None) is not None:
            result = str(self.monsters[self.position])
            if result[0] == 'jgsbat':
                response.append(cowsay.cowsay(result[1], cowfile=custom_monster))
            else:
                response.append(result)

        return '\n'.join(response)

    def addmon(self, args):
        response = []
        args = shlex.split(args)
        if len(args) != 5:
            return addmon_errors['1']

        elif not isinstance(args[0], str): # name
            return addmon_errors['2']
        elif args[0] not in cowsay.list_cows() \
                and args[0] != 'jgsbat':
            print('~3~')
            return addmon_errors['3']

        elif not args[4].isdigit(): # hp
            return addmon_errors['5']
        elif int(args[4]) <= 0:
            return addmon_errors['6'] 
        
        elif not args[1].isdigit(): # x
            return addmon_errors['7']
        elif int(args[1]) < 0 \
                or int(args[1]) >= MAP_LENGTH:
            return addmon_errors['8']
        
        elif not args[2].isdigit(): # y
            return addmon_errors['9']
        elif int(args[2]) < 0 \
                or int(args[2]) >= MAP_LENGTH:
            return addmon_errors['10']
        
        elif not isinstance(args[3], str): # message
            return addmon_errors['4']
        
        response.append(f'Added monster {args[0]} with {args[4]} hp')

        key = (int(args[1]), int(args[2]))
        if self.monsters.get(key, None) is not None:
            del self.monsters[key]
            response.append("Replaced the old monster")

        self.monsters[key] = Monster(
            args[0],
            args[3],
            int(args[4]),
        )

        return '\n'.join(response)

    def attack(self, args):
        response = []
        key = self.position
        name, wepon = shlex.split(args)

        if self.monsters.get(key, None) is None \
                or self.monsters[key].name != name:
            
            return f'No {name} here'
        wepon = inventory[wepon].damage
        mon = self.monsters[key]
        dmg = mon.healing(wepon)
        
        response.append(f'Attacked {name}, damage {dmg} hp')

        if not mon:
            response.append(f'{name} died')
            del self.monsters[key]
        else:
            response.append(f'{name} now has {mon.hp} hp')

        return '\n'.join(response)

    def sendall(self, s):
        global res
        match com := shlex.split(s.decode()):
            case ['addmon', *args]:
                res.append(self.addmon(shlex.join(args)))
            case [
                'up' | 'down' | 'right' | 'left'
                ]:
                res.append(self.move(com[0]))
            case ['attack', *args]:
                res.append(self.attack(shlex.join(args)))
            case _:
                pass

         
class TestClient(unittest.TestCase):

    def setUp(self):
        self.mocker = MyMock()

    def test_mocker_moving(self):
        global res
        res = []
        self.mocker = MyMock()
        self.mocker.position = (0, 0)
        self.mocker.monsters = {}

        with open("./test/in/test_mocker_moving.mood") as file:
            
            scr = CMD_Game(self.mocker, 'name', stdin=file, test_mode=True)
            scr.prompt = ''
            scr.use_rawinput = False
            scr.cmdloop()

        self.assertEqual(len(res), 4)
        self.assertEqual(res, ['Moved to (0, 9)', 'Moved to (0, 0)', 'Moved to (9, 0)', 'Moved to (0, 0)'])
        res = []

    def test_mocker_addmon(self):
        global res
        res = []
        self.mocker = MyMock()
        self.mocker.position = (0, 0)
        self.mocker.field_size = 10
        self.mocker.monsters = {}
        
        with open("./test/in/test_mocker_addmon.mood") as file:
            scr = CMD_Game(self.mocker, 'test', stdin=file, test_mode=True)
            scr.prompt = ''
            scr.use_rawinput = False
            scr.cmdloop()
        
        self.assertEqual(len(res), 3)
        with open('./test/add_monster.test', 'r') as f:
            ans = f.read()
        with open('./test/tmp', 'w+') as f:
            f.write(res[-1])
        self.assertEqual(res,
            [
                'Added monster default with 19 hp',
                'Added monster default with 19 hp\nReplaced the old monster',
                ans,
            ]
        )
        res = []

    def test_mocker_attack(self):
        global res
        self.mocker = MyMock()
        self.mocker.position = (0, 0)
        self.mocker.field_size = 10
        self.mocker.monsters = {}

        with open("./test/in/test_mocker_attack.mood") as file:
            scr = CMD_Game(self.mocker, 'test', stdin=file, test_mode=True)
            scr.prompt = ''
            scr.use_rawinput = False
            scr.cmdloop()
        
        self.assertEqual(len(res), 4)
        self.assertEqual(res,
            [
                'Added monster default with 19 hp',
                'Attacked default, damage 15 hp\ndefault now has 4 hp',
                'Attacked default, damage 4 hp\ndefault died',
                'No default here'
            ])
        res = []
