class WorldBase:
    def __init__(self, frameArray, pg, pgScreen, frameChangeSpeed):
        self.pg = pg  # PyGame Reference
        self.pgScreen = pgScreen  # PyGame Screen Reference
        self.frameChangeSpeed = frameChangeSpeed  # How many frames to wait for until we skip to the next frame
        self.CurrentGameFrame = 0  # To Keep trace of which frame we are at.
        self.CurrentFrameIndex = 0  # Current Frame in use
        self.frame = frameArray

    def drawWorld(self):
        img = self.frame[self.CurrentFrameIndex]  # Get current Image from frame variable
        img = self.pg.transform.scale(img, self.pgScreen.get_size())  # Scale it to fit display
        self.pgScreen.blit(img, (0, 0))  # Draw it on the screen
        self.CurrentGameFrame += 1  # Increment Current Game Frame by 1

        if self.CurrentGameFrame >= self.frameChangeSpeed:
            self.CurrentGameFrame = 0  # Reset the currentFrame Count
            # Set current Image to 0 if we are at the end of frames else we use the next image in the frame
            # print(self.CurrentFrameIndex)
            self.CurrentFrameIndex = self.CurrentFrameIndex + 1 if (self.CurrentFrameIndex < len(self.frame) - 1) else 0
            # print("Changing World Frame")
