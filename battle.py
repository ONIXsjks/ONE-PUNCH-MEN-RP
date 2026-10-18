import random
import sqlite3
from config import (DB_NAME, ABILITIES_3, DOMAINS, BANKAI, ABILITIES, BUFFS, ITEMS,
                    DOMAINS_JJK, BLEACH_BANKAI,
                    BOSSES, BOSSES_JJK, BLEACH_BOSSES, BOSSES_OPM,
                    AOT_BOSSES, BLACKCLOVER_BOSSES, BERSERK_BOSSES,
                    DEMONSLAYER_BOSSES, CHAINSAWMAN_BOSSES,
                    JJK_CE_COST_ABILITY_1, JJK_CE_COST_ABILITY_2,
                    JJK_CE_COST_ABILITY_3, JJK_CE_COST_DOMAIN, ABILITIES_JJK,
                    BLEACH_REI_COST_ABILITY_1, BLEACH_REI_COST_ABILITY_2,
                    BLEACH_REI_COST_ABILITY_3, BLEACH_REI_COST_BANKAI, ABILITIES_BLEACH,
                    GEASS_COST_ABILITY_1, GEASS_COST_ABILITY_2,
                    GEASS_COST_ABILITY_3, GEASS_COST_ULTIMATE, ABILITIES_CODEGEASS,
                    ULTIMATE_GEASS,
                    HAKI_COST_ABILITY_1, HAKI_COST_ABILITY_2, HAKI_COST_ABILITY_3, ABILITIES_ONEPIECE)

from onepiece_data import ONEPIECE_BOSSES, ONEPIECE_FODDER
from dragonball_data import DRAGONBALL_BOSSES, DRAGONBALL_FODDER, ABILITIES_DRAGONBALL
from hxh_data import HXH_BOSSES, HXH_FODDER, ABILITIES_HXH
from sakamoto_data import SAKAMOTO_BOSSES, SAKAMOTO_FODDER, ABILITIES_SAKAMOTO
from sololeveling_data import SOLOLEVELING_BOSSES, SOLOLEVELING_FODDER, ABILITIES_SOLOLEVELING
from mushoku_data import MUSHOKU_BOSSES, MUSHOKU_FODDER, ABILITIES_MUSHOKU
from codegeass_data import CODEGEASS_BOSSES, CODEGEASS_FODDER
from tokyoghoul_data import TOKYOGHOUL_BOSSES, TOKYOGHOUL_FODDER, ABILITIES_TOKYOGHOUL
from jjk_data import FODDER_JJK
from bleach_data import BLEACH_FODDER
from aot_data import AOT_FODDER, ABILITIES_AOT
from blackclover_data import BLACKCLOVER_FODDER, ABILITIES_BLACKCLOVER
from berserk_data import BERSERK_FODDER, ABILITIES_BERSERK
from demonslayer_data import DEMONSLAYER_FODDER, ABILITIES_DEMONSLAYER
from chainsawman_data import CHAINSAWMAN_FODDER, ABILITIES_CHAINSAWMAN
from naruto_data import ABILITIES_NARUTO
from sevendeadlysins_data import ABILITIES_SDS
from opm_data import ABILITIES_OPM

from database import (add_coins, get_battle, update_battle, end_battle,
                      get_coins, get_shadows_atk_bonus)

AWAKEN_NAMES = {
    "Gojo Satoru": {"blue": "Blue", "red": "Black Flash", "purple": "Hollow Purple (200%)"},
    "Sukuna": {"blue": "Dismantle", "red": "Cleave", "purple": "Malevolent Shrine"},
    "Yuji Itadori": {"blue": "Divergent Fist", "red": "Black Flash", "purple": "Sukuna's Vessel"},
    "Megumi Fushiguro": {"blue": "Divine Dogs", "red": "Mahoraga", "purple": "Chimera Shadow Garden"},
    "Mahito": {"blue": "Idle Transfiguration", "red": "Soul Multiplicity", "purple": "Self-Embodiment of Perfection"},
    "Ichigo Kurosaki": {"blue": "Getsuga Tensho", "red": "Mugetsu", "purple": "True Bankai"},
    "Sosuke Aizen": {"blue": "Kyoka Suigetsu", "red": "Hogyoku Fusion", "purple": "Final Getsuga Tensho"},
    "Byakuya Kuchiki": {"blue": "Senbonzakura", "red": "Senbonzakura Kageyoshi", "purple": "Ikka Senjinka"},
    "Monkey D. Luffy": {"blue": "Gum-Gum Red Roc", "red": "Gum-Gum Bajrang Gun", "purple": "Sun God Nika (200%)"},
    "Roronoa Zoro": {"blue": "Three-Sword Style", "red": "King of Hell", "purple": "Asura"},
    "Naruto Uzumaki": {"blue": "Rasengan", "red": "Rasen-Shuriken", "purple": "Baryon Mode"},
    "Sasuke Uchiha": {"blue": "Chidori", "red": "Amaterasu", "purple": "Indra's Arrow"},
    "Son Goku": {"blue": "Kamehameha", "red": "Spirit Bomb", "purple": "Ultra Instinct"},
    "Vegeta": {"blue": "Final Flash", "red": "Big Bang Attack", "purple": "Ultra Ego"},
    "Sung Jin-Woo": {"blue": "Shadow Exchange", "red": "Ruler's Authority", "purple": "Shadow Monarch (200%)"},
    "Eren Yeager": {"blue": "Attack Titan", "red": "Founding Titan", "purple": "Rumbling"},
    "Levi Ackerman": {"blue": "Spinning Slash", "red": "Thunder Spear", "purple": "Humanity's Strongest"},
    "Asta": {"blue": "Black Hurricane", "red": "Black Slash", "purple": "Devil Union"},
    "Tanjiro Kamado": {"blue": "Water Breathing", "red": "Hinokami Kagura", "purple": "Sun Breathing 13th Form"},
    "Lelouch Lamperouge": {"blue": "Absolute Command", "red": "Geass of the King", "purple": "Ragnarok Connection"},
}

def get_awaken_name(char_name, color):
    names = AWAKEN_NAMES.get(char_name)
    if names:
        return names.get(color, f"Awaken {color.capitalize()}")
    return f"Awaken {color.capitalize()}"

def get_reward_by_wave(wave):
    if wave <= 10: return 20000
    elif wave <= 20: return 40000
    elif wave <= 30: return 60000
    elif wave <= 40: return 80000
    elif wave <= 50: return 90000
    elif wave <= 60: return 110000
    elif wave <= 70: return 250000
    elif wave <= 80: return 350000
    elif wave <= 90: return 500000
    else: return 1000000

