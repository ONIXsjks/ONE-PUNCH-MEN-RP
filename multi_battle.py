import random
import json
import sqlite3
from config import (BOSSES, ABILITIES, BUFFS, ITEMS,
                    ABILITY_FA, BUFF_FA, ITEM_FA)
from jjk_data import DOMAINS_JJK, FODDER_JJK, BOSSES_JJK, ABILITIES_JJK
from bleach_data import BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER
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
        extra_data TEXT DEFAULT '{}',
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
         boss_name, boss_hp, boss_max_hp, current_turn, turn_index, status, extra_data)
        VALUES (?,?,?,?,?,?,?,?,?,?,0,'active','{}')""",
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
                        current_turn, turn_index, status, extra_data
                 FROM multi_battles WHERE session_id=? AND status='active'""",
        (session_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None

    try:
        extra = json.loads(row[13]) if row[13] else {}
    except Exception:
        extra = {}

    battle = {
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
        "status": row[12],
    }
    battle.update(extra)
    return battle


def update_multi_battle(session_id, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    main_keys = {"team1", "team2", "boss_hp", "current_turn", "turn_index", "status",
                 "id", "session_id", "type", "host", "players", "boss_name", "boss_max_hp"}

    extra = {k: v for k, v in data.items() if k not in main_keys}

    c.execute("""UPDATE multi_battles SET
        team1=?, team2=?, boss_hp=?, current_turn=?, turn_index=?, status=?, extra_data=?
        WHERE session_id=?""",
        (json.dumps(data["team1"]), json.dumps(data["team2"]),
         data["boss_hp"], json.dumps(data["current_turn"]),
         data["turn_index"], data["status"], json.dumps(extra), session_id))
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
    if not players:
        battle["current_turn"] = None
        return
    idx = battle["turn_index"] + 1
    max_iter = len(players) * 3
    counter = 0
    while counter < max_iter:
        candidate = players[idx % len(players)]
        for p in battle["team1"] + battle["team2"]:
            if str(p["uid"]) == str(candidate) and p["hp"] > 0:
                battle["current_turn"] = candidate
                battle["turn_index"] = idx
                return
        idx += 1
        counter += 1
    battle["current_turn"] = None


def get_player(battle, uid):
    for p in battle["team1"]:
        if str(p["uid"]) == str(uid):
            return p, "team1"
    for p in battle["team2"]:
        if str(p["uid"]) == str(uid):
            return p, "team2"
    return None, None


def get_enemies(battle, team):
    if team == "team1":
        return [p for p in battle["team2"] if p["hp"] > 0]
    return [p for p in battle["team1"] if p["hp"] > 0]


def get_boss_atk(boss_name):
    if boss_name in BLEACH_BOSSES:
        return BLEACH_BOSSES[boss_name]["atk"]
    if boss_name in BLEACH_FODDER:
        return BLEACH_FODDER[boss_name]["atk"]
    if boss_name in BOSSES_JJK:
        return BOSSES_JJK[boss_name]["atk"]
    if boss_name in FODDER_JJK:
        return FODDER_JJK[boss_name]["atk"]
    if boss_name in BOSSES:
        return BOSSES[boss_name]["atk"]
    return 100


def build_battle_view(battle):
    text = f"⚔️ نوع: {battle['type'].upper()}\n\n"

    if battle["boss_name"]:
        text += f"👹 {battle['boss_name']}\n"
        text += f"❤️ HP: {battle['boss_hp']}/{battle['boss_max_hp']}\n\n"

    text += "🟦 Team 1:\n"
    for p in battle["team1"]:
        status = "✅" if p["hp"] > 0 else "💀"
        turn_mark = " 🎯" if str(p["uid"]) == str(battle["current_turn"]) else ""
        text += f"  {status} {p['name']} — HP {p['hp']}/{p['max_hp']}{turn_mark}\n"

    if battle["team2"]:
        text += "\n🟥 Team 2:\n"
        for p in battle["team2"]:
            status = "✅" if p["hp"] > 0 else "💀"
            turn_mark = " 🎯" if str(p["uid"]) == str(battle["current_turn"]) else ""
            text += f"  {status} {p['name']} — HP {p['hp']}/{p['max_hp']}{turn_mark}\n"

    text += f"\n━━━━━━━━━━━━━━━━\n"
    if battle["current_turn"]:
        text += f"🎯 نوبت: {battle['current_turn']}"
    else:
        text += "⏳ در حال پردازش..."
    return text


def player_action(session_id, uid, action, extra=None):
    battle = get_multi_battle(session_id)
    if not battle:
        return None, "نبرد فعال نیست."

    if str(battle["current_turn"]) != str(uid):
        return None, "نوبت تو نیست!"

    player, team = get_player(battle, uid)
    if not player or player["hp"] <= 0:
        return None, "تو مرده‌ای!"

    log = ""

    # ========== حمله ==========
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

    # ========== دفاع ==========
    elif action == "defend":
        player["defending"] = 1
        log = f"🛡️ {player['name']} دفاع گرفت."

    # ========== جاخالی ==========
    elif action == "dodge":
        if random.randint(1, 100) <= player["dodge"]:
            log = f"💨 {player['name']} جاخالی داد!"
            player["dodged_next"] = 1
        else:
            log = f"❌ {player['name']} جاخالی ناموفق!"

    # ========== Domain ==========
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

        next_turn(battle)
        update_multi_battle(session_id, battle)
        return "active", log

    # ========== Bankai (Bleach) ==========
    elif action == "bankai":
        char_name = player["name"]
        if char_name not in BLEACH_BANKAI:
            return None, "❌ این کاراکتر Bankai نداره!"

        if battle.get(f"bankai_used_{uid}", 0) == 1:
            return None, "❌ Bankai فقط یه بار در نبرد!"

        bankai = BLEACH_BANKAI[char_name]
        battle[f"bankai_used_{uid}"] = 1

        log = f"⚔️ Bankai: {bankai['name']}!\n"

        if "atk_boost" in bankai:
            player["atk_boost"] = bankai["atk_boost"]
            log += f"⚔️ ATK +{bankai['atk_boost']}٪\n"

        if "dodge_boost" in bankai:
            player["dodge"] += bankai["dodge_boost"]
            log += f"💨 دوج +{bankai['dodge_boost']}٪\n"

        if "def_boost" in bankai:
            player["def"] += bankai["def_boost"]
            log += f"🛡️ دفاع +{bankai['def_boost']}\n"

        if "heal" in bankai:
            heal = int(player["max_hp"] * bankai["heal"] / 100)
            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            log += f"💚 {heal} HP برگشت\n"

        if "self_dmg" in bankai:
            dmg = int(player["max_hp"] * bankai["self_dmg"] / 100)
            player["hp"] = max(0, player["hp"] - dmg)
            log += f"🩸 خودت {dmg} HP از دست دادی\n"

        enemies = get_enemies(battle, team)
        for target in enemies:
            if "hp_drain" in bankai:
                drain = int(target["max_hp"] * bankai["hp_drain"] / 100)
                target["hp"] = max(0, target["hp"] - drain)
                log += f"💀 {target['name']}: -{drain} HP\n"

            if "freeze" in bankai:
                target["frozen"] = bankai["freeze"]
                log += f"❄️ {target['name']} فریز شد!\n"

            if "dodge_debuff" in bankai:
                target["dodge_debuff"] = bankai["dodge_debuff"]

            if "enemy_atk_debuff" in bankai:
                target["atk_debuff"] = bankai["enemy_atk_debuff"]

        next_turn(battle)
        update_multi_battle(session_id, battle)
        return "active", log

    # ========== Ability ==========
    elif action == "ability" and extra:
        ability_name = extra

        used_key = f"used_{uid}_{ability_name}"
        if battle.get(used_key, 0) == 1:
            return None, f"❌ {ability_name} قبلاً استفاده شده!"

        char_name = player["name"]
        jjk_abs = ABILITIES_JJK.get(char_name, {})
        found_ab = None

        for key in ["ability_1", "ability_2"]:
            if key in jjk_abs and jjk_abs[key]["name"] == ability_name:
                found_ab = jjk_abs[key]
                break

        if not found_ab and ability_name in ABILITIES:
            found_ab = {
                "name": ability_name,
                "effect": ABILITIES[ability_name]["effect"],
                "type": "shop",
            }

        if not found_ab:
            return None, "❌ Ability پیدا نشد."

        enemies = get_enemies(battle, team)
        target = random.choice(enemies) if enemies else None

        log = f"🔥 {ability_name}!\n"
        ab_type = found_ab.get("type", "damage")
        eff = found_ab.get("effect", "")

        if ab_type in ("damage", "shop"):
            mult = 2
            if "x6" in eff:
                mult = 6
            elif "x5" in eff:
                mult = 5
            elif "x4" in eff:
                mult = 4
            elif "x3.5" in eff:
                mult = 3.5
            elif "x3" in eff:
                mult = 3
            elif "x2.5" in eff:
                mult = 2.5
            dmg = int(player["atk"] * mult)
            if target:
                target["hp"] = max(0, target["hp"] - dmg)
                log += f"⚔️ {dmg} آسیب\n"
                if target["hp"] <= 0:
                    log += f"☠️ {target['name']} از نبرد خارج شد!"
            if "self" in eff and "20% HP" in eff:
                dmg_self = int(player["max_hp"] * 0.2)
                player["hp"] = max(0, player["hp"] - dmg_self)
                log += f"\n🩸 خودت {dmg_self} HP از دست دادی"

        elif ab_type == "dodge":
            player["dodged_next"] = 1
            log += "💨 جاخالی فعال\n"

        elif ab_type == "multi":
            hits = 3 if "3" in eff else 5 if "5" in eff else 2
            total = sum(player["atk"] for _ in range(hits))
            if target:
                target["hp"] = max(0, target["hp"] - total)
                log += f"⚔️ {hits} ضربه: {total} آسیب\n"
                if target["hp"] <= 0:
                    log += f"☠️ {target['name']} خارج شد!"

        elif ab_type == "gamble":
            if random.randint(1, 100) <= 50:
                dmg = player["atk"] * 4
                log += f"🎰 برنده! {dmg} آسیب"
            else:
                dmg = player["atk"] * 1
                log += f"🎰 باختی! {dmg} آسیب"
            if target:
                target["hp"] = max(0, target["hp"] - dmg)

        elif ab_type == "heal":
            heal = int(player["max_hp"] * 0.3)
            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            log += f"💚 {heal} HP برگشت\n"

        elif ab_type == "freeze":
            if target:
                target["frozen"] = 1
                log += f"❄️ {target['name']} فریز شد!\n"

        elif ab_type == "buff":
            player["atk_boost"] = 50
            log += "⚔️ ATK +۵۰٪\n"

        battle[used_key] = 1

        next_turn(battle)
        update_multi_battle(session_id, battle)
        return "active", log

    # ========== باف ==========
    elif action == "buff" and extra:
        buff_name = extra

        if buff_name not in BUFFS:
            return None, "❌ باف پیدا نشد."

        used_key = f"buff_used_{uid}_{buff_name}"
        if battle.get(used_key, 0) == 1:
            return None, f"❌ {buff_name} قبلاً استفاده شده!"

        eff = BUFFS[buff_name]["effect"]
        log = f"🔥 {buff_name}!\n"

        if "Max HP" in eff:
            player["max_hp"] += 500
            player["hp"] += 500
            log += "❤️ Max HP +۵۰۰\n"
        elif "ATK" in eff and "150" in eff:
            player["atk"] += 150
            log += "⚔️ ATK +۱۵۰\n"
        elif "DEF" in eff:
            player["def"] += 80
            log += "🛡️ DEF +۸۰\n"
        elif "DODGE" in eff:
            player["dodge"] += 10
            log += "💨 دوج +۱۰٪\n"
        elif "Crit" in eff:
            log += "🎯 شانس کریتیکال +۱۵٪\n"
        elif "dmg = HP" in eff:
            player["lifesteal"] = 10
            log += "🩸 Lifesteal ۱۰٪\n"
        elif "all +20" in eff:
            player["max_hp"] += 200
            player["hp"] += 200
            player["atk"] += 50
            player["def"] += 30
            log += "🔥 همه +۲۰٪\n"
        elif "all +50" in eff:
            player["max_hp"] += 500
            player["hp"] += 500
            player["atk"] += 150
            player["def"] += 80
            log += "🔥 همه +۵۰٪\n"

        battle[used_key] = 1

        next_turn(battle)
        update_multi_battle(session_id, battle)
        return "active", log

    # ========== بررسی پایان ==========
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
                boss_atk = get_boss_atk(battle["boss_name"])
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
        boss_name = battle["boss_name"]
        if boss_name in BLEACH_BOSSES:
            reward = BLEACH_BOSSES[boss_name]["reward"]
        elif boss_name in BLEACH_FODDER:
            reward = BLEACH_FODDER[boss_name]["reward"]
        elif boss_name in BOSSES_JJK:
            reward = BOSSES_JJK[boss_name]["reward"]
        elif boss_name in FODDER_JJK:
            reward = FODDER_JJK[boss_name]["reward"]
        else:
            reward = BOSSES.get(boss_name, {}).get("reward", 5000)
        for p in battle["team1"] + battle["team2"]:
            add_coins(p["uid"], reward)
            rewards[p["uid"]] = reward
        end_multi_battle(session_id)
        return {"type": "boss_win", "rewards": rewards, "boss": boss_name}

    if status == "team1_won":
        amount = 300 if battle["type"] == "pvp" else 1500
        for p in battle["team1"]:
            add_coins(p["uid"], amount)
            rewards[p["uid"]] = amount
        end_multi_battle(session_id)
        return {"type": "team1_win", "rewards": rewards}
      if status == "team2_won":
    amount = 300 if battle["type"] == "pvp" else 1500
    for p in battle["team2"]:
        add_coins(p["uid"], amount)
        rewards[p["uid"]] = amount
    end_multi_battle(session_id)
    return {"type": "team2_win", "rewards": rewards}

if status == "draw":
    for p in battle["team1"] + battle["team2"]:
        add_coins(p["uid"], 500)
        rewards[p["uid"]] = 500
    end_multi_battle(session_id)
    return {"type": "draw", "rewards": rewards}

return None
