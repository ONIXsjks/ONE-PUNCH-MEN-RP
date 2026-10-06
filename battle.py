import random
from config import BOSSES, ABILITIES, ITEMS
from database import add_coins
from quests import update_quest_progress


def roll_damage(atk, defender_def=0, defender_defending=0):
    base = atk * random.uniform(0.85, 1.15)
    crit = random.random() < 0.15
    if crit:
        base *= 2
    if defender_defending:
        base -= defender_def * 2
    else:
        base -= defender_def * 0.5
    dmg = max(1, int(base))
    return dmg, crit


def boss_ai(boss_name, boss_hp, boss_max_hp):
    """Returns action: 'attack', 'special', 'defend', 'heal'"""
    r = random.random()
    if boss_hp < boss_max_hp * 0.25 and r < 0.3:
        return "heal"
    if r < 0.4:
        return "attack"
    if r < 0.7:
        return "special"
    return "defend"


def player_attack(battle, char):
    """battle = (id, user_id, boss_name, hp, max_hp, boss_hp, boss_max_hp, defending, turn, status)"""
    bid, uid, boss_name, php, pmax, bhp, bmax, defending, turn, status = battle
    boss = BOSSES[boss_name]

    dmg, crit = roll_damage(char[6], 0, 0)
    new_bhp = max(0, bhp - dmg)

    text = f"⚔️ حمله کردی: {dmg} آسیب"
    if crit:
        text += " 🎯 کریتیکال!"
    text += f"\n👹 HP باس: {new_bhp}/{bmax}"

    if new_bhp <= 0:
        return "won", text, php, new_bhp

    # Boss turn
    action = boss_ai(boss_name, new_bhp, bmax)
    boss_text, php, bhp_after = boss_action(action, boss, php, pmax, new_bhp, bmax, defending=0)

    text += f"\n\n{boss_text}"

    if php <= 0:
        return "lost", text, php, bhp_after
    return "active", text, php, bhp_after


def player_defend(battle, char):
    bid, uid, boss_name, php, pmax, bhp, bmax, defending, turn, status = battle
    boss = BOSSES[boss_name]

    text = "🛡️ دفاع گرفتی! آسیب این راند کم می‌شه."

    action = boss_ai(boss_name, bhp, bmax)
    boss_text, php, bhp_after = boss_action(action, boss, php, pmax, bhp, bmax, defending=1)

    text += f"\n\n{boss_text}"

    if php <= 0:
        return "lost", text, php, bhp_after
    return "active", text, php, bhp_after


def player_dodge(battle, char):
    bid, uid, boss_name, php, pmax, bhp, bmax, defending, turn, status = battle
    boss = BOSSES[boss_name]

    dodge_chance = char[8]
    success = random.randint(1, 100) <= dodge_chance

    if success:
        text = "💨 جاخالی دادی! باس ضربه‌اش بهت نخورد."
        return "active", text, php, bhp
    else:
        text = "❌ جاخالی ناموفق بود! باس زدت."
        action = boss_ai(boss_name, bhp, bmax)
        boss_text, php, bhp_after = boss_action(action, boss, php, pmax, bhp, bmax, defending=0)
        text += f"\n\n{boss_text}"
        if php <= 0:
            return "lost", text, php, bhp_after
        return "active", text, php, bhp_after


def player_ability(battle, char, ability_name):
    bid, uid, boss_name, php, pmax, bhp, bmax, defending, turn, status = battle
    boss = BOSSES[boss_name]
    info = ABILITIES.get(ability_name)
    if not info:
        return "active", "❌ این Ability رو نداری.", php, bhp

    text = f"🔥 {ability_name} فعال شد!"
    new_bhp = bhp
    new_php = php

    if ability_name == "Iron Skin":
        text += " DEF +50 (این نوبت)"
    elif ability_name == "Shadow Step":
        text += " شانس دوج +15%"
    elif ability_name == "Counter Attack":
        text += " بعد دوج 2x ضربه"
    elif ability_name == "Heal Pulse":
        new_php = min(pmax, php + 200)
        text += f" HP +200 → {new_php}/{pmax}"
    elif ability_name == "Critical Eye":
        text += " شانس کریتیکال +20%"
    elif ability_name == "Berserker":
        text += " ATK +100 (HP<30%)"
    elif ability_name == "Mana Shield":
        text += " جذب 30% آسیب"
    elif ability_name == "Speed Boost":
        text += " اول حمله می‌کنی"
    elif ability_name == "Vampire":
        text += " 20% آسیب = HP"
    elif ability_name == "Dragon Fist":
        dmg = char[6] + 250
        new_bhp = max(0, bhp - dmg)
        text += f" ضربه ویژه: {dmg} آسیب!\n👹 HP باس: {new_bhp}/{bmax}"
    elif ability_name == "Double Strike":
        dmg1, _ = roll_damage(char[6])
        dmg2, _ = roll_damage(char[6])
        new_bhp = max(0, bhp - dmg1 - dmg2)
        text += f" دو ضربه: {dmg1}+{dmg2}\n👹 HP باس: {new_bhp}/{bmax}"
    elif ability_name == "God Mode":
        text += " این نوبت نامیرا هستی!"
    else:
        text += f" {info['effect']}"

    if new_bhp <= 0:
        return "won", text, new_php, new_bhp

    action = boss_ai(boss_name, new_bhp, bmax)
    boss_text, new_php, new_bhp_after = boss_action(action, boss, new_php, pmax, new_bhp, bmax, defending=0)
    text += f"\n\n{boss_text}"

    if new_php <= 0:
        return "lost", text, new_php, new_bhp_after
    return "active", text, new_php, new_bhp_after


