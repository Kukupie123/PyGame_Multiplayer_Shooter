import socket
import _thread
import sys

server = ""
port = 5555

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sk.bind((server, port))
except socket.error as e:
    print(e)

sk.listen(2)  # Max 2 number of clients allowed

print("Waiting For connection ")
