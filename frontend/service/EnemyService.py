class EnemyService:
    def __init__(self):
        pass


"""

Request server for enemy


Server will then check it's enemy list.
If it is empty then it will create an enemy and send it to all clients and keep trace of time

When client requests for enemy
this time server will send the enemies it has

The server will create enemies at specific interval after first request until it has n number of enemies

Then it will wait for enemy of that list to get removed before it can spawn new one

When an enemy is removed i.e goes out of bound or killed we reset the timer to spawn enemy 

Request enemy list from the server
If it is not empty we are going to get positions and enemy types and all those details and then draw them


MOVING THE ENEMIES :

After the first enemy is spawned we are going to have to update the x,y pos of enemies on the server side after specific interval at specific rate

If enemy list is not in server we are going to create an enemy and send it to
"""

# Destroy enemy if it goes over a border
