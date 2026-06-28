import pygame
import os

pygame.init()



# --- 2. نظام إدارة المسارات المحدث وفقاً للمجلد الحالي ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

assets_dir = os.path.join(BASE_DIR, "NAssets")

def get_safe_path(filename_png, filename_jpg):
    path_png = os.path.join(assets_dir, filename_png)
    path_jpg = os.path.join(assets_dir, filename_jpg)
    if os.path.exists(path_png):
        return path_png
    elif os.path.exists(path_jpg):
        return path_jpg
    return path_png

def load_background_safely(possible_names, default_color):
    for name in possible_names:
        full_path = os.path.join(BASE_DIR, name)
        if os.path.exists(full_path):
            try:
                img = pygame.image.load(full_path).convert()
                print(f"✅ تم تحميل الصورة بنجاح: {name}")
                return pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            except pygame.error:
                continue
    
    print(f"⚠️ Warning: لم يتم العثور على أي من الملفات {possible_names} - تم إنشاء خلفية بديلة.")
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill(default_color)
    return surf

menu_bg = load_background_safely(["one_piece_logo.jpeg", "one_piece_logo.jpg", "one_piece_logo.png", "one_piece_logo"], (20, 20, 40))
tbc_bg = load_background_safely(["to_be_continued.jpeg", "to_be_continued.jpg", "to_be_continued.png", "to_be_continued"], (10, 10, 10))

PATH_BASE = get_safe_path("luffy_base_sheet.png", "luffy_base_sheet.jpg")
PATH_SKILLS = get_safe_path("luffy_skills_sheet.png", "luffy_skills_sheet.jpg")
PATH_BACKGROUND_L1 = os.path.join(assets_dir, "level1.tmx") 
PATH_GEAR3 = get_safe_path("luffy_gear3_sheet.png", "luffy_gear3_sheet.jpg")
PATH_LVL2 = get_safe_path("luffy_lvl2_gatling.jpg.png", "luffy_lvl2_gatling.jpg")
PATH_FLAME = get_safe_path("luffy_flame_sheet.png", "luffy_flame_sheet.jpg") 
PATH_WOOD = get_safe_path("luffy_wood_sheet.png", "luffy_wood_sheet.jpg")  
PATH_GEAR5 = get_safe_path("luffy_gear5_sheet.png", "luffy_gear5_sheet.jpg") 
PATH_NEW_COMBO = get_safe_path("luffy_combo_attack_sheet.png", "luffy_combo_attack_sheet.jpg")

try:
    sheet_base = pygame.image.load(PATH_BASE).convert_alpha()
    sheet_skills = pygame.image.load(PATH_SKILLS).convert_alpha()
    sheet_luffy_lvl2 = pygame.image.load(PATH_LVL2).convert_alpha()
    sheet_gear3 = pygame.image.load(PATH_GEAR3).convert_alpha()
    sheet_flame = pygame.image.load(PATH_FLAME).convert_alpha()
    sheet_wood = pygame.image.load(PATH_WOOD).convert_alpha()  
    sheet_gear5 = pygame.image.load(PATH_GEAR5).convert_alpha() 
    sheet_new_combo = pygame.image.load(PATH_NEW_COMBO).convert_alpha() 
    
    if os.path.exists(PATH_BACKGROUND_L1):
        background_l1 = pygame.image.load(PATH_BACKGROUND_L1).convert()
        background_l1 = pygame.transform.scale(background_l1, (WIDTH, HEIGHT))
    else:
        background_l1 = pygame.Surface((WIDTH, HEIGHT))
        background_l1.fill((50, 50, 100))
        
except pygame.error as e:
    print(f"❌ Error loading character sheets: {e}")
    pygame.quit()
    exit()

SIZE_L1 = (130, 150)
SIZE_L2 = (160, 210)

def get_frame(sheet, x, y, w, h, size):
    sub = sheet.subsurface((int(x), int(y), int(w), int(h))).copy()
    sub.set_colorkey((0, 0, 0))  
    return pygame.transform.scale(sub, size)

# --- 3. بناء مصفوفات حركات ليفل 1 ---
idle_frames_l1 = [
    get_frame(sheet_base, 10, 85, 105, 185, SIZE_L1),
    get_frame(sheet_base, 140, 85, 105, 185, SIZE_L1),
    get_frame(sheet_base, 270, 85, 105, 185, SIZE_L1),
    get_frame(sheet_base, 400, 85, 105, 185, SIZE_L1),
    get_frame(sheet_base, 530, 85, 105, 185, SIZE_L1)
]
run_frames_l1 = [
    get_frame(sheet_base, 660, 85, 120, 185, SIZE_L1),
    get_frame(sheet_base, 790, 85, 125, 185, SIZE_L1),
    get_frame(sheet_base, 10, 310, 125, 185, SIZE_L1),
    get_frame(sheet_base, 170, 310, 125, 185, SIZE_L1)
]
jump_frames_l1 = [
    get_frame(sheet_base, 20, 535, 110, 135, SIZE_L1),
    get_frame(sheet_base, 150, 535, 110, 135, SIZE_L1)
]
gatling_frames_l1 = [
    get_frame(sheet_skills, 285, 275, 140, 180, SIZE_L1),
    get_frame(sheet_skills, 425, 275, 140, 180, SIZE_L1)
]

