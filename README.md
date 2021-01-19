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
    - We build class Charater, Player, Enemy, and Bullet. Notice that classes Player and Enemy are inharitted from class Character


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
  
  The game has "while" to make itself work continuously and use "if else" to decise how to work with parametrics. There are some buttons contraling them  in the game. 
  
  Before playing the game, players can choose single or cooperative mold and get help by use "set".
  
  When the game start, platers can cleared see role's left boold. If they get some new weapons by eating coconuts, the bollet limit of new weapons will disolay on the top of role. The game end when all roles died and there are more than 30 enemys on the map to avoid the computer crashes.
  
  If players want to look at their score, press down "score" after gameover. The top ten of the scores will be recorded and the record can be clear conveniently. If players want to play again, press down "again".
