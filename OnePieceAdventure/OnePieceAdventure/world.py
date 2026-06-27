import pygame
import pytmx

class World:
    def __init__(self, tmx_file):
        self.tmx_data = pytmx.load_pygame(tmx_file)
        self.tile_size = 32
        self.width = self.tmx_data.width * self.tile_size
        self.height = self.tmx_data.height * self.tile_size
        self.obstacles, self.dangers, self.meat_rects = [], [], []
        self.create_objects()

    def create_objects(self):
        # تصفير القوائم
        self.obstacles, self.dangers, self.meat_rects = [], [], []
        for layer_index, layer in enumerate(self.tmx_data.visible_layers):
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if props:
                        rect = pygame.Rect(x*32, y*32, 32, 32)
                        if props.get('solid'): self.obstacles.append(rect)
                        elif props.get('danger'): self.dangers.append(rect)
                        elif props.get('type') == 'meat': self.meat_rects.append(rect)

    def get_objects(self):
        return {obj.name: (obj.x, obj.y) for obj in self.tmx_data.objects if obj.name}

    def render(self, surface):
        for layer_index, layer in enumerate(self.tmx_data.visible_layers):
            # رسم المربعات (مع التأكد من رسم كل الطبقات عشان الأرضية تظهر)
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    props = self.tmx_data.get_tile_properties(x, y, layer_index)
                    # أهم سطر: لو المربع "لحمة"، ما ترسموش هنا (إحنا هنرسمه في main عشان يختفي)
                    if props and props.get('type') == 'meat': continue
                    if image: surface.blit(image, (x * 32, y * 32))
            # رسم الصور الكبيرة (الخلفية)
            elif isinstance(layer, pytmx.TiledImageLayer):
                if layer.image: surface.blit(layer.image, (int(layer.offsetx), int(layer.offsety)))
        
        # رسم الأجسام (القلعة)
        for obj in self.tmx_data.objects:
            img = self.tmx_data.get_tile_image_by_gid(obj.gid)
            if img: surface.blit(img, (obj.x, obj.y - obj.height))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        return temp_surface