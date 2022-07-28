from frontend.models.characters.CharBase import CharacterBase
from frontend.models.characters.Enemy import Enemy


class GuestService:
    def __init__(self, pg, win):
        self.UID = "NULL"
        # Other Players
        self.pos_dic = {}  # The raw data as {UID : (x,y)}
        self.players = {}

        # Enemies
        self.enemy_data = {}
        self.enemies = {}
        self.pg = pg
        self.win = win

    def updatePlayerPOSSERVER(self, pos_dic):  # {uid : (x,y)}
        self.pos_dic = pos_dic

    def updateEnemyPOSServer(self, enemy_data):
        """
        {
        enemy_data needs to be in this format
        343UID : {
            x : 12,
            y : 0,
            move : LEFT.
            type : crab
            }
        }
        """
        self.enemy_data = enemy_data

    def __createEnemy(self):
        testEnemy = Enemy(
            enemyFrameArray=[
                self.pg.image.load("../frontend/assets/enemy/crab0.png"),
                self.pg.image.load("../frontend/assets/enemy/crab1.png"),
                self.pg.image.load("../frontend/assets/enemy/crab2.png"),
                self.pg.image.load("../frontend/assets/enemy/crab3.png"),
            ],
            speed=1,
            piegae=self.pg,
            window=self.win,
            animationSpeed=15,
        )
        return testEnemy

    def drawEnemies(self):
        for k, v in self.enemy_data.items():
            if k not in self.enemies:  # If enemy we iterated over is not in the enemies list
                print(f"Adding {k} to enemy list with data {v['y']}")
                self.enemies[k] = self.__createEnemy()

            # Update the position of the enemies
            self.enemies[k].updatePos(v['x'], v['y'])

        # Remove Duplicates
        for k in self.enemies:
            if k not in self.enemy_data:
                self.enemies.pop(k)

        # Finally we draw
        for k in self.enemies:
            self.enemies[k].draw()

    def drawOtherPlayers(self):
        for k, v in self.pos_dic.items():
            if k == self.UID:  # If its the same player as this client we do not draw as it is the player
                continue
            if k not in self.players:  # if main player is not in list we create new player with the id
                idle = self.pg.image.load(
                    "../frontend/assets/aquaman1-1.png.png")  # Initialize the frames for the player
                print(f"Adding {k} to the guestList with position {v}")
                # Creating The MAIN PLAYER --------------------------------
                # Creating the player Object
                player = CharacterBase(
                    frameDict={
                        "idle": idle,
                        'top': idle,
                        'down': idle,
                        'left': idle,
                        'right': idle
                    },
                    speed=1, window=self.win, piegae=self.pg)
                self.players[k] = player

            self.players[k].updatePos(v[0], v[
                1])  # This should never fail as we are creating player for this ID in the if block above when its empty

        # Get rid of disconnected players, i.e players who are not in the parameter supplied which has all the current active player sent from the server
        for k in self.players:
            if k not in self.pos_dic:
                self.players.pop(k)

        # Draw each players now
        for k in self.players:
            self.players[k].draw()
