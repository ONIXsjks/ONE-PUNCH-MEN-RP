import random
from config import BOSSES
from database import add_coins
from images import IMAGES
from quests import update_quest_progress

def coop_fight_boss(user1_id, char1, user2_id, char2, boss_name):
    boss = BOSSES[boss_name]
    boss_hp = boss["hp"]
    hp1 = char1[5]
    hp2 = char2[5]
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
    while boss_hp > 0 and (hp1 > 0 or hp2 > 0):
        turn += 1

        if hp1 > 0:
            if random.randint(1, 100) <= char1[8]:
                log.append(f"[{turn}] P1 Dodged!")
            else:
                hp1 -= boss["atk"]
                log.append(f"[{turn}] Boss hit P1! HP1: {max(hp1, 0)}")

        if hp2 > 0:
            if random.randint(1, 100) <= char2[8]:
                log.append(f"[{turn}] P2 Dodged!")
            else:
                hp2 -= boss["atk"]
                log.append(f"[{turn}] Boss hit P2! HP2: {max(hp2, 0)}")

        if boss_name == "Saitama Phase 1":
            images_to_send.append(IMAGES["saitama_punch"])
        elif boss_name in ("Goku Lv1", "Goku Lv2", "Goku Lv3"):
            images_to_send.append(IMAGES["goku_blue"])
        elif boss_name == "Saitama + Goku":
            if turn % 2 == 0:
                images_to_send.append(IMAGES["saitama_punch"])
            else:
                images_to_send.append(IMAGES["goku_laser"])

        if hp1 > 0:
            dmg1 = char1[6] * (3 if random.random() < 0.15 else 1)
            boss_hp -= dmg1
            log.append(f"[{turn}] P1 hit: {dmg1}")

        if hp2 > 0:
            dmg2 = char2[6] * (3 if random.random() < 0.15 else 1)
            boss_hp -= dmg2
            log.append(f"[{turn}] P2 hit: {dmg2}")

    if boss_hp <= 0:
        reward = boss["reward"]
        add_coins(user1_id, reward)
        add_coins(user2_id, reward)
        update_quest_progress(user1_id, "win_1_coop")
        update_quest_progress(user2_id, "win_1_coop")
        return True, "\n".join(log), reward, images_to_send
    return False, "\n".join(log), 0, images_to_send
