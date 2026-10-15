import random
import json
import sqlite3
from config import (BOSSES, ABILITIES, BUFFS, ITEMS,
                    ABILITY_FA, BUFF_FA, ITEM_FA, ABILITIES_3, DOMAINS, BANKAI)
from jjk_data import DOMAINS_JJK, FODDER_JJK, BOSSES_JJK, ABILITIES_JJK
from bleach_data import BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER
from opm_data import BOSSES_OPM
from database import DB_NAME, add_coins, get_abilities
from quests import update_quest_progress


def format_num(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def hp_bar(current, maximum, length=10):
    if maximum <= 0:
        return "💔 [" + "░" * length + "] ۰/۰"
    pct = current / maximum
    filled = int(pct * length)
    filled = max(0, min(length, filled))
    empty = length - filled
    bar = "█" * filled + "░" * empty
    if pct > 0.6:
        icon = "❤️"
    elif pct > 0.3:
        icon = "🧡"
    else:
        icon = "💔"
    return f"{icon} [{bar}] {format_num(current)}/{format_num(maximum)}"


def box_title(text, width=26):
    pad = width - len(text)
    if pad < 0:
        text = text[:width]
        pad = 0
    left = pad // 2
    right = pad - left
    return f"╔{'═' * width}╗\n║{' ' * left}{text}{' ' * right}║\n╚{'═' * width}╝"


def box_simple(text, width=24):
    if len(text) > width - 2:
        text = text[:width - 2]
    return f"┌{'─' * width}┐\n│ {text.center(width - 2)} │\n└{'─' * width}┘"


# ============================================
# DATABASE - MULTI BATTLES
# ============================================

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


# ============================================
# UTILS
# ============================================

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
        return hp, f"⚠️ {defense_type} جزئی! {format_num(partial)} آسیب (۵۰٪)"
    else:
        hp = max(0, hp - base_dmg)
        return hp, f"❌ {defense_type} ناموفق! {format_num(base_dmg)} آسیب کامل"


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
    if boss_name in BOSSES_OPM:
        return BOSSES_OPM[boss_name]["atk"]
    if boss_name in BOSSES:
        return BOSSES[boss_name]["atk"]
    return 100
def build_battle_view(battle):
    btype = battle.get("type", "").upper()
    type_icons = {"PVP": "⚔️ PVP BATTLE", "COOP": "👥 CO-OP BATTLE", "TEAM": "⚔️ TEAM BATTLE"}
    type_title = type_icons.get(btype, f"⚔️ {btype}")

    text = box_title(type_title, 26) + "\n"

    if battle["boss_name"]:
        boss_name = battle["boss_name"]
        text += f"\n👹 {boss_name}\n"
        text += f"{hp_bar(battle['boss_hp'], battle['boss_max_hp'])}\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━━\n"

    text += "\n🟦 Team 1:\n"
    for p in battle["team1"]:
        if p["hp"] > 0:
            status = "🎯 نوبت" if str(p["uid"]) == str(battle["current_turn"]) else "⏳"
            frozen = "❄️" if p.get("frozen", 0) > 0 else ""
            text += f"├ 👤 {disp(p)} {frozen}\n"
            text += f"│ {hp_bar(p['hp'], p['max_hp'])}\n"
            text += f"└ {status}\n"
        else:
            text += f"├ 💀 {disp(p)}\n└ خارج شد\n"

    if battle["team2"]:
        text += "\n🟥 Team 2:\n"
        for p in battle["team2"]:
            if p["hp"] > 0:
                status = "🎯 نوبت" if str(p["uid"]) == str(battle["current_turn"]) else "⏳"
                frozen = "❄️" if p.get("frozen", 0) > 0 else ""
                text += f"├ 👤 {disp(p)} {frozen}\n"
                text += f"│ {hp_bar(p['hp'], p['max_hp'])}\n"
                text += f"└ {status}\n"
            else:
                text += f"├ 💀 {disp(p)}\n└ خارج شد\n"

    text += "\n━━━━━━━━━━━━━━━━━━━━━━━━\n"

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
        log += f"\n\n❄️ {disp(target)} فریزه! (نوبت از دست داد)"
        return log

    base_dmg, crit = roll_damage(boss_atk, 0, 0)

    log += f"\n\n{box_simple('👹 باس حمله کرد!')}"
    if crit:
        log += f"\n\n⚡ CRITICAL HIT! ⚡"
    log += f"\n\n💢 آسیب پایه: {format_num(base_dmg)}"

    defense = target.get("defense_action", None)
    if defense == "defend":
        target["hp"], def_log = apply_defense_check(base_dmg, target["hp"], "دفاع")
        log += f"\n{def_log}"
    elif defense == "dodge":
        target["hp"], def_log = apply_defense_check(base_dmg, target["hp"], "جاخالی")
        log += f"\n{def_log}"
    else:
        target["hp"] = max(0, target["hp"] - base_dmg)

    log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"

    if target["hp"] <= 0:
        log += f"\n\n☠️ {disp(target)} خارج شد!"

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
    char_name = player["name"]

    # حمله ساده
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
        battle[f"last_ab_{uid}"] = "simple"
        if crit:
            log = box_simple("⚡ CRITICAL HIT! ⚡")
        else:
            log = box_simple("⚔️ حمله!")
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب 💥"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"
        if target["hp"] <= 0:
            log += f"\n\n☠️ {disp(target)} خارج شد!"

    # دفاع
    elif action == "defend":
        player["defense_action"] = "defend"
        log = box_simple("🛡️ دفاع گرفتی!")
        log += "\n\n🎲 ۳۳٪ کامل / ۳۳٪ جزئی / ۳۳٪ ناموفق"

    # جاخالی
    elif action == "dodge":
        player["defense_action"] = "dodge"
        log = box_simple("💨 جاخالی می‌زنی!")
        log += "\n\n🎲 ۳۳٪ کامل / ۳۳٪ جزئی / ۳۳٪ ناموفق"

    # ABILITY 1 (🔵 آبی)
    elif action == "ability_1":
        abilities = ABILITIES_3.get(char_name, {})
        ab = abilities.get("ability_1")
        if not ab:
            return None, "❌ Ability 1 نداری!"
        last = battle.get(f"last_ab_{uid}", None)
        if last == "ability_1":
            return None, "🔒 برای استفاده دوباره آبی، اول قرمز بزن!"
        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."
        mult = ab.get("mult", 3)
        dmg = int(player["atk"] * mult)
        atk_boost = player.get("atk_boost", 0)
        if atk_boost:
            dmg = int(dmg * (1 + atk_boost / 100))
        target = random.choice(enemies)
        target["hp"] = max(0, target["hp"] - dmg)
        battle[f"last_ab_{uid}"] = "ability_1"
        log = box_simple(f"🔵 {ab['name'][:18]}!")
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب ({mult}x)"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"
        if target["hp"] <= 0:
            log += f"\n☠️ {disp(target)} خارج شد!"

    # ABILITY 2 (🔴 قرمز)
    elif action == "ability_2":
        abilities = ABILITIES_3.get(char_name, {})
        ab = abilities.get("ability_2")
        if not ab:
            return None, "❌ Ability 2 نداری!"
        last = battle.get(f"last_ab_{uid}", None)
        if last == "ability_2":
            return None, "🔒 برای استفاده دوباره قرمز، اول آبی یا بنفش بزن!"
        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."
        mult = ab.get("mult", 5)
        dmg = int(player["atk"] * mult)
        atk_boost = player.get("atk_boost", 0)
        if atk_boost:
            dmg = int(dmg * (1 + atk_boost / 100))
        target = random.choice(enemies)
        target["hp"] = max(0, target["hp"] - dmg)
        battle[f"last_ab_{uid}"] = "ability_2"
        log = box_simple(f"🔴 {ab['name'][:18]}!")
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب ({mult}x)"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"
        if target["hp"] <= 0:
            log += f"\n☠️ {disp(target)} خارج شد!"

    # ABILITY 3 (🟣 بنفش - ۱ بار)
    elif action == "ability_3":
        abilities = ABILITIES_3.get(char_name, {})
        ab = abilities.get("ability_3")
        if not ab:
            return None, "❌ Ultimate نداری!"
        if battle.get(f"purple_used_{uid}", 0) == 1:
            return None, "🟣 Ultimate فقط ۱ بار در کل نبرد!"
        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."
        mult = ab.get("mult", 10)
        dmg = int(player["atk"] * mult)
        atk_boost = player.get("atk_boost", 0)
        if atk_boost:
            dmg = int(dmg * (1 + atk_boost / 100))
        target = random.choice(enemies)
        target["hp"] = max(0, target["hp"] - dmg)
        battle[f"purple_used_{uid}"] = 1
        battle[f"last_ab_{uid}"] = "ability_3"
        log = box_title(f"🟣 {ab['name'][:20]}!", 26)
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب فاجعه‌بار! ({mult}x)"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"
        if target["hp"] <= 0:
            log += f"\n☠️ {disp(target)} خارج شد!"

    # DOMAIN (🌀 ×۸)
    elif action == "domain":
        if char_name not in DOMAINS:
            return None, "❌ این کاراکتر Domain نداره!"
        if battle.get(f"domain_used_{uid}", 0) == 1:
            return None, "❌ Domain فقط یه بار در نبرد!"
        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."
        dmg = int(player["atk"] * 8)
        atk_boost = player.get("atk_boost", 0)
        if atk_boost:
            dmg = int(dmg * (1 + atk_boost / 100))
        target = random.choice(enemies)
        target["hp"] = max(0, target["hp"] - dmg)
        battle[f"domain_used_{uid}"] = 1
        log = box_title(f"🌀 {DOMAINS[char_name]['name'][:20]}", 26)
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب (×۸)"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"
        if target["hp"] <= 0:
            log += f"\n☠️ {disp(target)} خارج شد!"

    # BANKAI (⚔️ ×۶)
    elif action == "bankai":
        if char_name not in BANKAI:
            return None, "❌ این کاراکتر Bankai نداره!"
        if battle.get(f"bankai_used_{uid}", 0) == 1:
            return None, "❌ Bankai فقط یه بار در نبرد!"
        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."
        dmg = int(player["atk"] * 6)
        atk_boost = player.get("atk_boost", 0)
        if atk_boost:
            dmg = int(dmg * (1 + atk_boost / 100))
        target = random.choice(enemies)
        target["hp"] = max(0, target["hp"] - dmg)
        battle[f"bankai_used_{uid}"] = 1
        log = box_title(f"⚔️ {BANKAI[char_name]['name'][:20]}", 26)
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب (×۶)"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"
        if target["hp"] <= 0:
            log += f"\n☠️ {disp(target)} خارج شد!"

    else:
        return None, "❌ اکشن نامعتبر."

    # چک پایان
    team1_alive = [p for p in battle["team1"] if p["hp"] > 0]
    team2_alive = [p for p in battle["team2"] if p["hp"] > 0]

    if battle["boss_name"]:
        if battle["boss_hp"] <= 0:
            battle["status"] = "won"
            update_multi_battle(session_id, battle)
            return "won", log
        log = boss_attack_players(battle, log)
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
    next_player, _ = get_player(battle, battle["current_turn"])
    if next_player and next_player.get("frozen", 0) > 0:
        next_player["frozen"] -= 1
        log += f"\n\n❄️ {disp(next_player)} فریزه! نوبتش رد شد."
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
        elif boss_name in BOSSES_OPM:
            reward = BOSSES_OPM[boss_name]["reward"]
        else:
            reward = BOSSES.get(boss_name, {}).get("reward", 5000)
        for p in battle["team1"] + battle["team2"]:
            add_coins(p["uid"], reward)
            rewards[p["uid"]] = reward
            try:
                from guild import give_guild_xp
                give_guild_xp(p["uid"], 30)
            except Exception:
                pass
        end_multi_battle(session_id)
        return {"type": "boss_win", "rewards": rewards, "boss": boss_name}

    if status == "team1_won":
        amount = 300 if battle["type"] == "pvp" else 1500
        for p in battle["team1"]:
            add_coins(p["uid"], amount)
            rewards[p["uid"]] = amount
            try:
                from guild import give_guild_xp
                xp = 25 if battle["type"] == "pvp" else 35
                give_guild_xp(p["uid"], xp)
            except Exception:
                pass
        end_multi_battle(session_id)
        return {"type": "team1_win", "rewards": rewards}

    if status == "team2_won":
        amount = 300 if battle["type"] == "pvp" else 1500
        for p in battle["team2"]:
            add_coins(p["uid"], amount)
            rewards[p["uid"]] = amount
            try:
                from guild import give_guild_xp
                xp = 25 if battle["type"] == "pvp" else 35
                give_guild_xp(p["uid"], xp)
            except Exception:
                pass
        end_multi_battle(session_id)
        return {"type": "team2_win", "rewards": rewards}

    if status == "draw":
        for p in battle["team1"] + battle["team2"]:
            add_coins(p["uid"], 500)
            rewards[p["uid"]] = 500
        end_multi_battle(session_id)
        return {"type": "draw", "rewards": rewards}

    return None