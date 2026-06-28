import pygame
import sys
import os

# ==========================================
# 1. تهيئة النظام وإعدادات الشاشة واكتشاف المسارات الذكي الشامل
# ==========================================
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Luffy vs Sir Crocodile - Logic Remastered")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 24, bold=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(BASE_DIR, "assets")

def find_image_by_prefix(prefix):
    """ دالة قوية تبحث عن أي صورة تبدأ بالاسم المطلوب في المجلد الرئيسي أو assets بغض النظر عن امتدادها """
    # البحث في المجلد الرئيسي
    if os.path.exists(BASE_DIR):
        for file in os.listdir(BASE_DIR):
            if file.lower().startswith(prefix.lower()) and file.lower().endswith(('.jpg', '.png', '.jpeg')):
                return os.path.join(BASE_DIR, file)
                
    # البحث داخل مجلد assets
    if os.path.exists(assets_dir):
        for file in os.listdir(assets_dir):
            if file.lower().startswith(prefix.lower()) and file.lower().endswith(('.jpg', '.png', '.jpeg')):
                return os.path.join(assets_dir, file)
    return None

# البحث الديناميكي عن الشيتات بأي امتداد متوفر
PATH_SHEET3 = find_image_by_prefix("sheet3")
PATH_SHEET4 = find_image_by_prefix("sheet4")

# التحقق النهائي والآمن جداً
if not PATH_SHEET3 or not PATH_SHEET4:
    print("\n❌ خطأ حرج: لم يتم العثور على ملفات صور كروكودايل نهائياً!")
    print(f"تأكدي من وجود الصور داخل الفولدر: {BASE_DIR}")
    print("أو داخل مجلد assets، وتأكدي أن أسماء الملفات تبدأ بـ sheet3 و sheet4")
    pygame.quit()
    exit()

try:
    print(f"🎯 تم العثور على شيت 3 بنجاح في: {PATH_SHEET3}")
    print(f"🎯 تم العثور على شيت 4 بنجاح في: {PATH_SHEET4}")
    sheet3 = pygame.image.load(PATH_SHEET3).convert_alpha()
    sheet4 = pygame.image.load(PATH_SHEET4).convert_alpha()
    print("✅ تم تحميل شيتات كروكودايل بنجاح وتطبيق المنطق الديناميكي!")
except pygame.error as e:
    print(f"❌ خطأ داخلي في مكتبة Pygame أثناء قراءة الصور: {e}")
    pygame.quit()
    exit()

# 🎯 الحجم الموحد لكروكودايل على الشاشة لضمان ثبات الرأس والجسد كاملاً
BOSS_SIZE = (140, 150)

def get_boss_frame(sheet, x, y, w, h):
    """ دالة التقطيع الآمنة والمباشرة المأخوذة من منطق كود لوفي الاحترافي """
    sub = sheet.subsurface((int(x), int(y), int(w), int(h))).copy()
    bg_color = sub.get_at((0, 0))
    sub.set_colorkey(bg_color)
    return pygame.transform.scale(sub, BOSS_SIZE)


# ==========================================
# 2. القذائف (الأعاصير الرملية)
# ==========================================
class Tornado:
    def __init__(self, x, y, direction, is_spada=False):
        self.x, self.y, self.direction = x, y, direction
        self.is_spada = is_spada
        self.width, self.height, self.speed = (90, 60, 10) if is_spada else (80, 120, 6)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x

    def draw(self, screen, offset_x):
        pygame.draw.rect(screen, (210, 180, 140), (self.rect.x - offset_x, self.rect.y, self.width, self.height))


