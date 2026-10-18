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

# 🆕 ایمپورت کردن لیست باس‌های جدید برای جلوگیری از خطا و اتک 0
from onepiece_data import ONEPIECE_BOSSES, ONEPIECE_FODDER
from dragonball_data import DRAGONBALL_BOSSES, DRAGONBALL_FODDER
from hxh_data import HXH_BOSSES, HXH_FODDER
from sakamoto_data import SAKAMOTO_BOSSES, SAKAMOTO_FODDER
from sololeveling_data import SOLOLEVELING_BOSSES, SOLOLEVELING_FODDER
from mushoku_data import MUSHOKU_BOSSES, MUSHOKU_FODDER
from codegeass_data import CODEGEASS_BOSSES, CODEGEASS_FODDER
from tokyoghoul_data import TOKYOGHOUL_BOSSES, TOKYOGHOUL_FODDER
from jjk_data import FODDER_JJK
from bleach_data import BLEACH_FODDER
from aot_data import AOT_FODDER
from blackclover_data import BLACKCLOVER_FODDER
from berserk_data import BERSERK_FODDER
from demonslayer_data import DEMONSLAYER_FODDER
from chainsawman_data import CHAINSAWMAN_FODDER

from database import (add_coins, get_battle, update_battle, end_battle,
                      get_coins, get_shadows_atk_bonus)


# ============================================================
# HELPER — پیدا کردن اطلاعات باس
# ============================================================
def get_boss_data(boss_name):
    if "Survival" in boss_name:
        return {"display_name": boss_name, "atk": 150, "hp": 10000, "reward": 1000}
        
    # 🆕 لیست کامل تمام باس‌های تمام انیمه‌ها
    all_boss_lists = [
        BOSSES_JJK, BLEACH_BOSSES, BOSSES_OPM, BOSSES, AOT_BOSSES, 
        BLACKCLOVER_BOSSES, BERSERK_BOSSES, DEMONSLAYER_BOSSES, CHAINSAWMAN_BOSSES,
        ONEPIECE_BOSSES, DRAGONBALL_BOSSES, HXH_BOSSES, SAKAMOTO_BOSSES, 
        SOLOLEVELING_BOSSES, MUSHOKU_BOSSES, CODEGEASS_BOSSES, TOKYOGHOUL_BOSSES
    ]
    
    # لیست فادرها (دشمنان ضعیف)
    all_fodder_lists = [
        FODDER_JJK, BLEACH_FODDER, AOT_FODDER, BLACKCLOVER_FODDER, BERSERK_FODDER,
        DEMONSLAYER_FODDER, CHAINSAWMAN_FODDER, ONEPIECE_FODDER, DRAGONBALL_FODDER,
        HXH_FODDER, SAKAMOTO_FODDER, SOLOLEVELING_FODDER, MUSHOKU_FODDER,
        CODEGEASS_FODDER, TOKYOGHOUL_FODDER
    ]
    
    # اول باس‌ها رو چک میکنیم
    for bosses in all_boss_lists:
        if boss_name in bosses:
            boss = bosses[boss_name].copy()
            if boss.get("atk", 0) <= 0:
                boss["atk"] = 250  # اتک پایه برای باس
            if boss.get("hp", 0) <= 0:
                boss["hp"] = 5000  # HP پایه
            if "display_name" not in boss:
                boss["display_name"] = boss_name
            return boss
            
    # اگر توی باس‌ها نبود، فادرها رو چک میکنیم
    for fodder in all_fodder_lists:
        if boss_name in fodder:
            boss = fodder[boss_name].copy()
            if boss.get("atk", 0) <= 0:
                boss["atk"] = 150  # اتک پایه برای فادرها
            if boss.get("hp", 0) <= 0:
                boss["hp"] = 1000  # HP پایه برای فادرها
            if "display_name" not in boss:
                boss["display_name"] = boss_name
            return boss
            
    return None


# ============================================================
# HELPER — نمایش
# ============================================================
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


def roll_damage(atk, defender_def=0, defender_defending=0):
    base = atk * random.uniform(0.85, 1.15)
    crit = random.random() < 0.15
    if crit:
        base *= 2
    if defender_defending:
        base -= defender_def * 2
    else:
        base -= defender_def * 0.5
    return max(1, int(base)), crit


def boss_ai(boss_name, boss_hp, boss_max_hp):
    r = random.random()
    if boss_hp < boss_max_hp * 0.25 and r < 0.3:
        return "heal"
    if r < 0.4:
        return "attack"
    if r < 0.7:
        return "special"
    return "defend"


