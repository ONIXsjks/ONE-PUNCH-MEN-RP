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


def team_fight(team1, team2):
    """
    team1, team2 = list of (user_id, char) tuples
    Each team max 4 players.
    نوبتی: هر بازیکن یه بار حمله می‌کنه، به یه دشمن تصادفی.
    """
    t1 = [{"uid": u, "char": c, "hp": c[5], "max_hp": c[5], "alive": True} for u, c in team1]
    t2 = [{"uid": u, "char": c, "hp": c[5], "max_hp": c[5], "alive": True} for u, c in team2]

    log = []
    turn = 0

    while turn < 200:
        turn += 1

        alive1 = [p for p in t1 if p["alive"]]
        alive2 = [p for p in t2 if p["alive"]]

        if not alive1 or not alive2:
            break

        # === Team 1 turn ===
        for p in alive1:
            targets = [x for x in t2 if x["alive"]]
            if not targets:
                break
            target = random.choice(targets)
            dmg, crit = roll_damage(p["char"][6], target["char"][7])
            target["hp"] -= dmg
            crit_str = " (CRIT!)" if crit else ""
            log.append(f"[{turn}] T1-{p['uid']} → T2-{target['uid']}: {dmg}{crit_str}")
            if target["hp"] <= 0:
                target["hp"] = 0
                target["alive"] = False
                log.append(f"       ☠️ T2-{target['uid']} از نبرد خارج شد!")

        # === Team 2 turn ===
        alive2 = [p for p in t2 if p["alive"]]
        alive1 = [p for p in t1 if p["alive"]]
        if not alive2 or not alive1:
            break

        for p in alive2:
            targets = [x for x in t1 if x["alive"]]
            if not targets:
                break
            target = random.choice(targets)
            dmg, crit = roll_damage(p["char"][6], target["char"][7])
            target["hp"] -= dmg
            crit_str = " (CRIT!)" if crit else ""
            log.append(f"[{turn}] T2-{p['uid']} → T1-{target['uid']}: {dmg}{crit_str}")
            if target["hp"] <= 0:
                target["hp"] = 0
                target["alive"] = False
                log.append(f"       ☠️ T1-{target['uid']} از نبرد خارج شد!")

    alive1 = [p for p in t1 if p["alive"]]
    alive2 = [p for p in t2 if p["alive"]]

    # خلاصه آخر
    summary = "\n\n📊 خلاصه نبرد:\n"
    summary += "🟦 Team 1:\n"
    for p in t1:
        status = "✅" if p["alive"] else "💀"
        summary += f"  {status} {p['char'][2]} — HP {p['hp']}/{p['max_hp']}\n"
    summary += "🟥 Team 2:\n"
    for p in t2:
        status = "✅" if p["alive"] else "💀"
        summary += f"  {status} {p['char'][2]} — HP {p['hp']}/{p['max_hp']}\n"

    if alive1 and not alive2:
        for p in t1:
            add_coins(p["uid"], 1500)
            update_quest_progress(p["uid"], "win_1_pvp")
        return 1, "\n".join(log[-15:]) + summary, 1500
    elif alive2 and not alive1:
        for p in t2:
            add_coins(p["uid"], 1500)
            update_quest_progress(p["uid"], "win_1_pvp")
        return 2, "\n".join(log[-15:]) + summary, 1500
    else:
        for p in t1 + t2:
            add_coins(p["uid"], 500)
        return 0, "\n".join(log[-15:]) + summary, 500
