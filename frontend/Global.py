import pygame as pg

from frontend.models.characters.CharBase import CharacterBase
from frontend.models.worlds.WldBase import WorldBase
from _thread import *

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
    guestService.drawOtherPlayers()
    guestService.drawEnemies()
    player.draw()
    pg.display.update()


def perFrameTask():
    player.move()  # Listen to player input and allows the player to move
    serverHandler.sendEssentialData((player.posX, player.posY))
    draws()  # Draws


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

"""
Flow of the program:
When serverHandler object is created the constructor tries to connect to the server.
Once successful it receives a UID which is then stored in GuestService
The ServerHandler then starts a new thread and calls a function that runs an infinite loop and
Listens to the server's response and processes it

Every Frame we check for Key events and move the player 
Every Frame we send essential data to the server such as current player position and a request to get the enemy positions



"""