def get_boss_data(boss_name):
    if "Survival" in boss_name:
        return {"display_name": boss_name, "atk": 150, "hp": 10000, "reward": 1000}
    all_boss_lists = [BOSSES_JJK, BLEACH_BOSSES, BOSSES_OPM, BOSSES, AOT_BOSSES, BLACKCLOVER_BOSSES, BERSERK_BOSSES, DEMONSLAYER_BOSSES, CHAINSAWMAN_BOSSES, ONEPIECE_BOSSES, DRAGONBALL_BOSSES, HXH_BOSSES, SAKAMOTO_BOSSES, SOLOLEVELING_BOSSES, MUSHOKU_BOSSES, CODEGEASS_BOSSES, TOKYOGHOUL_BOSSES]
    all_fodder_lists = [FODDER_JJK, BLEACH_FODDER, AOT_FODDER, BLACKCLOVER_FODDER, BERSERK_FODDER, DEMONSLAYER_FODDER, CHAINSAWMAN_FODDER, ONEPIECE_FODDER, DRAGONBALL_FODDER, HXH_FODDER, SAKAMOTO_FODDER, SOLOLEVELING_FODDER, MUSHOKU_FODDER, CODEGEASS_FODDER, TOKYOGHOUL_FODDER]
    for bosses in all_boss_lists:
        if boss_name in bosses:
            boss = bosses[boss_name].copy()
            if boss.get("atk", 0) <= 0: boss["atk"] = 250
            if boss.get("hp", 0) <= 0: boss["hp"] = 5000
            if "display_name" not in boss: boss["display_name"] = boss_name
            return boss
    for fodder in all_fodder_lists:
        if boss_name in fodder:
            boss = fodder[boss_name].copy()
            if boss.get("atk", 0) <= 0: boss["atk"] = 150
            if boss.get("hp", 0) <= 0: boss["hp"] = 1000
            if "display_name" not in boss: boss["display_name"] = boss_name
            return boss
    return None

def format_num(n):
    try: return f"{int(n):,}"
    except Exception: return str(n)

def hp_bar(current, maximum, length=10):
    if maximum <= 0: return "💔 [" + "░" * length + "] ۰/۰"
    pct = current / maximum
    filled = int(pct * length)
    filled = max(0, min(length, filled))
    empty = length - filled
    bar = "█" * filled + "░" * empty
    if pct > 0.6: icon = "❤️"
    elif pct > 0.3: icon = "🧡"
    else: icon = "💔"
    return f"{icon} [{bar}] {format_num(current)}/{format_num(maximum)}"

def box_title(text, width=26):
    pad = width - len(text)
    if pad < 0: text = text[:width]; pad = 0
    left = pad // 2; right = pad - left
    return f"╔{'═' * width}╗\n║{' ' * left}{text}{' ' * right}║\n╚{'═' * width}╝"

def box_simple(text, width=24):
    if len(text) > width - 2: text = text[:width - 2]
    return f"┌{'─' * width}┐\n│ {text.center(width - 2)} │\n└{'─' * width}┘"

def roll_damage(atk, defender_def=0, defender_defending=0):
    base = atk * random.uniform(0.85, 1.15)
    crit = random.random() < 0.15
    if crit: base *= 2
    if defender_defending: base -= defender_def * 2
    else: base -= defender_def * 0.5
    return max(1, int(base)), crit
def boss_ai(boss_name, boss_hp, boss_max_hp):
    r = random.random()
    jjk_bosses = ["Sukuna", "Mahito", "Jogo", "Toji Fushiguro", "Kenjaku", "Gojo Satoru", "Satoru Gojo"]
    bleach_bosses = list(BLEACH_BOSSES.keys())
    if boss_name in jjk_bosses:
        if boss_hp < boss_max_hp * 0.2 and r < 0.3: return "heal"
        if r < 0.25: return "attack"
        if r < 0.85: return "special"
        return "defend"
    elif boss_name in bleach_bosses:
        if boss_hp < boss_max_hp * 0.2 and r < 0.3: return "heal"
        if r < 0.3: return "attack"
        if r < 0.8: return "special"
        return "defend"
    if boss_hp < boss_max_hp * 0.25 and r < 0.3: return "heal"
    if r < 0.4: return "attack"
    if r < 0.7: return "special"
    return "defend"

def apply_defense_check(base_dmg, php, defense_type, char_dodge=0):
    if defense_type == "دفاع":
        roll = random.randint(1, 3)
        if roll == 1: return php, f"✅ دفاع کامل! (۰ آسیب)"
        elif roll == 2:
            partial = max(1, int(base_dmg * 0.5)); php = max(0, php - partial)
            return php, f"⚠️ دفاع جزئی! ({format_num(partial)} آسیب - ۵۰٪)"
        else:
            php = max(0, php - base_dmg)
            return php, f"❌ دفاع ناموفق! ({format_num(base_dmg)} آسیب کامل)"
    elif defense_type == "جاخالی":
        roll = random.randint(1, 100)
        if roll <= 30: return php, f"✅ جاخالی کامل! (۰ آسیب)"
        else:
            php = max(0, php - base_dmg)
            return php, f"❌ جاخالی ناموفق! ({format_num(base_dmg)} آسیب کامل)"
    else:
        roll = random.randint(1, 100)
        if roll <= 33: return php, f"✅ {defense_type} کامل! ۰ آسیب"
        elif roll <= 66:
            partial = max(1, int(base_dmg * 0.5)); php = max(0, php - partial)
            return php, f"⚠️ {defense_type} جزئی! {format_num(partial)} آسیب (۵۰٪)"
        else:
            php = max(0, php - base_dmg)
            return php, f"❌ {defense_type} ناموفق! {format_num(base_dmg)} آسیب کامل"

def boss_attack_player(boss, php, pmax, battle, defense_flag=None, char_dodge=0):
    base_dmg, crit = roll_damage(boss["atk"], 0, 0)
    text = box_simple("👹 باس حمله کرد!")
    if crit and not defense_flag: text += f"\n\n⚡ CRITICAL HIT! ⚡"
    text += f"\n\n💢 آسیب پایه: {format_num(base_dmg)}"
    if defense_flag == "defend":
        php, def_log = apply_defense_check(base_dmg, php, "دفاع")
        text += f"\n{def_log}"
    elif defense_flag == "dodge":
        php, def_log = apply_defense_check(base_dmg, php, "جاخالی")
        text += f"\n{def_log}"
    else: php = max(0, php - base_dmg)
    text += f"\n\n👤 {hp_bar(php, pmax)}"
    return php, text, base_dmg

def apply_bankai_round(battle):
    if battle.get("bankai_used", 0) < 1: return battle
    bankai = battle.get("bankai_data", {})
    if not bankai: return battle
    if "atk_per_round" in bankai:
        cur = battle.get("bankai_atk_current", 0); max_a = bankai.get("max_atk", 30)
        if cur < max_a: battle["bankai_atk_current"] = min(max_a, cur + bankai["atk_per_round"])
    if "dodge_per_round" in bankai:
        cur = battle.get("bankai_dodge_current", 0); max_d = bankai.get("max_dodge", 15)
        if cur < max_d: battle["bankai_dodge_current"] = min(max_d, cur + bankai["dodge_per_round"])
    if "heal_per_round" in bankai:
        cur = battle.get("bankai_heal_current", 0); max_h = bankai.get("max_heal", 15)
        if cur < max_h: battle["bankai_heal_current"] = min(max_h, cur + bankai["heal_per_round"])
    if "bleed_per_round" in bankai:
        cur = battle.get("bankai_bleed_current", 0); max_b = bankai.get("max_bleed", 5)
        if cur < max_b: battle["bankai_bleed_current"] = min(max_b, cur + bankai["bleed_per_round"])
    if "enemy_atk_debuff" in bankai:
        cur = battle.get("bankai_enemy_debuff_current", 0); max_e = bankai.get("max_enemy_debuff", 15)
        if cur < max_e: battle["bankai_enemy_debuff_current"] = min(max_e, cur + bankai["enemy_atk_debuff"])
    if "self_dmg_per_round" in bankai:
        cur = battle.get("bankai_self_dmg_current", 0); max_s = bankai.get("max_self_dmg", 5)
        if cur < max_s: battle["bankai_self_dmg_current"] = min(max_s, cur + bankai["self_dmg_per_round"])
    return battle

