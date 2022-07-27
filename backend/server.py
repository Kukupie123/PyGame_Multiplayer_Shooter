import socket
from _thread import *  # Import everything from thread
import sys

server = "192.168.29.95"  # Local IP
port = 5555

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sk.bind((server, port))  # Open up the server
except socket.error as e:
    print(e)

sk.listen(2)  # Max 2 number of clients allowed

print("Waiting For connection, Server Started ")


def threaded_client(conn):
    """
    Should be run at a bg thread. Keeps track of a client and handles receiving and sending data
    :param conn: The connection object obtained upon calling socket.accept(). It will hold all the connected clients
    """
    conn.send(str.encode("Connected Successfully"))  # Send The client a message saying that connection was successful
    reply = ""
    # Continuously Try to receive data. If no data received we assume that the client has disconnected. A better way would be to ping and see if we get back a response
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")  # Decode the Encoded data we receive
            if data is None:
                print("Disconnected")
                break
            else:
                print(f"Received : {reply}")
                print(f"Sending : {reply}")
            conn.sendall(str.encode(reply))  # Encode our information and then send it back to all connected clients
        except e:
            print(f"Error at ThreadedClient Message {str(e)}")
            break
    print("Lost Connection")
    conn.close()

    pass


while True:
    # Continuously Look for Connection
    conn, addr = sk.accept()
    print(f"Connected to {addr}")
    # We start a new thread because without a thread the program is going to wait for "threaded_client" function to be done before proceeding
    # We are going to have multiple client join at once and for each client we are going to run the threaded_client function in a different thread to not block the main thread
    start_new_thread(threaded_client, (conn,))
