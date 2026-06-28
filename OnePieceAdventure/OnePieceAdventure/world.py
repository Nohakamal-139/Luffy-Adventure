import pygame
import pytmx

class World:
    def __init__(self, tmx_file):
        self.tmx_data = pytmx.load_pygame(tmx_file)
        # التعديل: جلب مقاس المربعات أوتوماتيكياً من الخريطة (عشان يظبط ليفل 1 وغرفة البوس)
        self.tile_size = self.tmx_data.tilewidth 
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
                        # استخدام self.tile_size لضمان الدقة
                        rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                        if props.get('solid'): self.obstacles.append(rect)
                        elif props.get('danger'): self.dangers.append(rect)
                        elif props.get('type') == 'meat': self.meat_rects.append(rect)

    def get_objects(self):
        return {obj.name: (obj.x, obj.y) for obj in self.tmx_data.objects if obj.name}

    def render(self, surface):
        # ١. أولاً: رسم طبقات الصور (Image Layers) - دي دايماً في الخلفية
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledImageLayer):
                if layer.image:
                    surface.blit(layer.image, (int(layer.offsetx), int(layer.offsety)))

        # ٢. ثانياً: رسم المربعات (Tile Layers) - زي الأرضية والرمل
        for layer_index, layer in enumerate(self.tmx_data.visible_layers):
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    props = self.tmx_data.get_tile_properties(x, y, layer_index)
                    if props and props.get('type') == 'meat': continue 
                    if image:
                        surface.blit(image, (x * self.tile_size, y * self.tile_size))

        # ٣. ثالثاً: رسم الأجسام (Objects) - زي القلعة أو أي ديكور إضافي
        for obj in self.tmx_data.objects:
            tile_img = self.tmx_data.get_tile_image_by_gid(obj.gid)
            if tile_img:
                # رسمها مع مراعاة الطول عشان ما تطيرش
                surface.blit(tile_img, (obj.x, obj.y - obj.height))

    def make_map(self):
        # SRCALPHA مهم جداً لظهور الأرضية فوق الخلفية
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        return temp_surface