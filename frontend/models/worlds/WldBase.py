class WorldBase:
    def __init__(self, frameArray, frameChangeSpeed, piegae, window):
        """
        BG of the game worlds
        :param frameArray: An array of frames that the Image will loop over to animate
        :param frameChangeSpeed: The Speed at which the frames will change
        """
        self.pg = piegae
        self.win = window
        self.maxFrame = 20  # How many frames to wait for until we skip to the next frame
        self.currentFrame = 0  # To Keep trace of which frame we are at.
        self.CurrentFrameIndex = 0  # Current Frame in use
        self.frame = frameArray

    def drawWorld(self):
        img = self.frame[self.CurrentFrameIndex]  # Get current Image from frame variable
        img = self.pg.transform.scale(img, self.win.get_size())  # Scale it to fit display
        self.win.blit(img, (0, 0))  # Draw it on the screen
        self.currentFrame += 1  # Increment Current Game Frame by 1

        if self.currentFrame >= self.maxFrame:
            self.currentFrame = 0  # Reset the currentFrame Count
            # Set current Image to 0 if we are at the end of frames else we use the next image in the frame
            # print(self.CurrentFrameIndex)
            self.CurrentFrameIndex = self.CurrentFrameIndex + 1 if (self.CurrentFrameIndex < len(self.frame) - 1) else 0
            # print("Changing World Frame")
