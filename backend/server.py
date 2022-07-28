import socket
from _thread import *  # Import everything from thread
import json
import logging

# Web Socket Config
from backend.EnemyHandler import EnemyHandler

server = "192.168.29.95"  # Local IP
port = 5555
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Logger Config
logger = logging.getLogger("Server")
logger.addHandler(logging.StreamHandler())

# Variables
playersPos = {}  # clientUID : position. Holds all the players connected position
enemyHandler = EnemyHandler(800, 600)  # Server code that handles enemy character of the game

try:
    sk.bind((server, port))  # Open up the server
except socket.error as e:
    print(e)

sk.listen(2)  # Max 2 number of clients allowed

logger.warning("Waiting For connection, Server Started ")

dataSize = 5


def threaded_clientV2(conn, uid):
    global playersPos
    # On first connect send the UID to the client so that they know their UID
    resp = [
        {
            "action": "uid",
            "data": uid
        }
    ]

    conn.sendall(json.dumps(resp).encode())
    logging.warning(f"{uid} connected")

    while True:
        try:
            if conn.recv(2048*dataSize) is not None:
                response = []
                reqs = json.loads(conn.recv(2048 * dataSize).decode("utf-8"))  # Array of action and data dictionary

                # For each action we want to create a response action dictionary and at the end of iteration send it
                for req in reqs:
                    action = req['action']

                    # If client wants their UID
                    if action == 'get_uid':
                        resp = {
                            "action": "uid",
                            "data": uid
                        }
                        response.append(resp)

                    # If client wants to update it's position
                    if action == 'update_pos':
                        x = req['data']['x']
                        y = req['data']['y']
                        playersPos[uid] = (x, y)
                        resp = {"action": "pos_data", "data": playersPos}
                        response.append(resp)

                    # If client wants to get enemy data
                    if action == 'get_enemy_data':
                        dat = enemyHandler.getEnemies()  # Get the enemies data and send it to client
                        resp = {
                            "action": "enemy_data", "data": dat
                        }
                        response.append(resp)

                # Once iteration over we are going to send the response array of action&Data as string
                conn.sendall(json.dumps(response).encode())
        except:
            break
    print("Lost Connection")
    playersPos.pop(uid)
    conn.close()


def threaded_client(conn, uid):
    global playersPos
    # on first connect send the uid
    response = {
        "action": "uid",
        "data": uid
    }
    conn.sendall(json.dumps(response).encode())
    logger.warning(f"Client with UID {uid} connected.")
    """
    Should be run at a bg thread. Keeps track of a client and handles receiving and sending data
    :param conn: The connection object obtained upon calling socket.accept(). It will hold all the connected clients
    :param uid: The UID that was assigned by the server when accepting the connection
    """

    """
    When a player connects it has to next send it's data, the server will then store that player's data in a dictionary 
    And then we will return the whole player list to the client that way the client can update the player count as well as their position
    
    Player will continuously keep on sending it's player data which in turn will keep the server sending it updated the dictionary where all the players are stored
    """

    # Continuously Try to receive data. If no data received we assume that the client has disconnected. A better way would be to ping and see if we get back a response
    while True:
        try:
            # If we are receiving data from client
            if conn.recv(2048) is not None:
                receive = json.loads(conn.recv(2048 * dataSize).decode("utf-8"))
                action = receive['action']
                logger.warning(f"Client {uid} requested action : {action}")
                if action == 'get_uid':
                    print(f"Initial Connection for UId {uid}")
                    response = {
                        "action": "uid",
                        "data": uid
                    }
                    conn.sendall(json.dumps(response).encode())

                elif action == 'update_pos':
                    x = receive['data']['x']
                    y = receive['data']['y']
                    playersPos[uid] = (x, y)

                    response = {"action": "pos_data", "data": playersPos}
                    # Send the client all the position data of other players in the server

                    conn.sendall(json.dumps(response).encode())

                elif action == 'get_enemy_data':
                    dat = enemyHandler.getEnemies()  # Get the enemies data and send it to client
                    resp = {
                        "action": "enemy_data", "data": dat
                    }
                    conn.sendall(json.dumps(resp).encode())

        except Exception as e:
            print(f"Something Went Wrong {e}")
            break
    print("Lost Connection")
    playersPos.pop(uid)
    conn.close()


while True:
    # Continuously Look for Connection
    conn, addr = sk.accept()  # Combination of IP and Port is unique
    uid = str(addr[0]) + str(addr[1])
    # We start a new thread because without a thread the program is going to wait for "threaded_client" function to be done before proceeding
    # We are going to have multiple client join at once and for each client we are going to run the threaded_client function in a different thread to not block the main thread
    start_new_thread(threaded_clientV2, (conn, uid))
