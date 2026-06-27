import pygame
import os

class Character:
    def __init__(self, start_pos):
        self.SIZE = (120, 120) # حجم لوفي المناسب
        self.initial_start = start_pos
        # تحميل الصورة (تأكدي من الاسم بالظبط)
        self.sheet = pygame.image.load("assets\luffy_lvl2_gatling.jpg.png").convert_alpha()
        self.sheet.set_colorkey((255, 174, 0)) # مسح الخلفية البرتقالية

        # --- تقطيع الحركات بدقة (إحداثيات من الصورة اللي بعتيها) ---
        # 1. الوقوف (Idle)
        self.idle_frames = self.load_frames([(10, 10, 60, 90), (75, 10, 60, 90), (140, 10, 60, 90)])
        
        # 2. الجري (Run)
        self.run_frames = self.load_frames([(530, 10, 80, 90), (620, 10, 80, 90), (710, 10, 80, 90)])
        
        # 3. القفز (Jump)
        self.jump_frames = self.load_frames([(10, 130, 70, 90)])

        # 4. الجاتلينج الأسطوري (Gatling) - زر Z (فريمات الأيدي الكثيرة)
        self.gatling_frames = self.load_frames([
            (110, 130, 120, 90), # بداية الحركة
            (240, 130, 150, 90), # الإيد الممتدة
            (400, 130, 150, 90), # ضربات سريعة
            (10, 260, 150, 95),  # تكملة الضرب من الصف الثالث
            (170, 260, 150, 95)  # أقوى فريم في الجاتلينج
        ])

        self.reset()
        self.speed = 8
        self.gravity = 0.8
        self.jump_power = -18

    def load_frames(self, coords):
        frames = []
        for c in coords:
            sub = self.sheet.subsurface(c).copy()
            sub.set_colorkey((255, 174, 0)) 
            frames.append(pygame.transform.scale(sub, self.SIZE))
        return frames

    def reset(self):
        self.x, self.y = self.initial_start
        self.health, self.energy = 100, 100
        self.vel_y, self.on_ground = 0, False
        self.state, self.frame_index = "idle", 0
        self.facing_left = False
        self.image = self.idle_frames[0]

    def update(self, keys, obstacles, dangers):
        # تجميد الحركة لو بيعمل جاتلينج (عشان يركز في الضرب)
        if self.state == "gatling":
            self.animate()
            return

        new_state = "idle"
        # الحركة يمين وشمال
        if keys[pygame.K_RIGHT]: 
            self.x += self.speed; new_state = "run"; self.facing_left = False
        elif keys[pygame.K_LEFT]: 
            self.x -= self.speed; new_state = "run"; self.facing_left = True
        
        # القفز
        if keys[pygame.K_UP] and self.on_ground: 
            self.vel_y = self.jump_power; self.on_ground = False

        # تفعيل الجاتلينج بـ Z
        if keys[pygame.K_z]:
            new_state = "gatling"

        # الفيزياء
        self.vel_y += self.gravity
        self.y += self.vel_y

        # التصادم (Solid)
        l_rect = pygame.Rect(int(self.x + 30), int(self.y), 60, 100)
        self.on_ground = False
        for b in obstacles:
            if l_rect.colliderect(b) and self.vel_y > 0:
                self.y = b.top - 100; self.vel_y = 0; self.on_ground = True

        # التصادم (Danger)
        for d in dangers:
            if l_rect.colliderect(d): self.health -= 0.5
            if self.health <= 0: self.reset()

        if not self.on_ground and new_state != "gatling": new_state = "jump"
        
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0
        self.animate()

    def animate(self):
        frames = self.animations_map()
        
        # سرعة الجاتلينج أسرع من المشي
        anim_speed = 0.25 if self.state == "gatling" else 0.15
        
        self.frame_index += anim_speed
        if self.frame_index >= len(frames):
            if self.state == "gatling":
                self.state = "idle" # يرجع يقف بعد الجاتلينج
            self.frame_index = 0
        
        self.image = frames[int(self.frame_index)]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def animations_map(self):
        if self.state == "run": return self.run_frames
        if self.state == "jump": return self.jump_frames
        if self.state == "gatling": return self.gatling_frames
        return self.idle_frames

    def draw(self, surface, camera_x):
        # أهم سطر لمنع اللاج (تحويل لـ int)
        render_x = int(self.x + camera_x)
        if self.facing_left and self.state == "gatling":
            # زحزحة لوفي عشان إيده تضرب في الاتجاه الصح وهو باصص شمال
            render_x -= 50
        surface.blit(self.image, (render_x, int(self.y)))