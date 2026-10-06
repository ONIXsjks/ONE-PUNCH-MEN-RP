import random
from database import add_coins

def team_fight(team1, team2):
    t1 = [{"uid": u, "char": c, "hp": c[5]} for u, c in team1]
    t2 = [{"uid": u, "char": c, "hp": c[5]} for u, c in team2]
    log = []
    turn = 0

    while turn < 100:
        turn += 1
        alive1 = [p for p in t1 if p["hp"] > 0]
        alive2 = [p for p in t2 if p["hp"] > 0]
        if not alive1 or not alive2:
            break

        for p in alive1:
            target = random.choice(alive2)
            if random.randint(1, 100) > target["char"][8]:
                dmg = p["char"][6] * (3 if random.random() < 0.15 else 1)
                target["hp"] -= dmg
                log.append(f"[{turn}] T1-{p['uid']} -> T2-{target['uid']}: {dmg}")
            else:
                log.append(f"[{turn}] T2-{target['uid']} Dodged!")

        alive2 = [p for p in t2 if p["hp"] > 0]
        alive1 = [p for p in t1 if p["hp"] > 0]
        for p in alive2:
            target = random.choice(alive1) if alive1 else None
            if not target:
                break
            if random.randint(1, 100) > target["char"][8]:
                dmg = p["char"][6] * (3 if random.random() < 0.15 else 1)
                target["hp"] -= dmg
                log.append(f"[{turn}] T2-{p['uid']} -> T1-{target['uid']}: {dmg}")
            else:
                log.append(f"[{turn}] T1-{target['uid']} Dodged!")

    alive1 = [p for p in t1 if p["hp"] > 0]
    alive2 = [p for p in t2 if p["hp"] > 0]

    if alive1 and not alive2:
        for p in t1:
            add_coins(p["uid"], 1500)
        return 1, "\n".join(log[-15:]), 1500
    elif alive2 and not alive1:
        for p in t2:
            add_coins(p["uid"], 1500)
        return 2, "\n".join(log[-15:]), 1500
    else:
        for p in t1 + t2:
            add_coins(p["uid"], 500)
        return 0, "\n".join(log[-15:]), 500
