class GMService:
    def __init__(self):
        self.players = {}
        self.UID = "NULL"
        self.processingPlayersPOS = False
        self.pos_dic = {}

    def updatePlayerPOSSERVER(self, pos_dic):  # {uid : (x,y)}
        self.pos_dic = pos_dic

    def updatePlayersPOS(self, pos_dic):  # { uid : (x,y)}
        # If we are already processing then do not try to process again. Needed since this runs in multi threaded env
        if self.processingPlayersPOS:
            print("Processing in progress")
            return
        self.processingPlayersPOS = True
        print(pos_dic)
        """
        takes the response from server for action "pos_update[data]" and then iterates over each key to set the characters it needs to draw and at which position
        :param pos_dic: the json dumped data of pos_update, pos_update['data']
        """

        # Iterate through the pos_dic
        for k, v in pos_dic.items():
            print(f"key : {k} value : {v}")
            # Check if player is in players dict by comparing the key
            if k not in self.players:  # Player is not in the players dict
                # Create New player with the players
                # Add it to players dict and then update position
                self.players[k] = otherPlayerModel
                print(f"created new connected player {self.players[k]}")

            # When code reaches here we SHOULD have the player we need inside the players dict

            if k != self.UID:  # Update the player position IF not player
                self.players[k].updatePos(pos_dic[v][0], pos_dic[v][1])  # updatePos(x,y)
                print(f"Updated Pos of player {v}")
            else:
                print(f"Not updating pos as {k} == {self.UID}")

        # Remove duplicates
        for k in self.players:
            # The player we current have on the iteration is NOT in the server meaning the player has disconnected and we need to remove
            if pos_dic[k] is None:
                self.players.pop(k)
        self.processingPlayersPOS = False

    def getConnectedUsersCount(self):
        return

    def drawPlayers(self):
        """
        Draws every single player stored in players dict
        """
        for p in self.players:
            p.draw()
