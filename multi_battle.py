import random
import json
import sqlite3
from config import BOSSES, ABILITIES
from jjk_data import DOMAINS_JJK, FODDER_JJK, BOSSES_JJK
from database import DB_NAME, add_coins
from quests import update_quest_progress


def init_multi_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS multi_battles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE,
        battle_type TEXT,
        host_id INTEGER,
        players TEXT,
        team1 TEXT,
        team2 TEXT,
        boss_name TEXT,
        boss_hp INTEGER,
        boss_max_hp INTEGER,
        current_turn TEXT,
        turn_index INTEGER,
        status TEXT DEFAULT 'active',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()


def create_multi_battle(session_id, battle_type, host_id, players, team1, team2,
                        boss_name=None, boss_hp=0):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM multi_battles WHERE session_id=?", (session_id,))
    c.execute("""INSERT INTO multi_battles
        (session_id, battle_type, host_id, players, team1, team2,
         boss_name, boss_hp, boss_max_hp, current_turn, turn_index, status)
        VALUES (?,?,?,?,?,?,?,?,?,?,0,'active')""",
        (session_id, battle_type, host_id, json.dumps(players),
         json.dumps(team1), json.dumps(team2),
         boss_name, boss_hp, boss_hp, json.dumps(players[0] if players else None)))
    conn.commit()
    conn.close()


def get_multi_battle(session_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT id, session_id, battle_type, host_id, players,
                        team1, team2, boss_name, boss_hp, boss_max_hp,
                        current_turn, turn_index, status
                 FROM multi_battles WHERE session_id=? AND status='active'""",
        (session_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "session_id": row[1],
        "type": row[2],
        "host": row[3],
        "players": json.loads(row[4]),
        "team1": json.loads(row[5]),
        "team2": json.loads(row[6]),
        "boss_name": row[7],
        "boss_hp": row[8],
        "boss_max_hp": row[9],
        "current_turn": json.loads(row[10]) if row[10] else None,
        "turn_index": row[11],
        "status": row[12]
    }


def update_multi_battle(session_id, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""UPDATE multi_battles SET
        team1=?, team2=?, boss_hp=?, current_turn=?, turn_index=?, status=?
        WHERE session_id=?""",
        (json.dumps(data["team1"]), json.dumps(data["team2"]),
         data["boss_hp"], json.dumps(data["current_turn"]),
         data["turn_index"], data["status"], session_id))
    conn.commit()
    conn.close()


