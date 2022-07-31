# noinspection PyMethodMayBeStatic


# noinspection PyMethodMayBeStatic,DuplicatedCode
class CharacterBase:
    def __init__(self,
                 frameDict, speed, piegae, window):

        """
        When creating a characters you need to supply all the necessary frames
        :param frameDict: Dictionary of your Character state images named appropriately as idle,top,down,left,right (Type must be of pygame.SurfaceType)
        :param speed: speed of the characters movement
        """

        # Image dictionary setup with the necessary image
        if frameDict is not None:
            self.frame = {
                "idle": frameDict['idle'],
                "top": frameDict['top'],
                "down": frameDict['down'],
                "left": frameDict['left'],
                "right": frameDict['right']
            }
        self.pg = piegae
        self.window = window
        # Setup Additional Data
        self.speed = speed  # Speed of player
        self.posX = (self.window.get_size()[0]) / 2
        self.posY = (self.window.get_size()[1]) / 2
        self.lastX = 0
        self.lastY = 0
        if frameDict is not None:
            self.currentFrame = self.frame['idle']

    def __clamp(self, minAllowed, maxAllowed, value):
        if value < minAllowed or value > maxAllowed:
            minDif = abs(value - minAllowed)
            maxDif = abs(value - maxAllowed)
            if minDif > maxDif:
                return maxAllowed
                # Closer to max
            else:
                return minAllowed
        return value

    def __updateFrame(self, x, y):
        # Update the Frame based on XY values

        # No Left/Right Movement
        if x == 0:
            if y == 0:
                self.currentFrame = self.frame['idle']
            elif y < 0:
                self.currentFrame = self.frame['top']
            elif y > 0:
                pass
                self.currentFrame = self.frame['down']
        # Right Movement
        elif x > 0:
            if y == 0:
                self.currentFrame = self.frame['right']
            elif y < 0:
                self.currentFrame = self.frame['right']
            elif y > 0:
                self.currentFrame = self.frame['right']
        # Left Movement
        elif x < 0:
            if y == 0:
                pass
                self.currentFrame = self.frame['left']
            elif y < 0:
                pass
                self.currentFrame = self.frame['left']
            elif y > 0:
                self.currentFrame = self.frame['left']

    def draw(self):
        """
        Draws the current image on the screen based on posX and posY value
        """
        # print(f"Drawing Player at location : {self.posX} and {self.posY}")
        self.window.blit(self.currentFrame, (self.posX, self.posY))  # Draw characters at current position

    # noinspection SpellCheckingInspection
    def updatePos(self, x, y):
        """
        Update the character's position directly instead of adding input
        :param x: the x value
        :param y: the y value
        """

        self.posX = x
        self.posY = y

        # self.__updateFrame(xAxis, yAxis)

    def listenInput(self):
        """
        Checks keys dictionary of PyGame and uses it to update posX and posY value of characters.
        Do NOT forget to call draw to draw the characters with the updated location data
        """
        keys = self.pg.key.get_pressed()  # Key active dict

        if keys[self.pg.K_LEFT]:
            x = -1
        elif keys[self.pg.K_RIGHT]:
            x = 1
        else:
            x = 0

        if keys[self.pg.K_UP]:
            y = -1
        elif keys[self.pg.K_DOWN]:
            y = 1
        else:
            y = 0

        # Add the XY Values
        self.posX += x * self.speed  # current player's X + x
        self.posY += y * self.speed

        self.posY = self.__clamp(minAllowed=0, maxAllowed=self.window.get_size()[1] - 50, value=self.posY)
        self.posX = self.__clamp(minAllowed=0, maxAllowed=self.window.get_size()[0] - 50, value=self.posX)

        # Update the Frame based on XY values
        # No Left/Right Movement
        if x == 0:
            if y == 0:
                self.currentFrame = self.frame['idle']
            elif y < 0:  # 1
                self.currentFrame = self.frame['top']
            elif y > 0:  # -1
                pass
                self.currentFrame = self.frame['down']
        # Right Movement
        elif x > 0:
            if y == 0:
                self.currentFrame = self.frame['right']
            elif y < 0:
                self.currentFrame = self.frame['right']
            elif y > 0:
                self.currentFrame = self.frame['right']
        # Left Movement
        elif x < 0:
            if y == 0:
                pass
                self.currentFrame = self.frame['left']
            elif y < 0:
                pass
                self.currentFrame = self.frame['left']
            elif y > 0:
                self.currentFrame = self.frame['left']
