# Stranger Bubble

This is a coop network game for two players (network is necessary because each player has to have his own screen/display for this to work).

The aim of the game is for BOTH players to MEET at the same spot in the map.
However, each player lives in his own "bubble" and therefore has limited information about his surroundings, i.e. some parts of each player's screen are covered.

Thus, for walking around the map, sometimes each player has to ask the other player whether it's safe to walk across a covered part of the map, because there might be hazards like lava, deadly skulls, or mines.

Take care of the following aspects:
- Each player has to open a door in order to make the meeting happen. The door is opened by collecting 3 keys in a consecutive order (each key is only visible once the previous key has been collected).
- The skulls are not visible for the co-player, so be careful when taking his advice.
- The mines can be temporarily deactivated by having the co-player step on his "magic bubble"

Have fun!

![stranger-bubble-ingame](https://github.com/user-attachments/assets/7edc384f-e232-4331-bfbe-7e14635433d8)


# network info

- Start the game on one computer and select "START GAME"
- Start the executable on another computer within the same network (not over the internet!) and select "JOIN GAME"
- Wait until JOINer (client) discovers STARTer (server), then hit space as JOINer
- The game should run now

- You can add specific hosts (also via internet!) into a settings.py:

KNOWN_SERVERS = [('example 1', ('ip address or hostname', port)),
                 ('example 2', ('ip address or hostname', port)),
                 ]


# how to run from source
note: requires python3.8+ and pygame2+

cd into the source directory and enter the following command:
```
 python3 .
```

