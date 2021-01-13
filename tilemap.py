import pygame 
import pytmx
from character import Explosion




class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = 14 * 64 # tilesize = 64×64, mapsize = 14×14 tiles
        self.height = 14 * 64 
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))


    def draw(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.tracking = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.show = pygame.Surface((width, height))
        self.x = 0
        self.y = 0

    # track the movement of players to scroll map
    def update(self, player_list):
        if len(player_list) == 1 :
            self.x = -1*player_list[0].x - player_list[0].width + 480//2
            self.y = -1*player_list[0].y - player_list[0].height + 480//2
        elif len(player_list) == 2 :
            self.x = (-1*(player_list[0].x)-1*(player_list[1].x))//2 - player_list[0].width + 480//2
            self.y = (-1*(player_list[0].y)-1*(player_list[1].y))//2 - player_list[0].height + 480//2
        
        
        # limit scrolling to map size  
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top

        
        self.x = max(-415, self.x)  # right  -(480 - 64)
        self.y = max(-415, self.y)  # bottom
        
        
        self.tracking = pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.hitbox = [x, y, width, height]

    def checkPlayerStoneCollision(self,player, obstacle_list):
        player_hb_0 = player.hitbox[0]
        player_hb_1 = player.hitbox[1]
        player_hb_2 = player.hitbox[2]
        player_hb_3 = player.hitbox[3]

        for obstacle in obstacle_list:
            obstacle_hb_0 = obstacle.hitbox[0]
            obstacle_hb_1 = obstacle.hitbox[1]
            obstacle_hb_2 = obstacle.hitbox[2]
            obstacle_hb_3 = obstacle.hitbox[3]
            if  player_hb_1 + player_hb_3 > obstacle_hb_1 and player_hb_1 < obstacle_hb_1 + obstacle_hb_3 and player_hb_0 + player_hb_2 > obstacle_hb_0 and player_hb_0 < obstacle_hb_0 + obstacle_hb_2:
                if player.left == True:
                    player.x += player.velx
                elif player.right == True:
                    player.x -= player.velx
                elif player.up == True:
                    player.y -= player.vely
                elif player.down == True:
                    player.y += player.vely

    def checkEnemyStoneCollision(self, enemy, obstacle_list):
        enemy_hb_0 = enemy.hitbox[0]
        enemy_hb_1 = enemy.hitbox[1]
        enemy_hb_2 = enemy.hitbox[2]
        enemy_hb_3 = enemy.hitbox[3]

        for obstacle in obstacle_list:
            obstacle_hb_0 = obstacle.hitbox[0] 
            obstacle_hb_1 = obstacle.hitbox[1] 
            obstacle_hb_2 = obstacle.hitbox[2] 
            obstacle_hb_3 = obstacle.hitbox[3] 
            if  enemy_hb_1 + enemy_hb_3 > obstacle_hb_1 and enemy_hb_1 < obstacle_hb_1 + obstacle_hb_3 and enemy_hb_0 + enemy_hb_2 > obstacle_hb_0 and enemy_hb_0 < obstacle_hb_0 + obstacle_hb_2:
                if enemy.left == True:
                    enemy.x += 2
                    # enemy.y += 1  # bounce-off effect, or the enemy will stuck there
                elif enemy.right == True:
                    enemy.x -= 2
                    # enemy.y -= 1

                elif enemy.up == True:
                    enemy.y -= 2
                    # enemy.x -= 1
                    
                elif enemy.down == True:
                    enemy.y += 2
                    # enemy.x += 1

class Proof:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.hitbox = [x, y, width, height]

    def checkBulletProofCollision(self,bullet, proof_list):
        for proof in proof_list:
            proof_hb_0 = proof.hitbox[0]
            proof_hb_1 = proof.hitbox[1]
            proof_hb_2 = proof.hitbox[2]
            proof_hb_3 = proof.hitbox[3]
            if bullet.x > proof_hb_0 and bullet.x < proof_hb_0 + proof_hb_2 and bullet.y > proof_hb_1 and bullet.y < proof_hb_1 + proof_hb_3:
                return True

                


class Block:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.hitbox = [x, y, width, height]
                   
    def draw(self, win):
        win.blit(pygame.image.load('./materials/block.png'), (self.x, self.y))

    def checkPlayerBlockCollision(self,player, block_list):
        player_hb_0 = player.hitbox[0]
        player_hb_1 = player.hitbox[1]
        player_hb_2 = player.hitbox[2]
        player_hb_3 = player.hitbox[3]

        for block in block_list:
            block_hb_0 = block.hitbox[0]
            block_hb_1 = block.hitbox[1]
            block_hb_2 = block.hitbox[2]
            block_hb_3 = block.hitbox[3]
            if  player_hb_1 + player_hb_3 > block_hb_1 and player_hb_1 < block_hb_1 + block_hb_3 and player_hb_0 + player_hb_2 > block_hb_0 and player_hb_0 < block_hb_0 + block_hb_2:
                if player.left == True:
                    player.x += player.velx
                elif player.right == True:
                    player.x -= player.velx
                elif player.up == True:
                    player.y += player.vely
                elif player.down == True:
                    player.y -= player.vely

    def checkEnemyBlockCollision(self, enemy, block_list):
        enemy_hb_0 = enemy.hitbox[0]
        enemy_hb_1 = enemy.hitbox[1]
        enemy_hb_2 = enemy.hitbox[2]
        enemy_hb_3 = enemy.hitbox[3]

        for block in block_list:
            block_hb_0 = block.hitbox[0] 
            block_hb_1 = block.hitbox[1] 
            block_hb_2 = block.hitbox[2] 
            block_hb_3 = block.hitbox[3] 
            if  enemy_hb_1 + enemy_hb_3 > block_hb_1 and enemy_hb_1 < block_hb_1 + block_hb_3 and enemy_hb_0 + enemy_hb_2 > block_hb_0 and enemy_hb_0 < block_hb_0 + block_hb_2:
                if enemy.left == True:
                    enemy.x += 1
                elif enemy.right == True:
                    enemy.x -= 1
                elif enemy.up == True:
                    enemy.y += 2
                elif enemy.down == True:
                    enemy.y -= 2

    def checkBlockBulletCollision(self, bullet, block_list, player):
        for block in block_list:
            block_hb_0 = block.hitbox[0]
            block_hb_1 = block.hitbox[1]
            block_hb_2 = block.hitbox[2]
            block_hb_3 = block.hitbox[3]
            if bullet.x > block_hb_0 and bullet.x < block_hb_0 + block_hb_2 and bullet.y > block_hb_1 and bullet.y < block_hb_1 + block_hb_3:
                x = block_hb_0 
                y = block_hb_1 
                exp = Explosion(x,y)
                player.explode_list.append(exp)
                player.bullet_list.pop(player.bullet_list.index(bullet))
                block_list.pop(block_list.index(block))
                break