def apply_bankai_effects(battle, php, pmax, bhp, bmax):
    if battle.get("bankai_used", 0) < 1: return php, bhp, ""
    text = ""
    heal_pct = battle.get("bankai_heal_current", 0)
    if heal_pct > 0:
        heal = int(pmax * heal_pct / 100); php = min(pmax, php + heal)
        text += f"\n💚 بانکای: +{format_num(heal)} HP"
    bleed_pct = battle.get("bankai_bleed_current", 0)
    if bleed_pct > 0:
        bleed = int(bmax * bleed_pct / 100); bhp = max(0, bhp - bleed)
        text += f"\n🩸 بانکای: باس -{format_num(bleed)} HP"
    self_pct = battle.get("bankai_self_dmg_current", 0)
    if self_pct > 0:
        dmg = int(pmax * self_pct / 100); php = max(0, php - dmg)
        text += f"\n🩸 بانکای: خودت -{format_num(dmg)} HP"
    return php, bhp, text

def apply_domain_round(battle):
    if battle.get("domain_active", 0) == 1:
        battle["domain_turns"] -= 1
        if battle["domain_turns"] <= 0:
            battle["domain_active"] = 0; battle["domain_atk_boost"] = 0
            battle["domain_turns"] = 0; battle["domain_name"] = ""
    return battle

def boss_turn(battle, boss, php, pmax, bhp, bmax, text, defense_flag=None):
    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n\n❄️ باس فریزه! (نوبت از دست داد)"
        return php, bhp, text
    boss_energy = battle.get("boss_energy", 5000)
    if boss_energy < 500: boss_energy = 5000
    battle["boss_energy"] = boss_energy
    action = boss_ai(battle["boss_name"], bhp, bmax)
    if action == "attack":
        php, boss_text, _ = boss_attack_player(boss, php, pmax, battle, defense_flag)
        text += f"\n\n{boss_text}"
    elif action == "special":
        boss_name = battle["boss_name"]
        is_jjk = boss_name in BOSSES_JJK or boss_name in FODDER_JJK
        is_bleach = boss_name in BLEACH_BOSSES or boss_name in BLEACH_FODDER
        is_geass = boss_name in CODEGEASS_BOSSES or boss_name in CODEGEASS_FODDER
        special_name = "Awaken"
        if is_jjk: special_name = "Domain Expansion"
        elif is_bleach: special_name = "Bankai"
        elif is_geass: special_name = "Geass"
        if bmax <= 1000: mult = 2; energy_cost = 200
        elif bmax <= 10000: mult = 3; energy_cost = 300
        elif bmax <= 30000: mult = 4; energy_cost = 400
        else: mult = 6; energy_cost = 550
        battle["boss_energy"] = max(0, boss_energy - energy_cost)
        base_dmg, _ = roll_damage(boss["atk"] * mult, 0, 0)
        if defense_flag:
            php, def_log = apply_defense_check(base_dmg, php, defense_flag.capitalize())
            text += f"\n\n{box_simple(f'💥 {special_name} باس!')}"
            text += f"\n\n💢 آسیب پایه: {format_num(base_dmg)}"
            text += f"\n{def_log}"
            text += f"\n⚡ انرژی باس: {energy_cost}-"
            text += f"\n\n👤 {hp_bar(php, pmax)}"
        else:
            php = max(0, php - base_dmg)
            text += f"\n\n{box_simple(f'💥 {special_name} باس!')}"
            text += f"\n\n💢 {format_num(base_dmg)} آسیب!"
            text += f"\n⚡ انرژی باس: {energy_cost}-"
            text += f"\n\n👤 {hp_bar(php, pmax)}"
    elif action == "defend":
        text += f"\n\n🛡️ باس دفاع گرفت."
        battle["boss_defending"] = 1
    elif action == "heal":
        heal = int(bmax * 0.1); bhp = min(bmax, bhp + heal)
        text += f"\n\n💚 باس درمان: +{format_num(heal)}"
        text += f"\n👹 {hp_bar(bhp, bmax)}"
    return php, bhp, text
def player_attack(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss: return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]; pmax = battle["pmax"]; bmax = battle["bmax"]
    mult = 1.5
    if char[2] in DOMAINS_JJK or char[2] in ABILITIES_JJK: mult = 1.2
    elif char[2] == "Sung Jin-Woo": mult = 1.5
    char_level = char[4]; attack_power = char[6]
    if char_level >= 300: attack_power = min(attack_power, 20000)
    base_dmg, crit = roll_damage(attack_power * mult, 0, 0)
    if char[2] == "Sung Jin-Woo":
        shadow_bonus = get_shadows_atk_bonus(battle["uid"], char[2])
        base_dmg += shadow_bonus
    atk_boost = battle.get("domain_atk_boost", 0)
    if atk_boost: base_dmg = int(base_dmg * (1 + atk_boost / 100))
    bankai_atk = battle.get("bankai_atk_current", 0)
    if bankai_atk: base_dmg = int(base_dmg * (1 + bankai_atk / 100))
    boss_defended_last_turn = battle.get("boss_defending", 0) == 1
    if boss_defended_last_turn: battle["boss_defending"] = 0
    boss_reaction_roll = random.randint(1, 100)
    final_dmg = base_dmg; boss_reaction_text = ""
    if boss_reaction_roll <= 30:
        final_dmg = 0; boss_reaction_text = "\n\n💨 **باس جاخالی داد!** (۰ آسیب)"
    elif boss_reaction_roll <= 60:
        final_dmg = int(base_dmg * 0.5); boss_reaction_text = f"\n\n🛡️ **باس دفاع کرد!** (نصف دمیج: {format_num(final_dmg)})"
    else:
        if boss_defended_last_turn:
            final_dmg = int(base_dmg * 0.5); boss_reaction_text = f"\n\n🛡️ **باس در نوبت قبل دفاع کرده بود!** (نصف دمیج: {format_num(final_dmg)})"
        else:
            final_dmg = base_dmg; boss_reaction_text = "\n\n❌ **دفاع باس ناموفق بود!** (آسیب کامل)"
    bhp = max(0, bhp - final_dmg)
    if crit: text = box_simple("⚡ CRITICAL HIT! ⚡")
    else: text = box_simple("⚔️ حمله!")
    text += f"\n\n💥 آسیب پایه تو: {format_num(base_dmg)}"
    text += boss_reaction_text
    text += f"\n\n👹 {boss['display_name']}"
    text += f"\n{hp_bar(bhp, bmax)}"
    if bhp <= 0:
        battle["php"] = php; battle["bhp"] = bhp
        return "won", text, battle
    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)
    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt: text += f"\n{bt}"
    battle = apply_domain_round(battle)
    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0: return "won", text, battle
    if php <= 0: return "lost", text, battle
    return "active", text, battle

