import random
from config import BOSSES, ABILITIES, ITEMS, ABILITY_FA, ITEM_FA
from database import add_coins, update_battle
from images import IMAGES
from quests import update_quest_progress
from jjk_data import (ABILITIES_JJK, DOMAINS_JJK, BOSSES_JJK, FODDER_JJK)


# ============================================================
# HELPER
# ============================================================

def get_boss_data(boss_name):
    if boss_name in BOSSES_JJK:
        data = BOSSES_JJK[boss_name]
        return {
            "hp": data["hp"],
            "atk": data["atk"],
            "reward": data["reward"],
            "display_name": data.get("display_name", boss_name),
        }
    if boss_name in FODDER_JJK:
        data = FODDER_JJK[boss_name]
        return {
            "hp": data["hp"],
            "atk": data["atk"],
            "reward": data["reward"],
            "display_name": data.get("display_name", boss_name),
        }
    if boss_name in BOSSES:
        data = BOSSES[boss_name]
        return {
            "hp": data["hp"],
            "atk": data["atk"],
            "reward": data.get("reward", 100),
            "display_name": boss_name,
        }
    return None


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
    r = random.random()
    if boss_hp < boss_max_hp * 0.25 and r < 0.3:
        return "heal"
    if r < 0.4:
        return "attack"
    if r < 0.7:
        return "special"
    return "defend"


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


# ============================================================
# PLAYER ACTIONS (dict-based)
# ============================================================

