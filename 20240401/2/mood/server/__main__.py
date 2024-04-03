"""Start game server."""

import asyncio

from .server import Server


async def main():
    """Start game server."""
    server = await asyncio.start_server(Server().new_client(), '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
