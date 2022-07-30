import random
import time
import uuid
from _thread import *


# noinspection PyMethodMayBeStatic,DuplicatedCode,PyUnboundLocalVariable
class EnemyHandler:
    def __init__(self, x, y):
        self.width = x  # Width of the client
        self.height = y  # Height of the client
        self.spawnTimerActive = False  # To keep trace if spawn timer is active or not
        self.moveTimerActive = False  # To keep track if move timer is active or not
        self.enemies = {}  # Store all enemies
        self.enemyType = ['crab', 'octo']  # Types of enemies. Used by frontend to draw the appropriate image

    def __clamp(self, minAllowed, maxAllowed, value):
        """
        Internal Helper function used to clamp a value to its min or max if it crosses it
        """
        if value < minAllowed or value > maxAllowed:
            minDif = abs(value - minAllowed)
            maxDif = abs(value - maxAllowed)
            if minDif > maxDif:
                return maxAllowed
                # Closer to max
            else:
                return minAllowed
        return value

    def __moveEnemies(self):
        """
        Moves all the enemies in the list to a specific direction depending on it's
        "move" key.
        Enemies that spawn at the top will have its "move" set as "down" implying
        that the char needs to move down
        :return:
        """
        try:  # Since we are multi threading the elements may be deleted mid iteration
            speed = 1
            for k, v in self.enemies.items():
                addX = 0
                addY = 0
                move = v['move']

                # For Up Down
                if move == 'DOWN' or 'UP':
                    # X first
                    if random.randint(-50, 50) % 2 == 0:
                        if random.randint(-50, 50) % 2 == 0:
                            addX = speed
                        else:
                            addX = speed * -1
                    newX = v['x'] + addX

                    # Clamp newX if needed
                    newX = self.__clamp(minAllowed=0, maxAllowed=self.width - 50, value=newX)

                    # Y now
                    addY = speed if move == 'DOWN' else (speed * -1)
                    newY = v['y'] + addY
                    # Delete if we hit boundary
                    newY = self.__clamp(minAllowed=0, maxAllowed=self.height - 50, value=newY)
                    if newY == 0 or newY == self.height - 50:
                        self.enemies.pop(k)
                        return
                    self.enemies[k] = {
                        'x': newX,
                        'y': newY,
                        'move': v['move'],
                        'etype': v['etype']
                    }

                if move == 'RIGHT' or move == 'LEFT':
                    if random.randint(-50, 50) % 2 == 0:
                        if random.randint(-50, 50) % 2 == 0:
                            addY = speed
                        else:
                            addY = speed * -1

                    newY = v['y'] + addY
                    # Clamp newY if needed
                    newY = self.__clamp(minAllowed=0, maxAllowed=self.height - 50, value=newY)

                    # X now
                    addX = speed if move == 'RIGHT' else speed * -1
                    newX = addX + v['x']
                    # If we hit boundary delete
                    newX = self.__clamp(minAllowed=0, maxAllowed=self.width - 50, value=newX)
                    if newX == 0 or newX == self.width - 50:
                        self.enemies.pop(k)
                        return
                self.enemies[k] = {
                    'x': newX,
                    'y': newY,
                    'move': v['move'],
                    'etype': v['etype']
                }
        except:
            pass

    def __createEnemy(self):
        try:
            EnemySpawnData = [
                {
                    # Enemy will spawn on random X and Top Y and will move down gradually
                    'x': random.randint(0, self.width - 50),
                    'y': 0,
                    'move': 'DOWN',
                    'etype': random.choice(self.enemyType),
                },
                {
                    # Enemy will spawn on random X and Bottom Y and will move up gradually
                    'x': random.randint(0, self.width - 50),
                    'y': self.height - 50,
                    'move': 'UP',
                    'etype': random.choice(self.enemyType),

                },
                {
                    # Enemy will spawn on random Y and Left X and will move Right gradually
                    'x': 0,
                    'y': random.randint(0, self.height - 50),
                    'move': 'RIGHT',
                    'etype': random.choice(self.enemyType),
                },
                {
                    # Enemy will spawn on random Y and Right X and will move Left gradually
                    'x': self.width - 50,
                    'y': random.randint(0, self.height - 50),
                    'move': 'LEFT',
                    'etype': random.choice(self.enemyType),
                }
            ]
            randEnemyData = random.choice(EnemySpawnData)
            uid = str(uuid.uuid4())  # Generate UID for the enemy

            # This will look like
            # {654 : {x:34, y : 0, move : LEFT, type : crab}}
            self.enemies[uid] = {
                'x': randEnemyData['x'],
                'y': randEnemyData['y'],
                'etype': randEnemyData['etype'],
                'move': randEnemyData['move']
            }
            print(
                f"Created Enemy at position {self.enemies[uid]['x']} {self.enemies[uid]['y']} move : {self.enemies[uid]['move']}")
        except:
            pass

    def startSpawnTimer(self):
        print("Spawn TIMER ACTIVE\n")
        """
        Needs to run in a multi thread env.
        Adds enemy to enemies list after certain interval of time
        Timer resets when an enemy is removed from the enemies list.
        Enemies are removed from list when it goes out of bound or is killed by client
        """
        while True:
            if len(self.enemies) < 10:
                self.__createEnemy()
            time.sleep(15)

    def startMoveTimer(self):
        """
        For all the enemies in the list, it moves their position after a certain period of time
        """
        print("Move timer ACTIVE\n")
        while True:
            time.sleep(0.01)
            self.__moveEnemies()

    def removeEnemy(self, UID):
        """
        Delete an enemy from the enemies list
        :param UID: the UID of the enemy to remove
        """
        pass

    def getEnemies(self):
        # If enemies dict is empty
        if not self.enemies:
            self.__createEnemy()  # Created first enemy

        # Start timers if not started
        if not self.spawnTimerActive:
            self.spawnTimerActive = True
            start_new_thread(self.startSpawnTimer, ())
        if not self.moveTimerActive:
            self.moveTimerActive = True
            start_new_thread(self.startMoveTimer, ())

        return self.enemies

    def enemyHit(self, x, y, acceptedRange):
        kills = []
        try:
            for k, v in self.enemies.items():
                enemyX = v['x'] + 20
                enemyY = v['y'] + 20
                difX = abs(enemyX - x)
                difY = abs(enemyY - y)
                if difX < acceptedRange and difY < acceptedRange:
                    # Delete the enemy
                    hitX = v['x']
                    hitY = v['y']
                    etype = v['etype']
                    kills.append({'x': hitX, 'y': hitY, 'type': etype})
                    self.enemies.pop(k)
            return kills
        except:
            return kills
