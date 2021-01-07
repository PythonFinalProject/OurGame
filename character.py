import pygame
import math
import random
import copy
import threading 


CREATE_ENEMY_EVENT = pygame.USEREVENT
CREATE_COCONUT_EVENT = pygame.USEREVENT + 1

class Character():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.health = 5
        self.healthmax = self.health  #繪製血條用
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        # self.walk_up = []
        # self.walk_down = []
        # self.walk_left = []
        # self.walk_right = []
        # self.walk_sheet = []
        # self.hitbox = None
        self.walk_pause = None
        self.walkcount = 0
    
    def set_hitbox(self, x_offset, y_offset, width, height):
        self.hitbox = (self.x + x_offset, self.y + y_offset, width, height)

    def extract_from_sprite_sheet(self, image_source, dir, steps):
        sprite_sheet = pygame.image.load(image_source)
        self.walk_sheet = []
        self.walk_up = []
        self.walk_down = []
        self.walk_right = []
        self.walk_left = []
        self.walk_sheet = [self.walk_up, self.walk_left, self.walk_down, self.walk_right]
        for i in range(dir):
            for  j in range(steps):
                self.walk_sheet[i].append(sprite_sheet.subsurface((self.width*j, self.height*i, self.width, self.height)))
        self.walk_pause = self.walk_sheet[2][0]

        # self.walk_sheet[0][0] = pygame.transform.scale(self.walk_sheet[0][0], (20, 20))
    
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
        self.DIR = 4
        self.STEP = 9
        self.extract_from_sprite_sheet('materials/blue_woman_sprite.png', self.DIR, self.STEP)
        self.player_selection = {"1P": {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "shoot": pygame.K_SPACE, "switch": pygame.K_LSHIFT}, "2P": {"left": pygame.K_j, "right": pygame.K_l, "up": pygame.K_i, "down": pygame.K_k, "shoot": pygame.K_SLASH, "switch": pygame.K_RSHIFT}}
        self.bullet_list = []
        self.cold_time = 0    #12.26新增 受傷冷卻時間
        self.shootLoop = 0
        self.shootCoolDown = 10
        self.shootAvailabe = True
        self.switchLoop = 0
        self.switchCoolDown = 10
        self.switchAvailabe = True
        self.explode_list = []
        self.weapon_list = ["1.pistol"]
        self.weapon = "1.pistol"
        self.is_super_man = False
        self.is_enlarged = False
        self.is_medium = True
        self.weapon_dict = WEAPON_DICT
 
 

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
                self.shootAvailabe = False

        if keys[player_control["switch"]]:
            if self.switchLoop == 0:
                self.switchAvailabe = False
                if self.weapon != self.weapon_list[-1]:
                    self.weapon= self.weapon_list[self.weapon_list.index(self.weapon)+1]

                else:
                    self.weapon = self.weapon_list[0]
                        
        if keys[pygame.K_q]:
            run[0] = False

        # print("right", self.right, "left", self.left, "up", self.up, "down", self.down)
    
    def enlarge(self):
        if not self.is_enlarged:
            self.extract_from_sprite_sheet('materials/blue_woman_sprite.png', self.DIR, self.STEP)
            for i in range(self.DIR):
                for j in range(self.STEP):
                    self.walk_sheet[i][j] = pygame.transform.scale(self.walk_sheet[i][j], (100, 100))
            self.set_hitbox(15, 8, int(self.width*0.8), int(self.height*1.2))
        elif self.is_enlarged:
            pass

    def medium(self):
        if not self.is_medium:
            self.extract_from_sprite_sheet('materials/blue_woman_sprite.png', self.DIR, self.STEP)
            # self.set_hitbox(15, 5, self.width-35, self.height-10)
            # for i in range(self.DIR):
            #     for j in range(self.STEP):
            #         self.walk_sheet[i][j] = pygame.transform.scale(self.walk_sheet[i][j], (10, 10))
            self.set_hitbox(-150, -5, self.width*5, self.height*5)

        elif self.is_medium:
            pass

    def draw(self, win, frames=3):
        if self.health > 0: 
            super().draw(win, frames)
            if self.is_medium:
                self.set_hitbox(15, 5, self.width - 35, self.height - 10)
            elif self.is_enlarged:
                self.set_hitbox(15, 8, int(self.width*0.8), int(self.height*1.2))
            # draw hitbox
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if self.health > 0: 
            self.health -= 1
            # print(self.health)
            # font1 = pygame.font.SysFont('comicsans', 100)
            # text = font1.render("hit", 1, (255, 0, 0))
            # # print(self.health)
            # win.blit(text, ((win_width - text.get_width()) // 2, (win_height - text.get_height()) // 2))
            # pygame.display.update()

    def shoot(self):
        if self.health > 0:
            x_bomb = self.x
            y_bomb = self.y
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
            for i in range(self.weapon_dict[self.weapon]['bullet_count']):
                self.bullet_list.append(Bullet(x=self.x+self.width//2, y=self.y+self.height//2, facing=facing, radius=self.weapon_dict[self.weapon]['bullet_radius'], velocity=self.weapon_dict[self.weapon]['vel'], damage=self.weapon_dict[self.weapon]['damage'], weapon=self.weapon, rotate=self.weapon_dict[self.weapon]['bullet_rotate'][0]+i*self.weapon_dict[self.weapon]['bullet_rotate'][1]))


# 576*256
class Enemy(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.target = None
        self.set_hitbox(15, 10, self.width - 35, self.height - 10)
        self.extract_from_sprite_sheet('materials/skull_sprite.png', 4, 9)
        self.vel = 1
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000) # Create enemy every 1 sec
    
    def chase(self, player):
        dx = (player.x - self.x)# + random.randrange(-200, 200, 1)
        dy = (player.y - self.y)# + random.randrange(-200, 200, 1)
        dl = (dx**2 + dy**2)**0.5
        if dl !=0:
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
    def __init__(self, x, y, facing, radius, velocity, damage, color=(0, 0, 0), weapon = '1.pistol', rotate = 0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = velocity
        self.damage = damage
        self.rotate = rotate
        self.weapon = weapon
    
    def fly(self):
        if self.rotate == 0:
            self.x += self.vel * self.facing[0]
            self.y += self.vel * self.facing[1]

        else:
            facing_adjust = copy.deepcopy(self.facing)
            if self.weapon == '4.missle':
                self.rotate += random.randrange(-50, 50, 1)
            rotate_adjust = self.rotate
            if self.facing[0] == 0:
                facing_adjust[0] = 1
                rotate_adjust =  (90 - self.rotate)
            elif self.facing[1] == 0:
                facing_adjust[1] = 1 
            elif self.facing == [1,1] or self.facing == [-1,-1]:
                rotate_adjust = 45 + self.rotate
            elif self.facing == [1,-1] or self.facing == [-1,1]:
                rotate_adjust = 45 - self.rotate
            self.x += int(self.vel * math.cos(math.radians(rotate_adjust))* facing_adjust[0])
            self.y += int(self.vel * math.sin(math.radians(rotate_adjust))* facing_adjust[1])



    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def out(self, win_width, win_height):
        if self.x < 0 or self.x > win_width or self.y < 0 or self.y > win_height:
            return True
        else:
            return False
    
    def hit(self):
        pass


class Explosion():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.remove = False
        self.exp = []
        self.expcount = 0
        self.extract_from_sprite_sheet('materials/explosion_sprite.png',4,8)

    def extract_from_sprite_sheet(self, image_source, scale, steps):
        sprite_sheet = pygame.image.load(image_source)
        for i in range(scale):
            for  j in range(steps):
                #self.width = 512//8  self.height = 331//5
                img = sprite_sheet.subsurface((512//8*j, 331//5*i, 512//8, 331//5))
                img = pygame.transform.scale(img, (75, 75))
                self.exp.append(img)   

    def draw(self, win, player):
        if self.x < 480 and self.y < 480: 
            win.blit(self.exp[self.expcount], (self.x, self.y))
            self.expcount += 1
            if self.expcount >= 30:
                self.expcount = 0
                self.remove = True
                # player.explode_list = []
                return None

class Coconut():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.offset = 8
        self.ignited = False
        self.read_image()
        self.surprise_list = ["revert walking", "super man", "add shotgun", "add bomb", "add missle", "heal"]
        pygame.time.set_timer(CREATE_COCONUT_EVENT, 5000)
        self.hitbox = (self.x + self.offset, self.y + self.offset, self.width - 2*self.offset, self.height - 2*self.offset)

    def read_image(self):
        img = pygame.image.load('./materials/coconut.png')
        self.img = pygame.transform.scale(img, (self.width, self.height))

    def create_surprise(self, player):
        self.ignited = True
        self.tracked_player = player
        self.surprise = random.choice(self.surprise_list)
        self.SURPRISE_TIME_TICK = 300
        self.surprise_count = 0
        self.update_surprise()
    
    def update_surprise(self):
        # print(id(self.tracked_player.walk_sheet[0]))
        self.surprise_count += 1
        if self.surprise == "revert walking":
            self.tracked_player.player_selection = {"1P": {"left": pygame.K_d, "right": pygame.K_a, "up": pygame.K_s, "down": pygame.K_w, "shoot": pygame.K_SPACE, "switch": pygame.K_LSHIFT}, "2P": {"left": pygame.K_l, "right": pygame.K_j, "up": pygame.K_k, "down": pygame.K_i, "shoot": pygame.K_SLASH, "switch": pygame.K_RSHIFT}}
        elif self.surprise == "super man":
            self.tracked_player.is_super_man = True
            self.tracked_player.enlarge()
            self.tracked_player.is_enlarged = True
            self.tracked_player.is_medium = False
            # for i in range(len(self.tracked_player.walk_left)):
            #     pygame.transform.scale(self.tracked_player.walk_left[i], (20, 20))
        elif self.surprise == "add shotgun":
            if "2.shotgun" not in self.tracked_player.weapon_list:
                self.tracked_player.weapon_list.append("2.shotgun")
                self.tracked_player.weapon_list.sort()
        
        elif self.surprise == "add bomb":
            if "3.bomb" not in self.tracked_player.weapon_list:
                self.tracked_player.weapon_list.append("3.bomb")
                self.tracked_player.weapon_list.sort()
        
        elif self.surprise == "add missle":
            if "4.missle" not in self.tracked_player.weapon_list:
                self.tracked_player.weapon_list.append("4.missle")
                self.tracked_player.weapon_list.sort()
        
        elif self.surprise == "heal":
            if self.tracked_player.health != 5:
                self.tracked_player.health += 1
    
    def remove_surprise(self):
        if self.surprise == 'revert walking':
            self.tracked_player.player_selection = {"1P": {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "shoot": pygame.K_SPACE, "switch": pygame.K_LSHIFT}, "2P": {"left": pygame.K_j, "right": pygame.K_l, "up": pygame.K_i, "down": pygame.K_k, "shoot": pygame.K_SLASH, "switch": pygame.K_RSHIFT}}
        elif self.surprise == 'super man':
            self.tracked_player.is_super_man = False
            self.tracked_player.medium()
            self.tracked_player.is_enlarged = False
            self.tracked_player.is_medium = True

    def draw(self, win):
        if not self.ignited:
            win.blit(self.img, (self.x, self.y))
        # draw hitbox
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

WEAPON_DICT = {
    "1.pistol" :{'damage': 1,'bullet_count': 1, 'vel': 5, 'bullet_radius': 6, 'bullet_rotate': [0,0]},
    "2.shotgun" : {'damage': 3,'bullet_count': 3, 'vel': 8, 'bullet_radius': 4, 'bullet_rotate': [-15,15]},
    "3.bomb" : {'damage': 1,'bullet_count': 1, 'vel': 0, 'bullet_radius': 6, 'bullet_rotate': [0,0]},
    "4.missle" : {'damage': 1, 'bullet_count': 2, 'vel': 5, 'bullet_radius': 4, 'bullet_rotate': [-5, 6]}
    }
