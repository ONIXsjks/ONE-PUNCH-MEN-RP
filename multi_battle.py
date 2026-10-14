import random
import json
import sqlite3
from config import (BOSSES, ABILITIES, BUFFS, ITEMS,
                    ABILITY_FA, BUFF_FA, ITEM_FA)
from jjk_data import DOMAINS_JJK, FODDER_JJK, BOSSES_JJK, ABILITIES_JJK
from bleach_data import BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER
from database import DB_NAME, add_coins, get_abilities
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
        "id": row[0], "session_id": row[1], "type": row[2], "host": row[3],
        "players": json.loads(row[4]), "team1": json.loads(row[5]),
        "team2": json.loads(row[6]), "boss_name": row[7],
        "boss_hp": row[8], "boss_max_hp": row[9],
        "current_turn": json.loads(row[10]) if row[10] else None,
        "turn_index": row[11], "status": row[12]
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
    return max(1, int(base)), crit


def disp(p):
    return p.get("display") or p.get("name", "؟")


def apply_defense_check(base_dmg, hp, defense_type):
    roll = random.randint(1, 100)
    if roll <= 33:
        return hp, f"✅ {defense_type} کامل! ۰ آسیب"
    elif roll <= 66:
        partial = max(1, int(base_dmg * 0.5))
        hp = max(0, hp - partial)
        return hp, f"⚠️ {defense_type} جزئی! {partial} آسیب (۵۰٪)"
    else:
        hp = max(0, hp - base_dmg)
        return hp, f"❌ {defense_type} ناموفق! {base_dmg} آسیب کامل"


def next_turn(battle):
    for key in list(battle.keys()):
        if key.startswith("domain_cd_") or key.startswith("bankai_cd_"):
            if battle[key] > 0:
                battle[key] -= 1
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
        mark = " 🎯" if str(p["uid"]) == str(battle["current_turn"]) else ""
        text += f"  {status} {disp(p)} — HP {p['hp']}/{p['max_hp']}{mark}\n"

    if battle["team2"]:
        text += "\n🟥 Team 2:\n"
        for p in battle["team2"]:
            status = "✅" if p["hp"] > 0 else "💀"
            mark = " 🎯" if str(p["uid"]) == str(battle["current_turn"]) else ""
            text += f"  {status} {disp(p)} — HP {p['hp']}/{p['max_hp']}{mark}\n"

    text += f"\n━━━━━━━━━━━━━━━━\n"
    if battle["current_turn"]:
        p, _ = get_player(battle, battle["current_turn"])
        if p:
            text += f"🎯 نوبت: {disp(p)}"
        else:
            text += f"🎯 نوبت: {battle['current_turn']}"
    else:
        text += "⏳ در حال پردازش..."
    return text


