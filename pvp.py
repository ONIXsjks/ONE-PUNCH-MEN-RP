import random
from database import add_coins
from quests import update_quest_progress

def pvp_fight(user1_id, char1, user2_id, char2):
    hp1 = char1[5]
    hp2 = char2[5]
    log = []
    turn = 0

    while hp1 > 0 and hp2 > 0 and turn < 50:
        turn += 1

        if random.randint(1, 100) > char2[8]:
            dmg1 = char1[6] * (3 if random.random() < 0.15 else 1)
            hp2 -= dmg1
            log.append(f"[{turn}] P1 -> P2: {dmg1}")
        else:
            log.append(f"[{turn}] P2 Dodged!")

        if hp2 <= 0:
            break

        if random.randint(1, 100) > char1[8]:
            dmg2 = char2[6] * (3 if random.random() < 0.15 else 1)
            hp1 -= dmg2
            log.append(f"[{turn}] P2 -> P1: {dmg2}")
        else:
            log.append(f"[{turn}] P1 Dodged!")

    if hp1 > 0 and hp2 <= 0:
        add_coins(user1_id, 1000)
        update_quest_progress(user1_id, "win_1_pvp")
        return 1, "\n".join(log), 1000
    elif hp2 > 0 and hp1 <= 0:
        add_coins(user2_id, 1000)
        update_quest_progress(user2_id, "win_1_pvp")
        return 2, "\n".join(log), 1000
    else:
        add_coins(user1_id, 300)
        add_coins(user2_id, 300)
        return 0, "\n".join(log), 300
