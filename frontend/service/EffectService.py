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
        self.bigBoom = [
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_01.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_02.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_03.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_04.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_05.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_06.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_07.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_08.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_09.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_10.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_11.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_12.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_13.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_14.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_15.png"),
            self.pg.image.load("../frontend/assets/nuke/Layer 1_sprite_16.png"),

        ]

        self.scoreFont = self.pg.font.Font('freesansbold.ttf', 32)
        self.score = 0
        self.scoreText = self.scoreFont.render("Score : " + str(self.score), False, (0, 0, 0))

    def addBoom(self, x, y, boomType):
        self.booms.append({
            'x': x,
            'y': y,
            'type': boomType,
            'frameIndex': 0,
            'duration': 0
        })

    def incrementScore(self):
        self.score += 1
        self.scoreText = self.scoreFont.render("Score : " + str(self.score), False, (0, 0, 0))

    def draw(self):
        width = self.win.get_size()[0]
        self.win.blit(self.scoreText, (width / 2, 20))

        for boom in self.booms:
            frame = boom['frameIndex']
            duration = boom['duration']
            boomList = self.smallBoom if boom['type'] == 'small' else self.bigBoom
            if frame >= len(boomList):
                # No more explosion frame to play. This explosion is complete
                self.booms.remove(boom)
                continue

            self.win.blit(boomList[frame], (boom['x'], boom['y']))  # Drawing
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
                "duration": duration,
                'type': boom['type']
            }