def player_defend(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss: return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]; pmax = battle["pmax"]; bmax = battle["bmax"]
    text = box_simple("🛡️ دفاع گرفتی!")
    text += "\n\n🎲 ۳۳٪ کامل / ۳۳٪ جزئی / ۳۳٪ ناموفق"
    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text, "defend")
    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt: text += f"\n{bt}"
    battle = apply_domain_round(battle)
    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0: return "won", text, battle
    if php <= 0: return "lost", text, battle
    return "active", text, battle

def player_dodge(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss: return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]; pmax = battle["pmax"]; bmax = battle["bmax"]
    text = box_simple("💨 جاخالی می‌زنی!")
    text += "\n\n🎲 ۷۰٪ آسیب کامل / ۳۰٪ جاخالی کامل"
    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text, "dodge")
    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt: text += f"\n{bt}"
    battle = apply_domain_round(battle)
    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0: return "won", text, battle
    if php <= 0: return "lost", text, battle
    return "active", text, battle
def goku_transform(battle, char):
    current_form = battle.get("goku_form", 0)
    if current_form >= 4: return "active", "🔥 گوکو به حداکثر قدرت رسیده! (Ultra Instinct)", battle
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT dragonball_ki FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
    row = c.fetchone(); energy = row[0] if row else 0
    if energy < 30:
        conn.close(); return "active", "❌ انرژی کی کافی نداری! (نیاز: ۳۰)", battle
    c.execute("UPDATE characters SET dragonball_ki = dragonball_ki - 30 WHERE user_id=? AND is_active=1", (battle["uid"],))
    conn.commit(); conn.close()
    new_form = current_form + 1
    if new_form == 1: atk_boost, dodge_boost, form_name = 10, 5, "Super Saiyan 2"
    elif new_form == 2: atk_boost, dodge_boost, form_name = 20, 10, "Super Saiyan 3"
    elif new_form == 3: atk_boost, dodge_boost, form_name = 35, 15, "Super Saiyan God"
    else: atk_boost, dodge_boost, form_name = 50, 25, "Super Saiyan Blue"
    battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + atk_boost; battle["goku_form"] = new_form
    text = f"⚡ **گوکو به فرم {form_name} رفت!**\n\n⚔️ ATK: +{atk_boost}٪\n💨 DODGE: +{dodge_boost}٪\n⚡ انرژی مصرفی: ۳۰"
    return "active", text, battle

def luffy_transform(battle, char):
    current_form = battle.get("luffy_form", 0)
    if current_form >= 4: return "active", "🔥 لوفی در فرم **Gear 5 (Sun God Nika)** است و به حداکثر قدرت رسیده!", battle
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT haki FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
    row = c.fetchone(); energy = row[0] if row else 0
    if energy < 30:
        conn.close(); return "active", "❌ انرژی هاکی کافی نداری! (نیاز: ۳۰)", battle
    c.execute("UPDATE characters SET haki = haki - 30 WHERE user_id=? AND is_active=1", (battle["uid"],))
    conn.commit(); conn.close()
    new_form = current_form + 1
    if new_form == 1: atk_boost, dodge_boost, form_name = 15, 10, "Gear 2"
    elif new_form == 2: atk_boost, dodge_boost, form_name = 25, 15, "Gear 3"
    elif new_form == 3: atk_boost, dodge_boost, form_name = 40, 20, "Gear 4 (Bounceman)"
    else: atk_boost, dodge_boost, form_name = 60, 30, "Gear 5 (Sun God Nika)"
    battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + atk_boost; battle["luffy_form"] = new_form
    text = f"⚡ **لوفی به فرم {form_name} رفت!**\n\n⚔️ ATK: +{atk_boost}٪\n💨 DODGE: +{dodge_boost}٪\n⚡ انرژی مصرفی: ۳۰"
    return "active", text, battle

