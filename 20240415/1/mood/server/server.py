"""Contain all neadet classes to network game."""

import asyncio
import shlex

from ..utils.logic import Game, Map, Player
from ..utils import exeptions


class Server:
    """A class that stores information about the game session and manages game processes."""

    def __init__(self, wandering_monster=False, t_sleep_mon=30) -> None:
        """Init game."""
        self.game = Game(Map(), Player('adm'), t_sleep_mon)
        self.clients = dict()
        self.wandering_monster = None
        if wandering_monster:
            self.wandering_monster = asyncio.create_task(
                self.game.wandering_monster(self.clients)
            )

    async def _client(self, reader, writer):
        """Client's request handler."""
        name = (await reader.readline()).decode().rstrip()

        try:
            me = self.game.add_new_player(name)
        except exeptions.PlayerExist:

            writer.write('1'.encode())
            writer.close()
            await writer.wait_closed()
            return

        self.clients[me] = asyncio.Queue()

        send = asyncio.create_task(reader.readline())
        receive = asyncio.create_task(self.clients[me].get())

        for el in self.clients.values():
            if el is not self.clients[me]:
                await el.put(f"User {me.name} connected")

        print('connect!', name)
        writer.write('0'.encode())

        while not reader.at_eof():
            done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

            for q in done:
                if q is send:
                    send = asyncio.create_task(reader.readline())
                    data = q.result().decode().strip()

                    comand = shlex.split(data)
                    match comand:
                        case ['movemonsters', state]:
                            if state == 'on':
                                if (
                                    self.wandering_monster is None
                                    or self.wandering_monster.cancelled()
                                    or self.wandering_monster.done()
                                ):
                                    self.wandering_monster = asyncio.create_task(
                                        self.game.wandering_monster(
                                            self.clients
                                        )
                                    )
                            else:
                                self.wandering_monster.cancel()

                            for el in self.clients.values():
                                await el.put('Moving monsters: ' + state)

                        case['sayall', *message]:
                            for el in self.clients.values():
                                if el is not self.clients[me]:
                                    await el.put(f'({me.name}): ' + ' '.join(message))

                        case ['me']:
                            await self.clients[me].put(str(me))

                        case ['cows']:
                            await self.clients[me].put(str(self.game.name_of_monster))

                        case ['invent']:
                            await self.clients[me].put(str(list(me.inventory.keys())))

                        case ['left' | 'right' | 'up' | 'down']:
                            res = self.game.go_to(comand[0], me)
                            ans = f'Move to {res[0]}'
                            if res[1]:
                                ans += '\n' + res[1]
                            await self.clients[me].put(str((ans+'\n')))

                        case ['addmon', *args]:
                            ans = (
                                    f'Added monster {args[0]} to '
                                    f'{(int(args[1]), int(args[2]))} saying "{args[3]}"'
                                )

                            try:
                                self.game.addmon(
                                    (int(args[1]), int(args[2])), args[0],
                                    args[3], int(args[4])
                                )
                            except exeptions.UnknownMonster:
                                ans = 'Cannot add unknown monster'
                                continue
                            except exeptions.ReplaseMonster:
                                ans += '\nReplaced the old monster'
                            await self.clients[me].put(ans)

                            for el in self.clients.values():
                                if el is not self.clients[me]:
                                    await el.put(f'User {me.name} added monster {args[0]} with {args[4]} hp')

                        case ['attack', *args]:
                            res = 'Attacked {name}, damage {dmg} hp'

                            name, weapon = args[0], args[1]
                            try:
                                dmg = self.game.attack(player=me, name=name, weapon=weapon)

                            except exeptions.MonsterRIP as err:
                                await self.clients[me].put(
                                    res.format(name=err.name, dmg=err.dmg) + f'\n{err.name} died'
                                )
                                for el in self.clients.values():
                                    if el is not self.clients[me]:
                                        await el.put(
                                            f'User {me.name} attacked monster {err.name} with {weapon},'
                                            + f' damage {err.dmg} hp'
                                            + f'\n{name} died'
                                        )

                                continue
                            except exeptions.NOMonster:
                                await self.clients[me].put('No monster here')
                                continue
                            except exeptions.NONamedMonster:
                                await self.clients[me].put(f'No {name} here')
                                continue
                            except exeptions.NOWepon:
                                await self.clients[me].put('Unknown weapon')
                                continue
                            await self.clients[me].put(
                                res.format(name=name, dmg=dmg[0]) + f'\n{name} now has {dmg[2]} hp'
                            )

                            for el in self.clients.values():
                                if el is not self.clients[me]:
                                    await el.put(
                                        f"User {me.name} attacked monster {name} with {weapon}, damage {dmg[0]} hp"
                                        + (f"\n{name} now has {dmg[2]} hp")
                                    )

                        case ['drp']:
                            self.game.del_player(me)
                            del self.clients[me]
                            for el in self.clients.values():
                                await el.put(f'{me.name} disconnected')
                            me = None
                            break

                elif q is receive:
                    receive = asyncio.create_task(self.clients[me].get())
                    writer.write(f"{q.result()}\n".encode())
                    await writer.drain()

        send.cancel()
        receive.cancel()
        if me:
            self.game.del_player(me)
            del self.clients[me]
            for el in self.clients.values():
                await el.put(f'{me.name} disconnected')

        writer.close()
        await writer.wait_closed()

    def new_client(self):
        """Return the client's request handler."""
        return self._client