def apply_defense_check(base_dmg, php, defense_type, char_dodge=0):
    roll = random.randint(1, 100)
    if roll <= 33:
        return php, f"✅ {defense_type} کامل! ۰ آسیب"
    elif roll <= 66:
        partial = max(1, int(base_dmg * 0.5))
        php = max(0, php - partial)
        return php, f"⚠️ {defense_type} جزئی! {format_num(partial)} آسیب (۵۰٪)"
    else:
        php = max(0, php - base_dmg)
        return php, f"❌ {defense_type} ناموفق! {format_num(base_dmg)} آسیب کامل"


def boss_attack_player(boss, php, pmax, battle, defense_flag=None, char_dodge=0):
    base_dmg, crit = roll_damage(boss["atk"], 0, 0)
    text = box_simple("👹 باس حمله کرد!")
    if crit and not defense_flag:
        text += f"\n\n⚡ CRITICAL HIT! ⚡"
    text += f"\n\n💢 آسیب پایه: {format_num(base_dmg)}"

    if defense_flag == "defend":
        php, def_log = apply_defense_check(base_dmg, php, "دفاع")
        text += f"\n{def_log}"
    elif defense_flag == "dodge":
        php, def_log = apply_defense_check(base_dmg, php, "جاخالی")
        text += f"\n{def_log}"
    else:
        php = max(0, php - base_dmg)

    text += f"\n\n👤 {hp_bar(php, pmax)}"
    return php, text, base_dmg


def apply_bankai_round(battle):
    if battle.get("bankai_used", 0) < 1:
        return battle
    bankai = battle.get("bankai_data", {})
    if not bankai:
        return battle
    if "atk_per_round" in bankai:
        cur = battle.get("bankai_atk_current", 0)
        max_a = bankai.get("max_atk", 30)
        if cur < max_a:
            battle["bankai_atk_current"] = min(max_a, cur + bankai["atk_per_round"])
    if "dodge_per_round" in bankai:
        cur = battle.get("bankai_dodge_current", 0)
        max_d = bankai.get("max_dodge", 15)
        if cur < max_d:
            battle["bankai_dodge_current"] = min(max_d, cur + bankai["dodge_per_round"])
    if "heal_per_round" in bankai:
        cur = battle.get("bankai_heal_current", 0)
        max_h = bankai.get("max_heal", 15)
        if cur < max_h:
            battle["bankai_heal_current"] = min(max_h, cur + bankai["heal_per_round"])
    if "bleed_per_round" in bankai:
        cur = battle.get("bankai_bleed_current", 0)
        max_b = bankai.get("max_bleed", 5)
        if cur < max_b:
            battle["bankai_bleed_current"] = min(max_b, cur + bankai["bleed_per_round"])
    if "enemy_atk_debuff" in bankai:
        cur = battle.get("bankai_enemy_debuff_current", 0)
        max_e = bankai.get("max_enemy_debuff", 15)
        if cur < max_e:
            battle["bankai_enemy_debuff_current"] = min(max_e, cur + bankai["enemy_atk_debuff"])
    if "self_dmg_per_round" in bankai:
        cur = battle.get("bankai_self_dmg_current", 0)
        max_s = bankai.get("max_self_dmg", 5)
        if cur < max_s:
            battle["bankai_self_dmg_current"] = min(max_s, cur + bankai["self_dmg_per_round"])
    return battle


def apply_bankai_effects(battle, php, pmax, bhp, bmax):
    if battle.get("bankai_used", 0) < 1:
        return php, bhp, ""
    text = ""
    heal_pct = battle.get("bankai_heal_current", 0)
    if heal_pct > 0:
        heal = int(pmax * heal_pct / 100)
        php = min(pmax, php + heal)
        text += f"\n💚 بانکای: +{format_num(heal)} HP"
    bleed_pct = battle.get("bankai_bleed_current", 0)
    if bleed_pct > 0:
        bleed = int(bmax * bleed_pct / 100)
        bhp = max(0, bhp - bleed)
        text += f"\n🩸 بانکای: باس -{format_num(bleed)} HP"
    self_pct = battle.get("bankai_self_dmg_current", 0)
    if self_pct > 0:
        dmg = int(pmax * self_pct / 100)
        php = max(0, php - dmg)
        text += f"\n🩸 بانکای: خودت -{format_num(dmg)} HP"
    return php, bhp, text


