"""Start game server."""

import asyncio
import sys

from .server import Server


async def main():
    """Start game server."""
    args = sys.argv
    test = False
    t_sleep_monst = 30
    if '--test' not in args:
        test = True
    if '--t_sleep' in args:
        ix = args.index('--t_sleep')
        t_sleep_monst = int(args[ix + 1])
    server = await asyncio.start_server(Server(test, t_sleep_monst).new_client(), '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
