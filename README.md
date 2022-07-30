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
5.

<br>

6. 2 Types of animation we have and how they work