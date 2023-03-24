import websockets
from gameclass import Game
import json
import asyncio


class Server:
    def __init__(self, port):
        self.port = port
        self.game = Game()
        self.connections = set()
        self.start_server = websockets.serve(self.handler, 'localhost', self.port)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.start_server)
        self.loop.create_task(self.tick())
        self.loop.run_forever()

    async def handler(self, websocket, path):
        self.connections.add(websocket)
        try:
            while True:
                data = await websocket.recv()
                data = json.loads(data)
                if data['type'] == 'expandPixels':
                    self.game.expandPixels(data['id'])
                elif data['type'] == 'registerNation':
                    self.game.registerNation(data)
        except websockets.exceptions.ConnectionClosed:
            self.connections.remove(websocket)

    async def broadcast(self, data):
        for connection in self.connections:
            await connection.send(data)

    async def tick(self):
        while True:
            await asyncio.sleep(1)
            if len(self.game.outboundData) > 0:
                for data in self.game.outboundData:
                    await self.broadcast(json.dumps(data))
                self.game.outboundData = []


if __name__ == '__main__':
    server = Server(4444)
