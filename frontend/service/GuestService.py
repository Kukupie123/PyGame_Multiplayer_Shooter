class GuestService:
    def __init__(self):
        self.UID = "NULL"
        self.pos_dic = {}  # The raw data as {UID : (x,y)}
        self.players = {}

    def updatePlayerPOSSERVER(self, pos_dic):  # {uid : (x,y)}
        self.pos_dic = pos_dic

    def drawGuests(self):
        for k, v in self.pos_dic.items():
            print(f"{k} = {v}")