def boss_attack_players(battle, log):
    all_players = [p for p in battle["team1"] + battle["team2"] if p["hp"] > 0]
    if not all_players:
        return log

    target = random.choice(all_players)
    boss_atk = get_boss_atk(battle["boss_name"])

    if target.get("frozen", 0) > 0:
        target["frozen"] -= 1
        log += f"\n❄️ {disp(target)} فریزه!"
        return log

    base_dmg, crit = roll_damage(boss_atk, 0, 0)
    crit_str = " 🎯" if crit else ""
    log += f"\n👹 باس → {disp(target)}!\n⚔️ آسیب پایه: {base_dmg}{crit_str}"

    defense = target.get("defense_action", None)
    if defense == "defend":
        target["hp"], def_log = apply_defense_check(base_dmg, target["hp"], "دفاع")
        log += f"\n{def_log}"
        log += f"\n👤 HP {disp(target)}: {target['hp']}/{target['max_hp']}"
    elif defense == "dodge":
        target["hp"], def_log = apply_defense_check(base_dmg, target["hp"], "جاخالی")
        log += f"\n{def_log}"
        log += f"\n👤 HP {disp(target)}: {target['hp']}/{target['max_hp']}"
    else:
        target["hp"] = max(0, target["hp"] - base_dmg)
        log += f"\n👤 HP {disp(target)}: {target['hp']}/{target['max_hp']}"

    if target["hp"] <= 0:
        log += f"\n☠️ {disp(target)} خارج شد!"

    target["defense_action"] = None

    return log


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
        log = f"⚔️ {disp(player)} → {disp(target)}: {dmg}{crit_str}"
        if target["hp"] <= 0:
            log += f"\n☠️ {disp(target)} خارج شد!"

    elif action == "defend":
        player["defense_action"] = "defend"
        log = f"🛡️ {disp(player)} دفاع گرفت. (۳۳٪ کامل / ۳۳٪ جزئی)"

    elif action == "dodge":
        player["defense_action"] = "dodge"
        log = f"💨 {disp(player)} جاخالی می‌زنه. (۳۳٪ کامل / ۳۳٪ جزئی)"

    elif action == "domain":
        char_name = player["name"]
        if char_name not in DOMAINS_JJK:
            return None, "❌ این کاراکتر Domain نداره!"
        if battle.get(f"domain_used_{uid}", 0) == 1:
            return None, "❌ Domain فقط یه بار در نبرد!"
        cd_key = f"domain_cd_{uid}"
        if battle.get(cd_key, 0) > 0:
            return None, f"⏱️ کول‌داون: {battle[cd_key]} راند"
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
            if "damage_mult" in effects:
                dmg = int(player["atk"] * effects["damage_mult"])
                target["hp"] = max(0, target["hp"] - dmg)
                log += f"⚔️ {disp(target)}: {dmg} آسیب\n"
            if "hp_drain" in effects:
                drain = int(target["max_hp"] * effects["hp_drain"] / 100)
                target["hp"] = max(0, target["hp"] - drain)
                log += f"💀 {disp(target)}: -{drain} HP\n"
            if "freeze" in effects:
                target["frozen"] = effects["freeze"]
                log += f"❄️ {disp(target)} فریز!\n"
            if "dodge_debuff" in effects:
                target["dodge_debuff"] = effects["dodge_debuff"]
        if "atk_boost" in effects:
            player["atk_boost"] = effects["atk_boost"]
            log += f"⚔️ ATK +{effects['atk_boost']}٪\n"
        if "heal" in effects:
            heal = int(player["max_hp"] * effects["heal"] / 100)
            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            log += f"💚 {heal} HP\n"
        battle[f"domain_used_{uid}"] = 1
        battle[cd_key] = 2
        next_turn(battle)
        update_multi_battle(session_id, battle)
        return "active", log

    elif action == "bankai":
        char_name = player["name"]
        if char_name not in BLEACH_BANKAI:
            return None, "❌ این کاراکتر Bankai نداره!"
        if battle.get(f"bankai_used_{uid}", 0) == 1:
            return None, "❌ Bankai فقط یه بار در نبرد!"
        cd_key = f"bankai_cd_{uid}"
        if battle.get(cd_key, 0) > 0:
            return None, f"⏱️ کول‌داون: {battle[cd_key]} راند"
        bankai = BLEACH_BANKAI[char_name]
        battle[f"bankai_used_{uid}"] = 1
        battle[cd_key] = 2
        log = f"⚔️ Bankai: {bankai['name']}!\n"
        if "atk_boost" in bankai:
            player["atk_boost"] = bankai["atk_boost"]
            log += f"⚔️ ATK +{bankai['atk_boost']}٪\n"
        if "atk_per_round" in bankai:
            player["atk_per_round"] = bankai["atk_per_round"]
            player["bankai_max_atk"] = bankai.get("max_atk", 50)
            player["bankai_atk_current"] = 0
            log += f"⚔️ ATK +{bankai['atk_per_round']}٪/راند\n"
        if "dodge_per_round" in bankai:
            player["dodge_per_round"] = bankai["dodge_per_round"]
            player["bankai_max_dodge"] = bankai.get("max_dodge", 25)
            player["bankai_dodge_current"] = 0
            log += f"💨 دوج +{bankai['dodge_per_round']}٪/راند\n"
        if "heal_per_round" in bankai:
            player["heal_per_round"] = bankai["heal_per_round"]
        if "bleed_per_round" in bankai:
            player["bleed_per_round"] = bankai["bleed_per_round"]
            player["bankai_bleed_current"] = 0
            player["bankai_max_bleed"] = bankai.get("max_bleed", 8)
        if "crit_chance" in bankai:
            player["crit_chance"] = bankai["crit_chance"]
        if "extra_hit_chance" in bankai:
            player["extra_hit_chance"] = bankai["extra_hit_chance"]
        next_turn(battle)
        update_multi_battle(session_id, battle)
        return "active", log

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
            found_ab = {"name": ability_name, "effect": ABILITIES[ability_name]["effect"], "type": "shop"}
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
                    log += f"☠️ {disp(target)} خارج شد!"
        elif ab_type == "heal":
            heal = int(player["max_hp"] * 0.3)
            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            log += f"💚 {heal} HP\n"
        elif ab_type == "freeze":
            if target:
                target["frozen"] = 1
                log += f"❄️ {disp(target)} فریز!\n"
        elif ab_type == "buff":
            player["atk_boost"] = 50
            log += "⚔️ ATK +۵۰٪\n"
        battle[used_key] = 1
        next_turn(battle)
        update_multi_battle(session_id, battle)
        return "active", log

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

    else:
        return None, "❌ اکشن نامعتبر."

    team1_alive = [p for p in battle["team1"] if p["hp"] > 0]
    team2_alive = [p for p in battle["team2"] if p["hp"] > 0]

    if battle["boss_name"]:
        if battle["boss_hp"] <= 0:
            battle["status"] = "won"
            update_multi_battle(session_id, battle)
            return "won", log
        log = boss_attack_players(battle, log)

        for p in battle["team1"] + battle["team2"]:
            if p["hp"] > 0 and p.get("atk_per_round"):
                cur = p.get("bankai_atk_current", 0)
                mx = p.get("bankai_max_atk", 50)
                if cur < mx:
                    p["bankai_atk_current"] = min(mx, cur + p["atk_per_round"])
                    p["atk_boost"] = p["bankai_atk_current"]
            if p["hp"] > 0 and p.get("dodge_per_round"):
                cur = p.get("bankai_dodge_current", 0)
                mx = p.get("bankai_max_dodge", 25)
                if cur < mx:
                    p["bankai_dodge_current"] = min(mx, cur + p["dodge_per_round"])
            if p["hp"] > 0 and p.get("bleed_per_round"):
                cur = p.get("bankai_bleed_current", 0)
                mx = p.get("bankai_max_bleed", 8)
                if cur < mx:
                    p["bankai_bleed_current"] = min(mx, cur + p["bleed_per_round"])
                bleed = int(battle["boss_max_hp"] * p["bankai_bleed_current"] / 100)
                battle["boss_hp"] = max(0, battle["boss_hp"] - bleed)
                log += f"\n🩸 {disp(p)} بانکای: باس {bleed} HP"
            if p["hp"] > 0 and p.get("heal_per_round"):
                heal = int(p["max_hp"] * p["heal_per_round"] / 100)
                p["hp"] = min(p["max_hp"], p["hp"] + heal)
                log += f"\n💚 {disp(p)} بانکای: {heal} HP"

        if battle["boss_hp"] <= 0:
            battle["status"] = "won"
            update_multi_battle(session_id, battle)
            return "won", log
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
