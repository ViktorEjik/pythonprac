import asyncio
import shlex

from logic import Game, Map, Player
import exeptions


class Server:
    def __init__(self) -> None:
        self.game = Game(Map(), Player())

    async def _client(self, reader, writer):
        name = reader.readline().decode()
        while data := await reader.readline():
            comand = shlex.split(data.decode())
            match comand:
                case ['cows']:
                    writer.write(str(self.game.name_of_monster).encode())

                case ['invent']:
                    writer.write(
                        str(list(self.game.player.inventory.keys())).encode())

                case ['left' | 'right' | 'up' | 'down']:
                    res = self.game.go_to(comand[0])
                    ans = f'{res[0][0]}, {res[0][1]}'
                    if res[1]:
                        ans += '\\' + res[1] + ' ' + '"' + res[2] + '"'
                    writer.write((ans+'\n').encode())

                case ['addmon', *args]:
                    ans = '0'

                    try:
                        self.game.addmon(
                            (int(args[1]), int(args[2])), args[0],
                            args[3], int(args[4])
                        )
                    except exeptions.UnknownMonster:
                        ans = '2'
                    except exeptions.ReplaseMonster:
                        ans = '1'
                    writer.write(ans.encode())

                case ['attack', *args]:
                    name, weapon = args[0], args[1]
                    try:
                        dmg = self.game.attack(name=name, weapon=weapon)

                    except exeptions.MonsterRIP as err:
                        writer.write(
                            f'1 {err.dmg}'.encode())
                        continue
                    except exeptions.NOMonster:
                        writer.write('2'.encode())
                        continue
                    except exeptions.NONamedMonster:
                        writer.write('3'.encode())
                        continue
                    except exeptions.NOWepon:
                        writer.write('4'.encode())
                        continue

                    writer.write(f'0 {dmg[0]} {dmg[2]}'.encode())

        writer.close()
        await writer.wait_closed()

    def new_client(self):
        return self._client


async def main():
    server = await asyncio.start_server(Server().new_client(), '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
