import random
from database import add_coins
from quests import update_quest_progress


def roll_damage(atk, defender_def=0):
    base = atk * random.uniform(0.85, 1.15)
    crit = random.random() < 0.15
    if crit:
        base *= 2
    base -= defender_def * 0.5
    return max(1, int(base)), crit


def pvp_fight(user1_id, char1, user2_id, char2):
    hp1 = char1[5]
    hp2 = char2[5]
    max1 = hp1
    max2 = hp2
    log = []
    turn = 0

    while hp1 > 0 and hp2 > 0 and turn < 100:
        turn += 1

        # P1
        dmg1, crit1 = roll_damage(char1[6], char2[7])
        hp2 -= dmg1
        crit_str = " (CRIT!)" if crit1 else ""
        log.append(f"[{turn}] P1 → P2: {dmg1}{crit_str}")
        if hp2 <= 0:
            hp2 = 0
            break

        # P2
        dmg2, crit2 = roll_damage(char2[6], char1[7])
        hp1 -= dmg2
        crit_str = " (CRIT!)" if crit2 else ""
        log.append(f"[{turn}] P2 → P1: {dmg2}{crit_str}")
        if hp1 <= 0:
            hp1 = 0
            break

    summary = f"\n\n📊 نتیجه:\n"
    summary += f"👤 P1: HP {hp1}/{max1}\n"
    summary += f"👤 P2: HP {hp2}/{max2}"

    if hp1 > 0 and hp2 <= 0:
        add_coins(user1_id, 1000)
        update_quest_progress(user1_id, "win_1_pvp")
        return 1, "\n".join(log) + summary, 1000
    elif hp2 > 0 and hp1 <= 0:
        add_coins(user2_id, 1000)
        update_quest_progress(user2_id, "win_1_pvp")
        return 2, "\n".join(log) + summary, 1000
    else:
        add_coins(user1_id, 300)
        add_coins(user2_id, 300)
        return 0, "\n".join(log) + summary, 300