def boss_turn(battle, boss, php, pmax, bhp, bmax, text, defense_flag=None):
    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n\n❄️ باس فریزه! (نوبت از دست داد)"
        return php, bhp, text

    action = boss_ai(battle["boss_name"], bhp, bmax)
    if action == "attack":
        php, boss_text, _ = boss_attack_player(boss, php, pmax, battle, defense_flag)
        text += f"\n\n{boss_text}"
    elif action == "special":
        base_dmg, _ = roll_damage(boss["atk"] * 2, 0, 0)
        if defense_flag:
            php, def_log = apply_defense_check(base_dmg, php, defense_flag.capitalize())
            text += f"\n\n{box_simple('💥 حمله ویژه باس!')}"
            text += f"\n\n💢 آسیب پایه: {format_num(base_dmg)}"
            text += f"\n{def_log}"
            text += f"\n\n👤 {hp_bar(php, pmax)}"
        else:
            php = max(0, php - base_dmg)
            text += f"\n\n{box_simple('💥 حمله ویژه باس!')}"
            text += f"\n\n💢 {format_num(base_dmg)} آسیب!"
            text += f"\n\n👤 {hp_bar(php, pmax)}"
    elif action == "defend":
        text += f"\n\n🛡️ باس دفاع گرفت."
    elif action == "heal":
        heal = int(bmax * 0.1)
        bhp = min(bmax, bhp + heal)
        text += f"\n\n💚 باس درمان: +{format_num(heal)}"
        text += f"\n👹 {hp_bar(bhp, bmax)}"

    return php, bhp, text


