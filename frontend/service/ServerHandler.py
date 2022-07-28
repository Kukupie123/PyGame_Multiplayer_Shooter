import json
import logging
import socket
from _thread import *

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
            self.processResponse(self.client.recv(2048).decode())
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

                respParsed = json.loads(decodedResp)  # Parse the Raw response to dict
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
                msgRaw = self.client.recv(2048).decode()
                print(msgRaw)
                self.processResponse(msgRaw)
            except Exception:
                pass

    def sendPlayerPos2Server(self, x, y):
        """
        Call After updating player position, this will also receive the server's response and call processResponse Function appropriately
        """
        try:
            req = {
                "action": "update_pos",
                "data": {"x": x, "y": y}
            }
            reqStr = json.dumps(req).encode()
            self.client.send(reqStr)
        except socket.error as e:
            print(f"Exception at send at ClientNetwork.sendPos : {e}")

    def requestEnemiesData(self):
        """
        Request the enemies data from the server
        """
        try:
            req = {"action": "get_enemy_data"}
            reqStr = json.dumps(req).encode()
            self.client.send(reqStr)
            pass
        except:
            print(f"Exception at ServerHandler.requestEnemiesData : {e}")