def player_ability(battle, char, ability_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss: return "active", "❌ باس پیدا نشد.", battle
    char_name = char[2]; php = battle["php"]; bhp = battle["bhp"]; pmax = battle["pmax"]; bmax = battle["bmax"]
    abilities = ABILITIES_3.get(char_name, {}); extra_text = ""
    if ability_name == "DOMAIN":
        if battle.get("domain_used", 0) >= 1: return "active", "❌ Domain فقط ۱ بار در نبرد!", battle
    if ability_name == "BANKAI":
        if battle.get("bankai_used", 0) >= 1: return "active", "❌ Bankai فقط ۱ بار در نبرد!", battle
    if ability_name == "ULTIMATE_GEASS":
        if battle.get("geass_used", 0) >= 1: return "active", "❌ گیاس دوم فقط ۱ بار در نبرد!", battle
    found_key = None
    for key in ["ability_1", "ability_2", "ability_3"]:
        if key in abilities and abilities[key]["name"] == ability_name:
            found_key = key; break
    if found_key == "ability_3":
        if battle.get("spam_state") == "purple_used": return "active", f"🟣 {ability_name} فقط ۱ بار در کل نبرد!", battle

    energy_types = []
    if char_name in DOMAINS_JJK or char_name in ABILITIES_JJK or char_name in ABILITIES_NARUTO: energy_types.append("jjk")
    if char_name in BLEACH_BANKAI or char_name in ABILITIES_BLEACH: energy_types.append("bleach")
    if char_name in ABILITIES_CODEGEASS: energy_types.append("geass")
    if char_name in ABILITIES_ONEPIECE: energy_types.append("op")
    if char_name in ABILITIES_DRAGONBALL: energy_types.append("db")
    if char_name in ABILITIES_HXH: energy_types.append("hxh")
    if char_name in ABILITIES_SAKAMOTO: energy_types.append("sakamoto")
    if char_name in ABILITIES_SOLOLEVELING: energy_types.append("solo")
    if char_name in ABILITIES_MUSHOKU: energy_types.append("mushoku")
    if char_name in ABILITIES_TOKYOGHOUL: energy_types.append("tg")
    if char_name in ABILITIES_SDS: energy_types.append("sds")
    if char_name in ABILITIES_AOT: energy_types.append("aot")
    if char_name in ABILITIES_BLACKCLOVER: energy_types.append("bc")
    if char_name in ABILITIES_BERSERK: energy_types.append("berserk")
    if char_name in ABILITIES_DEMONSLAYER: energy_types.append("ds")
    if char_name in ABILITIES_CHAINSAWMAN: energy_types.append("csm")
    if char_name in ABILITIES_OPM: energy_types.append("opm")

    if energy_types:
        conn = sqlite3.connect(DB_NAME); c = conn.cursor()
        if "jjk" in energy_types:
            c.execute("SELECT cursed_energy, max_cursed_energy FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0
            if ability_name == "DOMAIN": cost = JJK_CE_COST_DOMAIN
            elif found_key == "ability_1": cost = JJK_CE_COST_ABILITY_1
            elif found_key == "ability_2": cost = JJK_CE_COST_ABILITY_2
            elif found_key == "ability_3": cost = JJK_CE_COST_ABILITY_3
            energy_col = "cursed_energy"
        elif "bleach" in energy_types:
            c.execute("SELECT reiatsu, max_reiatsu FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0
            if ability_name == "BANKAI": cost = BLEACH_REI_COST_BANKAI
            elif found_key == "ability_1": cost = BLEACH_REI_COST_ABILITY_1
            elif found_key == "ability_2": cost = BLEACH_REI_COST_ABILITY_2
            elif found_key == "ability_3": cost = BLEACH_REI_COST_ABILITY_3
            energy_col = "reiatsu"
        elif "geass" in energy_types:
            c.execute("SELECT geass_power, max_geass_power FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0
            if ability_name == "ULTIMATE_GEASS": cost = GEASS_COST_ULTIMATE
            elif found_key == "ability_1": cost = GEASS_COST_ABILITY_1
            elif found_key == "ability_2": cost = GEASS_COST_ABILITY_2
            elif found_key == "ability_3": cost = GEASS_COST_ABILITY_3
            energy_col = "geass_power"
        elif "op" in energy_types:
            c.execute("SELECT haki, max_haki FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0
            if found_key == "ability_1": cost = HAKI_COST_ABILITY_1
            elif found_key == "ability_2": cost = HAKI_COST_ABILITY_2
            elif found_key == "ability_3": cost = HAKI_COST_ABILITY_3
            energy_col = "haki"
        elif "db" in energy_types:
            c.execute("SELECT dragonball_ki, max_dragonball_ki FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "dragonball_ki"
        elif "hxh" in energy_types:
            c.execute("SELECT hxh_nen, max_hxh_nen FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "hxh_nen"
        elif "sakamoto" in energy_types:
            c.execute("SELECT sakamoto_stamina, max_sakamoto_stamina FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "sakamoto_stamina"
        elif "solo" in energy_types:
            c.execute("SELECT sololeveling_mana, max_sololeveling_mana FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "sololeveling_mana"
        elif "mushoku" in energy_types:
            c.execute("SELECT mushoku_mana, max_mushoku_mana FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "mushoku_mana"
        elif "tg" in energy_types:
            c.execute("SELECT tokyoghoul_rc, max_tokyoghoul_rc FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "tokyoghoul_rc"
        elif "sds" in energy_types:
            c.execute("SELECT sds_magic, max_sds_magic FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "sds_magic"
        elif "aot" in energy_types:
            c.execute("SELECT aot_titan, max_aot_titan FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "aot_titan"
        elif "bc" in energy_types:
            c.execute("SELECT blackclover_mana, max_blackclover_mana FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "blackclover_mana"
        elif "berserk" in energy_types:
            c.execute("SELECT berserk_bloodlust, max_berserk_bloodlust FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "berserk_bloodlust"
        elif "ds" in energy_types:
            c.execute("SELECT demonslayer_breath, max_demonslayer_breath FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "demonslayer_breath"
        elif "csm" in energy_types:
            c.execute("SELECT chainsawman_blood, max_chainsawman_blood FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "chainsawman_blood"
        elif "opm" in energy_types:
            c.execute("SELECT opm_power, max_opm_power FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "opm_power"
        else:
            c.execute("SELECT cursed_energy, max_cursed_energy FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],)); row = c.fetchone(); energy = row[0] if row else 0; cost = 20; energy_col = "cursed_energy"

        char_level = char[4]; level_penalty = (char_level // 10) * 2; cost += level_penalty
        if energy < cost:
            hp_cost = (cost - energy) * 10
            if php <= hp_cost:
                conn.close()
                return "active", f"❌ نه انرژی داری نه HP کافی! (نیاز: {hp_cost} HP)", battle
            php -= hp_cost
            c.execute(f"UPDATE characters SET {energy_col} = 0 WHERE user_id=? AND is_active=1", (battle["uid"],))
            conn.commit()
            conn.close()
            extra_text = f"🩸 **از HP خودت انرژی ساختی! (-{format_num(hp_cost)} HP)**\n\n"
        else:
            c.execute(f"UPDATE characters SET {energy_col} = {energy_col} - ? WHERE user_id=? AND is_active=1", (cost, battle["uid"]))
            conn.commit()
            conn.close()
            extra_text = ""
        battle["php"] = php
    if ability_name == "DOMAIN":
        domain = DOMAINS.get(char_name) or DOMAINS_JJK.get(char_name)
        if not domain:
            return "active", "❌ این کاراکتر Domain نداره!", battle
        battle["domain_used"] = 1
        battle["domain_active"] = 1
        battle["domain_turns"] = domain.get("duration", 2)
        battle["domain_name"] = domain["name"]
        effects = domain.get("effects", {})
        battle["domain_atk_boost"] = effects.get("atk_boost", 0)
        dmg = int(char[6] * 2.5); bhp = max(0, bhp - dmg)
        text = extra_text + box_title(f"🌀 {domain['name'][:20]}", 26)
        text += f"\n\n💥 {format_num(dmg)} آسیب (×۲.۵)"
        if "freeze" in effects:
            battle["boss_frozen"] = effects["freeze"]
            text += f"\n❄️ باس فریز شد! ({effects['freeze']} نوبت)"
        if "atk_boost" in effects:
            text += f"\n⚔️ ATK +{effects['atk_boost']}٪"
        if "heal" in effects:
            heal = int(pmax * effects["heal"] / 100); php = min(pmax, php + heal)
            text += f"\n💚 +{format_num(heal)} HP"
        text += f"\n\n👹 {boss['display_name']}"; text += f"\n{hp_bar(bhp, bmax)}"
        if bhp <= 0:
            battle["php"] = php
            battle["bhp"] = bhp
            return "won", text, battle
        php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)
        battle = apply_bankai_round(battle)
        php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
        if bt: text += f"\n{bt}"
        battle = apply_domain_round(battle)
        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0: return "won", text, battle
        if php <= 0: return "lost", text, battle
        return "active", text, battle

    if ability_name == "BANKAI":
        bankai = BANKAI.get(char_name) or BLEACH_BANKAI.get(char_name)
        if not bankai: return "active", "❌ این کاراکتر Bankai نداره!", battle
        battle["bankai_used"] = 1; battle["bankai_data"] = bankai; battle["bankai_atk_current"] = 0; battle["bankai_dodge_current"] = 0
        battle["bankai_heal_current"] = 0; battle["bankai_bleed_current"] = 0; battle["bankai_enemy_debuff_current"] = 0; battle["bankai_self_dmg_current"] = 0
        dmg = int(char[6] * 6); bhp = max(0, bhp - dmg)
        text = extra_text + box_title(f"⚔️ {bankai['name'][:20]}", 26); text += f"\n\n💥 {format_num(dmg)} آسیب (×۶)"
        text += f"\n\n👹 {boss['display_name']}"; text += f"\n{hp_bar(bhp, bmax)}"
        if bhp <= 0: battle["php"] = php; battle["bhp"] = bhp; return "won", text, battle
        php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)
        battle = apply_bankai_round(battle); php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
        if bt: text += f"\n{bt}"
        battle = apply_domain_round(battle)
        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0: return "won", text, battle
        if php <= 0: return "lost", text, battle
        return "active", text, battle

    if ability_name == "ULTIMATE_GEASS":
        if char_name not in ABILITIES_CODEGEASS: return "active", "❌ این کاراکتر گیاس دوم نداره!", battle
        geass = ULTIMATE_GEASS.get(char_name)
        if not geass: return "active", "❌ گیاس دوم تعریف نشده!", battle
        battle["geass_used"] = 1; effect = geass.get("effect", "")
        dmg = int(char[6] * 4); bhp = max(0, bhp - dmg)
        text = extra_text + box_title(f"👁️ {geass['name'][:20]}", 26); text += f"\n\n💥 {format_num(dmg)} آسیب (×۴)"
        if effect == "skip_enemy_turn":
            battle["boss_frozen"] = geass.get("duration", 2); text += f"\n❄️ باس {geass.get('duration', 2)} نوبت محروم شد!"
        elif effect == "atk_boost":
            battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + geass.get("value", 100); text += f"\n⚔️ ATK +{geass.get('value', 100)}٪"
        elif effect == "def_boost": text += f"\n🛡️ DEF +{geass.get('value', 100)}٪"
        elif effect == "dodge_boost": text += f"\n💨 DODGE +{geass.get('value', 50)}٪"
        elif effect == "heal":
            heal = int(pmax * geass.get("value", 50) / 100); php = min(pmax, php + heal); text += f"\n💚 +{format_num(heal)} HP"
        text += f"\n\n👹 {boss['display_name']}"; text += f"\n{hp_bar(bhp, bmax)}"
        if bhp <= 0: battle["php"] = php; battle["bhp"] = bhp; return "won", text, battle
        php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)
        battle = apply_bankai_round(battle); php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
        if bt: text += f"\n{bt}"
        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0: return "won", text, battle
        if php <= 0: return "lost", text, battle
        return "active", text, battle

    if not abilities: return "active", "❌ Ability پیدا نشد.", battle
    found_ab = None
    for key in ["ability_1", "ability_2", "ability_3"]:
        if key in abilities and abilities[key]["name"] == ability_name: found_ab = abilities[key]; break
    if not found_ab: return "active", "❌ Ability پیدا نشد.", battle
    mult = found_ab.get("mult", 3); dmg = int(char[6] * mult)
    if char_name == "Sung Jin-Woo":
        shadow_bonus = get_shadows_atk_bonus(battle["uid"], char_name); dmg += shadow_bonus
    bhp = max(0, bhp - dmg)
    if found_key == "ability_3":
        text = extra_text + box_title(f"🟣 {ability_name[:20]}!", 26); battle["spam_state"] = "purple_used"
    elif found_key == "ability_1": text = extra_text + box_simple(f"🔵 {ability_name[:18]}!")
    else: text = extra_text + box_simple(f"🔴 {ability_name[:18]}!")
    text += f"\n\n💥 {format_num(dmg)} آسیب ({mult}x)"; text += f"\n\n👹 {boss['display_name']}"; text += f"\n{hp_bar(bhp, bmax)}"
    if bhp <= 0: battle["php"] = php; battle["bhp"] = bhp; return "won", text, battle
    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)
    battle = apply_bankai_round(battle); php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt: text += f"\n{bt}"
    battle = apply_domain_round(battle)
    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0: return "won", text, battle
    if php <= 0: return "lost", text, battle
    return "active", text, battle

def player_ability_v2(battle, char, action):
    char_name = char[2]
    if action == "domain": return player_ability(battle, char, "DOMAIN")
    if action == "bankai": return player_ability(battle, char, "BANKAI")
    if action == "ultimate_geass": return player_ability(battle, char, "ULTIMATE_GEASS")
    abilities = ABILITIES_3.get(char_name, {})
    if action in abilities:
        ab_name = abilities[action]["name"]; return player_ability(battle, char, ab_name)
    return "active", "❌ Ability نامعتبر.", battle

def player_awaken_ability(battle, char, color):
    boss = get_boss_data(battle["boss_name"])
    if not boss: return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]; pmax = battle["pmax"]; bmax = battle["bmax"]
    if color == "blue":
        if battle.get("awaken_blue_used", 0) == 1: return "active", "❌ قبلاً استفاده کردی!", battle
        mult, cost = 5, 30; battle["awaken_blue_used"] = 1
    elif color == "red":
        if battle.get("awaken_red_used", 0) == 1: return "active", "❌ قبلاً استفاده کردی!", battle
        mult, cost = 5, 35; battle["awaken_red_used"] = 1
    else:
        if battle.get("awaken_purple_used", 0) == 1: return "active", "❌ قبلاً استفاده کردی!", battle
        mult, cost = 6, 40; battle["awaken_purple_used"] = 1
    ability_name = get_awaken_name(char[2], color)
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    energy_col = "cursed_energy"
    if char[2] in BLEACH_BANKAI or char[2] in ABILITIES_BLEACH: energy_col = "reiatsu"
    elif char[2] in ABILITIES_CODEGEASS: energy_col = "geass_power"
    elif char[2] in ABILITIES_ONEPIECE: energy_col = "haki"
    elif char[2] in ABILITIES_NARUTO: energy_col = "naruto_chakra"
    elif char[2] in ABILITIES_DRAGONBALL: energy_col = "dragonball_ki"
    elif char[2] in ABILITIES_SOLOLEVELING: energy_col = "sololeveling_mana"
    elif char[2] in ABILITIES_HXH: energy_col = "hxh_nen"
    elif char[2] in ABILITIES_MUSHOKU: energy_col = "mushoku_mana"
    elif char[2] in ABILITIES_TOKYOGHOUL: energy_col = "tokyoghoul_rc"
    elif char[2] in ABILITIES_SDS: energy_col = "sds_magic"
    elif char[2] in ABILITIES_SAKAMOTO: energy_col = "sakamoto_stamina"
    elif char[2] in ABILITIES_AOT: energy_col = "aot_titan"
    elif char[2] in ABILITIES_BLACKCLOVER: energy_col = "blackclover_mana"
    elif char[2] in ABILITIES_BERSERK: energy_col = "berserk_bloodlust"
    elif char[2] in ABILITIES_DEMONSLAYER: energy_col = "demonslayer_breath"
    elif char[2] in ABILITIES_CHAINSAWMAN: energy_col = "chainsawman_blood"
    elif char[2] in ABILITIES_OPM: energy_col = "opm_power"
    c.execute(f"SELECT {energy_col} FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
    row = c.fetchone(); energy = row[0] if row else 0
    if energy < cost:
        conn.close(); return "active", f"❌ انرژی کافی نداری! (نیاز: {cost})", battle
    c.execute(f"UPDATE characters SET {energy_col} = {energy_col} - ? WHERE user_id=? AND is_active=1", (cost, battle["uid"]))
    conn.commit(); conn.close()
    dmg = int(char[6] * mult); bhp = max(0, bhp - dmg)
    text = box_title(f"🔥 {ability_name}!", 26)
    text += f"\n\n💥 {format_num(dmg)} آسیب ({mult}x)\n⚡ انرژی مصرفی: {cost}"
    text += f"\n\n👹 {boss['display_name']}"; text += f"\n{hp_bar(bhp, bmax)}"
    if bhp <= 0: battle["php"] = php; battle["bhp"] = bhp; return "won", text, battle
    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)
    battle = apply_bankai_round(battle); php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt: text += f"\n{bt}"
    battle = apply_domain_round(battle)
    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0: return "won", text, battle
    if php <= 0: return "lost", text, battle
    return "active", text, battle
def player_ability_shop(battle, char, ability_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss: return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]; pmax = battle["pmax"]; bmax = battle["bmax"]
    info = ABILITIES.get(ability_name)
    if not info: return "active", "❌ Ability پیدا نشد.", battle
    eff = info.get("effect", ""); text = box_simple(f"🔥 {ability_name}!")
    if "x2" in eff: dmg = int(char[6] * 2)
    elif "x3.5" in eff: dmg = int(char[6] * 3.5)
    elif "x3" in eff: dmg = int(char[6] * 3)
    elif "x4" in eff: dmg = int(char[6] * 4)
    elif "x5" in eff: dmg = int(char[6] * 5)
    elif "x6" in eff: dmg = int(char[6] * 6)
    elif "x7" in eff: dmg = int(char[6] * 7)
    elif "x8" in eff: dmg = int(char[6] * 8)
    else: dmg = int(char[6] * 2)
    bhp = max(0, bhp - dmg); text += f"\n\n💥 {format_num(dmg)} آسیب"; text += f"\n\n👹 {boss['display_name']}"; text += f"\n{hp_bar(bhp, bmax)}"
    if bhp <= 0: battle["php"] = php; battle["bhp"] = bhp; return "won", text, battle
    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)
    battle = apply_bankai_round(battle); php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt: text += f"\n{bt}"
    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0: return "won", text, battle
    if php <= 0: return "lost", text, battle
    return "active", text, battle

def player_buff_shop(battle, char, buff_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss: return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]; pmax = battle["pmax"]; bmax = battle["bmax"]
    info = BUFFS.get(buff_name)
    if not info: return "active", "❌ باف پیدا نشد.", battle
    eff = info.get("effect", ""); text = box_simple(f"✨ {buff_name}!")
    if "Max HP" in eff: heal = 500; php = min(pmax, php + heal); text += f"\n\n💚 +{format_num(heal)} HP"
    elif "ATK" in eff and "150" in eff: battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 15; text += "\n\n⚔️ ATK +۱۵٪"
    elif "DEF" in eff: text += "\n\n🛡️ DEF +۸۰"
    elif "DODGE" in eff: text += "\n\n💨 دوج +۱۰٪"
    elif "all +20" in eff: battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 20; text += "\n\n🔥 همه +۲۰٪"
    elif "all +50" in eff: battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 50; text += "\n\n🔥 همه +۵۰٪"
    text += f"\n\n👤 {hp_bar(php, pmax)}"
    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)
    battle = apply_bankai_round(battle); php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt: text += f"\n{bt}"
    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0: return "won", text, battle
    if php <= 0: return "lost", text, battle
    return "active", text, battle

def player_item(battle, char, item_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss: return "active", "❌ باس پیدا نشد.", battle
    info = ITEMS.get(item_name)
    if not info: return "active", "❌ آیتم نداری.", battle
    php = battle["php"]; bhp = battle["bhp"]; pmax = battle["pmax"]; bmax = battle["bmax"]
    text = box_simple(f"💊 {item_name}!"); new_php = php; new_bhp = bhp
    if item_name == "Health Potion": new_php = min(pmax, php + 500); text += "\n\n💚 HP +۵۰۰"
    elif item_name == "Mega Potion": new_php = min(pmax, php + 1500); text += "\n\n💚 HP +۱,۵۰۰"
    elif item_name == "Damage Boost":
        dmg, _ = roll_damage(char[6] * 2); new_bhp = max(0, bhp - dmg); text += f"\n\n💥 ATK x2 → {format_num(dmg)}"
    elif item_name == "Bomb": new_bhp = max(0, bhp - 500); text += "\n\n💥 ۵۰۰ آسیب"
    elif item_name == "Jinwoo Sword": battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 50; text += "\n\n🗡️ شمشیر جین‌وو! ATK +۵۰٪"
    elif item_name == "Magic Bean": new_php = pmax; text += "\n\n🫘 لوبیای جادویی! HP کامل"
    elif item_name == "Saiyan Crystal": battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 100; text += "\n\n💠 کریستال سایان! ATK +۱۰۰٪"
    elif item_name == "Sea Meat": heal = int(pmax * 0.7); new_php = min(pmax, php + heal); text += f"\n\n🍖 گوشت دریایی! +{format_num(heal)} HP"
    else: text += f"\n\n{info.get('effect_fa', info.get('effect', ''))}"
    if new_bhp <= 0: battle["php"] = new_php; battle["bhp"] = new_bhp; return "won", text, battle
    new_php, new_bhp, text = boss_turn(battle, boss, new_php, pmax, new_bhp, bmax, text)
    battle = apply_bankai_round(battle); new_php, new_bhp, bt = apply_bankai_effects(battle, new_php, pmax, new_bhp, bmax)
    if bt: text += f"\n{bt}"
    battle["php"] = new_php; battle["bhp"] = new_bhp
    if new_bhp <= 0: return "won", text, battle
    if new_php <= 0: return "lost", text, battle
    return "active", text, battle
def build_battle_message(battle, char):
    boss = get_boss_data(battle["boss_name"])
    boss_atk = boss["atk"] if boss else 0
    boss_display = boss["display_name"] if boss else battle["boss_name"]
    boss_energy = battle.get("boss_energy", 5000)
    text = f"╔══════════════════════════╗\n"
    text += f"║  👹 {boss_display[:20].center(20)} ║\n"
    text += f"╚══════════════════════════╝\n\n"
    text += f"{hp_bar(battle['bhp'], battle['bmax'])}\n"
    text += f"⚔️ ATK: {format_num(boss_atk)}\n"
    text += f"⚡ انرژی: {format_num(boss_energy)} 🔋\n"
    text += f"\n╭───── 👤 {char[2][:16]} ─────╮\n"
    text += f"│ ⭐ {char[3]} Rank{' ' * (14 - len(char[3]))}│\n"
    text += f"│ {hp_bar(battle['php'], battle['pmax'])} │\n"
    text += f"│ ⚔️ ATK: {format_num(char[6])}{' ' * (13 - len(format_num(char[6])))}│\n"
    text += f"│ 🛡️ DEF: {format_num(char[7])}{' ' * (13 - len(format_num(char[7])))}│\n"
    text += f"│ 💨 DODGE: {char[8]}%{' ' * (10 - len(str(char[8])))}│\n"
    text += f"╰{'─' * 25}╯"
    if char[2] == "Sung Jin-Woo":
        shadow_bonus = get_shadows_atk_bonus(battle["uid"], char[2])
        if shadow_bonus > 0: text += f"\n\n💀 **سایه‌ها: +{shadow_bonus} ATK**"
    try:
        conn = sqlite3.connect(DB_NAME); c = conn.cursor()
        c.execute("""SELECT cursed_energy, max_cursed_energy, reiatsu, max_reiatsu, geass_power, max_geass_power, haki, max_haki, 
                            naruto_chakra, max_naruto_chakra, dragonball_ki, max_dragonball_ki, sololeveling_mana, max_sololeveling_mana, 
                            hxh_nen, max_hxh_nen, mushoku_mana, max_mushoku_mana, tokyoghoul_rc, max_tokyoghoul_rc, sds_magic, max_sds_magic, 
                            sakamoto_stamina, max_sakamoto_stamina, aot_titan, max_aot_titan, blackclover_mana, max_blackclover_mana, 
                            berserk_bloodlust, max_berserk_bloodlust, demonslayer_breath, max_demonslayer_breath, chainsawman_blood, max_chainsawman_blood, 
                            opm_power, max_opm_power 
                     FROM characters WHERE user_id=? AND is_active=1""", (battle["uid"],))
        row = c.fetchone(); conn.close()
        if row:
            if char[2] in DOMAINS_JJK or char[2] in ABILITIES_JJK: text += f"\n\n🔮 انرژی نفرینی: {row[0]}/{row[1]}"
            elif char[2] in BLEACH_BANKAI or char[2] in ABILITIES_BLEACH: text += f"\n\n👻 ریستو: {row[2]}/{row[3]}"
            elif char[2] in ABILITIES_CODEGEASS: text += f"\n\n👁️ گیاس: {row[4]}/{row[5]}"
            elif char[2] in ABILITIES_ONEPIECE: text += f"\n\n🌊 هاکی: {row[6]}/{row[7]}"
            elif char[2] in ABILITIES_NARUTO: text += f"\n\n🍥 چاکرا: {row[8]}/{row[9]}"
            elif char[2] in ABILITIES_DRAGONBALL: text += f"\n\n🐉 کی: {row[10]}/{row[11]}"
            elif char[2] in ABILITIES_SOLOLEVELING: text += f"\n\n🗡️ مانا: {row[12]}/{row[13]}"
            elif char[2] in ABILITIES_HXH: text += f"\n\n🎯 نن: {row[14]}/{row[15]}"
            elif char[2] in ABILITIES_MUSHOKU: text += f"\n\n🌀 مانا: {row[16]}/{row[17]}"
            elif char[2] in ABILITIES_TOKYOGHOUL: text += f"\n\n👁️ RC: {row[18]}/{row[19]}"
            elif char[2] in ABILITIES_SDS: text += f"\n\n⚔️ جادو: {row[20]}/{row[21]}"
            elif char[2] in ABILITIES_SAKAMOTO: text += f"\n\n🍡 استقامت: {row[22]}/{row[23]}"
            elif char[2] in ABILITIES_AOT: text += f"\n\n⚡ قدرت تایتان: {row[24]}/{row[25]}"
            elif char[2] in ABILITIES_BLACKCLOVER: text += f"\n\n🍀 مانا: {row[26]}/{row[27]}"
            elif char[2] in ABILITIES_BERSERK: text += f"\n\n🩸 خون‌آشامی: {row[28]}/{row[29]}"
            elif char[2] in ABILITIES_DEMONSLAYER: text += f"\n\n🌸 نفس: {row[30]}/{row[31]}"
            elif char[2] in ABILITIES_CHAINSAWMAN: text += f"\n\n🪚 خون: {row[32]}/{row[33]}"
            elif char[2] in ABILITIES_OPM: text += f"\n\n💪 قدرت مطلق: {row[34]}/{row[35]}"
    except: pass
    if battle.get("domain_active", 0) == 1: text += f"\n\n🌀 قلمرو: {battle.get('domain_name', '')} ({battle.get('domain_turns', 0)} راند)"
    if battle.get("bankai_used", 0) >= 1:
        bankai = battle.get("bankai_data", {}); text += f"\n⚔️ Bankai: {bankai.get('name', '')}"
    if battle.get("boss_frozen", 0) > 0: text += f"\n❄️ باس فریز است ({battle['boss_frozen']} نوبت)"
    text += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n🎯 نوبت توئه!"
    return text

def finish_battle(uid, boss_name, won):
    # لیست تمام انرژی‌ها
    energies = ["cursed_energy", "reiatsu", "geass_power", "haki", "naruto_chakra",
                "dragonball_ki", "sololeveling_mana", "hxh_nen", "mushoku_mana", 
                "tokyoghoul_rc", "sds_magic", "sakamoto_stamina", "aot_titan", 
                "blackclover_mana", "berserk_bloodlust", "demonslayer_breath", 
                "chainsawman_blood", "opm_power"]

    # 🆕 صفر کردن انرژی‌ها بعد از مچ (تا مچ بعدی از اول پر بشه)
    set_query = ", ".join([f"{e} = 0" for e in energies])
    reset_query = f"UPDATE characters SET {set_query} WHERE user_id=? AND is_active=1"

    if won:
        boss = get_boss_data(boss_name)
        if "Survival" in boss_name:
            mode = "castle" if "Castle" in boss_name else ("zombie" if "Zombie" in boss_name else "tower")
            col = f"{mode}_wave"
            conn = sqlite3.connect(DB_NAME); c = conn.cursor()
            c.execute(f"SELECT {col} FROM characters WHERE user_id=? AND is_active=1", (uid,))
            row = c.fetchone()
            wave = row[0] if row else 1
            reward = get_reward_by_wave(wave)
            if wave < 100:
                c.execute(f"UPDATE characters SET {col} = {col} + 1 WHERE user_id=? AND is_active=1", (uid,))
            conn.commit(); conn.close()
        else:
            reward = boss["reward"] if boss else 5000

        add_coins(uid, reward)
        
        # صفر کردن انرژی‌ها
        conn = sqlite3.connect(DB_NAME); c = conn.cursor()
        c.execute(reset_query, (uid,))
        conn.commit(); conn.close()

        try:
            from quests import update_quest_progress
            update_quest_progress(uid, "win_3_bosses")
            update_quest_progress(uid, "win_5_bosses")
        except: pass
        try:
            from guild import give_guild_xp
            give_guild_xp(uid, 5)
        except: pass
        return reward
    else:
        if "Survival" in boss_name:
            mode = "castle" if "Castle" in boss_name else ("zombie" if "Zombie" in boss_name else "tower")
            col = f"{mode}_wave"
            conn = sqlite3.connect(DB_NAME); c = conn.cursor()
            c.execute(f"UPDATE characters SET {col} = 1 WHERE user_id=? AND is_active=1", (uid,))
            conn.commit(); conn.close()
        
        # صفر کردن انرژی‌ها
        conn = sqlite3.connect(DB_NAME); c = conn.cursor()
        c.execute(reset_query, (uid,))
        conn.commit(); conn.close()
        return 0