def end_multi_battle(session_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM multi_battles WHERE session_id=?", (session_id,))
    conn.commit()
    conn.close()


def roll_damage(atk, defender_def=0, defending=0):
    base = atk * random.uniform(0.85, 1.15)
    crit = random.random() < 0.15
    if crit:
        base *= 2
    if defending:
        base -= defender_def * 2
    else:
        base -= defender_def * 0.5
    return max(1, int(base)), crit


def next_turn(battle):
    players = battle["players"]
    idx = battle["turn_index"] + 1
    while idx < len(players) * 2:
        candidate = players[idx % len(players)]
        for p in battle["team1"] + battle["team2"]:
            if p["uid"] == candidate and p["hp"] > 0:
                battle["current_turn"] = candidate
                battle["turn_index"] = idx
                return
        idx += 1
    battle["current_turn"] = None


def get_player(battle, uid):
    for p in battle["team1"]:
        if p["uid"] == uid:
            return p, "team1"
    for p in battle["team2"]:
        if p["uid"] == uid:
            return p, "team2"
    return None, None


def get_enemies(battle, team):
    if team == "team1":
        return [p for p in battle["team2"] if p["hp"] > 0]
    return [p for p in battle["team1"] if p["hp"] > 0]


def build_battle_view(battle):
    text = f"⚔️ نوع: {battle['type'].upper()}\n\n"

    if battle["boss_name"]:
        text += f"👹 {battle['boss_name']}\n"
        text += f"❤️ HP: {battle['boss_hp']}/{battle['boss_max_hp']}\n\n"

    text += "🟦 Team 1:\n"
    for p in battle["team1"]:
        status = "✅" if p["hp"] > 0 else "💀"
        turn_mark = " 🎯" if p["uid"] == battle["current_turn"] else ""
        text += f"  {status} {p['name']} — HP {p['hp']}/{p['max_hp']}{turn_mark}\n"

    if battle["team2"]:
        text += "\n🟥 Team 2:\n"
        for p in battle["team2"]:
            status = "✅" if p["hp"] > 0 else "💀"
            turn_mark = " 🎯" if p["uid"] == battle["current_turn"] else ""
            text += f"  {status} {p['name']} — HP {p['hp']}/{p['max_hp']}{turn_mark}\n"

    text += f"\n━━━━━━━━━━━━━━━━\n"
    if battle["current_turn"]:
        text += f"🎯 نوبت: {battle['current_turn']}"
    else:
        text += "⏳ در حال پردازش..."
    return text


def player_action(session_id, uid, action):
    battle = get_multi_battle(session_id)
    if not battle:
        return None, "نبرد فعال نیست."

    if battle["current_turn"] != uid:
        return None, "نوبت تو نیست!"

    player, team = get_player(battle, uid)
    if not player or player["hp"] <= 0:
        return None, "تو مرده‌ای!"

    log = ""

    if action == "attack":
        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."
        target = random.choice(enemies)
        dmg, crit = roll_damage(player["atk"], target["def"], 0)

        atk_boost = player.get("atk_boost", 0)
        if atk_boost:
            dmg = int(dmg * (1 + atk_boost / 100))

        target["hp"] = max(0, target["hp"] - dmg)
        crit_str = " 🎯 CRIT!" if crit else ""
        log = f"⚔️ {player['name']} → {target['name']}: {dmg}{crit_str}"
        if target["hp"] <= 0:
            log += f"\n☠️ {target['name']} از نبرد خارج شد!"

    elif action == "defend":
        player["defending"] = 1
        log = f"🛡️ {player['name']} دفاع گرفت."

    elif action == "dodge":
        if random.randint(1, 100) <= player["dodge"]:
            log = f"💨 {player['name']} جاخالی داد!"
            player["dodged_next"] = 1
        else:
            log = f"❌ {player['name']} جاخالی ناموفق!"

    elif action == "domain":
        char_name = player["name"]
        if char_name not in DOMAINS_JJK:
            return None, "❌ این کاراکتر گسترش قلمرو نداره!"

        cd_key = f"domain_cd_{uid}"
        if battle.get(cd_key, 0) > 0:
            return None, f"⏱️ کول‌داون: {battle[cd_key]} راند مونده"

        domain = DOMAINS_JJK[char_name]
        effects = domain["effects"]
        enemies = get_enemies(battle, team)

        if domain["type"] == "single":
            targets = enemies[:1]
        elif domain["type"] == "multi":
            targets = enemies[:2]
        else:
            targets = enemies

        log = f"🌀 {domain['name']}!\n"

        for target in targets:
            if "hp_drain" in effects:
                drain = int(target["max_hp"] * effects["hp_drain"] / 100)
                target["hp"] = max(0, target["hp"] - drain)
                log += f"💀 {target['name']}: -{drain} HP\n"

            if "freeze" in effects:
                target["frozen"] = effects["freeze"]
                log += f"❄️ {target['name']} فریز شد!\n"

            if "dodge_debuff" in effects:
                target["dodge_debuff"] = effects["dodge_debuff"]
                log += f"💨 {target['name']}: جاخالی -{effects['dodge_debuff']}٪\n"

        if "atk_boost" in effects:
            player["atk_boost"] = effects["atk_boost"]
            log += f"⚔️ ATK تو +{effects['atk_boost']}٪\n"

        if "heal" in effects:
            heal = int(player["max_hp"] * effects["heal"] / 100)
            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            log += f"💚 {heal} HP برگشت\n"

        battle[cd_key] = domain["cooldown"]
        battle["domain_active"] = True
        battle["domain_caster"] = uid
        battle["domain_turns"] = domain["duration"]
        battle["domain_name"] = domain["name"]

        next_turn(battle)
        update_multi_battle(session_id, battle)
        return "active", log

    team1_alive = [p for p in battle["team1"] if p["hp"] > 0]
    team2_alive = [p for p in battle["team2"] if p["hp"] > 0]

    if battle["boss_name"]:
        if battle["boss_hp"] <= 0:
            battle["status"] = "won"
            update_multi_battle(session_id, battle)
            return "won", log
        all_players = [p for p in battle["team1"] + battle["team2"] if p["hp"] > 0]
        if all_players:
            target = random.choice(all_players)
            if target.get("dodged_next"):
                target["dodged_next"] = 0
                log += f"\n💨 {target['name']} از ضربه باس جاخالی داد!"
            elif target.get("frozen", 0) > 0:
                target["frozen"] -= 1
                log += f"\n❄️ {target['name']} فریزه!"
            else:
                boss_atk = 100
                if battle["boss_name"] in BOSSES_JJK:
                    boss_atk = BOSSES_JJK[battle["boss_name"]]["atk"]
                elif battle["boss_name"] in BOSSES:
                    boss_atk = BOSSES[battle["boss_name"]]["atk"]
                dmg, crit = roll_damage(boss_atk, target["def"], target.get("defending", 0))
                target["defending"] = 0
                target["hp"] = max(0, target["hp"] - dmg)
                crit_str = " 🎯" if crit else ""
                log += f"\n👹 باس → {target['name']}: {dmg}{crit_str}"
                if target["hp"] <= 0:
                    log += f"\n☠️ {target['name']} از نبرد خارج شد!"
    else:
        if not team1_alive or not team2_alive:
            if team1_alive and not team2_alive:
                battle["status"] = "team1_won"
            elif team2_alive and not team1_alive:
                battle["status"] = "team2_won"
            else:
                battle["status"] = "draw"
            update_multi_battle(session_id, battle)
            return battle["status"], log

    next_turn(battle)
    update_multi_battle(session_id, battle)
    return "active", log


def finish_multi_battle(session_id):
    battle = get_multi_battle(session_id)
    if not battle:
        return None

    status = battle["status"]
    rewards = {}

    if battle["boss_name"] and status == "won":
        if battle["boss_name"] in BOSSES_JJK:
            reward = BOSSES_JJK[battle["boss_name"]]["reward"]
        elif battle["boss_name"] in FODDER_JJK:
            reward = FODDER_JJK[battle["boss_name"]]["reward"]
        else:
            reward = BOSSES.get(battle["boss_name"], {}).get("reward", 100)
        for p in battle["team1"] + battle["team2"]:
            add_coins(p["uid"], reward)
            rewards[p["uid"]] = reward
        end_multi_battle(session_id)
        return {"type": "boss_win", "rewards": rewards, "boss": battle["boss_name"]}

    if status == "team1_won":
        for p in battle["team1"]:
            add_coins(p["uid"], 1500)
            rewards[p["uid"]] = 1500
        end_multi_battle(session_id)
        return {"type": "team1_win", "rewards": rewards}

    if status == "team2_won":
        for p in battle["team2"]:
            add_coins(p["uid"], 1500)
            rewards[p["uid"]] = 1500
        end_multi_battle(session_id)
        return {"type": "team2_win", "rewards": rewards}

    if status == "draw":
        for p in battle["team1"] + battle["team2"]:
            add_coins(p["uid"], 500)
            rewards[p["uid"]] = 500
        end_multi_battle(session_id)
        return {"type": "draw", "rewards": rewards}

    return None
