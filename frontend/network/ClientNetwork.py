import socket
import json


class ClientNetwork:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.29.95"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.uid = ""
        self.connect()  # Once we successfully connect we are going to get back an ID and it will be set as UID

    def connect(self):
        """
        Connect, to the Server.
        Call onDataReceived after connecting to listen to further responds
        :return:
        """
        try:
            self.client.connect(self.addr)  # try to connect
            self.processResponse(self.client.recv(2048).decode())
        except Exception as e:
            print(f"Exception when trying to connect to server in clientNetwork.connect {e}")

    def processResponse(self, decodedResp):
        """
        Listens to the server and when ever we get a response we try to parse it
        Parses the decodedString and performs appropriate action based on the action
        """
        if decodedResp is not None:

            respParsed = json.loads(decodedResp)  # Parse the Raw response to dict
            if respParsed['action'] == 'uid':
                self.uid = respParsed['data']
                print(f"UID Set to {self.uid}")

    def sendPosToServer(self, x, y):
        """
        Call After updating player position, this will also receive the server's response and call processResponse Function appropriately
        """
        try:
            resp = {
                "action": "update_pos",
                "data": {"x": x, "y": y}
            }
            respFinal = json.dumps(resp).encode()
            self.client.send(respFinal)
        except socket.error as e:
            print(f"Exception at send at ClientNetwork.sendPos : {e}")
