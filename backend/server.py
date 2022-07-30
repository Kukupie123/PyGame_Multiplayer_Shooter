import json  # JSON is how we store organise data
import logging  # For logging
import socket
from _thread import *  # Import everything from thread

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
connections = []
enemyHandler = EnemyHandler(800,
                            600)  # Server code that handles enemy character of the game, 800,600 is the Width and Height of the client

try:
    sk.bind((server, port))  # Open up the server
except socket.error as e:
    print(e)

sk.listen(2)  # Max 2 number of clients allowed

logger.warning("Waiting For connection, Server Started ")

dataSize = 5


# TODO: Better hit detection by taking the center of image for enemies

def broadcaster(action, data):
    print(f"Broadcasting {action} with data {data}")

    resp = [{
        "action": action,
        "data": data
    }]

    respStr = json.dumps(resp).encode()
    for conn in connections:
        try:
            conn.sendall(respStr)
        except:
            pass

    kills = enemyHandler.enemyHit(data['x'], data['y'], 25)  # [x,y,type]
    if len(kills) > 0:
        start_new_thread(broadcaster, ("kill", kills))


# noinspection PyTypeChecker
def threaded_clientV2(conn, uid):
    """
    Handles server and client interaction
    Sends responses and receives request

    NOTE: Responses are sent as array list of {action, data} dictionary
    This increases the size of the data we transfer but I used this because of the simplicity
    of the project and also because there was a bug that only sent the first response when we tried sending multiple response to the client

    NOTE: CLIENT MUST ALWAYS SEND AN ARRAY JSON EG: [{action:move}]
    :param conn: the connection object of the client connected
    :param uid: UID of the client
    """
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

    # Continuously Listen to the client and talk back when requested
    while True:

        try:
            data = conn.recv(2048 * dataSize).decode("utf-8")  # Decoded string response
            response = []  # To store array of response to send
            reqs = []  # Array to store the response we create to send the client
            try:
                reqs = json.loads(conn.recv(2048 * dataSize).decode("utf-8"))  # Array of action and data dictionary
            except:
                if data is not None:  # Non parsable data but client is still connected
                    continue

            # For each action we want to create a response action dictionary and at the end of iteration send it
            for req in reqs:  # {action, data : {}}
                # ACTIONS THAT CLIENT SEND AND SERVER UPDATES ---------------
                action = req['action']

                # If client wants to update it's position
                if action == 'update_pos':  # action, data : {x,y}
                    x = req['data']['x']
                    y = req['data']['y']
                    playersPos[uid] = (x,
                                       y)  # Update the dictionary key's value with the new XY value, This is why we needed UID for each client. To distinguish between them

                elif action == 'shoot':  # action, data : {x,y}
                    """
                    Send a broadcast to all client
                    action : shoot
                    data : {
                    x : x
                    y : y
                    uid : shootersID
                    }
                    """

                    start_new_thread(broadcaster,
                                     ("shoot",
                                      {"x": req['data']['x'], "y": req['data']['y'], "id": uid})
                                     )  # Start Broadcasting the message


                # ACTIONS THAT CLIENT REQUEST AND SERVER SENDS-----------------

                # Client wants position data of player
                elif action == 'get_player_pos':
                    resp = {"action": "pos_data", "data": playersPos}
                    response.append(resp)

                # If client wants their UID
                elif action == 'get_uid':
                    resp = {
                        "action": "uid",
                        "data": uid
                    }
                    response.append(resp)

                # If client wants to get enemy data
                if action == 'get_enemy_data':
                    enemies = enemyHandler.getEnemies()  # Get the enemies data and send it to client
                    resp = {
                        "action": "enemy_data", "data": enemies
                    }
                    response.append(resp)

                # Once iteration over we are going to send the response array of action&Data as string
            conn.sendall(json.dumps(response).encode())
        except Exception as e:
            print(e)
            break
    print("Lost Connection")
    playersPos.pop(uid)  # Broken out of loop, Disconnect player
    global connections
    connections.remove(conn)
    conn.close()


@DeprecationWarning  # Old method of talking to client. Works well but the bug where the server only sent first data when sending multiple data forced me to abandon this
def threaded_client(conn, uid):
    """
       Should be run at a bg thread. Keeps track of a client and handles receiving and sending data
       :param conn: The connection object obtained upon calling socket.accept(). It will hold all the connected clients
       :param uid: The UID that was assigned by the server when accepting the connection
       """
    global playersPos
    # on first connect send the uid
    response = {
        "action": "uid",
        "data": uid
    }
    conn.sendall(json.dumps(response).encode())
    logger.warning(f"Client with UID {uid} connected.")

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
    # Continuously Look for Connection and accept a connection when we find one
    conn, addr = sk.accept()  # Combination of IP and Port is unique
    uid = str(addr[0]) + str(addr[1])  # Create a UID for every client

    """
    Start a new thread to run threaded_clientV2 because it makes use of infinite loop to
    Keep trace of client and it's request and will block the program if run on main thread
    """
    connections.append(conn)
    start_new_thread(threaded_clientV2, (conn, uid))
