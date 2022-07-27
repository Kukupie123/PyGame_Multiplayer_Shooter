import socket


class ClientNetwork:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.29.95"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()  # Once we successfully connect we are going to get back an ID
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print("Exception when trying to connect to server")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Exception at send at ClientNetwork : {e}")


# DEBUG PURPOSE
def debug():
    n = ClientNetwork()
    print(n.send("Hello Does this work"))

debug()