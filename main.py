import pygame
import random
from character import Player, Enemy

pygame.init()

win_width = 480
win_height = 480
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()

CREATE_ENEMY_EVENT = pygame.USEREVENT

bg = pygame.image.load('Game/bg.jpg')


def redrawGameWindow(win):
    win.blit(bg, (0, 0))
    for player in player_list:
        player.draw(win)
    for enemy in enemy_list:
        enemy.draw(win)
    pygame.display.update()

def checkPlayEnemyCollision(player):
    player_hb_0 = player.hitbox[0]
    player_hb_1 = player.hitbox[1]
    player_hb_2 = player.hitbox[2]
    player_hb_3 = player.hitbox[3]
    for enemy in enemy_list:
        enemy_hb_0 = enemy.hitbox[0]
        enemy_hb_1 = enemy.hitbox[1]
        enemy_hb_2 = enemy.hitbox[2]
        enemy_hb_3 = enemy.hitbox[3]
        if player_hb_1 + player_hb_3 > enemy_hb_1 and player_hb_1 < enemy_hb_1 + enemy_hb_3 and player_hb_0 + player_hb_2 > enemy_hb_0 and player_hb_0 < enemy_hb_0 + enemy_hb_2:
            player.hit()

def checkEnemyEnemyCollision():
    for i in range(len(enemy_list)-1, -1, -1):
        collision = False
        first = enemy_list[i]
        first_hb_0 = first.hitbox[0]
        first_hb_1 = first.hitbox[1]
        first_hb_2 = first.hitbox[2]
        first_hb_3 = first.hitbox[3]
        for j in range(i-1, -1, -1):
            # if i == j:
            #     continue
            second = enemy_list[j]
            second_hb_0 = second.hitbox[0]
            second_hb_1 = second.hitbox[1]
            second_hb_2 = second.hitbox[2]
            second_hb_3 = second.hitbox[3]
            if first_hb_1 + first_hb_3 > second_hb_1 and first_hb_1 < second_hb_1 + second_hb_3 and first_hb_0 + first_hb_2 > second_hb_0 and first_hb_0 < second_hb_0 + second_hb_2:
                collision = True
                # print("collision")
                break
        if collision == False:
            first.chase(player_list[first.target])

# Initialize player
# player = Player(300, 410, 591//9, 261//4)
player_list = []
for i in range(2):
    player_list.append(Player(random.randrange(1, 400, 1), random.randrange(1, 400, 1), 591//9, 261//4))

# Initialize enemy
N = 1
enemy_list = []
for i in range(N):
    enemy_list.append(Enemy(random.randrange(1, 400, 1), random.randrange(1, 400, 1), 576//9, 256//4))
    enemy_list[i].target = random.randrange(0, len(player_list), 1)

# main loop
run = [True]
while run[0]:
    clock.tick(60) # Set FPS

    # Check if the window is closed
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run[0] = False 
        elif event.type == CREATE_ENEMY_EVENT:
            # This will create enemy every 0.2 sec
            enemy_list.append(Enemy(random.randrange(1, 400, 1), random.randrange(1, 400, 1), 576//9, 256//4))
            enemy_list[-1].target = random.randrange(0, len(player_list), 1)

    checkEnemyEnemyCollision()
    # Moving the player with "WASD"
    player_selection = ["1P", "2P"]
    for i, player in enumerate(player_list):
        checkPlayEnemyCollision(player)
        player.control(run, win_width, win_height, player_selection[i])

    print(len(player_list))

    redrawGameWindow(win)

pygame.quit()