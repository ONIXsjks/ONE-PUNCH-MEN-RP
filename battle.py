# battle.py

import random
from database import (get_battle, update_battle, end_battle,
                      get_abilities, get_items, use_item, add_coins)
from characters import get_active_character
from config import (BOSSES, ABILITIES, BUFFS, ITEMS,
                    ABILITY_FA, BUFF_FA, ITEM_FA)
from jjk_data import DOMAINS_JJK, BOSSES_JJK, FODDER_JJK, ABILITIES_JJK
from bleach_data import BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER, ABILITIES_BLEACH
from opm_data import BOSSES_OPM, ABILITIES_OPM
from quests import update_quest_progress


# ============ توابع کمکی ============

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


def get_boss_stats(boss_name):
    """آمار باس رو از هر سه دیتای موجود می‌خونه"""
    if boss_name in BLEACH_BOSSES:
        return BLEACH_BOSSES[boss_name]
    if boss_name in BLEACH_FODDER:
        return BLEACH_FODDER[boss_name]
    if boss_name in BOSSES_JJK:
        return BOSSES_JJK[boss_name]
    if boss_name in FODDER_JJK:
        return FODDER_JJK[boss_name]
    if boss_name in BOSSES_OPM:
        return BOSSES_OPM[boss_name]
    if boss_name in BOSSES:
        return BOSSES[boss_name]
    return {"hp": 1000, "atk": 100, "reward": 1000}


def build_battle_message(battle, extra_log=""):
    """پیام نبرد رو می‌سازه"""
    boss_name = battle["boss_name"]
    boss_info = get_boss_stats(boss_name)
    display_name = boss_info.get("display_name", boss_name)
    
    text = box_title("⚔️ BOSS BATTLE ⚔️", 26) + "\n\n"
    text += f"👹 {display_name}\n"
    text += f"{hp_bar(battle['bhp'], battle['bmax'])}\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    char = get_active_character(battle["uid"])
    if char:
        char_name = char[2]
        text += f"👤 {char_name}\n"
    else:
        text += f"👤 Player\n"
    
    text += f"{hp_bar(battle['php'], battle['pmax'])}\n\n"
    
    if battle.get("domain_active"):
        text += f"🌀 Domain فعال: {battle.get('domain_name', '')}\n"
        text += f"⏳ {battle.get('domain_turns', 0)} راند مونده\n\n"
    
    if battle.get("bankai_used"):
        text += f"⚔️ Bankai فعال\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"🎯 نوبت تو!  |  🌀 Round {battle.get('turn', 1)}\n"
    
    if extra_log:
        text += "\n" + extra_log
    
    return text


# ============ حمله ساده ============

def player_attack(user_id):
    """حمله ساده"""
    battle = get_battle(user_id)
    if not battle:
        return None, "نبرد فعالی وجود ندارد."
    
    char = get_active_character(user_id)
    if not char:
        return None, "کاراکتر فعالی نداری."
    
    atk = char[6]
    
    # اگه Domain فعاله، اتک کامل
    if battle.get("domain_active"):
        base_dmg = atk
    else:
        base_dmg = int(atk * 0.5)  # اتک ساده کمتر شد
    
    dmg = random.randint(int(base_dmg * 0.9), int(base_dmg * 1.1))
    crit = random.random() < 0.15
    if crit:
        dmg = int(dmg * 1.5)
    
    battle["bhp"] = max(0, battle["bhp"] - dmg)
    
    log = "⚔️ حمله ساده!"
    if crit:
        log = "⚡ CRITICAL HIT! ⚡"
    log += f"\n💥 {format_num(dmg)} آسیب"
    
    if battle["bhp"] > 0:
        boss_info = get_boss_stats(battle["boss_name"])
        boss_atk = boss_info.get("atk", 100)
        boss_dmg = random.randint(int(boss_atk * 0.85), int(boss_atk * 1.15))
        battle["php"] = max(0, battle["php"] - boss_dmg)
        log += f"\n\n👹 باس حمله کرد: {format_num(boss_dmg)} آسیب"
    
    battle["turn"] = battle.get("turn", 0) + 1
    update_battle(battle)
    return battle, log
# ============ ⭐ Ability جدید ============

