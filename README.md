# Aqua Mayhem Multiplayer

2D Top down Multiplayer game using PyGame And bare bone python's socket for the backend. Fairly easy, the hard part was
the multiplayer and making everything sync up perfectly with each client. It's not perfect, no where close To being
perfect But I am fairly okay with the result so decided to stop after few tweaks.

Enemy position, Enemy Spawn, are 100% server sided meaning server is responsible for spawning and moving enemies. The
player/ Clients can only request the data of the enemy

<br>
HOW TO RUN:
<br>
1. Start server.py in backend folder <br>
2. Start Global.py in fronend folder


<br>


Features

1. Top Down View
2. Multiple Clients can connect and play together
3. NPC enemies that will move around
4. Shoot the enemies with mouse click
5. Fully network replicated and functioning multiplayer
6. Animating sprites for NPCs and Background

<br>

**topics to talk about in presentation are :**

**General Flow of the program (Both Client and server)**
<br>Talk about how server stores clients and multithread dedicated while loop for each client when talking about server
WITH FLOWCHART<br>

**The way the payload that is sent between client and server is structured**
<br>SHOW IMAGE and Example <br>

1. Multi threading in our program
2. Character movement system and (Start from mainloop->draw, then mainLoop->listenInput(), then serverHandler->
   sendEssentialData()->sendPlayersPOS->ServerUpdatingPlayerPOS list)
3. How characters are synced across different clients(sendEssentialData->server listen-> send back players list->client
   sending this to guestService.updatePlayerPOS->mainLoop.guestService.draw().
4. Enemy Spawn system and move system
   <br>
   The flow of this system is fairly long so.....

   <br>
   In sendEssentialData we request EnemyPOS. Server listens this and calls enemyHandler.getEnemies and returns it back to the client




<br>

6. 2 Types of animation we have and how they work
7. Enemy Shoot System, kill system and explosion system
   1. In main loop listen for mouse event
   2. call serverHandler.sendShoot(xy) mouse pos
      1. sendShoot : informs the server about this event
      2. Server listens and starts a broadcast in a new thread, it does this because it needs to loop through every
         single player and notify them that a client has shot but if we run it in the current thread the whole program
         will be frozen until the loop is over and that iis not intended so we start a new thread for broadcasting it
         1. BroadCast:
         2. loops through each connected client and sends then the data
         3. calls enemyHandler.checkHit(xy)
            1. checkHit:
            2. Loops through all enemy and checks if they are close to hit position
            3. if they are we store them in a temporary list and remove them from the class's enemy list
            4. we then return this
         4. BroadCast:
         5. Checks if we killed any enemy (i.e checks if list is empty or not)
         6. if the shot killed an enemy we are going to broadcast this info as well in a new thread
   3. Client :
   4. client listens that a player has shot and calls guestService.updateShoot
   5. update shoot will then add a new shoot record that needs to be drawn in the main loop
   6. client listens that an enemy has been killed and calls effect.updateBoom
   7. we add a boom record and the draw function will take care of animating the boom in the given XY coordinate