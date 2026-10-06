import random
from config import BOSSES
from database import add_coins
from images import IMAGES
from quests import update_quest_progress

def attack(char):
    atk = char[6]
    crit = random.random() < 0.15
    dmg = atk * (3 if crit else 1)
    return dmg, crit

def fight_boss(user_id, char, boss_name):
    boss = BOSSES[boss_name]
    boss_hp = boss["hp"]
    char_hp = char[5]
    log = []
    images_to_send = []

    if boss_name == "Saitama Phase 1":
        images_to_send.append(IMAGES["saitama_normal"])
    elif boss_name.startswith("Goku"):
        images_to_send.append(IMAGES["goku_normal"])
    elif boss_name == "Saitama + Goku":
        images_to_send.append(IMAGES["saitama_normal"])
        images_to_send.append(IMAGES["goku_normal"])

    turn = 0
    while boss_hp > 0 and char_hp > 0:
        turn += 1

        if random.randint(1, 100) <= char[8]:
            log.append(f"[{turn}] Dodged!")
        else:
            char_hp -= boss["atk"]
            log.append(f"[{turn}] Boss hit! Your HP: {max(char_hp, 0)}")

            if boss_name == "Saitama Phase 1":
                images_to_send.append(IMAGES["saitama_punch"])
            elif boss_name in ("Goku Lv1", "Goku Lv2", "Goku Lv3"):
                images_to_send.append(IMAGES["goku_blue"])
            elif boss_name == "Saitama + Goku":
                if turn % 2 == 0:
                    images_to_send.append(IMAGES["saitama_punch"])
                else:
                    images_to_send.append(IMAGES["goku_laser"])

        if char_hp <= 0:
            break

        dmg, crit = attack(char)
        boss_hp -= dmg
        log.append(f"[{turn}] You hit: {dmg}{' (CRIT!)' if crit else ''}")

    if char_hp > 0:
        add_coins(user_id, boss["reward"])
        update_quest_progress(user_id, "win_3_bosses")
        update_quest_progress(user_id, "win_5_bosses")
        if boss_name == "Saitama Phase 1":
            update_quest_progress(user_id, "kill_saitama")
        if boss_name.startswith("Goku"):
            update_quest_progress(user_id, "kill_goku")
        return True, "\n".join(log), boss["reward"], images_to_send
    return False, "\n".join(log), 0, images_to_send
