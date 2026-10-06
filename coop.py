import random
from config import BOSSES
from database import add_coins
from images import IMAGES
from quests import update_quest_progress


def roll_damage(atk, defender_def=0):
    base = atk * random.uniform(0.85, 1.15)
    crit = random.random() < 0.15
    if crit:
        base *= 2
    base -= defender_def * 0.5
    return max(1, int(base)), crit


def coop_fight_boss(user1_id, char1, user2_id, char2, boss_name):
    boss = BOSSES[boss_name]
    boss_hp = boss["hp"]
    boss_max = boss["hp"]
    hp1 = char1[5]
    hp2 = char2[5]
    max1 = hp1
    max2 = hp2
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
    while boss_hp > 0 and (hp1 > 0 or hp2 > 0) and turn < 200:
        turn += 1

        # P1 attack
        if hp1 > 0:
            dmg, crit = roll_damage(char1[6])
            boss_hp -= dmg
            crit_str = " (CRIT!)" if crit else ""
            log.append(f"[{turn}] P1 → Boss: {dmg}{crit_str} | Boss HP: {max(boss_hp,0)}")
            if boss_hp <= 0:
                break

        # P2 attack
        if hp2 > 0:
            dmg, crit = roll_damage(char2[6])
            boss_hp -= dmg
            crit_str = " (CRIT!)" if crit else ""
            log.append(f"[{turn}] P2 → Boss: {dmg}{crit_str} | Boss HP: {max(boss_hp,0)}")
            if boss_hp <= 0:
                break

        # Boss hits
        if hp1 > 0:
            if random.randint(1, 100) <= char1[8]:
                log.append(f"[{turn}] P1 Dodged!")
            else:
                dmg, _ = roll_damage(boss["atk"], char1[7])
                hp1 -= dmg
                log.append(f"[{turn}] Boss → P1: {dmg} | P1 HP: {max(hp1,0)}")

        if hp2 > 0:
            if random.randint(1, 100) <= char2[8]:
                log.append(f"[{turn}] P2 Dodged!")
            else:
                dmg, _ = roll_damage(boss["atk"], char2[7])
                hp2 -= dmg
                log.append(f"[{turn}] Boss → P2: {dmg} | P2 HP: {max(hp2,0)}")

    summary = f"\n\n📊 خلاصه:\n👹 Boss HP: {max(boss_hp,0)}/{boss_max}\n👤 P1 HP: {max(hp1,0)}/{max1}\n👤 P2 HP: {max(hp2,0)}/{max2}"

    if boss_hp <= 0:
        reward = boss["reward"]
        add_coins(user1_id, reward)
        add_coins(user2_id, reward)
        update_quest_progress(user1_id, "win_1_coop")
        update_quest_progress(user2_id, "win_1_coop")
        return True, "\n".join(log[-20:]) + summary, reward, images_to_send
    return False, "\n".join(log[-20:]) + summary, 0, images_to_send
