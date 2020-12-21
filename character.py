import pygame
import random

CREATE_ENEMY_EVENT = pygame.USEREVENT

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
        self.right = True
        self.set_hitbox(15, 5, self.width-35, self.height-10)
        self.extract_from_sprite_sheet('Game/blue_woman_sprite.png', 4, 9)
        self.player_selection = {"1P": {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "shoot": pygame.K_SPACE}, "2P": {"left": pygame.K_j, "right": pygame.K_l, "up": pygame.K_i, "down": pygame.K_k, "shoot": pygame.K_SLASH}}
        self.bullet_list = []
        self.shootLoop = 0
        self.shootCoolDown = 5

    def control(self, run, win_width, win_height, num_player):
        keys = pygame.key.get_pressed()
        player_control = self.player_selection[num_player]
        
        if not keys[player_control["left"]] and not keys[player_control["right"]] and not keys[player_control["up"]] and not keys[player_control["down"]]:
            # self.right = False
            # self.left = False
            # self.down = False
            # self.up = False
            self.walkcount = 0
        elif keys[player_control["left"]] and not keys[player_control["right"]] and not keys[player_control["up"]] and not keys[player_control["down"]] and self.x > 0:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.up = False
            self.down = False
        elif keys[player_control["right"]] and not keys[player_control["left"]] and not keys[player_control["up"]] and not keys[player_control["down"]] and self.x < win_width - self.width:
            self.x += self.vel
            self.right = True
            self.left = False
            self.up = False
            self.down = False
        elif keys[player_control["up"]] and not keys[player_control["down"]] and not keys[player_control["right"]] and not keys[player_control["left"]] and self.y > 0:
            self.y -= self.vel
            self.up = True
            self.down = False
            self.right = False
            self.left = False
        elif keys[player_control["down"]] and not keys[player_control["up"]] and not keys[player_control["right"]] and not keys[player_control["left"]] and self.y < win_height - self.height:
            self.y += self.vel
            self.down = True
            self.up = False
            self.right = False
            self.left = False
        elif keys[player_control["left"]] and keys[player_control["up"]] and not keys[player_control["right"]] and not keys[player_control["down"]] and self.x > 0 and self.y > 0:
            self.x -= self.vel
            self.y -= self.vel
            self.left = True
            self.right = False
            self.up = True
            self.down = False
        elif keys[player_control["left"]] and keys[player_control["down"]] and not keys[player_control["right"]] and not keys[player_control["up"]] and self.x > 0 and self.y < win_height - self.height:
            self.x -= self.vel
            self.y += self.vel
            self.left = True
            self.right = False
            self.down = True
            self.up = False
        elif keys[player_control["right"]] and keys[player_control["up"]] and not keys[player_control["left"]] and not keys[player_control["down"]] and self.x < win_width - self.width and self.y > 0:
            self.x += self.vel
            self.y -= self.vel
            self.left = False
            self.right = True
            self.up = True
            self.down = False
        elif keys[player_control["right"]] and keys[player_control["down"]] and not keys[player_control["left"]] and not keys[player_control["up"]] and self.x < win_width - self.width and self.y < win_height - self.height:
            self.x += self.vel
            self.y += self.vel
            self.left = False
            self.right = True
            self.up = False
            self.down = True

        if keys[player_control["shoot"]]:
            if self.shootLoop == 0:
                self.shoot()
        if keys[pygame.K_q]:
            run[0] = False

        # print("right", self.right, "left", self.left, "up", self.up, "down", self.down)

    def draw(self, win, frames=3):
        super().draw(win, frames)
        self.set_hitbox(15, 5, self.width - 35, self.height - 10)
        # draw hitbox
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.health -= 1
        # print(self.health)
        # font1 = pygame.font.SysFont('comicsans', 100)
        # text = font1.render("hit", 1, (255, 0, 0))
        # # print(self.health)
        # win.blit(text, ((win_width - text.get_width()) // 2, (win_height - text.get_height()) // 2))
        # pygame.display.update()

    def shoot(self):
        facing = [0, 0]
        if self.right:
            facing[0] = 1
        elif self.left:
            facing[0] = -1
        if self.up:
            facing[1] = -1
        elif self.down:
            facing[1] = 1
        # if (self.right or self.left) and (self.up or self.down):
        #     facing = [x*(2**0.5) for x in facing]
        self.bullet_list.append(Bullet(x=self.x+self.width//2, y=self.y+self.height//2, facing=facing))

# 576*256
class Enemy(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.target = None
        self.set_hitbox(15, 10, self.width - 35, self.height - 10)
        self.extract_from_sprite_sheet('Game/skull_sprite.png', 4, 9)
        self.vel = 1
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 200) # Create enemy every 1 sec
    
    def chase(self, player):
        dx = (player.x - self.x)# + random.randrange(-200, 200, 1)
        dy = (player.y - self.y)# + random.randrange(-200, 200, 1)
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

        # print("right", self.right, "left", self.left, "up", self.up, "down", self.down, "dx", dx, "dy", dy)

    def draw(self, win, frames=3):
        super().draw(win, frames)
        self.set_hitbox(15, 10, self.width - 35, self.height - 10)
        # draw hitbox
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class Bullet():
    def __init__(self, x, y, facing, radius=6, color=(0, 0, 0), vel=8):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8
    
    def fly(self):
        self.x += self.vel * self.facing[0]
        self.y += self.vel * self.facing[1]

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def out(self, win_width, win_height):
        if self.x < 0 or self.x > win_width or self.y < 0 or self.y > win_height:
            return True
        else:
            return False
    
    def hit(self):
        pass
