import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Test")

clock = pygame.time.Clock()

# ==========================
# STATES
# ==========================

MENU = "menu"
BOSS = "boss"
WIN = "win"
GAME_OVER = "game_over"

game_state = MENU

# ==========================
# BOSS
# ==========================

class Boss:

    def __init__(self):

        self.x = 600
        self.y = 300

        self.width = 120
        self.height = 120

        self.health = 100

        self.speed = 2

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self, player_x):

        if player_x < self.x:
            self.x -= self.speed

        elif player_x > self.x:
            self.x += self.speed

        self.rect.x = self.x

    def take_damage(self, amount):

        self.health -= amount

        if self.health < 0:
            self.health = 0

    def is_dead(self):

        return self.health <= 0

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            self.rect
        )

        # Health Bar Background
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (20, 20, 200, 20)
        )

        # Health Bar
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (20, 20, self.health * 2, 20)
        )


boss = Boss()

# ==========================
# PLAYER
# ==========================

player_x = 100
player_y = 320

player_speed = 5

player_rect = pygame.Rect(
    player_x,
    player_y,
    60,
    80
)

font_big = pygame.font.Font(None, 80)
font_small = pygame.font.Font(None, 40)

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Start Game
            if game_state == MENU:

                if event.key == pygame.K_RETURN:
                    game_state = BOSS

            # Attack Boss
            elif game_state == BOSS:

                if event.key == pygame.K_x:

                    if player_rect.colliderect(boss.rect):

                        boss.take_damage(10)

                        print("Boss HP:", boss.health)

    keys = pygame.key.get_pressed()

    # ==========================
    # MENU
    # ==========================

    if game_state == MENU:

        screen.fill((30, 30, 30))

        title = font_big.render(
            "LUFFY ADVENTURE",
            True,
            (255, 255, 255)
        )

        start_text = font_small.render(
            "Press ENTER To Start",
            True,
            (255, 255, 255)
        )

        screen.blit(title, (130, 220))
        screen.blit(start_text, (250, 320))

    # ==========================
    # BOSS FIGHT
    # ==========================

    elif game_state == BOSS:

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        player_rect.x = player_x

        boss.update(player_x)

        if boss.is_dead():
            game_state = WIN

        screen.fill((200, 220, 255))

        pygame.draw.rect(
            screen,
            (0, 0, 255),
            player_rect
        )

        boss.draw(screen)

        info = font_small.render(
            "Move: Arrows | Attack: X",
            True,
            (0, 0, 0)
        )

        screen.blit(info, (20, 60))

    # ==========================
    # WIN
    # ==========================

    elif game_state == WIN:

        screen.fill((0, 120, 0))

        text = font_big.render(
            "YOU WIN!",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (220, 250))

    # ==========================
    # GAME OVER
    # ==========================

    elif game_state == GAME_OVER:

        screen.fill((120, 0, 0))

        text = font_big.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (160, 250))

    pygame.display.update()
    clock.tick(60)

pygame.quit()