import pygame
import pytmx

class World:
    def __init__(self, tmx_file):
        self.tmx_data = pytmx.load_pygame(tmx_file)
        self.tile_size = 32
        self.width = self.tmx_data.width * self.tile_size
        self.height = self.tmx_data.height * self.tile_size
        
        self.obstacles = [] 
        self.dangers = []   
        self.meats = []
        self.create_objects()

    def create_objects(self):
        self.obstacles = []
        self.dangers = []
        self.meats = [] 
        
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile_props:
                        rect = pygame.Rect(x * 32, y * 32, 32, 32)
                        if tile_props.get('solid'):
                            self.obstacles.append(rect)
                        elif tile_props.get('danger'):
                            self.dangers.append(rect)
                        elif tile_props.get('type') == 'meat':
                            self.meats.append([rect, x, y, layer]) 

    def get_objects(self):
        return {obj.name: (obj.x, obj.y) for obj in self.tmx_data.objects if obj.name}

    def render(self, surface):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if image:
                        surface.blit(image, (x * self.tile_size, y * self.tile_size))
        
        for obj in self.tmx_data.objects:
            tile_image = self.tmx_data.get_tile_image_by_gid(obj.gid)
            if tile_image:
                surface.blit(tile_image, (obj.x, obj.y - obj.height))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        return temp_surface