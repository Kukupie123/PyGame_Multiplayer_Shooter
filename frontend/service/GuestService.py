from frontend.models.characters.CharBase import CharacterBase
import pygame


class GuestService:
    def __init__(self, pg, win):
        self.UID = "NULL"
        self.pos_dic = {}  # The raw data as {UID : (x,y)}
        self.players = {}
        self.pg = pg
        self.win = win

    def updatePlayerPOSSERVER(self, pos_dic):  # {uid : (x,y)}
        self.pos_dic = pos_dic

    def drawGuests(self):
        for k, v in self.pos_dic.items():
            if k == self.UID:  # If its the same player as this client we do not draw as it is the player
                continue
            if k not in self.players:  # if main player is not in list we create new player with the id
                idle = self.pg.image.load("../frontend/assets/aquaman1-1.png.png")  # Initialize the frames for the player
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