# ==========================================
# 3. زعيم المرحلة (كروكودايل بالمنطق الجديد)
# ==========================================
class Boss:
    def __init__(self, x, y, hp, damage):
        self.x, self.y, self.hp, self.max_hp, self.damage = x, y, hp, hp, damage
        self.speed, self.base_speed, self.facing, self.state, self.phase = 3, 3, "LEFT", "IDLE", 1
        
        self.width, self.height = BOSS_SIZE
        self.visible, self.active_tornados, self.state_timer, self.invuln_timer = True, [], 0, 0
        self.velocity_y, self.gravity, self.ground, self.on_ground = 0, 0.6, y, True
        self.attack_range, self.rect = 110, pygame.Rect(self.x, self.y, self.width, self.height)
        self.has_seen_player = False
        
        self.current_frame = 0
        self.animation_speed = 0.15  
        self.slice_animations()

    def slice_animations(self):
        """ تطبيق منطق لوفي: التقطيع البرمجي المباشر بالبكسل من الشيتات لضمان كامل الهيبة والرأس """
        self.animations = {
            "idle": [], "run": [], "melee_attack": [], "dash_attack": [], 
            "hurt": [], "sand_fly": [], "ground_smash": []
        }
        
        # 1. حركات الإعصار من Sheet 3
        # Idle (الوقوف بالإعصار)
        for i in range(4):
            self.animations["idle"].append(get_boss_frame(sheet3, i * 125, 0, 125, 145))
        # Run (التحرك بالإعصار)
        for i in range(4):
            self.animations["run"].append(get_boss_frame(sheet3, i * 125, 145, 125, 145))
        # Sand Fly (الطيران الرملي)
        for i in range(2):
            self.animations["sand_fly"].append(get_boss_frame(sheet3, i * 145, 500, 145, 140))

        # 2. حركات القتال الأرضي من Sheet 4
        # Melee Attack (الضربات الخطافية النظيفة بكامل ملامح الوجه والسيجار)
        for i in range(4):
            self.animations["melee_attack"].append(get_boss_frame(sheet4, i * 130, 0, 130, 135))
        # Dash Attack (الاندفاع والانقضاض القوي)
        for i in range(4):
            self.animations["dash_attack"].append(get_boss_frame(sheet4, i * 130, 135, 130, 135))
        # Ground Smash (تحطيم الأرض)
        for i in range(2):
            self.animations["ground_smash"].append(get_boss_frame(sheet4, i * 140, 345, 140, 140))
        # Hurt (التأثر بالضرب)
        self.animations["hurt"].append(get_boss_frame(sheet4, 0, 270, 130, 135))

    def animate(self):
        state_key = self.state.lower()
        frames = self.animations.get(state_key, self.animations["idle"])
        self.current_frame += self.animation_speed
        if self.current_frame >= len(frames):
            if state_key in ["melee_attack", "ground_smash", "hurt"]:
                self.current_frame = len(frames) - 1 
            else:
                self.current_frame = 0 

    def update(self, px, p_rect, dmg_callback, lvl_width, state):
        old_state = self.state
        if self.state not in ["DASH_ATTACK", "GROUND_SMASH", "HURT"]:
            self.facing = "RIGHT" if px > self.x else "LEFT"

        self.invuln_timer = max(0, self.invuln_timer - 1)
        self.state_timer = max(0, self.state_timer - 1)
        dist = abs(px - self.x)
        
        if not self.has_seen_player:
            if dist <= 500 or self.hp < self.max_hp or "BOSS" in state:
                self.has_seen_player = True
            else:
                self.state = "IDLE"

        for tor in self.active_tornados[:]:
            tor.update()
            if tor.rect.colliderect(p_rect):
                dmg_callback(self.damage)
                self.active_tornados.remove(tor)
            elif tor.rect.x < -200 or tor.rect.x > lvl_width + 200:
                self.active_tornados.remove(tor)

        if self.has_seen_player:
            if self.state == "HURT":
                if self.state_timer <= 0: self.state = "IDLE"
            elif self.state == "DASH_ATTACK":
                self.x += (-5 if self.facing == "LEFT" else 5) * self.speed
                if self.rect.colliderect(p_rect): dmg_callback(int(self.damage * 1.5))
                if self.state_timer == 0 or self.x < 0 or self.x > lvl_width: self.state = "IDLE"
            elif self.state == "GROUND_SMASH":
                if self.state_timer == 15 and dist < 150:
                    dmg_callback(int(self.damage * 1.8))
                if self.state_timer <= 0: self.state = "IDLE"
            elif self.state == "MELEE_ATTACK":
                if self.state_timer == 15 and dist < self.attack_range + 20:
                    dmg_callback(self.damage)
                if self.state_timer <= 0: self.state = "IDLE"
            else:
                if dist > 320 and self.phase >= 2 and self.state_timer == 0:
                    self.state = "DASH_ATTACK"
                    self.state_timer = 40
                elif dist > self.attack_range:
                    self.state = "SAND_FLY" if self.phase == 3 else "RUN"
                    run_dir = 1 if px > self.x else -1
                    self.x += run_dir * self.speed
                else:
                    if dist < 60 and self.phase >= 2:
                        self.state = "GROUND_SMASH"
                        self.state_timer = 35
                    else:
                        self.state = "MELEE_ATTACK"
                        self.state_timer = 30

            self.x = max(0, min(self.x, lvl_width - self.width))
            self.rect.x = self.x
        
        if self.state != old_state: self.current_frame = 0
        self.animate()

        self.velocity_y += self.gravity
        self.y += self.velocity_y
        if self.y >= self.ground: self.y, self.velocity_y, self.on_ground = self.ground, 0, True
        self.rect.y = self.y

    def take_damage(self, amount):
        if self.invuln_timer > 0: return
        self.hp = max(0, self.hp - amount)
        self.phase = 3 if self.hp <= self.max_hp * 0.3 else 2 if self.hp <= self.max_hp * 0.6 else 1
        self.speed = self.base_speed + (self.phase - 1)
        self.state, self.state_timer, self.invuln_timer = "HURT", 25, 35
        self.x += 20 if self.facing == "LEFT" else -20
        self.current_frame = 0

    def draw(self, screen, offset_x):
        for tor in self.active_tornados: tor.draw(screen, offset_x)
        if self.visible and not (self.invuln_timer > 0 and (self.invuln_timer // 5) % 2 == 0):
            state_key = self.state.lower()
            frames = self.animations.get(state_key, self.animations["idle"])
            frame_idx = int(self.current_frame) % len(frames)
            current_sprite = frames[frame_idx]
            
            if self.facing == "RIGHT":
                current_sprite = pygame.transform.flip(current_sprite, True, False)
                render_x = self.rect.x - (current_sprite.get_width() - BOSS_SIZE[0])
            else:
                render_x = self.rect.x
                
            screen.blit(current_sprite, (render_x - offset_x, self.rect.y))


# ==========================================
# 4. اللاعب والمنصات البيئية
# ==========================================
class LuffyPlayer:
    def __init__(self, x, y):
        self.x, self.y, self.width, self.height = x, y, 70, 80
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed, self.velocity_y, self.gravity, self.jump_power, self.on_ground = 6, 0, 0.6, -14, False
        self.health, self.max_health, self.facing, self.is_attacking, self.attack_timer = 100, 100, "RIGHT", False, 0

    def update(self, keys, platforms, lvl_width):
        if keys[pygame.K_RIGHT]: self.x, self.facing = self.x + self.speed, "RIGHT"
        if keys[pygame.K_LEFT]: self.x, self.facing = self.x - self.speed, "LEFT"
        if keys[pygame.K_SPACE] and self.on_ground: self.velocity_y, self.on_ground = self.jump_power, False

        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.on_ground = False
        self.rect.x, self.rect.y = self.x, self.y

        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.velocity_y > 0 and self.rect.bottom <= p.rect.top + 15:
                    self.rect.bottom, self.y, self.velocity_y, self.on_ground = p.rect.top, self.rect.y, 0, True
                    if p.is_moving: self.x += p.speed_x

        self.x = max(0, min(self.x, lvl_width - self.width))
        self.rect.x = self.x
        if self.y > 500: self.health = 0

    def draw(self, screen, offset_x):
        pygame.draw.rect(screen, (0, 102, 204), (self.rect.x - offset_x, self.rect.y, self.width, self.height), border_radius=5)
        if self.is_attacking:
            fist_x = self.rect.right - offset_x if self.facing == "RIGHT" else self.rect.left - offset_x - 20
            pygame.draw.rect(screen, (255, 51, 51), (fist_x, self.rect.y + 25, 20, 20))


class Platform:
    def __init__(self, x, y, width, height, is_moving=False, range_x=200):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_moving, self.start_x, self.range_x, self.speed_x = is_moving, x, range_x, (2 if is_moving else 0)

    def update(self):
        if self.is_moving:
            self.rect.x += self.speed_x
            if abs(self.rect.x - self.start_x) >= self.range_x: self.speed_x *= -1

    def draw(self, screen, offset_x):
        pygame.draw.rect(screen, (194, 178, 128) if self.is_moving else (139, 128, 0), (self.rect.x - offset_x, self.rect.y, self.rect.width, self.rect.height), border_radius=3)


# ==========================================
# 5. حلقة اللعبة الأساسية (Main Loop)
# ==========================================
if __name__ == "__main__":
    state, player, platforms, current_boss, level_width, offset_x = "MAIN_MENU", None, [], None, 1000, 0
    levels = {
        1: (1600, [Platform(0, 500, 1600, 100), Platform(300, 380, 200, 20), Platform(700, 300, 250, 20, True, 150)]),
        2: (2000, [Platform(0, 500, 2000, 100), Platform(200, 380, 150, 20), Platform(500, 290, 200, 20), Platform(900, 350, 200, 20, True, 200)]),
        3: (2500, [Platform(0, 500, 2500, 100), Platform(200, 400, 120, 20), Platform(450, 300, 120, 20, True), Platform(850, 230, 200, 20), Platform(1300, 350, 150, 20)])
    }

    def start_level(idx):
        global player, platforms, level_width, current_boss, offset_x
        level_width, platforms = levels[idx]
        player = LuffyPlayer(100, 400)
        current_boss = Boss(level_width - 180, 350, 120 if idx==1 else 180 if idx==2 else 300, 4 if idx==1 else 8 if idx==2 else 14)
        offset_x = 0

    running = True
    while running:
        screen.fill((245, 230, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and state == "MAIN_MENU":
                    state = "LEVEL1"
                    start_level(1)
                elif event.key == pygame.K_r and state == "GAME_OVER":
                    state = "MAIN_MENU"
                elif event.key == pygame.K_x and player and not player.is_attacking:
                    player.is_attacking, player.attack_timer = True, 15
                    if current_boss and abs(player.x - current_boss.x) < 150 and abs(player.y - current_boss.y) < 130:
                        current_boss.take_damage(15)

        if player and player.is_attacking:
            player.attack_timer -= 1
            if player.attack_timer <= 0: player.is_attacking = False

        if "LEVEL" in state or "BOSS" in state:
            idx = 1 if "1" in state else 2 if "2" in state else 3
            keys = pygame.key.get_pressed()
            
            if player:
                player.update(keys, platforms, level_width)
                if player.health <= 0: state = "GAME_OVER"
            
            for p in platforms: p.update()
            if current_boss and player:
                current_boss.update(player.x, player.rect, lambda dmg: player.__setattr__('health', max(0, player.health - dmg)), level_width, state)
                if current_boss.hp <= 0:
                    if idx < 3:
                        state = f"LEVEL{idx+1}"
                        start_level(idx+1)
                    else:
                        state = "WIN"

            if player and "LEVEL" in state and player.x >= level_width - 120: state = f"BOSS{idx}"
            if player: offset_x = max(0, min(player.x - 500, level_width - 1000))

            for p in platforms: p.draw(screen, offset_x)
            if player: player.draw(screen, offset_x)
            if current_boss: current_boss.draw(screen, offset_x)

            pygame.draw.rect(screen, (50, 50, 50), (30, 20, 200, 20), border_radius=4)
            if player: pygame.draw.rect(screen, (0, 204, 102), (30, 20, int((player.health / player.max_health) * 200), 20), border_radius=4)
            screen.blit(font.render("Luffy HP", True, (50, 50, 50)), (30, 45))
            screen.blit(font.render(f"LEVEL {idx} - " + ("SHOWDOWN" if "BOSS" in state else "EXPLORATION"), True, (100, 50, 0)), (350, 20))

            if "BOSS" in state and current_boss:
                pygame.draw.rect(screen, (50, 50, 50), (30, 80, 200, 15), border_radius=4)
                bar_color = (0, 255, 0) if current_boss.phase == 1 else ((255, 165, 0) if current_boss.phase == 2 else (255, 0, 0))
                pygame.draw.rect(screen, bar_color, (30, 80, int((current_boss.hp / current_boss.max_hp) * 200), 15), border_radius=4)
                screen.blit(font.render("Crocodile HP", True, (150, 0, 0)), (30, 100))

        elif state == "MAIN_MENU":
            screen.blit(font.render("ONE PIECE: CROCODILE'S WRATH", True, (139, 69, 19)), (320, 200))
            screen.blit(font.render("Press ENTER to Begin the Adventure", True, (0, 102, 204)), (310, 280))
        elif state == "GAME_OVER":
            screen.blit(font.render("GAME OVER! Sir Crocodile Defeated You.", True, (204, 0, 0)), (300, 240))
            screen.blit(font.render("Press 'R' to Return to Main Menu", True, (50, 50, 50)), (340, 300))
        elif state == "WIN":
            screen.blit(font.render("CONGRATULATIONS! YOU SAVED ALABASTA!", True, (0, 153, 76)), (280, 230))

        pygame.display.update()
        clock.tick(60)
    pygame.quit()