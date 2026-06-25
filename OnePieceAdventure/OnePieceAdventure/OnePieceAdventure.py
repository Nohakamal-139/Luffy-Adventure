import pygame
import sys
from world import World
from Character import Character # استدعاء الكلاس الجديد

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.load_level('level1.tmx')
        self.clock = pygame.time.Clock()
        self.running = True

    def load_level(self, level_name):
        self.world = World(level_name)
        self.map_surface = self.world.make_map()
        self.map_rect = self.map_surface.get_rect()
        self.camera_x = 0
        
        # جلب نقطة البداية من الخريطة
        start_pos = self.world.get_objects().get('start', (100, 300))
        
        # إنشاء كائن لوفي في مكان البداية
        self.luffy = Character(start_pos)
        
        pygame.display.set_caption("Luffy's Adventure")
        print(f"Loaded level: {level_name}")

    def run(self):
        while self.running:
            self.handle_events()
            
            keys = pygame.key.get_pressed()
            
            # تحديث لوفي (الحركة والفيزياء)
            self.luffy.update(keys)
            
            # جعل الكاميرا تتبع لوفي (اختياري)
            self.camera_x = -(self.luffy.x - 300)
            
            # حدود الكاميرا
            if self.camera_x > 0: self.camera_x = 0
            if self.camera_x < self.screen.get_width() - self.map_rect.width:
                self.camera_x = self.screen.get_width() - self.map_rect.width

            # الرسم
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.map_surface, (self.camera_x, 0)) # رسم الخريطة
            self.luffy.draw(self.screen, self.camera_x) # رسم لوفي
            
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.load_level('level1.tmx')
                if event.key == pygame.K_2:
                    self.load_level('boss_room.tmx')

if __name__ == "__main__":
    game = Game()
    game.run()