def player_attack(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    if char[2] in DOMAINS_JJK or char[2] in ABILITIES_JJK:
        dmg, crit = roll_damage(char[6] * 0.8, 0, 0)
    else:
        dmg, crit = roll_damage(char[6], 0, 0)

    if char[2] == "Sung Jin-Woo":
        shadow_bonus = get_shadows_atk_bonus(battle["uid"], char[2])
        dmg += shadow_bonus
    atk_boost = battle.get("domain_atk_boost", 0)
    if atk_boost:
        dmg = int(dmg * (1 + atk_boost / 100))
    bankai_atk = battle.get("bankai_atk_current", 0)
    if bankai_atk:
        dmg = int(dmg * (1 + bankai_atk / 100))

    bhp = max(0, bhp - dmg)

    if crit:
        text = box_simple("⚡ CRITICAL HIT! ⚡")
    else:
        text = box_simple("⚔️ حمله!")
    text += f"\n\n💥 {format_num(dmg)} آسیب 💥"
    text += f"\n\n👹 {boss['display_name']}"
    text += f"\n{hp_bar(bhp, bmax)}"

    if bhp <= 0:
        battle["php"] = php; battle["bhp"] = bhp
        return "won", text, battle

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_defend(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    text = box_simple("🛡️ دفاع گرفتی!")
    text += "\n\n🎲 ۳۳٪ کامل / ۳۳٪ جزئی / ۳۳٪ ناموفق"

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text, "defend")

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_dodge(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    text = box_simple("💨 جاخالی می‌زنی!")
    text += "\n\n🎲 ۳۳٪ کامل / ۳۳٪ جزئی / ۳۳٪ ناموفق"

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text, "dodge")

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_ability(battle, char, ability_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    char_name = char[2]
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    abilities = ABILITIES_3.get(char_name, {})
    extra_text = ""

    if ability_name == "DOMAIN":
        if battle.get("domain_used", 0) >= 1:
            return "active", "❌ Domain فقط ۱ بار در نبرد!", battle
    if ability_name == "BANKAI":
        if battle.get("bankai_used", 0) >= 1:
            return "active", "❌ Bankai فقط ۱ بار در نبرد!", battle
    if ability_name == "ULTIMATE_GEASS":
        if battle.get("geass_used", 0) >= 1:
            return "active", "❌ گیاس دوم فقط ۱ بار در نبرد!", battle

    found_key = None
    for key in ["ability_1", "ability_2", "ability_3"]:
        if key in abilities and abilities[key]["name"] == ability_name:
            found_key = key
            break

    if found_key == "ability_3":
        if battle.get("spam_state") == "purple_used":
            return "active", f"🟣 {ability_name} فقط ۱ بار در کل نبرد!", battle

    if char_name in DOMAINS_JJK or char_name in ABILITIES_JJK or char_name in BLEACH_BANKAI or char_name in ABILITIES_BLEACH or char_name in ABILITIES_CODEGEASS or char_name in ABILITIES_ONEPIECE:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        is_jjk = char_name in DOMAINS_JJK or char_name in ABILITIES_JJK
        is_bleach = char_name in BLEACH_BANKAI or char_name in ABILITIES_BLEACH
        is_geass = char_name in ABILITIES_CODEGEASS
        is_op = char_name in ABILITIES_ONEPIECE
        
        cost = 0
        if is_jjk:
            c.execute("SELECT cursed_energy, max_cursed_energy FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
            row = c.fetchone()
            energy = row[0] if row else 0
            if ability_name == "DOMAIN": cost = JJK_CE_COST_DOMAIN
            elif found_key == "ability_1": cost = JJK_CE_COST_ABILITY_1
            elif found_key == "ability_2": cost = JJK_CE_COST_ABILITY_2
            elif found_key == "ability_3": cost = JJK_CE_COST_ABILITY_3
        elif is_bleach:
            c.execute("SELECT reiatsu, max_reiatsu FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
            row = c.fetchone()
            energy = row[0] if row else 0
            if ability_name == "BANKAI": cost = BLEACH_REI_COST_BANKAI
            elif found_key == "ability_1": cost = BLEACH_REI_COST_ABILITY_1
            elif found_key == "ability_2": cost = BLEACH_REI_COST_ABILITY_2
            elif found_key == "ability_3": cost = BLEACH_REI_COST_ABILITY_3
        elif is_geass:
            c.execute("SELECT geass_power, max_geass_power FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
            row = c.fetchone()
            energy = row[0] if row else 0
            if ability_name == "ULTIMATE_GEASS": cost = GEASS_COST_ULTIMATE
            elif found_key == "ability_1": cost = GEASS_COST_ABILITY_1
            elif found_key == "ability_2": cost = GEASS_COST_ABILITY_2
            elif found_key == "ability_3": cost = GEASS_COST_ABILITY_3
        elif is_op:
            c.execute("SELECT haki, max_haki FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
            row = c.fetchone()
            energy = row[0] if row else 0
            if found_key == "ability_1": cost = HAKI_COST_ABILITY_1
            elif found_key == "ability_2": cost = HAKI_COST_ABILITY_2
            elif found_key == "ability_3": cost = HAKI_COST_ABILITY_3

        char_level = char[4]
        level_penalty = (char_level // 10) * 2
        cost += level_penalty
            
        if energy < cost:
            hp_cost = (cost - energy) * 10
            if php <= hp_cost:
                conn.close()
                return "active", f"❌ نه انرژی داری نه HP کافی! (نیاز: {hp_cost} HP)", battle
            
            php -= hp_cost
            if is_jjk: c.execute("UPDATE characters SET cursed_energy = 0 WHERE user_id=? AND is_active=1", (battle["uid"],))
            elif is_bleach: c.execute("UPDATE characters SET reiatsu = 0 WHERE user_id=? AND is_active=1", (battle["uid"],))
            elif is_geass: c.execute("UPDATE characters SET geass_power = 0 WHERE user_id=? AND is_active=1", (battle["uid"],))
            else: c.execute("UPDATE characters SET haki = 0 WHERE user_id=? AND is_active=1", (battle["uid"],))
            conn.commit()
            conn.close()
            extra_text = f"🩸 **از HP خودت انرژی ساختی! (-{format_num(hp_cost)} HP)**\n\n"
        else:
            if is_jjk: c.execute("UPDATE characters SET cursed_energy = cursed_energy - ? WHERE user_id=? AND is_active=1", (cost, battle["uid"]))
            elif is_bleach: c.execute("UPDATE characters SET reiatsu = reiatsu - ? WHERE user_id=? AND is_active=1", (cost, battle["uid"]))
            elif is_geass: c.execute("UPDATE characters SET geass_power = geass_power - ? WHERE user_id=? AND is_active=1", (cost, battle["uid"]))
            else: c.execute("UPDATE characters SET haki = haki - ? WHERE user_id=? AND is_active=1", (cost, battle["uid"]))
            conn.commit()
            conn.close()
            extra_text = ""

        battle["php"] = php
    # ========== DOMAIN ==========
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

        dmg = int(char[6] * 2.5)
        bhp = max(0, bhp - dmg)
        text = extra_text + box_title(f"🌀 {domain['name'][:20]}", 26)
        text += f"\n\n💥 {format_num(dmg)} آسیب (×۲.۵)"

        if "freeze" in effects:
            battle["boss_frozen"] = effects["freeze"]
            text += f"\n❄️ باس فریز شد! ({effects['freeze']} نوبت)"
        if "atk_boost" in effects:
            text += f"\n⚔️ ATK +{effects['atk_boost']}٪"
        if "heal" in effects:
            heal = int(pmax * effects["heal"] / 100)
            php = min(pmax, php + heal)
            text += f"\n💚 +{format_num(heal)} HP"

        text += f"\n\n👹 {boss['display_name']}"
        text += f"\n{hp_bar(bhp, bmax)}"

        if bhp <= 0:
            battle["php"] = php; battle["bhp"] = bhp
            return "won", text, battle

        php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

        battle = apply_bankai_round(battle)
        php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
        if bt:
            text += f"\n{bt}"

        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0:
            return "won", text, battle
        if php <= 0:
            return "lost", text, battle
        return "active", text, battle

    # ========== BANKAI ==========
    if ability_name == "BANKAI":
        bankai = BANKAI.get(char_name) or BLEACH_BANKAI.get(char_name)
        if not bankai:
            return "active", "❌ این کاراکتر Bankai نداره!", battle
        battle["bankai_used"] = 1
        battle["bankai_data"] = bankai
        battle["bankai_atk_current"] = 0
        battle["bankai_dodge_current"] = 0
        battle["bankai_heal_current"] = 0
        battle["bankai_bleed_current"] = 0
        battle["bankai_enemy_debuff_current"] = 0
        battle["bankai_self_dmg_current"] = 0

        dmg = int(char[6] * 6)
        bhp = max(0, bhp - dmg)
        text = extra_text + box_title(f"⚔️ {bankai['name'][:20]}", 26)
        text += f"\n\n💥 {format_num(dmg)} آسیب (×۶)"
        text += f"\n\n👹 {boss['display_name']}"
        text += f"\n{hp_bar(bhp, bmax)}"

        if bhp <= 0:
            battle["php"] = php; battle["bhp"] = bhp
            return "won", text, battle

        php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

        battle = apply_bankai_round(battle)
        php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
        if bt:
            text += f"\n{bt}"

        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0:
            return "won", text, battle
        if php <= 0:
            return "lost", text, battle
        return "active", text, battle

    # ========== ULTIMATE GEASS ==========
    if ability_name == "ULTIMATE_GEASS":
        if char_name not in ABILITIES_CODEGEASS:
            return "active", "❌ این کاراکتر گیاس دوم نداره!", battle
        
        geass = ULTIMATE_GEASS.get(char_name)
        if not geass:
            return "active", "❌ گیاس دوم تعریف نشده!", battle
        
        battle["geass_used"] = 1
        effect = geass.get("effect", "")
        
        dmg = int(char[6] * 4)
        bhp = max(0, bhp - dmg)
        
        text = extra_text + box_title(f"👁️ {geass['name'][:20]}", 26)
        text += f"\n\n💥 {format_num(dmg)} آسیب (×۴)"
        
        if effect == "skip_enemy_turn":
            battle["boss_frozen"] = geass.get("duration", 2)
            text += f"\n❄️ باس {geass.get('duration', 2)} نوبت محروم شد!"
        elif effect == "atk_boost":
            battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + geass.get("value", 100)
            text += f"\n⚔️ ATK +{geass.get('value', 100)}٪"
        elif effect == "def_boost":
            text += f"\n🛡️ DEF +{geass.get('value', 100)}٪"
        elif effect == "dodge_boost":
            text += f"\n💨 DODGE +{geass.get('value', 50)}٪"
        elif effect == "heal":
            heal = int(pmax * geass.get("value", 50) / 100)
            php = min(pmax, php + heal)
            text += f"\n💚 +{format_num(heal)} HP"
            
        text += f"\n\n👹 {boss['display_name']}"
        text += f"\n{hp_bar(bhp, bmax)}"

        if bhp <= 0:
            battle["php"] = php; battle["bhp"] = bhp
            return "won", text, battle

        php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

        battle = apply_bankai_round(battle)
        php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
        if bt:
            text += f"\n{bt}"

        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0:
            return "won", text, battle
        if php <= 0:
            return "lost", text, battle
        return "active", text, battle

    # ========== ABILITY های ۳گانه ==========
    if not abilities:
        return "active", "❌ Ability پیدا نشد.", battle

    found_ab = None
    for key in ["ability_1", "ability_2", "ability_3"]:
        if key in abilities and abilities[key]["name"] == ability_name:
            found_ab = abilities[key]
            break

    if not found_ab:
        return "active", "❌ Ability پیدا نشد.", battle

    mult = found_ab.get("mult", 3)
    dmg = int(char[6] * mult)
    if char_name == "Sung Jin-Woo":
        shadow_bonus = get_shadows_atk_bonus(battle["uid"], char_name)
        dmg += shadow_bonus
    bhp = max(0, bhp - dmg)

    if found_key == "ability_3":
        text = extra_text + box_title(f"🟣 {ability_name[:20]}!", 26)
        battle["spam_state"] = "purple_used"
    elif found_key == "ability_1":
        text = extra_text + box_simple(f"🔵 {ability_name[:18]}!")
    else:
        text = extra_text + box_simple(f"🔴 {ability_name[:18]}!")

    text += f"\n\n💥 {format_num(dmg)} آسیب ({mult}x)"
    text += f"\n\n👹 {boss['display_name']}"
    text += f"\n{hp_bar(bhp, bmax)}"

    if bhp <= 0:
        battle["php"] = php; battle["bhp"] = bhp
        return "won", text, battle

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle

# 🆕 فرم گوکو
def goku_transform(battle, char):
    current_form = battle.get("goku_form", 0)
    if current_form >= 4:
        return "active", "🔥 گوکو به حداکثر قدرت رسیده! (Ultra Instinct)", battle
    
    new_form = current_form + 1
    
    if new_form == 1:
        atk_boost, dodge_boost, form_name = 10, 5, "Super Saiyan 2"
    elif new_form == 2:
        atk_boost, dodge_boost, form_name = 20, 10, "Super Saiyan 3"
    elif new_form == 3:
        atk_boost, dodge_boost, form_name = 35, 15, "Super Saiyan God"
    else:
        atk_boost, dodge_boost, form_name = 50, 25, "Super Saiyan Blue"
    
    battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + atk_boost
    battle["goku_form"] = new_form
    
    text = f"⚡ **گوکو به فرم {form_name} رفت!**\n\n"
    text += f"⚔️ ATK: +{atk_boost}٪\n"
    text += f"💨 DODGE: +{dodge_boost}٪\n"
    
    return "active", text, battle

# 🆕 فرم لوفی (One Piece)
def luffy_transform(battle, char):
    current_form = battle.get("luffy_form", 0)
    
    if current_form >= 4:
        return "active", "🔥 لوفی در فرم **Gear 5 (Sun God Nika)** است و به حداکثر قدرت رسیده!", battle
    
    new_form = current_form + 1
    
    if new_form == 1:
        atk_boost, dodge_boost, form_name = 15, 10, "Gear 2"
    elif new_form == 2:
        atk_boost, dodge_boost, form_name = 25, 15, "Gear 3"
    elif new_form == 3:
        atk_boost, dodge_boost, form_name = 40, 20, "Gear 4 (Bounceman)"
    else:
        atk_boost, dodge_boost, form_name = 60, 30, "Gear 5 (Sun God Nika)"
    
    battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + atk_boost
    battle["luffy_form"] = new_form
    
    text = f"⚡ **لوفی به فرم {form_name} رفت!**\n\n"
    text += f"⚔️ ATK: +{atk_boost}٪\n"
    text += f"💨 DODGE: +{dodge_boost}٪\n"
    
    return "active", text, battle
def player_ability_v2(battle, char, action):
    char_name = char[2]
    if action == "domain":
        return player_ability(battle, char, "DOMAIN")
    if action == "bankai":
        return player_ability(battle, char, "BANKAI")
    if action == "ultimate_geass":
        return player_ability(battle, char, "ULTIMATE_GEASS")
    abilities = ABILITIES_3.get(char_name, {})
    if action in abilities:
        ab_name = abilities[action]["name"]
        return player_ability(battle, char, ab_name)
    return "active", "❌ Ability نامعتبر.", battle


def player_ability_shop(battle, char, ability_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    info = ABILITIES.get(ability_name)
    if not info:
        return "active", "❌ Ability پیدا نشد.", battle

    eff = info.get("effect", "")
    text = box_simple(f"🔥 {ability_name}!")

    if "x2" in eff:
        dmg = int(char[6] * 2)
    elif "x3.5" in eff:
        dmg = int(char[6] * 3.5)
    elif "x3" in eff:
        dmg = int(char[6] * 3)
    elif "x4" in eff:
        dmg = int(char[6] * 4)
    elif "x5" in eff:
        dmg = int(char[6] * 5)
    elif "x6" in eff:
        dmg = int(char[6] * 6)
    elif "x7" in eff:
        dmg = int(char[6] * 7)
    elif "x8" in eff:
        dmg = int(char[6] * 8)
    else:
        dmg = int(char[6] * 2)

    bhp = max(0, bhp - dmg)
    text += f"\n\n💥 {format_num(dmg)} آسیب"
    text += f"\n\n👹 {boss['display_name']}"
    text += f"\n{hp_bar(bhp, bmax)}"

    if bhp <= 0:
        battle["php"] = php; battle["bhp"] = bhp
        return "won", text, battle

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_buff_shop(battle, char, buff_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    info = BUFFS.get(buff_name)
    if not info:
        return "active", "❌ باف پیدا نشد.", battle

    eff = info.get("effect", "")
    text = box_simple(f"✨ {buff_name}!")

    if "Max HP" in eff:
        heal = 500
        php = min(pmax, php + heal)
        text += f"\n\n💚 +{format_num(heal)} HP"
    elif "ATK" in eff and "150" in eff:
        battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 15
        text += "\n\n⚔️ ATK +۱۵٪"
    elif "DEF" in eff:
        text += "\n\n🛡️ DEF +۸۰"
    elif "DODGE" in eff:
        text += "\n\n💨 دوج +۱۰٪"
    elif "all +20" in eff:
        battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 20
        text += "\n\n🔥 همه +۲۰٪"
    elif "all +50" in eff:
        battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 50
        text += "\n\n🔥 همه +۵۰٪"

    text += f"\n\n👤 {hp_bar(php, pmax)}"

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_item(battle, char, item_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    info = ITEMS.get(item_name)
    if not info:
        return "active", "❌ آیتم نداری.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    text = box_simple(f"💊 {item_name}!")
    new_php = php
    new_bhp = bhp

    if item_name == "Health Potion":
        new_php = min(pmax, php + 500)
        text += "\n\n💚 HP +۵۰۰"
    elif item_name == "Mega Potion":
        new_php = min(pmax, php + 1500)
        text += "\n\n💚 HP +۱,۵۰۰"
    elif item_name == "Damage Boost":
        dmg, _ = roll_damage(char[6] * 2)
        new_bhp = max(0, bhp - dmg)
        text += f"\n\n💥 ATK x2 → {format_num(dmg)}"
    elif item_name == "Bomb":
        new_bhp = max(0, bhp - 500)
        text += "\n\n💥 ۵۰۰ آسیب"
    elif item_name == "Jinwoo Sword":
        battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 50
        text += "\n\n🗡️ شمشیر جین‌وو! ATK +۵۰٪"
    elif item_name == "Magic Bean":
        new_php = pmax
        text += "\n\n🫘 لوبیای جادویی! HP کامل"
    elif item_name == "Saiyan Crystal":
        battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 100
        text += "\n\n💠 کریستال سایان! ATK +۱۰۰٪"
    elif item_name == "Sea Meat":
        heal = int(pmax * 0.7)
        new_php = min(pmax, php + heal)
        text += f"\n\n🍖 گوشت دریایی! +{format_num(heal)} HP"
    else:
        text += f"\n\n{info.get('effect_fa', info.get('effect', ''))}"

    if new_bhp <= 0:
        battle["php"] = new_php; battle["bhp"] = new_bhp
        return "won", text, battle

    new_php, new_bhp, text = boss_turn(battle, boss, new_php, pmax, new_bhp, bmax, text)

    battle = apply_bankai_round(battle)
    new_php, new_bhp, bt = apply_bankai_effects(battle, new_php, pmax, new_bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = new_php; battle["bhp"] = new_bhp
    if new_bhp <= 0:
        return "won", text, battle
    if new_php <= 0:
        return "lost", text, battle
    return "active", text, battle
def build_battle_message(battle, char):
    boss = get_boss_data(battle["boss_name"])
    boss_atk = boss["atk"] if boss else 0
    boss_display = boss["display_name"] if boss else battle["boss_name"]

    text = f"╔══════════════════════════╗\n"
    text += f"║  👹 {boss_display[:20].center(20)} ║\n"
    text += f"╚══════════════════════════╝\n\n"
    text += f"{hp_bar(battle['bhp'], battle['bmax'])}\n"
    text += f"⚔️ ATK: {format_num(boss_atk)}\n"

    text += f"\n╭───── 👤 {char[2][:16]} ─────╮\n"
    text += f"│ ⭐ {char[3]} Rank{' ' * (14 - len(char[3]))}│\n"
    text += f"│ {hp_bar(battle['php'], battle['pmax'])} │\n"
    text += f"│ ⚔️ ATK: {format_num(char[6])}{' ' * (13 - len(format_num(char[6])))}│\n"
    text += f"│ 🛡️ DEF: {format_num(char[7])}{' ' * (13 - len(format_num(char[7])))}│\n"
    text += f"│ 💨 DODGE: {char[8]}%{' ' * (10 - len(str(char[8])))}│\n"
    text += f"╰{'─' * 25}╯"

    if char[2] == "Sung Jin-Woo":
        shadow_bonus = get_shadows_atk_bonus(battle["uid"], char[2])
        if shadow_bonus > 0:
            text += f"\n\n💀 **سایه‌ها: +{shadow_bonus} ATK**"

    if char[2] in DOMAINS_JJK or char[2] in ABILITIES_JJK:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT cursed_energy, max_cursed_energy FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
            row = c.fetchone()
            conn.close()
            if row:
                text += f"\n\n🔮 انرژی نفرینی: {row[0]}/{row[1]}"
        except Exception:
            pass
    elif char[2] in BLEACH_BANKAI or char[2] in ABILITIES_BLEACH:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT reiatsu, max_reiatsu FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
            row = c.fetchone()
            conn.close()
            if row:
                text += f"\n\n👻 ریستو: {row[0]}/{row[1]}"
        except Exception:
            pass
    elif char[2] in ABILITIES_CODEGEASS:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT geass_power, max_geass_power FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
            row = c.fetchone()
            conn.close()
            if row:
                text += f"\n\n👁️ گیاس: {row[0]}/{row[1]}"
        except Exception:
            pass
    elif char[2] in ABILITIES_ONEPIECE:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT haki, max_haki FROM characters WHERE user_id=? AND is_active=1", (battle["uid"],))
            row = c.fetchone()
            conn.close()
            if row:
                text += f"\n\n🌊 هاکی: {row[0]}/{row[1]}"
        except Exception:
            pass

    if battle.get("domain_active", 0) == 1:
        text += f"\n\n🌀 قلمرو: {battle.get('domain_name', '')} ({battle.get('domain_turns', 0)} راند)"
    if battle.get("bankai_used", 0) >= 1:
        bankai = battle.get("bankai_data", {})
        text += f"\n⚔️ Bankai: {bankai.get('name', '')}"

    if battle.get("boss_frozen", 0) > 0:
        text += f"\n❄️ باس فریز است ({battle['boss_frozen']} نوبت)"

    text += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n🎯 نوبت توئه!"
    return text


def finish_battle(uid, boss_name, won):
    if won:
        boss = get_boss_data(boss_name)
        reward = boss["reward"] if boss else 5000
        
        if "Survival" in boss_name:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT survival_wave FROM characters WHERE user_id=? AND is_active=1", (uid,))
            row = c.fetchone()
            wave = row[0] if row else 1
            if wave < 100:
                c.execute("UPDATE characters SET survival_wave = survival_wave + 1 WHERE user_id=? AND is_active=1", (uid,))
            conn.commit()
            conn.close()
            
        add_coins(uid, reward)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE characters SET cursed_energy = max_cursed_energy WHERE user_id=? AND is_active=1", (uid,))
        c.execute("UPDATE characters SET reiatsu = max_reiatsu WHERE user_id=? AND is_active=1", (uid,))
        c.execute("UPDATE characters SET geass_power = max_geass_power WHERE user_id=? AND is_active=1", (uid,))
        c.execute("UPDATE characters SET haki = max_haki WHERE user_id=? AND is_active=1", (uid,))
        conn.commit()
        conn.close()

        try:
            from quests import update_quest_progress
            update_quest_progress(uid, "win_3_bosses")
            update_quest_progress(uid, "win_5_bosses")
        except Exception:
            pass

        try:
            from guild import give_guild_xp
            give_guild_xp(uid, 5)
        except Exception:
            pass

        return reward
    else:
        if "Survival" in boss_name:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("UPDATE characters SET survival_wave = 1 WHERE user_id=? AND is_active=1", (uid,))
            conn.commit()
            conn.close()
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE characters SET cursed_energy = max_cursed_energy WHERE user_id=? AND is_active=1", (uid,))
        c.execute("UPDATE characters SET reiatsu = max_reiatsu WHERE user_id=? AND is_active=1", (uid,))
        c.execute("UPDATE characters SET geass_power = max_geass_power WHERE user_id=? AND is_active=1", (uid,))
        c.execute("UPDATE characters SET haki = max_haki WHERE user_id=? AND is_active=1", (uid,))
        conn.commit()
        conn.close()
        
        return 0