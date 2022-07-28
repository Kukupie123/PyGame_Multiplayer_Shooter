from frontend.models.characters.CharBase import CharacterBase
import random


class Enemy(CharacterBase):
    def __init__(self, enemyFrameArray, speed, piegae, window, animationSpeed, spawnPoint):  # spawnPoint = 0/1/2/3
        super().__init__(frameDict=None, speed=speed, piegae=piegae, window=window)
        self.maxFrame = animationSpeed  # Threshold to switch frame
        self.currentFrame = 0  # Once this reaches the animation speed we switch to the next animation
        self.currentImageIndex = 0
        self.frames = enemyFrameArray
        # Set spawn point based on spawnPoint set
        if spawnPoint == 0 or spawnPoint == 1:
            self.posX = random.randint(0, window.get_size()[0])  # Random X value
            self.posY = 0 if spawnPoint == 0 else window.get_size()[1] - 50
            self.moveDir = "DOWN" if spawnPoint == 0 else "UP"
        elif spawnPoint == 2 or spawnPoint == 3:
            self.posY = random.randint(0, window.get_size()[1])
            self.posX = 0 if spawnPoint == 2 else window.get_size()[0] - 50
            self.moveDir = "RIGHT" if spawnPoint == 2 else "LEFT"

    def draw(self):
        img = self.frames[self.currentImageIndex]
        self.window.blit(img, (self.posX, self.posY))
        self.currentFrame += 1  # Increase the frame count by 1

        if self.currentFrame >= self.maxFrame:
            self.currentFrame = 0  # Reset CurrentFrame count and set a new image

            self.currentImageIndex = self.currentImageIndex + 1 if (
                    self.currentImageIndex < len(self.frames) - 1) else 0
