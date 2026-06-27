import pygame
import sys
from world import World
from Character import Character

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        # تحميل صورك
        self.hud_border = pygame.image.load("hud_border.png").convert_alpha()
        self.health_fill = pygame.image.load("health_fill.png").convert_alpha()
        self.energy_fill = pygame.image.load("energy_fill.png").convert_alpha()
        self.meat_img = pygame.transform.scale(pygame.image.load("New Piskel (5).png").convert_alpha(), (32, 32))
        self.boss_hud_border = pygame.image.load("boss_hud_border.png").convert_alpha()
        self.boss_health_fill = pygame.image.load("boss_health_fill.png").convert_alpha()

        self.current_level = ""
        self.load_level('level1.tmx')
        self.clock = pygame.time.Clock()
        self.running = True

    def load_level(self, level_name):
        if self.current_level == level_name: return
        self.current_level = level_name
        self.world = World(level_name)
        self.map_surface = self.world.make_map()
        self.luffy = Character(self.world.get_objects().get('start', (100, 300)))
        self.goal_pos = self.world.get_objects().get('goal', None)
        self.meats = list(self.world.meat_rects)
        self.is_boss_room = (level_name == 'boss_room.tmx')
        self.camera_x = 0

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
            
            keys = pygame.key.get_pressed()
            self.luffy.update(keys, self.world.obstacles, self.world.dangers)
            
            # منطق اللحمة
            luffy_rect = pygame.Rect(int(self.luffy.x), int(self.luffy.y), 100, 100)
            for m in self.meats[:]:
                if luffy_rect.colliderect(m):
                    self.luffy.health = min(100, self.luffy.health + 20)
                    self.meats.remove(m)

            # الانتقال لغرفة البوس
            if self.goal_pos and luffy_rect.colliderect(pygame.Rect(self.goal_pos[0], self.goal_pos[1], 64, 64)):
                self.load_level('boss_room.tmx')

            # الكاميرا
            self.camera_x = int(-(self.luffy.x - 350))
            if self.camera_x > 0: self.camera_x = 0
            if self.camera_x < -(self.world.width - 800): self.camera_x = -(self.world.width - 800)

            # الرسم
            self.screen.fill((135, 206, 235))
            self.screen.blit(self.map_surface, (self.camera_x, 0))
            for m in self.meats: self.screen.blit(self.meat_img, (m.x + self.camera_x, m.y))
            self.luffy.draw(self.screen, self.camera_x)
            self.draw_gui()
            
            pygame.display.flip()
            self.clock.tick(60)

    def draw_gui(self):
        # شريط لوفي
        health_w = int(200 * (self.luffy.health / 100))
        if health_w > 0: self.screen.blit(self.health_fill, (20, 20), (0,0, health_w, 20))
        self.screen.blit(self.hud_border, (20, 20))
        # شريط الطاقة
        energy_w = int(200 * (self.luffy.energy / 100))
        if energy_w > 0: self.screen.blit(self.energy_fill, (20, 50), (0,0, energy_w, 20))
        self.screen.blit(self.hud_border, (20, 50))
        if self.is_boss_room:
            self.screen.blit(self.boss_health_fill, (550, 20), (0, 0, 200, 20))
            self.screen.blit(self.boss_hud_border, (550, 20))

if __name__ == "__main__":
    Game().run()