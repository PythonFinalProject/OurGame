import pygame
pygame.init()

win_width = 480
win_height = 480
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('First Game')
sprite_sheet = pygame.image.load('Game/blue_woman_sprite.png') # 594 * 261 (9 * 4)
clock = pygame.time.Clock()

x = 50
y = 200
width = 594 // 9
height = 261 // 4
vel = 6
left = False
right = False
up = False
down = False
walkcount = 0

walk_R = []
walk_L = []
walk_U = []
walk_D = []

char_sheet = [walk_U, walk_L, walk_D, walk_R]

bg = pygame.image.load('Game/bg.jpg')
# char = sprite_sheet.subsurface((0, 0, width, height))

for i in range(4):
    for j in range(9):
        char_sheet[i].append(sprite_sheet.subsurface((width*j, height*i, width, height)))

char = char_sheet[2][0]


def redrawGameWindow():
    global walkcount
    win.blit(bg, (0, 0))
    if walkcount + 1 >= 20:
        walkcount = 0
    if left:
        win.blit(walk_L[walkcount//5], (x, y))
        walkcount += 1
    elif right:
        win.blit(walk_R[walkcount//5], (x, y))
        walkcount += 1
    elif up:
        win.blit(walk_U[walkcount//5], (x, y))
        walkcount += 1
    elif down:
        win.blit(walk_D[walkcount//5], (x, y))
        walkcount += 1
    else:
        win.blit(char, (x, y))
    pygame.display.update()

# main loop
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    print("l", left, "r", right, "u", up, "d", down, "key_a", keys[pygame.K_a])

    if keys[pygame.K_a] and x > 0:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_d] and x < win_width - width:
        x += vel
        right = True
        left = False
    if keys[pygame.K_w] and y > 0:
        y -= vel
        up = True
        down = False
    elif keys[pygame.K_s] and y < win_height - height:
        y += vel
        down = True
        up = False
    if keys[pygame.K_a] == 0 and keys[pygame.K_d] == 0 and keys[pygame.K_s] == 0 and keys[pygame.K_w] == 0:
        right = False
        left = False
        down = False
        up = False
        walkcount = 0


    if keys[pygame.K_q]:
        run = False

    redrawGameWindow()

pygame.quit()