import pygame
import os

class Character:
    def __init__(self, start_pos):
        self.SIZE = (64, 64) 
        self.initial_start = start_pos
        self.x, self.y = start_pos
        
        # تحميل الصور
        assets_dir = "assets"
        self.sheet_base = pygame.image.load(os.path.join(assets_dir, "luffy_base_sheet.png")).convert_alpha()
        self.sheet_skills = pygame.image.load(os.path.join(assets_dir, "luffy_skills_sheet.png")).convert_alpha()
        self.sheet_lvl2 = pygame.image.load(os.path.join(assets_dir, "luffy_lvl2_gatling.jpg.png")).convert_alpha()
        self.sheet_combo = pygame.image.load(os.path.join(assets_dir, "luffy_combo_attack_sheet.png")).convert_alpha()

        self.idle_frames = [self.get_frame(self.sheet_base, x, 65, 105, 205) for x in [10, 140, 270]]
        self.run_frames = [self.get_frame(self.sheet_base, 655, 65, 110, 205), self.get_frame(self.sheet_base, 785, 65, 115, 205)]
        self.jump_frames = [self.get_frame(self.sheet_base, 20, 510, 110, 160)]
        self.dodge_frames = [self.get_frame(self.sheet_skills, 35, 65, 110, 180)]

        # الجاتلينج (Z)
        self.gatling_lvl1 = [self.get_frame(self.sheet_lvl2, 10, 260, 115, 170), self.get_frame(self.sheet_lvl2, 385, 260, 195, 170)]
        # الكومبو الأسطوري (X)
        self.boss_combo = [self.get_frame(self.sheet_combo, 750, 625, 245, 160), self.get_frame(self.sheet_combo, 480, 575, 230, 225)]

        self.reset()
        self.speed, self.gravity, self.jump_power = 8, 0.6, -14
        
        # --- نظام الكومبو الجديد ---
        self.gatling_usage = 0 # عداد استخدام الجاتلينج
        self.combo_ready = False

    def get_frame(self, sheet, x, y, w, h):
        sub = sheet.subsurface((int(x), int(y), int(w), int(h))).copy()
        sub.set_colorkey((255, 174, 0))
        ratio = w / h
        return pygame.transform.scale(sub, (int(64 * ratio), 64))

    def reset(self):
        self.x, self.y = self.initial_start
        self.health, self.energy, self.velocity_y = 100, 100, 0
        self.on_ground, self.state, self.frame_index = False, "idle", 0
        self.facing_left, self.image = False, self.idle_frames[0]
        self.gatling_usage = 0
        self.combo_ready = False

    def update(self, keys, obstacles, dangers):
        # زيادة الطاقة بالراحة
        if self.energy < 100: self.energy += 0.1
        
        new_state = "idle"
        is_attacking = self.state in ["gatling", "boss_combo", "dodge"]

        if not is_attacking:
            if keys[pygame.K_RIGHT]: self.x += self.speed; new_state = "run"; self.facing_left = False
            elif keys[pygame.K_LEFT]: self.x -= self.speed; new_state = "run"; self.facing_left = True
            if keys[pygame.K_UP] and self.on_ground: self.velocity_y = self.jump_power; self.on_ground = False
            
            # زر Z (جاتلينج)
            if keys[pygame.K_z] and self.energy >= 15:
                new_state = "gatling"
                self.energy -= 10
                self.gatling_usage += 1
                if self.gatling_usage >= 3: self.combo_ready = True
            
            # زر X (الكومبو الأسطوري - متاح بعد 3 جاتلينج)
            if keys[pygame.K_x] and self.combo_ready and self.energy >= 30:
                new_state = "boss_combo"
                self.energy -= 25
                self.combo_ready = False
                self.gatling_usage = 0
            
            if keys[pygame.K_DOWN]: new_state = "dodge"
        else: new_state = self.state

        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        l_rect = pygame.Rect(int(self.x + 25), int(self.y + 10), self.SIZE[0], self.SIZE[1]-1)
        self.on_ground = False
        for b in obstacles + dangers:
            if abs(b.x - self.x) < 200:
                if l_rect.colliderect(b):
                    if self.velocity_y >= 0:
                        self.y = b.top - 64
                        self.velocity_y = 0
                        self.on_ground = True
                    if b in dangers:
                        self.health -= 1 # تأثر لوفي بالـ Danger
                        if self.health <= 0: self.reset()
                    break

        if not self.on_ground and new_state not in ["gatling", "boss_combo", "dodge"]: new_state = "jump"
        if new_state != self.state: self.state = new_state; self.frame_index = 0
        self.animate()

    def animate(self):
        if self.state == "run": anim = self.run_frames
        elif self.state == "gatling": anim = self.gatling_lvl1
        elif self.state == "boss_combo": anim = self.boss_combo
        elif self.state == "dodge": anim = self.dodge_frames
        elif self.state == "jump": anim = self.jump_frames
        else: anim = self.idle_frames

        self.frame_index += 0.15
        if self.frame_index >= len(anim):
            if self.state in ["gatling", "boss_combo", "dodge"]: self.state = "idle"
            self.frame_index = 0
        self.image = anim[int(self.frame_index) % len(anim)]
        if self.facing_left: self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface, camera_x):
        render_x = int(self.x + camera_x)
        if self.facing_left: render_x -= (self.image.get_width() - 64)
        surface.blit(self.image, (render_x, int(self.y)))