def player_ability(user_id, ability_slot=None):
    """
    استفاده از Ability
    ability_slot: 1, 2, یا 3
    """
    battle = get_battle(user_id)
    if not battle:
        return None, "نبرد فعالی وجود ندارد."
    
    char = get_active_character(user_id)
    if not char:
        return None, "کاراکتر فعالی نداری."
    
    char_name = char[2]
    atk = char[6]
    
    # === پیدا کردن Ability از دیتای کاراکتر ===
    abilities = {}
    
    if char_name in ABILITIES_JJK:
        abilities = ABILITIES_JJK[char_name]
    elif char_name in ABILITIES_BLEACH:
        abilities = ABILITIES_BLEACH[char_name]
    elif char_name in ABILITIES_OPM:
        abilities = ABILITIES_OPM[char_name]
    else:
        return None, "❌ این کاراکتر Ability نداره!"
    
    ability_key = f"ability_{ability_slot}"
    if ability_key not in abilities:
        return None, "❌ این Ability وجود ندارد."
    
    ability = abilities[ability_key]
    ability_name = ability["name"]
    mult = ability.get("mult", 1.0)
    is_once = ability.get("once", False)
    
    # === چک اسپم ===
    spam_state = battle.get("spam_state", "")
    
    if is_once:
        if battle.get(f"used_once_{ability_name}", 0) == 1:
            return None, f"❌ {ability_name} قبلاً استفاده شده!"
    else:
        if spam_state == ability_key:
            return None, f"❌ برای استفاده مجدد از {ability_name}، اول یه Ability دیگه بزن!"
    
    # === محاسبه دمیج ===
    if battle.get("domain_active"):
        base_dmg = atk
    else:
        base_dmg = int(atk * mult)
    
    dmg = random.randint(int(base_dmg * 0.9), int(base_dmg * 1.1))
    crit = random.random() < 0.15
    if crit:
        dmg = int(dmg * 1.5)
    
    battle["bhp"] = max(0, battle["bhp"] - dmg)
    
    # === لاگ ===
    log = f"🔥 {ability_name}!"
    if crit:
        log = f"⚡ CRITICAL! ⚡\n🔥 {ability_name}!"
    log += f"\n💥 {format_num(dmg)} آسیب"
    
    if is_once:
        log += f"\n\n💜 (یک بار مصرف)"
    
    # === آپدیت اسپم ===
    if is_once:
        battle[f"used_once_{ability_name}"] = 1
        battle["spam_state"] = ""
    else:
        battle["spam_state"] = ability_key
    
    # === حمله باس ===
    if battle["bhp"] > 0:
        boss_info = get_boss_stats(battle["boss_name"])
        boss_atk = boss_info.get("atk", 100)
        
        if battle.get("boss_frozen", 0) > 0:
            battle["boss_frozen"] -= 1
            log += f"\n\n❄️ باس فریزه! نوبتش رو از دست داد."
        else:
            boss_dmg = random.randint(int(boss_atk * 0.85), int(boss_atk * 1.15))
            battle["php"] = max(0, battle["php"] - boss_dmg)
            log += f"\n\n👹 باس حمله کرد: {format_num(boss_dmg)} آسیب"
    
    battle["turn"] = battle.get("turn", 0) + 1
    update_battle(battle)
    return battle, log


# ============ دفاع، جاخالی، آیتم ============

def player_defend(user_id):
    """دفاع"""
    battle = get_battle(user_id)
    if not battle:
        return None, "نبرد فعالی وجود ندارد."
    
    log = "🛡️ دفاع گرفتی! آسیب بعدی ۵۰٪ کمتر"
    
    if battle["bhp"] > 0:
        boss_info = get_boss_stats(battle["boss_name"])
        boss_atk = boss_info.get("atk", 100)
        boss_dmg = random.randint(int(boss_atk * 0.85), int(boss_atk * 1.15))
        boss_dmg = int(boss_dmg * 0.5)
        battle["php"] = max(0, battle["php"] - boss_dmg)
        log += f"\n\n👹 باس حمله کرد: {format_num(boss_dmg)} آسیب (دفاع کردی)"
    
    battle["turn"] = battle.get("turn", 0) + 1
    update_battle(battle)
    return battle, log


def player_dodge(user_id):
    """جاخالی"""
    battle = get_battle(user_id)
    if not battle:
        return None, "نبرد فعالی وجود ندارد."
    
    char = get_active_character(user_id)
    dodge_chance = char[8] if char else 10
    
    if random.randint(1, 100) <= dodge_chance:
        log = "💨 جاخالی موفق! آسیب صفر"
    else:
        boss_info = get_boss_stats(battle["boss_name"])
        boss_atk = boss_info.get("atk", 100)
        boss_dmg = random.randint(int(boss_atk * 0.85), int(boss_atk * 1.15))
        battle["php"] = max(0, battle["php"] - boss_dmg)
        log = f"❌ جاخالی ناموفق!\n👹 باس: {format_num(boss_dmg)} آسیب"
    
    battle["turn"] = battle.get("turn", 0) + 1
    update_battle(battle)
    return battle, log


def player_item(user_id, item_name):
    """استفاده از آیتم"""
    battle = get_battle(user_id)
    if not battle:
        return None, "نبرد فعالی وجود ندارد."
    
    if not use_item(user_id, item_name):
        return None, "❌ این آیتم رو نداری."
    
    log = f"💊 {item_name} استفاده شد!"
    
    if "Potion" in item_name:
        heal = int(battle["pmax"] * 0.3)
        battle["php"] = min(battle["pmax"], battle["php"] + heal)
        log += f"\n💚 {format_num(heal)} HP درمان شد"
    
    if battle["bhp"] > 0:
        boss_info = get_boss_stats(battle["boss_name"])
        boss_atk = boss_info.get("atk", 100)
        boss_dmg = random.randint(int(boss_atk * 0.85), int(boss_atk * 1.15))
        battle["php"] = max(0, battle["php"] - boss_dmg)
        log += f"\n\n👹 باس: {format_num(boss_dmg)} آسیب"
    
    battle["turn"] = battle.get("turn", 0) + 1
    update_battle(battle)
    return battle, log


# ============ پایان نبرد ============

def finish_battle(user_id):
    """پایان نبرد - چک برد/باخت"""
    battle = get_battle(user_id)
    if not battle:
        return None
    
    if battle["bhp"] <= 0:
        boss_info = get_boss_stats(battle["boss_name"])
        reward = boss_info.get("reward", 1000)
        add_coins(user_id, reward)
        
        log = box_title("🏆 VICTORY! 🏆", 26)
        log += f"\n\n💰 جایزه: {format_num(reward)} سکه"
        log += f"\n🎯 تعداد راند: {battle.get('turn', 0)}"
        
        update_quest_progress(user_id, "kill_1_boss")
        end_battle(battle["id"])
        return log
    
    elif battle["php"] <= 0:
        log = box_title("💀 DEFEAT 💀", 26)
        log += f"\n\n😢 شکست خوردی!"
        log += f"\n🎯 تعداد راند: {battle.get('turn', 0)}"
        
        end_battle(battle["id"])
        return log
    
    return None