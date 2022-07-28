import time
import uuid
import random
from _thread import *


# noinspection PyMethodMayBeStatic
class EnemyHandler:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spawnTimerActive = False
        self.moveTimerActive = False
        self.enemies = {}
        self.enemyType = ['crab', 'octopus']

    def __moveEnemies(self):
        for k, v in self.enemies.items():
            pass

    def __createEnemy(self):
        EnemySpawnData = [
            {
                # Enemy will spawn on random X and Top Y and will move down gradually
                "move": 'DOWN',
                'x': random.randint(0, self.x - 50),
                'y': 0
            },
            {
                # Enemy will spawn on random X and Bottom Y and will move up gradually
                "move": 'UP',
                'x': random.randint(0, self.x - 50),
                'y': self.y - 50
            },
            {
                # Enemy will spawn on random Y and Left X and will move Right gradually
                "move": 'RIGHT',
                'x': 0,
                'y': random.randint(0, self.y - 50)
            },
            {
                # Enemy will spawn on random Y and Right X and will move Left gradually
                "move": 'LEFT',
                'x': self.x - 50,
                'y': random.randint(0, self.y - 50)
            }
        ]
        randEnemyData = random.choice(EnemySpawnData)
        uid = str(uuid.uuid4())  # UID for the enemy
        # This will look like
        # {654 : {x:34, y : 0, move : LEFT, type : crab}}
        self.enemies[uid] = {
            'x': randEnemyData['x'],
            'y': randEnemyData['y'],
            'move': randEnemyData['move'],
            'type': random.choice(self.enemyType)
        }
        print(f"Created Enemy at position {self.enemies[uid]['x']} {self.enemies[uid]['y']}")

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
            time.sleep(0.5)
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
            # start_new_thread(self.startMoveTimer, ())

        return self.enemies
