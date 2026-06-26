import pygame
import os

class Character:
    def __init__(self, start_pos):
        self.SIZE = (64, 64)
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
      
        self.sheet_base = pygame.image.load(os.path.join(self.BASE_DIR, "assets", "luffy_base_sheet.png")).convert_alpha()
        self.sheet_skills = pygame.image.load(os.path.join(self.BASE_DIR, "assets", "luffy_skills_sheet.png")).convert_alpha()

        
        self.idle_frames = self.load_frames(self.sheet_base, [(10, 85, 105, 185), (140, 85, 105, 185), (270, 85, 105, 185), (400, 85, 105, 185), (530, 85, 105, 185)])
        self.run_frames = self.load_frames(self.sheet_base, [(660, 85, 120, 185), (790, 85, 125, 185), (10, 310, 125, 185), (170, 310, 125, 185)])
        self.jump_frames = self.load_frames(self.sheet_base, [(20, 535, 110, 135), (150, 535, 110, 135)])
        self.attack_frames = self.load_frames(self.sheet_skills, [(35, 65, 110, 180), (235, 65, 110, 180), (435, 65, 110, 180)])

        
        self.health = 100
        self.max_health = 100
        self.energy = 100
        self.max_energy = 100
        
        
        self.x, self.y = start_pos
        self.initial_start = start_pos
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_power = -16
        self.speed = 7
        self.on_ground = False
        
        self.state = "idle"
        self.frame_index = 0
        self.facing_left = False

    def load_frames(self, sheet, coords):
        frames = []
        for x, y, w, h in coords:
            sub = sheet.subsurface((x, y, w, h)).copy()
            sub.set_colorkey((0, 0, 0))
            frames.append(pygame.transform.scale(sub, self.SIZE))
        return frames

    def update(self, keys, obstacles, dangers):
        new_state = "idle"
        
       
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            new_state = "run"
            self.facing_left = False
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed
            new_state = "run"
            self.facing_left = True

   
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

       
        if keys[pygame.K_z]:
            new_state = "gum_gum"

      
        self.vel_y += self.gravity
        self.y += int(self.vel_y)
        
        luffy_rect = pygame.Rect(self.x, self.y, self.SIZE[0], self.SIZE[1])
        self.on_ground = False
        for block in obstacles:
            if luffy_rect.colliderect(block):
                if self.vel_y > 0:
                    self.y = block.top - self.SIZE[1]
                    self.vel_y = 0
                    self.on_ground = True

        for trap in dangers:
            if luffy_rect.colliderect(trap):
                self.health -= 0.5 
                if self.health <= 0: self.reset()

        if not self.on_ground and new_state != "gum_gum":
            new_state = "jump"
        
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0
        self.animate()

    def reset(self):
        self.health = 100
        self.energy = 100
        self.x, self.y = self.initial_start
        self.vel_y = 0

    def animate(self):
        frames = self.idle_frames
        if self.state == "run": frames = self.run_frames
        elif self.state == "jump": frames = self.jump_frames
        elif self.state == "attack": frames = self.attack_frames

        self.frame_index += 0.15
        if self.frame_index >= len(frames):
            if self.state == "attack": self.state = "idle"
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface, camera_x):
        surface.blit(self.image, (int(self.x + camera_x), int(self.y)))