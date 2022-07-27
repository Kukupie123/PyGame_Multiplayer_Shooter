import pygame as pg
from frontend.models.character.CharBase import CharacterBase
from frontend.models.world.WorldBase import WorldBase
from frontend.network.ClientNetwork import ClientNetwork

# Initializing PyGame Core ----------------------------
screenSize = (800, 600)  # Set width and height
pg.init()  # initialize pygame
screen = pg.display.set_mode(screenSize)  # Setup Screen
icon = pg.image.load("./assets/aquaman1-1.png.png")  # Load Icon
pg.display.set_icon(icon)
# Draw the World
world = WorldBase(frameArray=[
    pg.image.load("./assets/World/1/1_(1).png"),
    pg.image.load("./assets/World/1/1_(2).png"),
    pg.image.load("./assets/World/1/1_(3).png"),
    pg.image.load("./assets/World/1/1_(4).png"),
    pg.image.load("./assets/World/1/1_(5).png"),
    pg.image.load("./assets/World/1/1_(6).png"),
    pg.image.load("./assets/World/1/1_(7).png")
], frameChangeSpeed=30, pgScreen=screen, pg=pg)

# Spawning The MAIN PLAYER --------------------------------
idle = pg.image.load("./assets/aquaman1-1.png.png")  # Initialize the frames for the player
# Creating the player Object
mainPlayer = CharacterBase(
    frameDict={
        "idle": idle,
        'top': idle,
        'down': idle,
        'left': idle,
        'right': idle
    },
    speed=1, pg=pg, pgScreen=screen, spawnPoint=None)


# FUNCTIONS --------------------------

def redraw():
    world.drawWorld()
    mainPlayer.draw()
    pg.display.update()


# Game Loop Logic
def startGame():
    n = ClientNetwork()  # Connects to the server
    running = True
    # Game Loop
    while running:
        # Quit Event
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
        mainPlayer.move()
        n.sendPosToServer(mainPlayer.posX, mainPlayer.posY)
        redraw()


startGame()  # Start Main Game Loop

# TODO : Add Boundary
# TODO : Add Enemy
# TODO : Add Shooting
# TODO : Collision Detection
