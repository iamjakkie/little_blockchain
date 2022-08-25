import asyncio

async def handle_connection(reader, writer):
    writer.write("Hello, type something...\n".encode())

    data = await reader.readuntil(b'\n')

    writer.write('Your message: '.encode() + data)
    await writer.drain()

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_connection, '0.0.0.0', 8889)

    async with server:
        await server.serve_forever()

asyncio.run(main())