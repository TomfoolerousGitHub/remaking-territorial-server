import websockets
import asyncio
from gameclass import Game
import json


class Server:
    def __init__(self, port):
        self.port = port
        self.game = Game()
        self.connections = set()
        self.start_server = websockets.serve(self.handler, 'localhost', self.port)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.start_server)
        self.loop.run_forever()

    async def handler(self, websocket, path):
        self.connections.add(websocket)
        try:
            while True:
                data = await websocket.recv()
                data = json.loads(data)
                if data['type'] == 'expandPixels':
                    pixelsToOccupy, newBorderPixels, noLongerBorderPixels = self.game.expandPixels(data['id'])
                    outboundData = {
                        'type': 'expandPixels',
                        'nation': data['id'],
                        'pixelsToOccupy': list(pixelsToOccupy),
                        'newBorderPixels': list(newBorderPixels),
                        'noLongerBorderPixels': list(noLongerBorderPixels)
                    }
                    await self.broadcast(json.dumps(outboundData))
                elif data['type'] == 'registerNation':
                    outboundData = self.game.registerNation(data)
                    await self.broadcast(json.dumps(outboundData))
        except websockets.exceptions.ConnectionClosed:
            self.connections.remove(websocket)

    async def broadcast(self, data):
        for connection in self.connections:
            await connection.send(data)


if __name__ == '__main__':
    server = Server(4444)
