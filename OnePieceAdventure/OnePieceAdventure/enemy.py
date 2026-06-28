import pygame
import os

class Marine:
    def __init__(self, x, y, sheet):
        self.x, self.y = x, y
        self.sheet = sheet
        self.size = (64, 64)
        self.walk_left, self.walk_right = [], []
        
        for i in range(6):
            sub = self.sheet.subsurface((25 + (i * 42), 38, 50, 55)).copy()
            pa = pygame.PixelArray(sub)
            pa.replace((255, 174, 0), (0,0,0,0), distance=0.15)
            del pa
            scaled = pygame.transform.scale(sub, self.size)
            self.walk_left.append(scaled)
            self.walk_right.append(pygame.transform.flip(scaled, True, False))

        self.health = 100
        self.speed = 1.5
        self.bullets = []
        self.cooldown = 0
        self.frame_index = 0
        self.velocity_y = 0
        self.gravity = 0.8
        self.facing_left = True
        self.flash_timer = 0
        
        self.sight_range = 500 

    def update(self, luffy_x, luffy_y, obstacles, dangers):
        dist = abs(self.x - luffy_x)
        
        if dist < self.sight_range:
            self.facing_left = (self.x > luffy_x)
            
            if self.x > luffy_x + 100: self.x -= self.speed
            elif self.x < luffy_x - 100: self.x += self.speed

            if self.cooldown > 0: self.cooldown -= 1
            if self.cooldown == 0:
                direction = -1 if self.facing_left else 1
                self.bullets.append({"rect": pygame.Rect(self.x + 30, self.y + 30, 12, 5), "dir": direction})
                self.cooldown = 80
        else:
            pass

        self.velocity_y += self.gravity
        self.y += self.velocity_y
        marine_rect = pygame.Rect(int(self.x), int(self.y), 64, 64)
        for b in obstacles + dangers:
            if marine_rect.colliderect(b) and self.velocity_y >= 0:
                self.y = b.top - 64
                self.velocity_y = 0

        for b in self.bullets[:]:
            b["rect"].x += 7 * b["dir"]
            if b["rect"].x < 0 or b["rect"].x > 5000: self.bullets.remove(b)

        self.frame_index = (self.frame_index + 0.1) % len(self.walk_left)
        if self.flash_timer > 0: self.flash_timer -= 1

    def draw(self, surface, camera_x):
        if -100 < self.x + camera_x < 900:
            img = self.walk_left[int(self.frame_index)] if self.facing_left else self.walk_right[int(self.frame_index)]
            if self.flash_timer > 0:
                temp = img.copy()
                temp.fill((255, 0, 0, 150), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(temp, (int(self.x + camera_x), int(self.y)))
            else:
                surface.blit(img, (int(self.x + camera_x), int(self.y)))
            
            for b in self.bullets:
                pygame.draw.rect(surface, (240, 210, 20), (int(b["rect"].x + camera_x), int(b["rect"].y), 12, 5))




class Crocodile:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.size = (150, 160)
        self.sheet3 = pygame.image.load("luffy/sheet3.jpg.png").convert_alpha()
        self.sheet4 = pygame.image.load("luffy/sheet4.jpg.png").convert_alpha()
        
        self.idle_frames = []
        for i in range(4):
            sub = self.sheet3.subsurface((i * 125, 0, 125, 145)).copy()
            sub.set_colorkey(sub.get_at((0,0)))
            self.idle_frames.append(pygame.transform.scale(sub, self.size))
            
        self.attack_frames = []
        for i in range(4):
            sub = self.sheet4.subsurface((i * 130, 0, 130, 135)).copy()
            sub.set_colorkey(sub.get_at((0,0)))
            self.attack_frames.append(pygame.transform.scale(sub, self.size))

        self.image = self.idle_frames[0]
        self.health, self.max_health = 500, 500
        self.state, self.frame_index, self.flash_timer = "idle", 0, 0
        self.facing_left, self.attack_timer = True, 0

    def update(self, luffy_x, luffy_y):
        self.facing_left = (self.x > luffy_x)
        self.attack_timer += 1
        
        if self.attack_timer > 120:
            self.state = "attack"
            if self.attack_timer > 180:
                self.state = "idle"
                self.attack_timer = 0

        frames = self.attack_frames if self.state == "attack" else self.idle_frames
        self.frame_index = (self.frame_index + 0.1) % len(frames)
        self.image = frames[int(self.frame_index)]
        if self.flash_timer > 0: self.flash_timer -= 1

    def draw(self, surface, camera_x):
        img = self.image
        if not self.facing_left: img = pygame.transform.flip(img, True, False)
        
        render_pos = (int(self.x + camera_x), int(self.y))
        
        if self.flash_timer > 0:
            temp = img.copy()
            temp.fill((255, 0, 0, 150), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(temp, render_pos)
        else:
            surface.blit(img, render_pos)