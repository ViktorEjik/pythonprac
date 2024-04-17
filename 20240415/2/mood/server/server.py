"""Contain all neadet classes to network game."""

import asyncio
import shlex
import gettext
import os

from ..utils.logic import Game, Map, Player
from ..utils import exeptions

root_path = os.path.dirname(__file__).find("server")
_path = os.path.join(os.path.dirname(__file__)[:root_path], "po")

LOCALES = {
    ("ru_RU"): gettext.translation("server", _path, ["ru"]),
    ("en_US"): gettext.NullTranslations(),
}

def _(text, locale):
    print('_', text)
    return LOCALES[locale].gettext(text)

def ngettext(*args, locale):
    return LOCALES[locale].ngettext(*args)

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
            me = self.game.add_new_player(name, locale='en_US')
        except exeptions.PlayerExist:

            writer.write('1'.encode())
            writer.close()
            await writer.wait_closed()
            return

        self.clients[me] = asyncio.Queue()

        send = asyncio.create_task(reader.readline())
        receive = asyncio.create_task(self.clients[me].get())
        me.locale = 'en_US'
        for obj, el in self.clients.items():
            if el is not self.clients[me]:
                await el.put(_('User {} connected', locale=obj.locale).format(me.name))

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
                        case ['locale', args]:
                            if args == 'ru':
                                me.locale = 'ru_RU'
                            elif args == 'en':
                                me.locale = 'en_US'
                            await self.clients[me].put('Locale: ' + me.locale)

                        case['online']:
                            await self.clients[me].put(', '.join(self.game.pl_list))

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

                            for obj, qeue in self.clients.items():
                                await qeue.put(_('Moving monsters: ', locale=obj.locale) + state)

                        case['sayall', *message]:
                            for el in self.clients.values():
                                if el is not self.clients[me]:
                                    await el.put(f"({me.name}): " + ' '.join(message))

                        case ['me']:
                            await self.clients[me].put(str(me))

                        case ['cows']:
                            await self.clients[me].put(str(self.game.name_of_monster))

                        case ['invent']:
                            await self.clients[me].put(str(list(me.inventory.keys())))

                        case ['left' | 'right' | 'up' | 'down']:
                            
                            res = self.game.go_to(comand[0], me)
                            ans = _('Move to {}', locale=me.locale).format(res[0])
                            if res[1]:
                                ans += '\n' + res[1]
                            await self.clients[me].put(str((ans+'\n')))

                        case ['addmon', *args]:
                            ans = (
                                    _('Added monster {} to ', locale=me.locale).format(args[0])
                                    + '({}, {}) '.format(int(args[1]), int(args[2]))
                                    + _('saying "{}"', locale=me.locale).format(args[3])
                                )

                            try:
                                self.game.addmon(
                                    (int(args[1]), int(args[2])), args[0],
                                    args[3], int(args[4])
                                )
                            except exeptions.UnknownMonster:
                                ans = _('Cannot add unknown monster', locale=me.locale)
                                continue
                            except exeptions.ReplaseMonster:
                                ans += _('\nReplaced the old monster', locale=me.locale)
                            await self.clients[me].put(ans)

                            for obj, el in self.clients.items():
                                if el is not self.clients[me]:
                                    await el.put(
                                        _('User {} ', locale=obj.locale).format(me.name)
                                        + _('added monster {} ', locale=obj.locale).format(args[0])
                                        + ngettext(
                                            'with {} hp', 'with {} hps',
                                            int(args[4]), locale=obj.locale
                                        ).format(args[4])
                                    )

                        case ['attack', *args]:
                            res = (
                                'Attacked {name}, damage {dmg} hp',
                                'Attacked {name}, damage {dmg} hps'
                            )

                            name, weapon = args[0], args[1]
                            try:
                                dmg = self.game.attack(player=me, name=name, weapon=weapon)

                            except exeptions.MonsterRIP as err:
                                await self.clients[me].put(
                                    ngettext(
                                        *res,
                                        err.dmg, locale=me.locale
                                    ).format(name=err.name, dmg=err.dmg)
                                    + _('\n{} died', locale=me.locale).format(err.name)
                                )
                                for obj, el in self.clients.items():
                                    if el is not self.clients[me]:
                                        await el.put(
                                            _('User {} ', locale=obj.locale).format(me.name)
                                            + _('attacked monster {} ', locale=obj.locale).format(err.name)
                                            + _('with {}, ', locale=obj.locale).format(weapon)
                                            + ngettext(
                                                'damage {} hp', 'damage {} hps',
                                                err.dmg, locale=obj.locale
                                            ).format(err.dmg)
                                            + _('\n{} died', locale=obj.locale).format(name)
                                        )

                                continue
                            except exeptions.NOMonster:
                                await self.clients[me].put(_('No monster here', locale=me.locale))
                                continue
                            except exeptions.NONamedMonster:
                                await self.clients[me].put(_('No {} here', locale=me.locale).format(name))
                                continue
                            except exeptions.NOWepon:
                                await self.clients[me].put(_('Unknown weapon', locale=me.locale))
                                continue
                            await self.clients[me].put(
                                ngettext(
                                        *res,
                                        dmg[0], locale=me.locale
                                    ).format(name=name, dmg=dmg[0])
                                + ngettext(
                                    '\n{} now has {} hp', '\n{} now has {} hps',
                                    dmg[2], locale=me.locale
                                ).format(name, dmg[2])
                            )

                            for obj, el in self.clients.items():
                                if el is not self.clients[me]:
                                    await el.put(
                                        _('User {} ', locale=obj.locale).format(me.name)
                                        + _('attacked monster {} ', locale=obj.locale).format(name)
                                        + _('with {}, ', locale=obj.locale).format(weapon)
                                        + ngettext(
                                            'damage {} hp', 'damage {} hps',
                                            dmg[0], locale=obj.locale
                                        ).format(dmg[0])
                                        + ngettext(
                                            '\n{} now has {} hp', '\n{} now has {} hps',
                                            dmg[2], locale=obj.locale
                                        ).format(name, dmg[2])
                                    )

                        case ['drp']:
                            self.game.del_player(me)
                            del self.clients[me]
                            for obj, el in self.clients.items():
                                await el.put(_('{} disconnected', locale=obj.locale).format(me.name))
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
            for obj, el in self.clients.items():
                await el.put(_('{} disconnected', locale=obj.locale).format(me.name))

        writer.close()
        await writer.wait_closed()

    def new_client(self):
        """Return the client's request handler."""
        return self._client
