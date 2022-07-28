import uuid
import random
from _thread import *


# noinspection PyMethodMayBeStatic
class EnemyHandler:
    def __init__(self, width, height):
        self.spawnTimerThreshold = 12
        self.currentSpawnTimer = 0

        self.moveTimerThreshold = 50
        self.currentMoveTimer = 0

        self.spawnTimerActive = False
        self.moveTimerActive = False
        self.enemies = {}
        self.EnemySpawnData = [
            {
                # Enemy will spawn on random X and Top Y and will move down gradually
                "move": 'DOWN',
                'x': random.randint(0, width - 50),
                'y': 0
            },
            {
                # Enemy will spawn on random X and Bottom Y and will move up gradually
                "move": 'UP',
                'x': random.randint(0, width - 50),
                'y': height - 50
            },
            {
                # Enemy will spawn on random Y and Left X and will move Right gradually
                "move": 'RIGHT',
                'x': 0,
                'y': random.randint(0, height - 50)
            },
            {
                # Enemy will spawn on random Y and Right X and will move Left gradually
                "move": 'LEFT',
                'x': width - 50,
                'y': random.randint(0, height - 50)
            }
        ]
        self.enemyType = ['crab', 'octopus']

    def __moveEnemies(self):
        pass

    def __createEnemy(self):
        randEnemyData = random.choice(self.EnemySpawnData)
        uid = str(uuid.uuid4())  # UID for the enemy
        # This will look like
        # {654 : {x:34, y : 0, move : LEFT, type : crab}}
        self.enemies[uid] = {
            'x': randEnemyData['x'],
            'y': randEnemyData['y'],
            'move': randEnemyData['move'],
            'type': random.choice(self.enemyType)
        }
        print(self.enemies)

    def startSpawnTimer(self):
        print("Spawn TIMER ACTIVE\n")
        """
        Needs to run in a multi thread env.
        Adds enemy to enemies list after certain interval of time
        Timer resets when an enemy is removed from the enemies list.
        Enemies are removed from list when it goes out of bound or is killed by client
        """
        while True:
            self.currentSpawnTimer += 1

            if self.currentSpawnTimer >= self.spawnTimerThreshold:
                # Time to spawn more enemies if its less than equal to 4
                if len(self.enemies) < 4:
                    self.__createEnemy()
                else:
                    print("Already 4 Enemies exist")
                self.currentSpawnTimer = 0

    def startMoveTimer(self):
        """
        For all the enemies in the list, it moves their position after a certain period of time
        """
        print("Move timer ACTIVE\n")
        while True:

            self.currentMoveTimer += 1

            if self.currentMoveTimer >= self.moveTimerThreshold:
                self.__moveEnemies()
                self.currentMoveTimer = 0

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
            # start_new_thread(self.startMoveTimer, ())

        return self.enemies
