from frontend.models.characters.CharBase import CharacterBase
import random


class Enemy(CharacterBase):
    def __init__(self, enemyFrameArray, speed, piegae, window, animationSpeed):  # spawnPoint = 0/1/2/3
        super().__init__(frameDict=None, speed=speed, piegae=piegae, window=window)
        self.maxFrame = animationSpeed  # Threshold to switch frame
        self.currentFrame = 0  # Once this reaches the animation speed we switch to the next animation
        self.currentImageIndex = 0
        self.frames = enemyFrameArray

    def draw(self):
        img = self.frames[self.currentImageIndex]
        self.window.blit(img, (self.posX, self.posY))
        self.currentFrame += 1  # Increase the frame count by 1

        if self.currentFrame >= self.maxFrame:
            self.currentFrame = 0  # Reset CurrentFrame count and set a new image

            self.currentImageIndex = self.currentImageIndex + 1 if (
                    self.currentImageIndex < len(self.frames) - 1) else 0
