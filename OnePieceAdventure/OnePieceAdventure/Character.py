import pygame
import os

class Character:
    def __init__(self, start_pos):
        # إعدادات الحجم والمسارات
        self.SIZE = (130, 150)
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # تحميل الصور
        path_base = os.path.join(self.BASE_DIR, "assets", "luffy_base_sheet.png")
        path_skills = os.path.join(self.BASE_DIR, "assets", "luffy_skills_sheet.png")
        
        try:
            self.sheet_base = pygame.image.load(path_base).convert_alpha()
            self.sheet_skills = pygame.image.load(path_skills).convert_alpha()
        except:
            # في حال كانت الامتدادات jpg
            path_base = path_base.replace(".png", ".jpg")
            path_skills = path_skills.replace(".png", ".jpg")
            self.sheet_base = pygame.image.load(path_base).convert_alpha()
            self.sheet_skills = pygame.image.load(path_skills).convert_alpha()

        # تقطيع الفريمات (نفس إحداثيات زميلتك)
        self.idle_frames = self.load_frames(self.sheet_base, [(10, 85, 105, 185), (140, 85, 105, 185), (270, 85, 105, 185), (400, 85, 105, 185), (530, 85, 105, 185)])
        self.run_frames = self.load_frames(self.sheet_base, [(660, 85, 120, 185), (790, 85, 125, 185), (10, 310, 125, 185), (170, 310, 125, 185)])
        self.jump_frames = self.load_frames(self.sheet_base, [(20, 535, 110, 135), (150, 535, 110, 135)])
        self.attack_frames = self.load_frames(self.sheet_skills, [(35, 65, 110, 180), (235, 65, 110, 180), (435, 65, 110, 180)])
        self.gatling_frames = self.load_frames(self.sheet_skills, [(285, 275, 140, 180), (425, 275, 140, 180)])
        self.gum_gum_frames = self.load_frames(self.sheet_skills, [(10, 970, 245, 185), (710, 1170, 265, 185)])

        # حالة اللاعب
        self.x, self.y = start_pos
        self.state = "idle"
        self.frame_index = 0
        self.anim_speed = 0.15
        self.facing_left = False
        
        # الفيزياء
        self.vel_y = 0
        self.gravity = 0.6
        self.jump_power = -14
        self.ground_y = self.y # الأرض هي النقطة التي بدأ منها في الخريطة
        self.on_ground = True
        self.speed = 6

    def load_frames(self, sheet, coords):
        frames = []
        for x, y, w, h in coords:
            sub = sheet.subsurface((x, y, w, h)).copy()
            sub.set_colorkey((0, 0, 0))
            frames.append(pygame.transform.scale(sub, self.SIZE))
        return frames

    def update(self, keys):
        new_state = "idle"
        
        # الحركة يميناً ويساراً
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            new_state = "run"
            self.facing_left = False
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed
            new_state = "run"
            self.facing_left = True

        # القفز
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        # المهارات
        if keys[pygame.K_x]: new_state = "attack"
        elif keys[pygame.K_z]: new_state = "gatling"
        elif keys[pygame.K_c]: new_state = "gum_gum"

        # الجاذبية
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.vel_y = 0
            self.on_ground = True
        else:
            if new_state not in ["attack", "gatling", "gum_gum"]:
                new_state = "jump"

        # تحديث الأنيميشن
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0

        self.animate()

    def animate(self):
        frames = self.idle_frames
        if self.state == "run": frames = self.run_frames
        elif self.state == "jump": frames = self.jump_frames
        elif self.state == "attack": frames = self.attack_frames
        elif self.state == "gatling": frames = self.gatling_frames
        elif self.state == "gum_gum": frames = self.gum_gum_frames

        self.frame_index += self.anim_speed
        if self.frame_index >= len(frames):
            if self.state in ["attack", "gatling", "gum_gum"]:
                self.state = "idle" # العودة للوقوف بعد الضربة
            self.frame_index = 0
        
        self.image = frames[int(self.frame_index)]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface, camera_x):
        # الرسم مع مراعاة مكان الكاميرا
        surface.blit(self.image, (self.x + camera_x, self.y))