# --- 4. بناء مصفوفات حركات ليفل 2 ---
idle_frames_l2 = [
    get_frame(sheet_base, 10, 65, 105, 205, SIZE_L2),
    get_frame(sheet_base, 140, 65, 105, 205, SIZE_L2),
    get_frame(sheet_base, 270, 65, 105, 205, SIZE_L2),
    get_frame(sheet_base, 400, 65, 105, 205, SIZE_L2),
    get_frame(sheet_base, 530, 65, 105, 205, SIZE_L2)
]
run_frames_l2 = [
    get_frame(sheet_base, 655, 65, 110, 205, SIZE_L2),   
    get_frame(sheet_base, 785, 65, 115, 205, SIZE_L2),   
    get_frame(sheet_base, 5, 275, 120, 185, SIZE_L2),    
    get_frame(sheet_base, 145, 275, 120, 185, SIZE_L2)   
]
jump_frames_l2 = [
    get_frame(sheet_base, 20, 510, 110, 160, SIZE_L2),
    get_frame(sheet_base, 150, 510, 110, 160, SIZE_L2)
]
integrated_combo_frames_l2 = [
    get_frame(sheet_new_combo, 750, 625, 245, 160, (330, 210)),
    get_frame(sheet_new_combo, 752, 830, 243, 160, (330, 210)),
    get_frame(sheet_new_combo, 480, 575, 230, 225, (220, 210)),
    get_frame(sheet_new_combo, 175, 770, 220, 210, (220, 210))
]
gatling_lvl2_frames = [
    get_frame(sheet_luffy_lvl2, 10, 260, 115, 170, SIZE_L2),   
    get_frame(sheet_luffy_lvl2, 135, 260, 115, 170, SIZE_L2),  
    get_frame(sheet_luffy_lvl2, 260, 260, 115, 170, SIZE_L2),  
    get_frame(sheet_luffy_lvl2, 385, 260, 195, 170, (250, 210)),  
    get_frame(sheet_luffy_lvl2, 590, 260, 230, 170, (280, 210))   
]
gear3_idle_frames = [
    get_frame(sheet_gear3, 35, 65, 110, 175, SIZE_L2),  
    get_frame(sheet_gear3, 245, 65, 110, 175, SIZE_L2), 
    get_frame(sheet_gear3, 445, 65, 120, 175, SIZE_L2), 
    get_frame(sheet_gear3, 640, 65, 120, 175, SIZE_L2)  
]
gear3_run_frames = [
    get_frame(sheet_gear3, 35, 680, 125, 170, (180, 210)),  
    get_frame(sheet_gear3, 230, 680, 125, 170, (180, 210)), 
    get_frame(sheet_gear3, 410, 680, 125, 170, (180, 210)), 
    get_frame(sheet_gear3, 650, 680, 125, 170, (180, 210))  
]
red_hawk_frames = [
    get_frame(sheet_flame, 5, 5, 150, 140, SIZE_L2),       
    get_frame(sheet_flame, 180, 5, 140, 150, SIZE_L2),     
    get_frame(sheet_flame, 320, 5, 140, 150, SIZE_L2),     
    get_frame(sheet_flame, 5, 275, 140, 210, SIZE_L2)     
]
red_hawk_wood_frames = [
    get_frame(sheet_wood, 15, 870, 150, 180, SIZE_L2),    
    get_frame(sheet_wood, 185, 870, 150, 180, SIZE_L2),   
    get_frame(sheet_wood, 355, 870, 150, 180, SIZE_L2),   
    get_frame(sheet_wood, 525, 870, 160, 180, (180, 210))    
]
gear5_idle_frames = [
    get_frame(sheet_gear5, 7, 10, 130, 135, SIZE_L2),
    get_frame(sheet_gear5, 145, 10, 130, 135, SIZE_L2),
    get_frame(sheet_gear5, 285, 10, 130, 135, SIZE_L2),
    get_frame(sheet_gear5, 425, 10, 130, 135, SIZE_L2)
]
gear5_run_frames = [
    get_frame(sheet_gear5, 5, 345, 145, 135, SIZE_L2),
    get_frame(sheet_gear5, 155, 345, 145, 135, SIZE_L2),
    get_frame(sheet_gear5, 315, 345, 145, 135, SIZE_L2)
]

