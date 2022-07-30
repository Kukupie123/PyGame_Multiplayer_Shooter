# noinspection PyRedundantParentheses,PyTypeChecker
class EffectService:
    def __init__(self, pg, win):
        self.pg = pg
        self.win = win

        self.boomFrameDuration = 12
        self.booms = []  # [ {x,y}]
        self.smallBoom = [
            self.pg.image.load("../frontend/assets/effects/explosion/bom00.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom01.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom02.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom03.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom04.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom05.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom06.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom07.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom08.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom09.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom10.png"),
            self.pg.image.load("../frontend/assets/effects/explosion/bom11.png"),
        ]

    def addBoom(self, x, y, boomType):
        self.booms.append({
            'x': x,
            'y': y,
            'type': boomType,
            'frameIndex': 0,
            'duration': 0
        })

    def __drawBoom(self, boom):
        if boom is None:
            print("boom is none")
        frame = boom['frameIndex']
        duration = 0
        while True:
            if frame >= len(self.smallBoom):
                break
        self.win.blit(self.smallBoom[frame], (boom['x'], boom['y']))
        duration += 1
        if duration > self.boomFrameDuration:  # If we have drawn this frame for FrameDuration amount of time
            frame += 1  # We will play the next frame
            print(f"Playing next frame {frame}")
        # Update the element, since we are running in multi thread ENV we need to make sure we are updating the correct element as they can change mid loop by other function calls

    def draw(self):
        for boom in self.booms:
            frame = boom['frameIndex']
            duration = boom['duration']

            if frame >= len(self.smallBoom):
                # No more explosion frame to play. This explosion is complete
                self.booms.remove(boom)

            else:
                self.win.blit(self.smallBoom[frame], (boom['x'], boom['y']))  # Drawing
                duration += 1  # increment duration after drawing
                if duration > self.boomFrameDuration:
                    # If we have played a frame enough we increment the frame
                    frame += 1
                    duration = 0
                index = self.booms.index(boom)
                self.booms[index] = {
                    "x": boom['x'],
                    "y": boom['y'],
                    "frameIndex": frame,
                    "duration": duration
                }
