import pygame as pg

from frontend.models.characters.CharBase import CharacterBase
from frontend.models.worlds.WldBase import WorldBase

screenSize = (800, 600)  # Set width and height
pg.init()  # initialize pygame
win = pg.display.set_mode(screenSize)  # Setup Screen

from frontend.service.GuestService import GuestService

guestService = GuestService(pg, win)  # Handles interacting with other players

from frontend.service.EffectService import EffectService

effectService = EffectService(pg, win)  # Handles drawing effects like explosion

from frontend.service.ServerHandler import ServerHandler

serverHandler = ServerHandler(
    guestService=guestService,
    effectService=effectService)  # Creates object, connects to internet and starts listening to server for processing
# We pass guestService because it needs to interact with it, same goes for effectService

# Creating LEVEL ----------------------------------------

world = WorldBase(frameArray=[
    pg.image.load("./assets/World/Layer 1_sprite_01.png"),
    pg.image.load("./assets/World/Layer 1_sprite_02.png"),
    pg.image.load("./assets/World/Layer 1_sprite_03.png"),
    pg.image.load("./assets/World/Layer 1_sprite_04.png"),
    pg.image.load("./assets/World/Layer 1_sprite_05.png"),
    pg.image.load("./assets/World/Layer 1_sprite_06.png"),
    pg.image.load("./assets/World/Layer 1_sprite_07.png"),
    pg.image.load("./assets/World/Layer 1_sprite_08.png"),
    pg.image.load("./assets/World/Layer 1_sprite_09.png"),
    pg.image.load("./assets/World/Layer 1_sprite_10.png"),
    pg.image.load("./assets/World/Layer 1_sprite_11.png"),
    pg.image.load("./assets/World/Layer 1_sprite_12.png"),
    pg.image.load("./assets/World/Layer 1_sprite_13.png"),
    pg.image.load("./assets/World/Layer 1_sprite_14.png"),
    pg.image.load("./assets/World/Layer 1_sprite_15.png"),
    pg.image.load("./assets/World/Layer 1_sprite_16.png"),
    pg.image.load("./assets/World/Layer 1_sprite_17.png"),
    pg.image.load("./assets/World/Layer 1_sprite_18.png"),
    pg.image.load("./assets/World/Layer 1_sprite_19.png"),
    pg.image.load("./assets/World/Layer 1_sprite_20.png"),
    pg.image.load("./assets/World/Layer 1_sprite_21.png"),
    pg.image.load("./assets/World/Layer 1_sprite_22.png"),
    pg.image.load("./assets/World/Layer 1_sprite_23.png"),
    pg.image.load("./assets/World/Layer 1_sprite_24.png"),
    pg.image.load("./assets/World/Layer 1_sprite_25.png"),
    pg.image.load("./assets/World/Layer 1_sprite_26.png"),

], frameChangeSpeed=30, piegae=pg, window=win)

# Creating The MAIN PLAYER --------------------------------
idle = pg.image.load("./assets/char/p/p_f.png")  # Initialize the frames for the player
bwd = pg.image.load("./assets/char/p/p_b.png")  # Initialize the frames for the player
lft = pg.image.load("./assets/char/p/p_l.png")  # Initialize the frames for the player
rt = pg.image.load("./assets/char/p/p_r.png")  # Initialize the frames for the player

# Creating the player Object
player = CharacterBase(
    frameDict={
        "idle": idle,
        'top': idle,
        'down': bwd,
        'left': lft,
        'right': rt
    },
    speed=1, window=win, piegae=pg)


def draws():
    """
    Draws several entities on the screen when called
    """
    world.drawWorld()  # level
    guestService.drawOtherPlayers()  # other players
    guestService.drawEnemies()  # Enemies draw
    guestService.drawShoot()  # shooting
    player.draw()  # Player
    effectService.draw()  # Explosions effect
    pg.display.update()


def perFrameTask():
    """
    Tasks that need to be performed every frame
    """
    player.listenInput()  # Listen to player input and allows the player to move
    serverHandler.sendEssentialData(
        (player.posX, player.posY))  # Send players position to the server and request enemies position
    draws()  # Draws


def gameLoop():
    running = True
    while running:
        # Quit Event
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                pg.quit()

            # If we press mouse down. We are shooting.
            if e.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()  # Store position of the mouse
                serverHandler.sendShoot(pos[0],
                                        pos[1])  # call sendShoot function and pass XY coordinate of the mouse position

        perFrameTask()


gameLoop()  # Start the main game loop
