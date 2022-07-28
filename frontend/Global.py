import pygame as pg

from frontend.models.characters.CharBase import CharacterBase
from frontend.models.worlds.WldBase import WorldBase

screenSize = (800, 600)  # Set width and height
pg.init()  # initialize pygame
win = pg.display.set_mode(screenSize)  # Setup Screen
icon = pg.image.load("./assets/aquaman1-1.png.png")  # Load Icon
pg.display.set_icon(icon)

# Setup Server handler (Sends request to server as well as processes responses fro the server)
from frontend.service.GuestService import GuestService

guestService = GuestService(pg, win)  # Handles interacting with other players
from frontend.service.ServerHandler import ServerHandler

serverHandler = ServerHandler(
    guestService=guestService)  # Creates object, connects to internet and starts listening to server for processing
# We pass guestService because it needs to interact with it

world = WorldBase(frameArray=[
    pg.image.load("./assets/World/1/1_(1).png"),
    pg.image.load("./assets/World/1/1_(2).png"),
    pg.image.load("./assets/World/1/1_(3).png"),
    pg.image.load("./assets/World/1/1_(4).png"),
    pg.image.load("./assets/World/1/1_(5).png"),
    pg.image.load("./assets/World/1/1_(6).png"),
    pg.image.load("./assets/World/1/1_(7).png")
], frameChangeSpeed=30, piegae=pg, window=win)

# Creating The MAIN PLAYER --------------------------------
idle = pg.image.load("./assets/aquaman1-1.png.png")  # Initialize the frames for the player
# Creating the player Object
player = CharacterBase(
    frameDict={
        "idle": idle,
        'top': idle,
        'down': idle,
        'left': idle,
        'right': idle
    },
    speed=1, window=win, piegae=pg)


def draws():
    world.drawWorld()
    player.draw()
    guestService.drawGuests()
    pg.display.update()


def perFrameTask():
    player.move()
    serverHandler.sendPosToServer(player.posX, player.posY)
    draws()


def gameLoop():
    running = True
    while running:
        # Quit Event
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                pg.quit()
        perFrameTask()


gameLoop()