# --- 5. نظام إدارة الحالات ---
GAME_STATE = "START_MENU" 
CURRENT_LEVEL = 1  

player_x = 100
player_y = 280
current_state = "idle"
frame_index = 0
facing_left = False
velocity_y = 0
gravity = 0.6
jump_power = -14
on_ground = True
speed = 6

font_title = pygame.font.SysFont("Arial", 45, bold=True)
font_sub = pygame.font.SysFont("Arial", 20, bold=True)
font_play = pygame.font.SysFont("Arial", 32, bold=True) # خط أوضح وأكبر لزر PLAY الشفاف

def reset_player(level):
    global player_x, player_y, current_state, frame_index, velocity_y, on_ground, CURRENT_LEVEL
    player_x = 100
    current_state = "idle"
    frame_index = 0
    velocity_y = 0
    on_ground = True
    CURRENT_LEVEL = level
    if level == 1:
        player_y = 280
    else:
        player_y = 310

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if GAME_STATE == "START_MENU":
                # تحديث إحداثيات الضغط لتناسب الموقع الجديد y=260
                if 350 <= mx <= 450 and 260 <= my <= 300:
                    reset_player(1)
                    GAME_STATE = "LEVEL_1"
            elif GAME_STATE == "GAME_OVER":
                if 300 <= mx <= 500 and 440 <= my <= 500:
                    reset_player(CURRENT_LEVEL)
                    GAME_STATE = "LEVEL_1" if CURRENT_LEVEL == 1 else "LEVEL_2"

    keys = pygame.key.get_pressed()

    # ====== الشاشة الرئيسية ======
    if GAME_STATE == "START_MENU":
        screen.blit(menu_bg, (0, 0)) 
        
        # تم تغيير اللون إلى الأسود (0, 0, 0) وإنزال الكلمة لـ y=260
        play_txt = font_play.render("PLAY", True, (0, 0, 0))
        screen.blit(play_txt, (WIDTH//2 - play_txt.get_width()//2, 260))
        
        # صندوق الإرشادات الشفاف تم إنزاله أيضاً ليتناسب مع موقع الزر الجديد
        guide_box = pygame.Surface((560, 200), pygame.SRCALPHA)
        guide_box.fill((0, 0, 0, 180)) 
        screen.blit(guide_box, (120, 310)) 
        
        t1 = font_sub.render("How to Play / Instructions :", True, (255, 140, 0))
        t2 = font_sub.render("- Use Keyboard Arrows (Right / Left) to move.", True, (255, 255, 255))
        t3 = font_sub.render("- Press Arrow UP or SPACE to Jump.", True, (255, 255, 255))
        t4 = font_sub.render("- Press [ Z ] to use level skills.", True, (255, 255, 255))
        
        screen.blit(t1, (150, 330))
        screen.blit(t2, (150, 375))
        screen.blit(t3, (150, 415))
        screen.blit(t4, (150, 455))

    # ====== ليفل 1 ======
    elif GAME_STATE == "LEVEL_1":
        screen.blit(background_l1, (0, 0))
        new_state = "idle"

        if keys[pygame.K_RIGHT]:
            player_x += speed
            new_state = "run"
            facing_left = False
        elif keys[pygame.K_LEFT]:
            player_x -= speed
            new_state = "run"
            facing_left = True

        if player_x > WIDTH - SIZE_L1[0] - 10:
            GAME_STATE = "TO_BE_CONTINUED"
            continue

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground:
            velocity_y = jump_power
            on_ground = False

        if keys[pygame.K_z]: new_state = "gatling"

        velocity_y += gravity
        player_y += velocity_y
        if player_y >= 280:
            player_y = 280
            velocity_y = 0
            on_ground = True
        else:
            if new_state not in ["gatling"]: new_state = "jump"

        if new_state != current_state:
            current_state = new_state
            frame_index = 0

        active_list = idle_frames_l1
        if current_state == "run": active_list = run_frames_l1
        elif current_state == "jump": active_list = jump_frames_l1
        elif current_state == "gatling": active_list = gatling_frames_l1   

        frame_index = (frame_index + 0.15) % len(active_list)
        current_image = active_list[int(frame_index)]
        if facing_left: current_image = pygame.transform.flip(current_image, True, False)
        
        screen.blit(current_image, (player_x, player_y))

    # ====== شاشة الانتقال ======
    elif GAME_STATE == "TO_BE_CONTINUED":
        screen.blit(tbc_bg, (0,0)) 
        
        next_txt = font_sub.render("Press [ENTER] to Start Level 2", True, (255, 215, 0))
        pygame.draw.rect(screen, (0,0,0), (WIDTH//2 - 180, HEIGHT - 75, 360, 36))
        screen.blit(next_txt, (WIDTH//2 - next_txt.get_width()//2, HEIGHT - 68))
        
        if keys[pygame.K_RETURN]:
            reset_player(2)
            GAME_STATE = "LEVEL_2"

    # ====== ليفل 2 ======
    elif GAME_STATE == "LEVEL_2":
        screen.fill((135, 206, 235))  
        pygame.draw.rect(screen, (34, 139, 34), (0, 520, WIDTH, 80)) 

        new_state = "idle"
        is_attacking = current_state in ["combo_attack", "gatling_lvl2", "red_hawk", "red_hawk_wood"]

        if not is_attacking:
            if keys[pygame.K_RIGHT]:
                player_x += speed
                if keys[pygame.K_g]: new_state = "gear5_run"      
                elif keys[pygame.K_r]: new_state = "gear3_run"
                else: new_state = "run"
                facing_left = False
            elif keys[pygame.K_LEFT]:
                player_x -= speed
                if keys[pygame.K_g]: new_state = "gear5_run"      
                elif keys[pygame.K_r]: new_state = "gear3_run"
                else: new_state = "run"
                facing_left = True

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground and not is_attacking:
            velocity_y = jump_power
            on_ground = False

        if is_attacking:
            new_state = current_state  
        else:
            if keys[pygame.K_z]: new_state = "combo_attack" 
            elif keys[pygame.K_b]: new_state = "gatling_lvl2"
            elif keys[pygame.K_r]: new_state = "gear3_idle"
            elif keys[pygame.K_g]: new_state = "gear5_idle" 
            elif keys[pygame.K_f]: new_state = "red_hawk"       
            elif keys[pygame.K_h]: new_state = "red_hawk_wood"  

        velocity_y += gravity
        player_y += velocity_y
        if player_y >= 310:
            player_y = 310
            velocity_y = 0
            on_ground = True
        else:
            if new_state not in ["combo_attack", "gatling_lvl2", "gear3_idle", "gear3_run", "gear5_idle", "gear5_run", "red_hawk", "red_hawk_wood"]:
                new_state = "jump"

        if new_state != current_state:
            current_state = new_state
            frame_index = 0

        active_list = idle_frames_l2
        if current_state == "run": active_list = run_frames_l2
        elif current_state == "jump": active_list = jump_frames_l2
        elif current_state == "combo_attack": active_list = integrated_combo_frames_l2 
        elif current_state == "gatling_lvl2": active_list = gatling_lvl2_frames  
        elif current_state == "gear3_idle": active_list = gear3_idle_frames  
        elif current_state == "gear3_run": active_list = gear3_run_frames  
        elif current_state == "gear5_idle": active_list = gear5_idle_frames  
        elif current_state == "gear5_run": active_list = gear5_run_frames    
        elif current_state == "red_hawk": active_list = red_hawk_frames  
        elif current_state == "red_hawk_wood": active_list = red_hawk_wood_frames  

        frame_index += 0.15
        
        if int(frame_index) >= len(active_list):
            if current_state in ["combo_attack", "gatling_lvl2"]:
                current_state = "idle"
                new_state = "idle"
                active_list = idle_frames_l2
            frame_index = 0

        current_image = active_list[int(frame_index)]

        if facing_left:
            current_image = pygame.transform.flip(current_image, True, False)
            render_x = player_x - (current_image.get_width() - SIZE_L2[0])
        else:
            render_x = player_x

        screen.blit(current_image, (render_x, player_y))
        
        if player_x > WIDTH - SIZE_L2[0] - 10: 
            GAME_STATE = "WIN"

    # ====== شاشة الخسارة ======
    elif GAME_STATE == "GAME_OVER":
        screen.blit(tbc_bg, (0, 0)) 
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((100, 0, 0, 80)) 
        screen.blit(overlay, (0, 0))
        
        go_txt = font_title.render("GAME OVER", True, (255, 0, 0))
        screen.blit(go_txt, (WIDTH//2 - go_txt.get_width()//2, 360))
        
        pygame.draw.rect(screen, (180, 0, 0), (300, 440, 200, 60), border_radius=10)
        retry_txt = font_sub.render("TRY AGAIN", True, (255, 255, 255))
        screen.blit(retry_txt, (WIDTH//2 - retry_txt.get_width()//2, 458))

    # ====== شاشة الفوز ======
    elif GAME_STATE == "WIN":
        screen.blit(tbc_bg, (0, 0)) 
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 100, 0, 80)) 
        screen.blit(overlay, (0, 0))
        
        w_txt = font_title.render("VICTORY! YOU WIN", True, (0, 255, 0))
        screen.blit(w_txt, (WIDTH//2 - w_txt.get_width()//2, 360))

    pygame.display.update()
    clock.tick(60)

pygame.quit()