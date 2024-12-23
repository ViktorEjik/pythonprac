import exeptions
from entity import Player
from logic import Game, Map


def main():
    game = Game(Map(), Player())

    while comand := input():
        comand = comand.split()
        match comand:
            case ['left' | 'right' | 'up' | 'down']:
                res = game.go_to(comand[0])
                print(f'Moved to ({res[0][0]}, {res[0][1]})')
                if res[1]:
                    print(res[1])

            case ['addmon', x, y, hello]:

                try:
                    x, y = int(x), int(y)
                except Exception:
                    print('Invalid arguments')
                    continue

                ans = f'Added monster to ({x}, {y}) saying {hello}'
                try:
                    game.addmon((x, y), hello)
                except exeptions.ReplaseMonster:
                    ans += '\nReplaced the old monster'
                except exeptions.IncorectArgument:
                    print('Invalid arguments')
                    continue
                print(ans)

            case _:
                print('Invalid command')


if __name__ == '__main__':
    main()
