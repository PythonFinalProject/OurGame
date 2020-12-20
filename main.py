import pygame
import random

pygame.init()

win_width = 480
win_height = 480
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()

bg = pygame.image.load('Game/bg.jpg')

class Character():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.health = 100
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.walk_up = []
        self.walk_down = []
        self.walk_left = []
        self.walk_right = []
        self.walk_pause = None
        self.walkcount = 0
    
    def set_hitbox(self, x_offset, y_offset, width, height):
        self.hitbox = (self.x + x_offset, self.y + y_offset, width, height)

    def extract_from_sprite_sheet(self, image_source, dir, steps):
        sprite_sheet = pygame.image.load(image_source)
        self.walk_sheet = [self.walk_up, self.walk_left, self.walk_down, self.walk_right]
        for i in range(dir):
            for  j in range(steps):
                self.walk_sheet[i].append(sprite_sheet.subsurface((self.width*j, self.height*i, self.width, self.height)))
        self.walk_pause = self.walk_sheet[2][0]
    
    def draw(self, win, frames=3):
        if self.walkcount + 1 >= frames*9:
            self.walkcount = 0
        if self.left:
            win.blit(self.walk_left[self.walkcount//frames], (self.x, self.y))
            self.walkcount += 1
        elif self.right:
            win.blit(self.walk_right[self.walkcount//frames], (self.x, self.y))
            self.walkcount += 1
        elif self.up:
            win.blit(self.walk_up[self.walkcount//frames], (self.x, self.y))
            self.walkcount += 1
        elif self.down:
            win.blit(self.walk_down[self.walkcount//frames], (self.x, self.y))
            self.walkcount += 1
        else:
            win.blit(self.walk_pause, (self.x, self.y))

class Player(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def control(self):
        global run
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.vel
            self.left = True
            self.right = False
        elif keys[pygame.K_d] and self.x < win_width - self.width:
            self.x += self.vel
            self.right = True
            self.left = False
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.vel
            self.up = True
            self.down = False
        elif keys[pygame.K_s] and self.y < win_height - self.height:
            self.y += self.vel
            self.down = True
            self.up = False
        if keys[pygame.K_a] == 0 and keys[pygame.K_d] == 0 and keys[pygame.K_s] == 0 and keys[pygame.K_w] == 0:
            self.right = False
            self.left = False
            self.down = False
            self.up = False
            self.walkcount = 0
        if keys[pygame.K_q]:
            run = False

# 576*256
class Enemy(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vel = 2
    
    def chase(self, player):
        dx = (player.x - self.x) + random.randrange(-200, 200, 1)
        dy = (player.y - self.y) + random.randrange(-200, 200, 1)
        dl = (dx**2 + dy**2)**0.5
        self.x += self.vel*dx/dl
        self.y += self.vel*dy/dl
        
        if dx > 0:
            self.right = True
            self.left = False
        else:
            self.left = True
            self.right = False
        if dy > 0:
            self.down = True
            self.up = False
        else:
            self.up = True
            self.down = False

        if abs(dx) > abs(dy):
            self.up = False
            self.down = False
        else:
            self.right = False
            self.left = False

        if dx == 0 and dy == 0:
            self.right = False
            self.left = False
            self.up = False
            self.down = False

        print("right", self.right, "left", self.left, "up", self.up, "down", self.down, "dx", dx, "dy", dy)

def redrawGameWindow(win):
    win.blit(bg, (0, 0))
    player.draw(win)
    for enemy in enemy_list:
        enemy.draw(win)
    pygame.display.update()

# Initialize
player = Player(300, 410, 591//9, 261//4)
player.set_hitbox(0, 0, 594//9, 261//4)
player.extract_from_sprite_sheet('Game/blue_woman_sprite.png', 4, 9)

N = 5
enemy_list = []
for i in range(N):
    enemy_list.append(Enemy(random.randrange(1, 400, 1), random.randrange(1, 400, 1), 576//9, 256//4))
    enemy_list[i].set_hitbox(0, 0, 576//9, 261//4)
    enemy_list[i].extract_from_sprite_sheet('Game/skull_sprite.png', 4, 9)
# enemy = Enemy(random.randrange(1, 400, 1), random.randrange(1, 400, 1), 576//9, 256//4)
# enemy.set_hitbox(0, 0, 576//9, 261//4)
# enemy.extract_from_sprite_sheet('Game/skull_sprite.png', 4, 9)


# main loop
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False 
    player.control()
    # enemy.chase(player)
    for enemy in enemy_list:
        enemy.chase(player)
    redrawGameWindow(win)

pygame.quit()