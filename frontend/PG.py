import pygame as pg


# Initializing PyGame Core ----------------------------
from frontend.network.ClientNetwork import ClientNetwork

screenSize = (800, 600)  # Set width and height
pg.init()  # initialize pygame
screen = pg.display.set_mode(screenSize)  # Setup Screen
icon = pg.image.load("./assets/aquaman1-1.png.png")  # Load Icon
pg.display.set_icon(icon)
