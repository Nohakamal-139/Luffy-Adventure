import pygame
import sys
from world import World
from Character import Character  # الآن سيتعرف عليها بنجاح!

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.load_level('level1.tmx')
        self.clock = pygame.time.Clock()
        self.running = True

    def load_level(self, level_name):
        self.world = World(level_name)
        # تصليح الخطأ الإملائي في ملف الـ world من التيم لاستدعاء الـ obstacles
        self.world.create_obstacles() 
        
        self.map_surface = self.world.make_map()
        self.map_rect = self.map_surface.get_rect()
        self.camera_x = 0
        
        # جلب نقاط البداية والنهاية من الخريطة
        self.start_pos = self.world.get_objects().get('start', (100, 350))
        self.goal_pos = self.world.get_objects().get('goal', (0, 0))
        
        # 🎯 إنشاء شخصية لوفي عند نقطة البداية المحددة في الخريطة!
        self.player = Character(self.start_pos)
        
        pygame.display.set_caption("Luffy's Adventure")
        print(f"Loaded level: {level_name}")

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill((0, 0, 0))
            
            keys = pygame.key.get_pressed()
            
            # تحديث حركة لوفي بناءً على الأزرار المضغوطة
            self.player.update(keys)
            
            # جعل الكاميرا تتبع حركة اللاعب بشكل احترافي
            self.camera_x = -self.player.x + 350
            
            # حماية الكاميرا من الخروج عن حدود الخريطة
            if self.camera_x > 0:
                self.camera_x = 0
            if self.camera_x < self.screen.get_width() - self.map_rect.width:
                self.camera_x = self.screen.get_width() - self.map_rect.width
            
            # 1. رسم الخريطة أولاً
            self.screen.blit(self.map_surface, (self.camera_x, 0))
            
            # 2. رسم لوفي فوق الخريطة مع إحداثيات الكاميرا المحدثة
            self.player.draw(self.screen, self.camera_x)
            
            # 3. رسم مؤشر الكومبو إذا كان جاهزاً
            if self.player.combo_ready:
                font = pygame.font.SysFont(None, 30)
                text = font.render("COMBO READY! Press V", True, (255, 69, 0))
                self.screen.blit(text, (20, 20))
                
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