def player_item(battle, char, item_name):
    bid, uid, boss_name, php, pmax, bhp, bmax, defending, turn, status = battle
    boss = BOSSES[boss_name]
    info = ITEMS.get(item_name)
    if not info:
        return "active", "❌ این آیتم رو نداری.", php, bhp

    text = f"💊 {item_name} استفاده کردی!"
    new_php = php
    new_bhp = bhp

    if item_name == "Health Potion":
        new_php = min(pmax, php + 500)
        text += f" HP +500 → {new_php}/{pmax}"
    elif item_name == "Mega Potion":
        new_php = min(pmax, php + 1500)
        text += f" HP +1500 → {new_php}/{pmax}"
    elif item_name == "Damage Boost":
        dmg, _ = roll_damage(char[6] * 2)
        new_bhp = max(0, bhp - dmg)
        text += f" ATK x2 → {dmg} آسیب!\n👹 HP باس: {new_bhp}/{bmax}"
    elif item_name == "Bomb":
        new_bhp = max(0, bhp - 500)
        text += f" 500 آسیب!\n👹 HP باس: {new_bhp}/{bmax}"
    else:
        text += f" {info['effect']}"

    if new_bhp <= 0:
        return "won", text, new_php, new_bhp

    action = boss_ai(boss_name, new_bhp, bmax)
    boss_text, new_php, new_bhp_after = boss_action(action, boss, new_php, pmax, new_bhp, bmax, defending=0)
    text += f"\n\n{boss_text}"

    if new_php <= 0:
        return "lost", text, new_php, new_bhp_after
    return "active", text, new_php, new_bhp_after


def boss_action(action, boss, php, pmax, bhp, bmax, defending=0):
    text = ""
    new_php = php
    new_bhp = bhp

    if action == "attack":
        dmg, crit = roll_damage(boss["atk"], 0, defending)
        new_php = max(0, php - dmg)
        text = f"👹 باس حمله کرد: {dmg} آسیب"
        if crit:
            text += " 🎯 کریتیکال!"
        text += f"\n👤 HP تو: {new_php}/{pmax}"

    elif action == "special":
        dmg, _ = roll_damage(boss["atk"] * 2, 0, defending)
        new_php = max(0, php - dmg)
        text = f"💥 حمله ویژه باس: {dmg} آسیب!\n👤 HP تو: {new_php}/{pmax}"

    elif action == "defend":
        text = "🛡️ باس دفاع گرفت."

    elif action == "heal":
        heal = int(bmax * 0.1)
        new_bhp = min(bmax, bhp + heal)
        text = f"💚 باس خودشو درمان کرد: +{heal}\n👹 HP باس: {new_bhp}/{bmax}"

    return text, new_php, new_bhp


def build_battle_message(battle, char):
    bid, uid, boss_name, php, pmax, bhp, bmax, defending, turn, status = battle

    text = (
        f"👹 {boss_name}\n"
        f"❤️ HP: {bhp}/{bmax}\n"
        f"⚔️ ATK: {BOSSES[boss_name]['atk']}\n\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"👤 {char[2]} ({char[3]} Rank)\n"
        f"❤️ HP: {php}/{pmax}\n"
        f"⚔️ ATK: {char[6]}\n"
        f"🛡️ DEF: {char[7]}\n"
        f"💨 DODGE: {char[8]}%\n\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"🎯 نوبت توئه! یه حرکت انتخاب کن:"
    )
    return text


def finish_battle(uid, boss_name, won):
    if won:
        reward = BOSSES[boss_name]["reward"]
        add_coins(uid, reward)
        update_quest_progress(uid, "win_3_bosses")
        update_quest_progress(uid, "win_5_bosses")
        if boss_name == "Saitama Phase 1":
            update_quest_progress(uid, "kill_saitama")
        if boss_name.startswith("Goku"):
            update_quest_progress(uid, "kill_goku")
        return reward
    return 0
