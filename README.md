# OurGame

## Quick View
![](https://i.imgur.com/zZ4BIQO.png)

## File structure
```
.
├── README.md
├── __pycache__
│   ├── character.cpython-36.pyc
│   └── character.cpython-38.pyc
├── character.py
├── main.py
├── main_test.py
├── materials
│   ├── bg.jpg
│   ├── blue_woman_sprite.png
│   └── skull_sprite.png
└── source.md
```
## Code description
 - main.py:
    - This is where we run the main loop
    - Currently the FPS of the game is set to 60
 - character.py:
    - We build class Charater, Player, Enemy, Bullet and Coconut. Notice that classes Player and Enemy are inharitted from class Character
 - tilemap.py:
    - Where we build class related to the background map, Tiledmap, Camera, Obstacle, Proof and Block. 


## Bug and Problem report
- ZeroDivisionError: float division by zero (12/27):
    - seldom happened.  In character.py,line 183,  self.x += self.vel*dx/dl     dl = 0???

- python pass by value or reference (12/21):
    - In order to force python pass the variable "run" as reference, Nelson set "run" as a list "[True]"

- arrow key "UP" didn't work in 2P mode (12/21):
    - Previously Nelson used arrow keys to control the second player but faced some problem: the second player couldn't shoot bullets while moving up. After changing control keys to "IJKL", everything works perfect

- PNG warning (12/21):
    - Previouly everytime Nelson created character using the png file "blue_woman_sprite.png" and "skull_sprite.png", the command window would print out warning message: "libpng warning: iCCP: known incorrect sRGB profile". This issue was caused because Libpng-1.6 is more stringent about checking ICC profiles than previous versions. We can ignore the warning. To get rid of it, remove the iCCP chunk from the PNG image by running the command "mogrify *.png" (Nelson ran it in WSL2 device, might not be able to run in Windows powershell)

## contents
- chen

  ![](https://i.imgur.com/OnOvF2S.png)
  
  Before starting the main game loop, we create a game interface to enhance user's gameplay experience.  
  
  For example, players can choose either single or cooperative mode or get help by clicking Set button.
  
  After the game starts, some basic game information are displayed on the game window, for example, players' health, current weapon, and the bullet left for special weapon (So don't relax even if you get really strong weapon!). The game ends if all the players died or more than 30 enemies appear on the map (Notice the "Warning" for the latter).
  
  Another game interface design is displayed if the game ends. The Score button displayed the top ten highest scores recorded(automatically) and the record can be clear if you want a brandnew start :) Press "Again" to restart a game.
