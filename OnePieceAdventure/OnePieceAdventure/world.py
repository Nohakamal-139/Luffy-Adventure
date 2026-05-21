import pygame
import pytmx
class World:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.obstacles =[]
        self.dangres = []
        self.create_obstacles
    def create_obstacles(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile_props:
                        rect = pygame.Rect(x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight, self.tmx_data.tilewidth, self.tmx_data.tileheight)
                        if tile_props.get('solid'):

                            self.obstacles.append(rect)
                        if tile_props.get('danger'):
                            self.dangres.append(rect)
    def render(self, surface):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
    def get_objects(self):
        points = {}
        for obj in self.tmx_data.objects:
            if obj.name == 'start':
                points['start'] = (obj.x, obj.y)
            if obj.name == 'goal':
                points['goal'] = (obj.x, obj.y)
        return points