import pygame 
import pytmx

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE 
        self.height = self.tileheight * TILESIZE

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

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    # track the movement of players to scroll map
    def update(self, player_list):
 
        if len(player_list) == 1 :
            x = -1*(player_list[0].x) + int(480)//2
            print(player_list[0])
            y = -1*(player_list[0].y)+ int(480)//2
        elif len(player_list) == 2 :
            x = (-1*(player_list[0].x)-1*(player_list[1].x))//2+ int(64*14)# w in_width = 480
            y = (-1*(player_list[0].y)-1*(player_list[1].y))//2+ int(64*14)# win_width = 480
            print(x,y)
        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-1*self.width + 480, x)   # right
        y = max(-1*self.height + 480, y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)

