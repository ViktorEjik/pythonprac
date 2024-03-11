import exeptions
from entity import Player
from logic import Game, Map


def main():
    game = Game(Map(), Player())
    print('<<< Welcome to Python-MUD 0.1 >>>')
    while comand := input('>>'):
        comand = comand.split()
        match comand:
            case ['left' | 'right' | 'up' | 'down']:
                res = game.go_to(comand[0])
                print(f'Moved to ({res[0][0]}, {res[0][1]})')
                if res[1]:
                    print(res[1])

            case ['addmon', *other]:
                i = 1
                tmp = dict()
                tmp['name'] = other[0]
                if len(other) < 8:
                    print('Invalid arguments', other)
                    continue
                try:
                    while i < len(other):
                            match other[i]:
                                case 'hello':
                                    hello = list()
                                    i += 1
                                    while i < len(other):
                                        if other[i] not in ['hello', 'hp', 'coords']:
                                            hello.append(other[i])
                                            i += 1
                                        else:
                                            break
                                    tmp['hello'] = ' '.join(hello)[1:-1]
                                case 'hp':
                                    tmp['hp'] = int(other[i+1])
                                    i += 2
                                case 'coords':
                                    tmp['coords'] = (int(other[i+1]), int(other[i+2]))
                                    i += 3
                                case _:
                                    print('Invalid command')
                                    raise exeptions.IncorectArgument
                except ValueError| IndexError:
                    print('Invalid arguments')
                    continue
                except exeptions.IncorectArgument:
                    continue

                ans = f'Added monster {tmp["name"]} to {tmp["coords"]} saying {tmp["hello"]}'
                try:
                    game.addmon(tmp['coords'], tmp["name"], tmp['hello'], tmp['hp'])
                except exeptions.UnknownMonster:
                    print('Cannot add unknown monster')
                    continue
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
