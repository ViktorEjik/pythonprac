"""Start game server."""

import asyncio
import sys

from .server import Server


async def main():
    """Start game server."""
    args = sys.argv
    move_on = False
    t_sleep_monst = 30
    if '--move_on' in args:
        move_on = True
    if '--t_sleep' in args:
        ix = args.index('--t_sleep')
        t_sleep_monst = int(args[ix + 1])
    
    server = await asyncio.start_server(Server(move_on, t_sleep_monst).new_client(), '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
