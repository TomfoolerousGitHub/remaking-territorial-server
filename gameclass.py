class Game:
    def __init__(self):
        self.nations = {}
        self.canvasWidth = 1000
        self.canvasHeight = 1000
        self.outboundData = []

    def registerNation(self, nation: dict):
        for interaction in self.outboundData:
            if interaction['type'] == 'registerNation':
                if interaction['id'] == nation['id']:
                    return
        self.nations[nation['id']] = {}
        self.nations[nation['id']]['color'] = nation['color']
        self.nations[nation['id']]['borderColor'] = nation['borderColor']
        self.nations[nation['id']]['pixelsOwned'] = set()
        self.nations[nation['id']]['borderPixels'] = set()
        self.nations[nation['id']]['Money'] = 540
        x = nation['x']
        y = nation['y']
        pixelsOwned = [[x, y], [x + 4, y], [x, y + 4], [x + 4, y + 4], [x - 4, y], [x, y - 4], [x + 8, y], [x, y + 8], [x - 4, y + 4], [x + 4, y - 4], [x + 4, y + 8], [x + 8, y + 4]]
        for pixel in pixelsOwned:
            self.nations[nation['id']]['pixelsOwned'].add(tuple(pixel))
        borderPixels = [[x - 4, y], [x, y - 4], [x + 8, y], [x, y + 8], [x - 4, y + 4], [x + 4, y - 4], [x + 4, y + 8], [x + 8, y + 4]]
        for pixel in borderPixels:
            self.nations[nation['id']]['borderPixels'].add(tuple(pixel))
        outboundData = {
            "type": "registerNation",
            "id": nation['id'],
            "color": self.nations[nation['id']]['color'],
            "borderColor": self.nations[nation['id']]['borderColor'],
            "x": nation['x'],
            "y": nation['y']
        }
        self.outboundData.append(outboundData)

    def expandPixels(self, id: str):
        for interaction in self.outboundData:
            if interaction['type'] == 'expandPixels':
                try:
                    if interaction['nation'] == id:
                        return
                except KeyError:
                    continue
        previousState = dict(self.nations[id])
        pixelsToOccupy = set()
        for pixel in self.nations[id]['borderPixels']:
            for neighbor in [[pixel[0] + 4, pixel[1]], [pixel[0] - 4, pixel[1]], [pixel[0], pixel[1] + 4], [pixel[0], pixel[1] - 4]]:
                if not (neighbor[0] < 0 or neighbor[0] > self.canvasWidth or neighbor[1] < 0 or neighbor[1] > self.canvasHeight):
                    if self.nations[id]['pixelsOwned'].isdisjoint({tuple(neighbor)}):
                        pixelsToOccupy.add(tuple(neighbor))
                    else:
                        continue
                else:
                    continue
        pixelsToOccupy2 = pixelsToOccupy.copy()
        for pixel in pixelsToOccupy2:
            for nation in self.nations:
                if nation == id:
                    continue
                elif pixel in self.nations[nation]['pixelsOwned']:
                    pixelsToOccupy.remove(pixel)
                    continue
        self.nations[id]['pixelsOwned'] = self.nations[id]['pixelsOwned'].union(pixelsToOccupy)
        noLongerBorderPixels = set()
        newBorderPixels = set()
        for pixel in self.nations[id]['borderPixels']:
            noLongerBorderPixels.add(pixel)
        for pixel in pixelsToOccupy:
            newBorderPixels.add(pixel)
        for pixel in self.nations[id]['pixelsOwned']:
            for neighbor in [[pixel[0] + 4, pixel[1]], [pixel[0] - 4, pixel[1]], [pixel[0], pixel[1] + 4], [pixel[0], pixel[1] - 4]]:
                if not (neighbor[0] < 0 or neighbor[0] > self.canvasWidth or neighbor[1] < 0 or neighbor[1] > self.canvasHeight):
                    for nation in self.nations:
                        if nation == id:
                            continue
                        elif tuple(neighbor) in self.nations[nation]['pixelsOwned']:
                            newBorderPixels.add(pixel)
                            try:
                                noLongerBorderPixels.remove(pixel)
                            except:
                                continue
                            continue
                        else:
                            continue
                else:
                    newBorderPixels.add(pixel)
                    try:
                        noLongerBorderPixels.remove(pixel)
                    except:
                        continue
        if len(pixelsToOccupy) * 2 > self.nations[id]['Money']:
            self.nations[id] = previousState
            return
        elif len(pixelsToOccupy) == 0:
            self.nations[id] = previousState
            return
        self.nations[id]['Money'] -= len(pixelsToOccupy) * 2
        self.nations[id]['borderPixels'] = newBorderPixels
        outboundData = {
            'type': 'expandPixels',
            'nation': id,
            'pixelsToOccupy': list(pixelsToOccupy),
            'newBorderPixels': list(newBorderPixels),
            'noLongerBorderPixels': list(noLongerBorderPixels),
            'money': self.nations[id]['Money']
        }
        self.outboundData.append(outboundData)

    def sendOutboundData(self):
        outboundData = self.outboundData
        self.outboundData = []
        return outboundData

    def addMoney(self, tick: int):
        if tick == 10:
            for nation in self.nations:
                self.nations[nation]['Money'] += self.nations[nation]['pixelsOwned'].__len__()
        else:
            for nation in self.nations:
                self.nations[nation]['Money'] += self.nations[nation]['Money'] * 0.05
