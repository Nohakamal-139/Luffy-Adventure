import pygame
import sys
from world import World
from Character import Character

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_level('level1.tmx')

    def load_level(self, level_name):
        self.world = World(level_name)
        self.map_surface = self.world.make_map()
        self.map_rect = self.map_surface.get_rect()
        
        points = self.world.get_objects()
        self.luffy = Character(points.get('start', (100, 300)))
        
        self.meats = []
        
        for obj in self.world.tmx_data.objects:
            if obj.name == 'meat':
                self.meats.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        self.camera_x = 0

    def run(self):
        while self.running:
            self.handle_events()
            keys = pygame.key.get_pressed()
            self.luffy.update(keys, self.world.obstacles, self.world.dangers)
            
            luffy_rect = pygame.Rect(self.luffy.x, self.luffy.y, 80, 80)
            for meat_data in self.world.meats[:]:
                meat_rect = meat_data[0]
                if luffy_rect.colliderect(meat_rect):
                    self.luffy.health = min(100, self.luffy.health + 10)
                    self.world.meats.remove(meat_data)
                    meat_data[3].data[meat_data[2]][meat_data[1]] = 0 

            self.camera_x = int(-(self.luffy.x - 350))
            if self.camera_x > 0: self.camera_x = 0
            if self.camera_x < -(self.map_rect.width - 800):
                self.camera_x = -(self.map_rect.width - 800)

            self.screen.fill((135, 206, 235))
            self.screen.blit(self.map_surface, (self.camera_x, 0))
            

            self.luffy.draw(self.screen, self.camera_x)
            self.draw_gui()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_gui(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 20, 200, 20)) # خلفية بار
        pygame.draw.rect(self.screen, (255, 0, 0), (20, 20, self.luffy.health * 2, 20))
        
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 50, 200, 15)) # خلفية بار
        pygame.draw.rect(self.screen, (255, 255, 0), (20, 50, self.luffy.energy * 2, 15))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False

if __name__ == "__main__":
    Game().run()