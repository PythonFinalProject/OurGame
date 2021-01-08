import pygame 
import pytmx




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

    # track the movement of players to scroll map
    def update(self, player_list):
        x, y = 0, 0
        if len(player_list) == 1 :
            x = -1*player_list[0].x - player_list[0].width + 480//2
            y = -1*player_list[0].y - player_list[0].height + 480//2
        elif len(player_list) == 2 :
            x = (-1*(player_list[0].x)-1*(player_list[1].x))//2 - player_list[0].width + 480//2
            y = (-1*(player_list[0].y)-1*(player_list[1].y))//2 - player_list[0].height + 480//2
        
        
        # limit scrolling to map size  
        x = min(0, x)  # left
        y = min(0, y)  # top

        
        x = max(-415, x)  # right  -(480 - 64)
        y = max(-415, y)  # bottom
        
        
        self.tracking = pygame.Rect(x, y, self.width, self.height)

