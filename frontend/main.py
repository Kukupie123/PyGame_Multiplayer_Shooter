from frontend.models.character.CharBase import CharacterBase
from frontend.models.world.WorldBase import WorldBase
from PG import pg

# Draw the World
from frontend.network.ClientNetwork import ClientNetwork
from frontend.service.GameModService import GMService

world = WorldBase(frameArray=[
    pg.image.load("./assets/World/1/1_(1).png"),
    pg.image.load("./assets/World/1/1_(2).png"),
    pg.image.load("./assets/World/1/1_(3).png"),
    pg.image.load("./assets/World/1/1_(4).png"),
    pg.image.load("./assets/World/1/1_(5).png"),
    pg.image.load("./assets/World/1/1_(6).png"),
    pg.image.load("./assets/World/1/1_(7).png")
], frameChangeSpeed=30)

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
    speed=1)

# Creating GameModeService and ClientNetwork

gms = GMService()
cn = ClientNetwork(gms)  # Will connect and start listening, this will then start using GMS to update client as needed


# FUNCTIONS --------------------------

def redraw():
    world.drawWorld()  # Draw the BG
    mainPlayer.draw()  # Draw the main player

    for k, v in gms.pos_dic.items():
        # Spawning The Client PLAYER --------------------------------
        idle = pg.image.load("./assets/aquaman1-1.png.png")  # Initialize the frames for the player
        # Creating the player Object
        tp = CharacterBase(
            frameDict={
                "idle": idle,
                'top': idle,
                'down': idle,
                'left': idle,
                'right': idle
            },
            speed=1)
        tp.updatePos(v[0], v[1])
        tp.draw()

    pg.display.update()  # Update the UI


# Game Loop Logic
def startGame():
    running = True
    # Game Loop
    while running:
        # Quit Event
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
        mainPlayer.move()
        cn.sendPosToServer(mainPlayer.posX, mainPlayer.posY)
        redraw()


startGame()  # Start Main Game Loop

# TODO : Add Boundary
# TODO : Add Enemy
# TODO : Add Shooting
# TODO : Collision Detection
