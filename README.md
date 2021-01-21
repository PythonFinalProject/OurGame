# OurGame - The ZombiNTU

Hi there! This is our final project of the course EE1004 Computer Programming at National Taiwan University (NTU). We created this game using the programming language Python and the game-design module Pygame. Hope you will like it!

## Story
ZombiNTU is a survival horror video game featuring the elements at NTU. The game's story revolves around the student's life at the time of 2050, where the campus was occupied by tons of zombies after the massive invasion in 2020. According to humans' last message back then, the zombies climb out from brown underground tunnels at the northwest and southeast corners. Also, the abundance of coconuts on the campus serves as the only means for survival, and it is said that there are weapons and magic inside. The predecessors already created some accelerating tunnels and shelter blocks in the campus, which provide you a way to hide or escape from the zombies. Be noticed that if the number of zombies exceeds 30, the campus will collapse... You are our last hope to defend the territory and honor of NTU.

![](https://i.imgur.com/UWpPnSS.png)

## File structure
```
.
├── README.md
├── character.py
├── tilemap.py
├── main.py
├── materials
└── score.csv
```

## Dependent python libraries
numpy == 1.19.5  
pandas == 1.2.0  
pygame == 2.0.1  
python-dateutil == 2.8.1  
PyTMX == 3.24  
pytz == 2020.5  
six == 1.15.0  

## Code description
 - main.py:
    - This is where we run the main loop
    - Currently the FPS of the game is set to 60
 - character.py:
    - We build class Charater, Player, Enemy, Bullet and Coconut. Notice that classes Player and Enemy are inharitted from class Character
 - tilemap.py:
    - Where we build class related to the background map, Tiledmap, Camera, Obstacle, Proof and Block. 
 - materials:
    - Where we store the game images, including characters' sprite sheets, background picture, and so on

## Game instruction
1. `git clone https://github.com/PythonFinalProject/OurGame.git`
2. Run the main.py and you will have a pop up window.
3. If you need any assist during the game, click SET and then HELP on the game window.


## Bug and Problem report
- ZeroDivisionError: float division by zero (12/27):
    - seldom happened.  In character.py,line 183,  self.x += self.vel*dx/dl     dl = 0???

- python pass by value or reference (12/21):
    - In order to force python pass the variable "run" as reference, Nelson set "run" as a list "[True]"

- arrow key "UP" didn't work in 2P mode (12/21):
    - Previously Nelson used arrow keys to control the second player but faced some problem: the second player couldn't shoot bullets while moving up. After changing control keys to "IJKL", everything works perfect

- PNG warning (12/21):
    - Previouly everytime Nelson created character using the png file "blue_woman_sprite.png" and "skull_sprite.png", the command window would print out warning message: "libpng warning: iCCP: known incorrect sRGB profile". This issue was caused because Libpng-1.6 is more stringent about checking ICC profiles than previous versions. We can ignore the warning. To get rid of it, remove the iCCP chunk from the PNG image by running the command "mogrify *.png" (Nelson ran it in WSL2 device, might not be able to run in Windows powershell)

## Game detail information
- chen

  ![](https://i.imgur.com/OnOvF2S.png)
  
  Before starting the main game loop, we create a game interface to enhance user's gameplay experience.  
  
  For example, players can choose either single or cooperative mode or get help by clicking Set button.
  
  After the game starts, some basic game information are displayed on the game window, for example, players' health, current weapon, and the bullet left for special weapon     (So don't relax even if you get really strong weapon!). The game ends if all the players died or more than 30 enemies appear on the map (Notice the "Warning" for the         latter) .
  
  Another game interface design is displayed if the game ends. The Score displayed the top ten highest scores recorded (the score are recorded automatically) and users can     easily reset the score record if they want. Click "Again" to restart a game.
  
- ChiaLingWeng

  ![](https://imgur.com/NuBjZtA)
  
  There are 3 different types of objects in our maps, Stone, Proof and Block.
  
  -Stone:
  It acts as an obstacle for Characters moving on x axis, but an accelerating tunnel for Characters moving on y axis. 
  
  -Proof:
  Just as literally, this kind of object is bullet-proof and the bullet will disappear after colliding with it.
  
  -Block:
  Different from Stone, Characters can't pass it from any direction, but it's destroyable with bullet.
  


