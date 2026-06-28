import os
from PIL import Image

sheets = {
    "sheet1": "sheet1.jpg.png",
    "sheet2": "sheet2.jpg.png",
    "sheet3": "sheet3.jpg.jpg",
    "sheet4": "sheet4.jpg.jpg"
}

def create_folders():
    states = ["idle", "run", "melee_attack", "dash_attack", "hurt", "sand_fly", "ground_smash"]
    for state in states:
        os.makedirs(f"assets/{state}", exist_ok=True)

def clip_crocodile():
    create_folders()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    p3 = os.path.join(current_dir, sheets["sheet3"])
    if os.path.exists(p3):
        print("🎯 جاري قص حركات الإعصار والطيران من Sheet 3...")
        img3 = Image.open(p3)
        for i in range(4):
            box = (i * 125, 0, (i + 1) * 125, 150)
            img3.crop(box).save(os.path.join(current_dir, f"assets/idle/{i}.png"))
        
        for i in range(4):
            box = (i * 125, 150, (i + 1) * 125, 300)
            img3.crop(box).save(os.path.join(current_dir, f"assets/run/{i}.png"))
            
        for i in range(2):
            box = (i * 150, 500, (i + 1) * 150, 650)
            img3.crop(box).save(os.path.join(current_dir, f"assets/sand_fly/{i}.png"))

    p4 = os.path.join(current_dir, sheets["sheet4"])
    if os.path.exists(p4):
        print("🎯 جاري قص حركات القتال الاحترافية من Sheet 4...")
        img4 = Image.open(p4)
        
        for i in range(4):
            box = (i * 130, 0, (i + 1) * 130, 140)
            img4.crop(box).save(os.path.join(current_dir, f"assets/melee_attack/{i}.png"))
            
        for i in range(4):
            box = (i * 130, 140, (i + 1) * 130, 280)
            img4.crop(box).save(os.path.join(current_dir, f"assets/dash_attack/{i}.png"))

        for i in range(2):
            box = (i * 150, 350, (i + 1) * 150, 490)
            img4.crop(box).save(os.path.join(current_dir, f"assets/ground_smash/{i}.png"))

        box = (0, 280, 130, 410)
        img4.crop(box).save(os.path.join(current_dir, f"assets/hurt/0.png"))
        

if __name__ == "__main__":
    clip_crocodile()