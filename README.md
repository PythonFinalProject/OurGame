# OurGame

## Quick View

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
- python pass by value or reference (12/21):
    - In order to force python pass the variable "run" as reference, Nelson set "run" as a list "[True]"

- arrow key "UP" didn't work in 2P mode (12/21):
    - Previously Nelson used arrow keys to control the second player but faced some problem: the second player couldn't shoot bullets while moving up. After changing control keys to "IJKL", everything works perfect

- PNG warning (12/21):
    - Previouly everytime Nelson created character using the png file "blue_woman_sprite.png" and "skull_sprite.png", the command window would print out warning message: "libpng warning: iCCP: known incorrect sRGB profile". This issue was caused because Libpng-1.6 is more stringent about checking ICC profiles than previous versions. We can ignore the warning. To get rid of it, remove the iCCP chunk from the PNG image by running the command "mogrify *.png" (Nelson ran it in WSL2 device, might not be able to run in Windows powershell)