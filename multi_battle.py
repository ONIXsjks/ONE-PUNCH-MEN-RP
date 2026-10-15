import random
import json
import sqlite3
from config import (BOSSES, ABILITIES, BUFFS, ITEMS,
                    ABILITY_FA, BUFF_FA, ITEM_FA)
from jjk_data import DOMAINS_JJK, FODDER_JJK, BOSSES_JJK, ABILITIES_JJK
from bleach_data import BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER
from opm_data import BOSSES_OPM, ABILITIES_OPM
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


def get_character_abilities(char_name):
    """گرفتن ۳ Ability کاراکتر از JJK یا OPM"""
    for data in [ABILITIES_JJK, ABILITIES_OPM]:
        if char_name in data:
            return data[char_name]
    return None
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
        return hp, f"⚠️ {defense_type} جزئی! {format_num(partial)} آسیب (۵۰٪)"
    else:
        hp = max(0, hp - base_dmg)
        return hp, f"❌ {defense_type} ناموفق! {format_num(base_dmg)} آسیب کامل"


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
    abs_data = get_character_abilities(char_name)

    # ==========================================
    # حمله ساده
    # ==========================================
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

        if crit:
            log = box_simple("⚡ CRITICAL HIT! ⚡")
        else:
            log = box_simple("⚔️ حمله!")
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب 💥"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"

        if target["hp"] <= 0:
            log += f"\n\n☠️ {disp(target)} خارج شد!"

    # ==========================================
    # دفاع
    # ==========================================
    elif action == "defend":
        player["defense_action"] = "defend"
        log = box_simple("🛡️ دفاع گرفتی!")
        log += "\n\n🎲 ۳۳٪ کامل / ۳۳٪ جزئی / ۳۳٪ ناموفق"

    # ==========================================
    # جاخالی
    # ==========================================
    elif action == "dodge":
        player["defense_action"] = "dodge"
        log = box_simple("💨 جاخالی می‌زنی!")
        log += "\n\n🎲 ۳۳٪ کامل / ۳۳٪ جزئی / ۳۳٪ ناموفق"

    # ==========================================
    # 🔵 ABILITY 1 (آبی - دمیج متوسط) + Spam Prevention
    # ==========================================
    elif action == "ability_1":
        if not abs_data:
            return None, "❌ این کاراکتر Ability نداره!"
        ab = abs_data.get("ability_1")
        if not ab:
            return None, "❌ Ability 1 تعریف نشده!"

        # 🔒 Spam: بعد از آبی باید قرمز بزنی
        last = battle.get(f"last_ab_{uid}", None)
        if last == "ability_1":
            return None, "🔒 برای استفاده دوباره آبی، اول قرمز بزن!"

        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."

        mult = ab.get("multiplier", 3)
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

    # ==========================================
    # 🔴 ABILITY 2 (قرمز - دمیج قوی) + Spam Prevention
    # ==========================================
    elif action == "ability_2":
        if not abs_data:
            return None, "❌ این کاراکتر Ability نداره!"
        ab = abs_data.get("ability_2")
        if not ab:
            return None, "❌ Ability 2 تعریف نشده!"

        # 🔒 Spam: بعد از قرمز باید آبی یا بنفش بزنی
        last = battle.get(f"last_ab_{uid}", None)
        if last == "ability_2":
            return None, "🔒 برای استفاده دوباره قرمز، اول آبی یا بنفش بزن!"

        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."

        mult = ab.get("multiplier", 5)
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

    # ==========================================
    # 🟣 ABILITY 3 (بنفش - ۱ بار مصرف در کل نبرد)
    # ==========================================
    elif action == "ability_3":
        if not abs_data:
            return None, "❌ این کاراکتر Ability نداره!"
        ab = abs_data.get("ability_3")
        if not ab:
            return None, "❌ Ultimate تعریف نشده!"

        # 🟣 فقط ۱ بار
        if battle.get(f"purple_used_{uid}", 0) == 1:
            return None, "🟣 Ultimate فقط ۱ بار در کل نبرد!"

        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."

        mult = ab.get("multiplier", 10)
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

    # ==========================================
    # 🌀 DOMAIN - اتک ساده × ۸ (بدون اسپم)
    # ==========================================
    elif action == "domain":
        if char_name not in DOMAINS_JJK:
            return None, "❌ این کاراکتر Domain نداره!"
        if battle.get(f"domain_used_{uid}", 0) == 1:
            return None, "❌ Domain فقط یه بار در نبرد!"
        cd_key = f"domain_cd_{uid}"
        if battle.get(cd_key, 0) > 0:
            return None, f"⏱️ کول‌داون: {battle[cd_key]} راند"

        domain = DOMAINS_JJK[char_name]
        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."

        # 🌀 ضریب ۸ (بدون اسپم - کل دمیج یکجا)
        dmg = int(player["atk"] * 8)
        atk_boost = player.get("atk_boost", 0)
        if atk_boost:
            dmg = int(dmg * (1 + atk_boost / 100))

        target = random.choice(enemies)
        target["hp"] = max(0, target["hp"] - dmg)
        battle[f"domain_used_{uid}"] = 1
        battle[cd_key] = 2

        log = box_title(f"🌀 {domain['name'][:20]}", 26)
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب (Domain!)"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"
        if target["hp"] <= 0:
            log += f"\n☠️ {disp(target)} خارج شد!"

    # ==========================================
    # ⚔️ BANKAI - اتک ساده × ۶ (بدون اسپم)
    # ==========================================
    elif action == "bankai":
        if char_name not in BLEACH_BANKAI:
            return None, "❌ این کاراکتر Bankai نداره!"
        if battle.get(f"bankai_used_{uid}", 0) == 1:
            return None, "❌ Bankai فقط یه بار در نبرد!"
        cd_key = f"bankai_cd_{uid}"
        if battle.get(cd_key, 0) > 0:
            return None, f"⏱️ کول‌داون: {battle[cd_key]} راند"

        bankai = BLEACH_BANKAI[char_name]
        enemies = get_enemies(battle, team)
        if not enemies:
            return None, "دشمنی نمونده."

        # ⚔️ ضریب ۶ (بدون اسپم)
        dmg = int(player["atk"] * 6)
        atk_boost = player.get("atk_boost", 0)
        if atk_boost:
            dmg = int(dmg * (1 + atk_boost / 100))

        target = random.choice(enemies)
        target["hp"] = max(0, target["hp"] - dmg)
        battle[f"bankai_used_{uid}"] = 1
        battle[cd_key] = 2

        log = box_title(f"⚔️ {bankai['name'][:20]}", 26)
        log += f"\n\n💥 {disp(player)} → {disp(target)}"
        log += f"\n💢 {format_num(dmg)} آسیب (Bankai!)"
        log += f"\n\n👤 {disp(target)}\n{hp_bar(target['hp'], target['max_hp'])}"
        if target["hp"] <= 0:
            log += f"\n☠️ {disp(target)} خارج شد!"

    # ==========================================
    # 💊 آیتم
    # ==========================================
    elif action == "item" and extra:
        item_name = extra
        if item_name not in ITEMS:
            return None, "❌ آیتم پیدا نشد."
        eff = ITEMS[item_name].get("effect", "")
        log = box_simple(f"💊 {item_name}!")

        if "HP" in eff:
            heal = 500
            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            log += f"\n\n💚 +{format_num(heal)} HP"
            log += f"\n{hp_bar(player['hp'], player['max_hp'])}"

    # ==========================================
    # 🔥 باف
    # ==========================================
    elif action == "buff" and extra:
        buff_name = extra
        if buff_name not in BUFFS:
            return None, "❌ باف پیدا نشد."
        used_key = f"buff_used_{uid}_{buff_name}"
        if battle.get(used_key, 0) == 1:
            return None, f"❌ {buff_name} قبلاً استفاده شده!"
        eff = BUFFS[buff_name]["effect"]

        log = box_simple(f"🔥 {buff_name}!")

        if "Max HP" in eff:
            player["max_hp"] += 500
            player["hp"] += 500
            log += "\n\n❤️ Max HP +۵۰۰"
        elif "ATK" in eff and "150" in eff:
            player["atk"] += 150
            log += "\n\n⚔️ ATK +۱۵۰"
        elif "DEF" in eff:
            player["def"] += 80
            log += "\n\n🛡️ DEF +۸۰"
        elif "DODGE" in eff:
            player["dodge"] += 10
            log += "\n\n💨 دوج +۱۰٪"
        elif "all +20" in eff:
            player["max_hp"] += 200
            player["hp"] += 200
            player["atk"] += 50
            player["def"] += 30
            log += "\n\n🔥 همه +۲۰٪"
        elif "all +50" in eff:
            player["max_hp"] += 500
            player["hp"] += 500
            player["atk"] += 150
            player["def"] += 80
            log += "\n\n🔥 همه +۵۰٪"

        log += f"\n\n{hp_bar(player['hp'], player['max_hp'])}"
        battle[used_key] = 1

    else:
        return None, "❌ اکشن نامعتبر."

    # ==========================================
    # چک پایان نبرد
    # ==========================================
    team1_alive = [p for p in battle["team1"] if p["hp"] > 0]
    team2_alive = [p for p in battle["team2"] if p["hp"] > 0]

    # ---------- باس (Coop) ----------
    if battle["boss_name"]:
        if battle["boss_hp"] <= 0:
            battle["status"] = "won"
            update_multi_battle(session_id, battle)
            return "won", log

        log = boss_attack_players(battle, log)

        # bleed/heal بانکای
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
                log += f"\n\n🩸 باس -{format_num(bleed)} HP"
            if p["hp"] > 0 and p.get("heal_per_round"):
                heal = int(p["max_hp"] * p["heal_per_round"] / 100)
                p["hp"] = min(p["max_hp"], p["hp"] + heal)
                log += f"\n💚 {disp(p)} +{format_num(heal)} HP"

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

    # فریز خودکار
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

    # ---------- برد با باس ----------
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

    # ---------- Team 1 برنده ----------
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

    # ---------- Team 2 برنده ----------
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

    # ---------- مساوی ----------
    if status == "draw":
        for p in battle["team1"] + battle["team2"]:
            add_coins(p["uid"], 500)
            rewards[p["uid"]] = 500
        end_multi_battle(session_id)
        return {"type": "draw", "rewards": rewards}

    return None