import pygame
import sys
import os
from world import World
from Character import Character
from enemy import Marine, Crocodile

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("One Piece Adventure")
        self.font_sub = pygame.font.SysFont("Arial", 20, bold=True)
        
        # --- تحميل الصور ---
        self.logo = pygame.image.load("one_piece_logo.jpeg").convert()
        self.logo = pygame.transform.scale(self.logo, (self.WIDTH, self.HEIGHT))
        self.tbc_img = pygame.image.load("to_be_continued.jpeg").convert()
        self.tbc_img = pygame.transform.scale(self.tbc_img, (self.WIDTH, self.HEIGHT))
        
        try:
            self.play_btn = pygame.image.load("play_btn.png").convert_alpha()
        except:
            self.play_btn = pygame.Surface((200, 60), pygame.SRCALPHA)
            pygame.draw.rect(self.play_btn, (139, 69, 19), (0, 0, 200, 60), border_radius=10)
        
        self.play_rect = self.play_btn.get_rect(center=(self.WIDTH//2, 300))

        self.hud_border = pygame.image.load("hud_border.png").convert_alpha()
        self.health_fill = pygame.image.load("health_fill.png").convert_alpha()
        self.energy_fill = pygame.image.load("energy_fill.png").convert_alpha()
        self.meat_img = pygame.transform.scale(pygame.image.load("New Piskel (5).png").convert_alpha(), (32, 32))
        self.boss_hud_border = pygame.image.load("boss_hud_border.png").convert_alpha()
        self.boss_health_fill = pygame.image.load("boss_health_fill.png").convert_alpha()

        self.GAME_STATE = "START_MENU"
        self.current_level = ""
        self.clock = pygame.time.Clock()
        self.running = True

    def load_level(self, level_name):
        if self.current_level == level_name: return
        self.current_level = level_name
        self.world = World(level_name)
        self.map_surface = self.world.make_map()
        
        start_pos = self.world.get_objects().get('start', (100, 300))
        self.luffy = Character(start_pos)
        self.goal_pos = self.world.get_objects().get('goal', None)
        self.meats = list(self.world.meat_rects)
        self.is_boss_room = (level_name == 'boss_room.tmx')
        self.luffy.is_boss_room = self.is_boss_room
        
        self.enemies = []
        if not self.is_boss_room:
            m_sheet = pygame.image.load("marine_gunman.png").convert_alpha()
            for obj in self.world.tmx_data.objects:
                if obj.name == 'enemy': self.enemies.append(Marine(obj.x, obj.y, m_sheet))
        
        self.boss = None
        if self.is_boss_room:
            b_pos = self.world.get_objects().get('boss', (1500, 350))
            self.boss = Crocodile(b_pos[0], b_pos[1])
        
        self.camera_x = 0

    def run(self):
        while self.running:
            if self.GAME_STATE == "START_MENU":
                self.draw_start_menu()
            elif self.GAME_STATE == "PLAYING":
                self.play_game()
            elif self.GAME_STATE == "WIN":
                self.screen.blit(self.tbc_img, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: self.running = False
            
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def draw_start_menu(self):
        self.screen.blit(self.logo, (0, 0))
        self.screen.blit(self.play_btn, self.play_rect)
        guide_box = pygame.Surface((560, 160), pygame.SRCALPHA)
        guide_box.fill((0, 0, 0, 180))
        self.screen.blit(guide_box, (120, 380))
        t1 = self.font_sub.render("Instructions: Arrows to move, UP to jump.", True, (255, 255, 255))
        t2 = self.font_sub.render("Press Z for Gatling, X for Combo.", True, (255, 255, 255))
        self.screen.blit(t1, (150, 400)); self.screen.blit(t2, (150, 440))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.play_rect.collidepoint(event.pos):
                self.load_level('level1.tmx'); self.GAME_STATE = "PLAYING"

    def play_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
        
        keys = pygame.key.get_pressed()
        self.luffy.update(keys, self.world.obstacles, self.world.dangers)
        
        # --- السحر: حدود الشاشة لمنع لوفي من الخروج ---
        if self.luffy.x < 0: self.luffy.x = 0
        if self.luffy.x > self.world.width - 64: self.luffy.x = self.world.width - 64
        
        l_rect = pygame.Rect(int(self.luffy.x), int(self.luffy.y), 64, 64)

        # تحديث الأعداء
        for e in self.enemies[:]:
            e.update(self.luffy.x, self.luffy.y, self.world.obstacles, self.world.dangers)
            if e.health <= 0: self.enemies.remove(e); continue
            for b in e.bullets[:]:
                if l_rect.colliderect(b["rect"]): self.luffy.health -= 5; e.bullets.remove(b)
            if keys[pygame.K_z] or keys[pygame.K_x]:
                atk_rect = pygame.Rect(int(self.luffy.x - 50), int(self.luffy.y), 200, 100)
                if atk_rect.colliderect(pygame.Rect(e.x, e.y, 64, 64)): e.health -= 10; e.flash_timer = 5

        # تحديث الزعيم (البوس)
        if self.boss:
            self.boss.update(self.luffy.x, self.luffy.y)
            boss_hitbox = pygame.Rect(int(self.boss.x), int(self.boss.y), 120, 130)
            if l_rect.colliderect(boss_hitbox): self.luffy.health -= 0.5
            
            # لوفي يضرب البوس
            if keys[pygame.K_z] or keys[pygame.K_x]:
                # مساحة هجوم لوفي
                attack_area = pygame.Rect(int(self.luffy.x - 80), int(self.luffy.y), 250, 120)
                if attack_area.colliderect(boss_hitbox):
                    self.boss.health -= 2
                    self.boss.flash_timer = 5
            
            if self.boss.health <= 0: self.GAME_STATE = "WIN"

        # اللحمة والانتقال
        for m in self.meats[:]:
            if l_rect.colliderect(m): self.luffy.health = min(100, self.luffy.health+20); self.meats.remove(m)
        if self.goal_pos and l_rect.colliderect(pygame.Rect(self.goal_pos[0], self.goal_pos[1], 64, 64)):
            self.load_level('boss_room.tmx')

        self.camera_x = int(-(self.luffy.x - 350))
        if self.camera_x > 0: self.camera_x = 0
        if self.camera_x < -(self.world.width - 800): self.camera_x = -(self.world.width - 800)

        self.screen.fill((135, 206, 235))
        self.screen.blit(self.map_surface, (self.camera_x, 0))
        for m in self.meats: self.screen.blit(self.meat_img, (int(m.x + self.camera_x), int(m.y)))
        for e in self.enemies: e.draw(self.screen, self.camera_x)
        if self.boss: self.boss.draw(self.screen, self.camera_x)
        self.luffy.draw(self.screen, self.camera_x)
        self.draw_gui()

    def draw_gui(self):
        # لوفي
        self.screen.blit(self.health_fill, (20, 20), (0, 0, int(self.luffy.health * 2), 20))
        self.screen.blit(self.hud_border, (20, 20))
        self.screen.blit(self.energy_fill, (20, 50), (0, 0, int(self.luffy.energy * 2), 20))
        self.screen.blit(self.hud_border, (20, 50))
        # البوس
        if self.is_boss_room and self.boss:
            bw = int(200 * (self.boss.health / 500))
            if bw > 0: self.screen.blit(self.boss_health_fill, (550, 20), (0, 0, bw, 20))
            self.screen.blit(self.boss_hud_border, (550, 20))

if __name__ == "__main__":
    Game().run()