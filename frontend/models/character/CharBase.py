from frontend.PG import pg, screen


class CharacterBase:
    def __init__(self,
                 frameDict, speed):
        """
        When creating a character you need to supply all the necessary frames
        :param frameDict: Dictionary of your Character state images named appropriately as idle,top,down,left,right (Type must be of pygame.SurfaceType)
        :param speed: speed of the character movement
        """

        # Image dictionary setup with the necessary image
        self.frame = {
            "idle": frameDict['idle'],
            "top": frameDict['top'],
            "down": frameDict['down'],
            "left": frameDict['left'],
            "right": frameDict['right']
        }
        # Setup Additional Data
        self.speed = speed  # Speed of player
        self.posX = (screen.get_size()[0]) / 2
        self.posY = (screen.get_size()[1]) / 2
        self.currentFrame = self.frame['idle']

    def draw(self):
        """
        Draws the current image on the screen based on posX and posY value
        """
        # print(f"Drawing Player at location : {self.posX} and {self.posY}")
        screen.blit(self.currentFrame, (self.posX, self.posY))  # Draw character at current position

    def updatePos(self, x, y):
        """
        Update the character's position directly instead of adding input
        :param x: the x value
        :param y: the y value
        """
        self.posX = x
        self.posY = y

    def move(self):
        """
        Checks keys dictionary of PyGame and uses it to update posX and posY value of character.
        Do NOT forget to call draw to draw the character with the updated location data
        """
        keys = pg.key.get_pressed()  # Key active dict

        if keys[pg.K_LEFT]:
            x = -1
        elif keys[pg.K_RIGHT]:
            x = 1
        else:
            x = 0
        if keys[pg.K_UP]:
            y = -1
        elif keys[pg.K_DOWN]:
            y = 1
        else:
            y = 0

        # Add the XY Values
        self.posX += x * self.speed
        self.posY += y * self.speed

        # Update the Frame based on XY values

        # No Left/Right Movement
        if x == 0:
            if y == 0:
                pass
                # print("Idle")
            elif y < 0:
                pass
                # print("Up")
            elif y > 0:
                pass
                # print("Down")
        # Right Movement
        elif x > 0:
            if y == 0:
                pass
                # print("Right")
            elif y < 0:
                pass
                # print("Top Right")
            elif y > 0:
                pass
                # print("Bottom Right")
        # Left Movement
        elif x < 0:
            if y == 0:
                pass
                # print("Left")
            elif y < 0:
                pass
                # print("Top Left")
            elif y > 0:
                pass
                # print("Bottom Left")
