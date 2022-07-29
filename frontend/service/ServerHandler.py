import json
import logging
import socket
from _thread import *

dataSize = 5

log = logging.getLogger("Client Network")


# noinspection PyMethodMayBeStatic
class ServerHandler:
    def __init__(self, guestService):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.29.95"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.guestService = guestService
        self.connect()  # Once we successfully connect we are going to continuously listen.

    def connect(self):
        """
        Connect, to the Server.
        Call onDataReceived after connecting to listen to further responds
        """
        try:
            self.client.connect(self.addr)  # try to connect
            # Continuously Listen for server's response
            self.client.recv(2048 * dataSize).decode()
            start_new_thread(self.multi_listen, ())
        except Exception as e:
            print(f"Exception when trying to connect to server in clientNetwork.connect {e}")

    def processResponse(self, decodedResp):
        try:
            """
            Listens to the server and when ever we get a response we try to parse it
            Parses the decodedString and performs appropriate action based on the action
            """
            if decodedResp is not None:

                respParsed = decodedResp  # Parse the Raw response to dict
                log.info(f"Server sent response : {respParsed}")
                if respParsed['action'] == 'uid':  # Update the Client UID
                    self.guestService.UID = respParsed['data']

                elif respParsed['action'] == 'pos_data':  # Position Data received
                    self.guestService.updatePlayerPOSSERVER(respParsed['data'])  # Update All players position

                elif respParsed['action'] == 'enemy_data':  # Enemy Data received
                    self.guestService.updateEnemyPOSServer(
                        respParsed['data']
                    )
        except:
            pass

    def multi_listen(self):
        """
        RUN in MultiThread mode. This is a loop that will make the client keep on listening to the server and will freeze the program if not made to run in a multithreading environment
        """
        while True:
            try:
                msgRaw = self.client.recv(2048 * dataSize).decode()  # Return an array of action&Data Dict
                response = json.loads(msgRaw)  # list of action&Data Dictionary
                for resp in response:  # Iterate and process each action
                    self.processResponse(resp)
            except Exception:
                pass

    def sendEssentialData(self, playerXYTuple):
        try:
            print(f"{playerXYTuple[0]} {playerXYTuple[1]}")
            playerPOS = {"action": "update_pos", "data": {"x": playerXYTuple[0], "y": playerXYTuple[1]}}
            reqEnemyData = {"action": "get_enemy_data"}
            reqPlayerPOSData = {"action": "get_player_pos"}
            reqs = [playerPOS, reqEnemyData, reqPlayerPOSData]
            reqStr = json.dumps(reqs)
            self.client.send(reqStr.encode())
        except Exception as e:
            print(f"Exception at sendEssentialData : {e}")