def player_attack(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle

    php = battle["php"]
    bhp = battle["bhp"]
    pmax = battle["pmax"]
    bmax = battle["bmax"]

    dmg, crit = roll_damage(char[6], 0, 0)

    # ATK boost از Domain
    atk_boost = battle.get("domain_atk_boost", 0)
    if atk_boost:
        dmg = int(dmg * (1 + atk_boost / 100))

    bhp = max(0, bhp - dmg)

    text = f"⚔️ حمله کردی: {dmg} آسیب"
    if crit:
        text += " 🎯 کریتیکال!"
    text += f"\n👹 HP باس: {bhp}/{bmax}"

    if bhp <= 0:
        battle["bhp"] = bhp
        return "won", text, battle

    # نوبت باس
    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n❄️ باس فریزه! حمله نمی‌کنه"
    else:
        action = boss_ai(battle["boss_name"], bhp, bmax)
        boss_text, php, bhp = boss_action(action, boss, php, pmax, bhp, bmax, defending=0)
        text += f"\n\n{boss_text}"

    battle["php"] = php
    battle["bhp"] = bhp

    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_defend(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle

    php = battle["php"]
    bhp = battle["bhp"]
    pmax = battle["pmax"]
    bmax = battle["bmax"]

    text = "🛡️ دفاع گرفتی! آسیب این راند کم می‌شه."

    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n❄️ باس فریزه!"
    else:
        action = boss_ai(battle["boss_name"], bhp, bmax)
        boss_text, php, bhp = boss_action(action, boss, php, pmax, bhp, bmax, defending=1)
        text += f"\n\n{boss_text}"

    battle["php"] = php
    battle["bhp"] = bhp

    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_dodge(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle

    php = battle["php"]
    bhp = battle["bhp"]
    pmax = battle["pmax"]
    bmax = battle["bmax"]

    dodge_chance = char[8] + battle.get("player_dodge_bonus", 0)
    success = random.randint(1, 100) <= dodge_chance

    if success:
        text = "💨 جاخالی دادی! باس ضربه‌اش بهت نخورد."
        battle["player_dodge_bonus"] = 0
        battle["php"] = php
        battle["bhp"] = bhp
        return "active", text, battle
    else:
        text = "❌ جاخالی ناموفق بود! باس زدت."
        if battle.get("boss_frozen", 0) > 0:
            battle["boss_frozen"] -= 1
            text += "\n❄️ باس فریزه!"
        else:
            action = boss_ai(battle["boss_name"], bhp, bmax)
            boss_text, php, bhp = boss_action(action, boss, php, pmax, bhp, bmax, defending=0)
            text += f"\n\n{boss_text}"

        battle["php"] = php
        battle["bhp"] = bhp

        if php <= 0:
            return "lost", text, battle
        return "active", text, battle


def player_ability(battle, char, ability_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle

    char_name = char[2]
    php = battle["php"]
    bhp = battle["bhp"]
    pmax = battle["pmax"]
    bmax = battle["bmax"]

    # ========== DOMAIN ==========
    if ability_name == "DOMAIN":
        # چک ۱ بار مصرف
        if battle.get("domain_used", 0) == 1:
            return "active", "❌ گسترش قلمرو فقط یه بار در نبرد قابل استفاده‌ست!", battle

        domain = DOMAINS_JJK.get(char_name)
        if not domain:
            return "active", "❌ این کاراکتر گسترش قلمرو نداره!", battle

        battle["domain_used"] = 1
        battle["domain_active"] = 1
        battle["domain_turns"] = domain["duration"]
        battle["domain_name"] = domain["name"]
        battle["domain_atk_boost"] = domain["effects"].get("atk_boost", 0)

        text = f"🌀 گسترش قلمرو: {domain['name']}!"
        effects = domain["effects"]

        if "hp_drain" in effects:
            drain = int(bmax * effects["hp_drain"] / 100)
            bhp = max(0, bhp - drain)
            text += f"\n💀 باس {drain} HP از دست داد"

        if "freeze" in effects:
            battle["boss_frozen"] = effects["freeze"]
            text += f"\n❄️ باس {effects['freeze']} راند فریز شد"

        if "heal" in effects:
            heal = int(pmax * effects["heal"] / 100)
            php = min(pmax, php + heal)
            text += f"\n💚 {heal} HP برگشت"

        if "atk_boost" in effects:
            text += f"\n⚔️ ATK تو +{effects['atk_boost']}٪"

        battle["php"] = php
        battle["bhp"] = bhp

        if bhp <= 0:
            return "won", text, battle

        return "active", text, battle

    # ========== چک کول‌داون ==========
    cd_key = f"cd_{ability_name}"
    if battle.get(cd_key, 0) > 0:
        return "active", f"⏱️ {ability_name} کول‌داون: {battle[cd_key]} راند", battle

    text = f"🔥 {ability_name} فعال شد!"
    new_bhp = bhp
    new_php = php

    # ========== JJK Abilities ==========
    jjk_abs = ABILITIES_JJK.get(char_name, {})
    found_jjk = False

    for key in ["ability_1", "ability_2"]:
        if key in jjk_abs and jjk_abs[key]["name"] == ability_name:
            ab = jjk_abs[key]
            ab_type = ab.get("type", "damage")
            found_jjk = True

            if ab_type == "damage":
                mult = 2
                eff = ab["effect"]
                if "x5" in eff:
                    mult = 5
                elif "x4" in eff:
                    mult = 4
                elif "x3" in eff:
                    mult = 3
                dmg = char[6] * mult
                new_bhp = max(0, bhp - dmg)
                text += f"\n⚔️ {dmg} آسیب ({mult}x)"
                if "HP" in eff and "%" in eff:
                    extra = int(bmax * 0.15)
                    new_bhp = max(0, new_bhp - extra)
                    text += f"\n💀 +{extra} آسیب مستقیم"

            elif ab_type == "dodge":
                battle["player_dodge_bonus"] = 90
                text += "\n💨 جاخالی +۹۰٪ برای ۱ راند"

            elif ab_type == "multi":
                hits = 3 if "3" in ab["effect"] else 2
                total = sum(char[6] for _ in range(hits))
                new_bhp = max(0, bhp - total)
                text += f"\n⚔️ {hits} ضربه: {total} آسیب"

            elif ab_type == "buff":
                battle["domain_atk_boost"] = 100
                text += "\n⚔️ ATK +۱۰۰ برای ۲ راند"

            elif ab_type == "gamble":
                if random.randint(1, 100) <= 50:
                    dmg = char[6] * 4
                    text += f"\n🎰 برنده! {dmg} آسیب"
                else:
                    dmg = char[6] * 1
                    text += f"\n🎰 باختی! {dmg} آسیب"
                new_bhp = max(0, bhp - dmg)

            elif ab_type == "debuff":
                battle["boss_atk_debuff"] = 25
                text += "\n🔻 ATK باس -۲۵٪ (۱ راند)"

            elif ab_type == "freeze":
                battle["boss_frozen"] = 1
                text += "\n❄️ باس ۱ راند فریز شد"

            elif ab_type == "heal":
                heal = int(pmax * 0.3)
                new_php = min(pmax, php + heal)
                text += f"\n💚 {heal} HP برگشت"

            elif ab_type == "copy":
                dmg = char[6] * 3
                new_bhp = max(0, bhp - dmg)
                text += f"\n🔴 تکنیک کپی: {dmg} آسیب"

            elif ab_type == "disable":
                battle["boss_disabled"] = 1
                text += "\n🔨 ۱ Ability باس غیرفعال شد"

            # کول‌داون
            cd = 1 if key == "ability_1" else 2
            battle[f"cd_{ability_name}"] = cd
            break

    # ========== Ability عادی ==========
    if not found_jjk:
        info = ABILITIES.get(ability_name)
        if not info:
            return "active", "❌ Ability پیدا نشد", battle
        text += f"\n{info.get('effect_fa', info.get('effect', ''))}"

    if new_bhp <= 0:
        battle["php"] = new_php
        battle["bhp"] = new_bhp
        return "won", text, battle

    # ========== حرکت باس ==========
    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n❄️ باس فریزه! حمله نمی‌کنه"
    else:
        action = boss_ai(battle["boss_name"], new_bhp, bmax)
        boss_text, new_php, new_bhp = boss_action(action, boss, new_php, pmax, new_bhp, bmax, 0)
        text += f"\n\n{boss_text}"

    battle["php"] = new_php
    battle["bhp"] = new_bhp

    if new_php <= 0:
        return "lost", text, battle

    # ========== کاهش کول‌داون ==========
    for k in list(battle.keys()):
        if k.startswith("cd_") and battle[k] > 0:
            battle[k] -= 1

    # ========== Domain Round ==========
    if battle.get("domain_active", 0) == 1:
        battle["domain_turns"] -= 1
        effects = DOMAINS_JJK.get(char_name, {}).get("effects", {})

        if "hp_drain" in effects:
            drain = int(bmax * effects["hp_drain"] / 100)
            battle["bhp"] = max(0, battle["bhp"] - drain)
            text += f"\n💀 قلمرو: باس {drain} HP از دست داد"

        if "heal_per_turn" in effects:
            heal = int(pmax * effects["heal_per_turn"] / 100)
            battle["php"] = min(pmax, battle["php"] + heal)
            text += f"\n💚 قلمرو: {heal} HP برگشت"

        if battle["domain_turns"] <= 0:
            battle["domain_active"] = 0
            battle["domain_atk_boost"] = 0
            text += "\n🌀 قلمرو بسته شد"

    return "active", text, battle


def player_item(battle, char, item_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle

    info = ITEMS.get(item_name)
    if not info:
        return "active", "❌ این آیتم رو نداری.", battle

    php = battle["php"]
    bhp = battle["bhp"]
    pmax = battle["pmax"]
    bmax = battle["bmax"]

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
        text += f" {info.get('effect_fa', info.get('effect', ''))}"

    if new_bhp <= 0:
        battle["php"] = new_php
        battle["bhp"] = new_bhp
        return "won", text, battle

    action = boss_ai(battle["boss_name"], new_bhp, bmax)
    boss_text, new_php, new_bhp = boss_action(action, boss, new_php, pmax, new_bhp, bmax, defending=0)
    text += f"\n\n{boss_text}"

    battle["php"] = new_php
    battle["bhp"] = new_bhp

    if new_php <= 0:
        return "lost", text, battle
    return "active", text, battle


def build_battle_message(battle, char):
    boss = get_boss_data(battle["boss_name"])
    boss_atk = boss["atk"] if boss else 0
    boss_display = boss["display_name"] if boss else battle["boss_name"]

    text = (
        f"👹 {boss_display}\n"
        f"❤️ HP: {battle['bhp']}/{battle['bmax']}\n"
        f"⚔️ ATK: {boss_atk}\n\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"👤 {char[2]} ({char[3]} Rank)\n"
        f"❤️ HP: {battle['php']}/{battle['pmax']}\n"
        f"⚔️ ATK: {char[6]}\n"
        f"🛡️ DEF: {char[7]}\n"
        f"💨 DODGE: {char[8]}%\n"
    )

    if battle.get("domain_active", 0) == 1:
        text += f"\n🌀 قلمرو فعال: {battle.get('domain_name', '')} ({battle.get('domain_turns', 0)} راند)\n"

    text += f"\n━━━━━━━━━━━━━━━━\n\n🎯 نوبت توئه! یه حرکت انتخاب کن:"
    return text


def finish_battle(uid, boss_name, won):
    if won:
        boss = get_boss_data(boss_name)
        reward = boss["reward"] if boss else 100
        add_coins(uid, reward)
        update_quest_progress(uid, "win_3_bosses")
        update_quest_progress(uid, "win_5_bosses")
        if boss_name == "Saitama Phase 1":
            update_quest_progress(uid, "kill_saitama")
        if boss_name.startswith("Goku"):
            update_quest_progress(uid, "kill_goku")
        return reward
    return 0
