import random
from config import BOSSES, ABILITIES, ITEMS, ABILITY_FA, ITEM_FA
from database import add_coins, update_battle
from images import IMAGES
from quests import update_quest_progress
from jjk_data import (ABILITIES_JJK, DOMAINS_JJK, BOSSES_JJK, FODDER_JJK)
from bleach_data import BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER
from opm_data import BOSSES_OPM


def get_boss_data(boss_name):
    if boss_name in BLEACH_BOSSES:
        data = BLEACH_BOSSES[boss_name]
        return {"hp": data["hp"], "atk": data["atk"], "reward": data["reward"],
                "display_name": data.get("display_name", boss_name)}
    if boss_name in BLEACH_FODDER:
        data = BLEACH_FODDER[boss_name]
        return {"hp": data["hp"], "atk": data["atk"], "reward": data["reward"],
                "display_name": data.get("display_name", boss_name)}
    if boss_name in BOSSES_JJK:
        data = BOSSES_JJK[boss_name]
        return {"hp": data["hp"], "atk": data["atk"], "reward": data["reward"],
                "display_name": data.get("display_name", boss_name)}
    if boss_name in FODDER_JJK:
        data = FODDER_JJK[boss_name]
        return {"hp": data["hp"], "atk": data["atk"], "reward": data["reward"],
                "display_name": data.get("display_name", boss_name)}
    if boss_name in BOSSES_OPM:
        data = BOSSES_OPM[boss_name]
        return {"hp": data["hp"], "atk": data["atk"], "reward": data["reward"],
                "display_name": data.get("display_name", boss_name)}
    if boss_name in BOSSES:
        data = BOSSES[boss_name]
        return {"hp": data["hp"], "atk": data["atk"], "reward": data.get("reward", 5000),
                "display_name": boss_name}
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
    return f"{icon} [{bar}] {current:,}/{maximum:,}"


def format_num(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


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
def apply_defense_check(base_dmg, php, defense_type, char_dodge=0):
    roll = random.randint(1, 100)

    if roll <= 33:
        log = f"✅ {defense_type} کامل! ۰ آسیب"
        return php, log
    elif roll <= 66:
        partial = max(1, int(base_dmg * 0.5))
        php = max(0, php - partial)
        log = f"⚠️ {defense_type} جزئی! {format_num(partial)} آسیب (۵۰٪)"
        return php, log
    else:
        php = max(0, php - base_dmg)
        log = f"❌ {defense_type} ناموفق! {format_num(base_dmg)} آسیب کامل"
        return php, log


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
    if battle.get("bankai_used", 0) != 1:
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
    if battle.get("bankai_used", 0) != 1:
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
def player_attack(battle, char):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    dmg, crit = roll_damage(char[6], 0, 0)
    atk_boost = battle.get("domain_atk_boost", 0)
    if atk_boost:
        dmg = int(dmg * (1 + atk_boost / 100))
    bankai_atk = battle.get("bankai_atk_current", 0)
    if bankai_atk:
        dmg = int(dmg * (1 + bankai_atk / 100))
    bankai = battle.get("bankai_data", {})
    if bankai.get("crit_chance"):
        if random.randint(1, 100) <= bankai["crit_chance"]:
            dmg = int(dmg * 2); crit = True
    if bankai.get("extra_hit_chance"):
        if random.randint(1, 100) <= bankai["extra_hit_chance"]:
            dmg += int(dmg * 0.5)

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

    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n\n❄️ باس فریزه! (نوبت از دست داد)"
    else:
        action = boss_ai(battle["boss_name"], bhp, bmax)
        if action == "attack":
            php, boss_text, _ = boss_attack_player(boss, php, pmax, battle, None)
            text += f"\n\n{boss_text}"
        elif action == "special":
            base_dmg, _ = roll_damage(boss["atk"] * 2, 0, 0)
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

    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n\n❄️ باس فریزه!"
    else:
        action = boss_ai(battle["boss_name"], bhp, bmax)
        if action == "attack":
            php, boss_text, _ = boss_attack_player(boss, php, pmax, battle, "defend")
            text += f"\n\n{boss_text}"
        elif action == "special":
            base_dmg, _ = roll_damage(boss["atk"] * 2, 0, 0)
            php, def_log = apply_defense_check(base_dmg, php, "دفاع")
            text += f"\n\n{box_simple('💥 حمله ویژه باس!')}"
            text += f"\n\n💢 آسیب پایه: {format_num(base_dmg)}"
            text += f"\n{def_log}"
            text += f"\n\n👤 {hp_bar(php, pmax)}"
        elif action == "defend":
            text += f"\n\n🛡️ باس دفاع گرفت."
        elif action == "heal":
            heal = int(bmax * 0.1)
            bhp = min(bmax, bhp + heal)
            text += f"\n\n💚 باس درمان: +{format_num(heal)}"
            text += f"\n👹 {hp_bar(bhp, bmax)}"

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

    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n\n❄️ باس فریزه!"
    else:
        action = boss_ai(battle["boss_name"], bhp, bmax)
        if action == "attack":
            php, boss_text, _ = boss_attack_player(boss, php, pmax, battle, "dodge")
            text += f"\n\n{boss_text}"
        elif action == "special":
            base_dmg, _ = roll_damage(boss["atk"] * 2, 0, 0)
            php, def_log = apply_defense_check(base_dmg, php, "جاخالی")
            text += f"\n\n{box_simple('💥 حمله ویژه باس!')}"
            text += f"\n\n💢 آسیب پایه: {format_num(base_dmg)}"
            text += f"\n{def_log}"
            text += f"\n\n👤 {hp_bar(php, pmax)}"
        elif action == "defend":
            text += f"\n\n🛡️ باس دفاع گرفت."
        elif action == "heal":
            heal = int(bmax * 0.1)
            bhp = min(bmax, bhp + heal)
            text += f"\n\n💚 باس درمان: +{format_num(heal)}"
            text += f"\n👹 {hp_bar(bhp, bmax)}"

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

    # ========== DOMAIN ==========
    if ability_name == "DOMAIN":
        if battle.get("domain_used", 0) == 1:
            return "active", "❌ گسترش قلمرو فقط یه بار!", battle
        domain = DOMAINS_JJK.get(char_name)
        if not domain:
            return "active", "❌ این کاراکتر Domain نداره!", battle
        battle["domain_used"] = 1
        battle["domain_active"] = 1
        battle["domain_turns"] = domain["duration"]
        battle["domain_name"] = domain["name"]
        battle["domain_atk_boost"] = domain["effects"].get("atk_boost", 0)

        dname = domain["name"][:22]
        text = f"╔══════════════════════════╗\n║   🌀 گسترش قلمرو!      ║\n║   {dname.center(22)} ║\n╚══════════════════════════╝"

        effects = domain["effects"]
        if "damage_mult" in effects:
            dmg = int(char[6] * effects["damage_mult"])
            bhp = max(0, bhp - dmg)
            text += f"\n\n⚔️ ضربه قلمرو: {format_num(dmg)} آسیب 💥"
        if "hp_drain" in effects:
            drain = int(bmax * effects["hp_drain"] / 100)
            bhp = max(0, bhp - drain)
            text += f"\n💀 HP باس: -{format_num(drain)}"
        if "freeze" in effects:
            battle["boss_frozen"] = effects["freeze"]
            text += f"\n❄️ باس فریز شد! ({effects['freeze']} راند)"
        if "heal" in effects:
            heal = int(pmax * effects["heal"] / 100)
            php = min(pmax, php + heal)
            text += f"\n💚 {format_num(heal)} HP"
        if "atk_boost" in effects:
            text += f"\n⚔️ ATK +{effects['atk_boost']}٪"

        text += f"\n\n👹 {boss['display_name']}\n{hp_bar(bhp, bmax)}"

        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0:
            return "won", text, battle
        return "active", text, battle

    # ========== BANKAI ==========
    if ability_name == "BANKAI":
        if battle.get("bankai_used", 0) == 1:
            return "active", "❌ Bankai فقط یه بار!", battle
        bankai = BLEACH_BANKAI.get(char_name)
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

        bname = bankai['name'][:22]
        text = f"╔══════════════════════════╗\n║      ⚔️ BANKAI!         ║\n║   {bname.center(22)} ║\n╚══════════════════════════╝"

        if "atk_per_round" in bankai:
            text += f"\n⚔️ ATK +{bankai['atk_per_round']}٪/راند"
        if "dodge_per_round" in bankai:
            text += f"\n💨 دوج +{bankai['dodge_per_round']}٪/راند"
        if "heal_per_round" in bankai:
            text += f"\n💚 HP +{bankai['heal_per_round']}٪/راند"
        if "bleed_per_round" in bankai:
            text += f"\n🩸 باس -{bankai['bleed_per_round']}٪/راند"
        if "crit_chance" in bankai:
            text += f"\n🎯 کریتیکال +{bankai['crit_chance']}٪"
        if "freeze_chance" in bankai:
            text += f"\n❄️ فریز {bankai['freeze_chance']}٪"
        if "extra_hit_chance" in bankai:
            text += f"\n⚡ ضربه اضافه {bankai['extra_hit_chance']}٪"
        if "enemy_atk_debuff" in bankai:
            text += f"\n🔻 ATK باس -{bankai['enemy_atk_debuff']}٪/راند"
        text += "\n\n⏳ تا پایان نبرد"
        return "active", text, battle

    # ========== Ability های خریداری ==========
    used_key = f"used_{ability_name}"
    if battle.get(used_key, 0) == 1:
        return "active", f"❌ {ability_name} قبلاً استفاده شده!", battle

    text = box_simple(f"🔥 {ability_name}!")
    new_bhp = bhp
    new_php = php
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
                if "x5" in eff: mult = 5
                elif "x4" in eff: mult = 4
                elif "x3" in eff: mult = 3
                dmg = char[6] * mult
                new_bhp = max(0, bhp - dmg)
                text += f"\n\n💥 {format_num(dmg)} آسیب ({mult}x)"
            elif ab_type == "multi":
                hits = 3 if "3" in ab["effect"] else 2
                total = sum(char[6] for _ in range(hits))
                new_bhp = max(0, bhp - total)
                text += f"\n\n💥 {hits} ضربه: {format_num(total)}"
            elif ab_type == "gamble":
                if random.randint(1, 100) <= 50:
                    dmg = char[6] * 4
                    text += f"\n\n🎰 برنده! {format_num(dmg)}"
                else:
                    dmg = char[6] * 1
                    text += f"\n\n🎰 باختی! {format_num(dmg)}"
                new_bhp = max(0, bhp - dmg)
            elif ab_type == "heal":
                heal = int(pmax * 0.3)
                new_php = min(pmax, php + heal)
                text += f"\n\n💚 {format_num(heal)} HP"
            elif ab_type == "freeze":
                battle["boss_frozen"] = 1
                text += "\n\n❄️ باس فریز شد"
            elif ab_type == "buff":
                battle["domain_atk_boost"] = 100
                text += "\n\n⚔️ ATK +۱۰۰٪"
            break

    if not found_jjk:
        info = ABILITIES.get(ability_name)
        if not info:
            return "active", "❌ Ability پیدا نشد", battle
        eff = info.get("effect_fa", info.get("effect", ""))
        text += f"\n\n{eff}"
        if "HP +500" in info.get("effect", ""):
            new_php = min(pmax, php + 500)
        elif "HP +200" in info.get("effect", ""):
            new_php = min(pmax, php + 200)
        elif "2 hits" in info.get("effect", ""):
            total = char[6] * 2
            new_bhp = max(0, bhp - total)
            text += f"\n💥 ۲ ضربه: {format_num(total)}"
        elif "ATK +250" in info.get("effect", ""):
            battle["domain_atk_boost"] = 250
        battle[used_key] = 1

    if new_bhp <= 0:
        battle["php"] = new_php; battle["bhp"] = new_bhp
        return "won", text, battle

    if battle.get("boss_frozen", 0) > 0:
        battle["boss_frozen"] -= 1
        text += "\n\n❄️ باس فریزه!"
    else:
        action = boss_ai(battle["boss_name"], new_bhp, bmax)
        if action == "attack":
            new_php, boss_text, _ = boss_attack_player(boss, new_php, pmax, battle, None)
            text += f"\n\n{boss_text}"
        elif action == "special":
            base_dmg, _ = roll_damage(boss["atk"] * 2, 0, 0)
            new_php = max(0, new_php - base_dmg)
            text += f"\n\n{box_simple('💥 حمله ویژه باس!')}"
            text += f"\n\n💢 {format_num(base_dmg)} آسیب!"
            text += f"\n\n👤 {hp_bar(new_php, pmax)}"
        elif action == "defend":
            text += f"\n\n🛡️ باس دفاع گرفت."
        elif action == "heal":
            heal = int(bmax * 0.1)
            new_bhp = min(bmax, new_bhp + heal)
            text += f"\n\n💚 باس درمان: +{format_num(heal)}"
            text += f"\n👹 {hp_bar(new_bhp, bmax)}"

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
    else:
        text += f"\n\n{info.get('effect_fa', info.get('effect', ''))}"

    if new_bhp <= 0:
        battle["php"] = new_php; battle["bhp"] = new_bhp
        return "won", text, battle

    action = boss_ai(battle["boss_name"], new_bhp, bmax)
    if action == "attack":
        new_php, boss_text, _ = boss_attack_player(boss, new_php, pmax, battle, None)
        text += f"\n\n{boss_text}"
    elif action == "special":
        base_dmg, _ = roll_damage(boss["atk"] * 2, 0, 0)
        new_php = max(0, new_php - base_dmg)
        text += f"\n\n{box_simple('💥 حمله ویژه باس!')}"
        text += f"\n\n💢 {format_num(base_dmg)} آسیب!"
        text += f"\n\n👤 {hp_bar(new_php, pmax)}"
    elif action == "defend":
        text += f"\n\n🛡️ باس دفاع گرفت."
    elif action == "heal":
        heal = int(bmax * 0.1)
        new_bhp = min(bmax, new_bhp + heal)
        text += f"\n\n💚 باس درمان: +{format_num(heal)}"
        text += f"\n👹 {hp_bar(new_bhp, bmax)}"

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

    if battle.get("domain_active", 0) == 1:
        text += f"\n\n🌀 قلمرو: {battle.get('domain_name', '')} ({battle.get('domain_turns', 0)} راند)"
    if battle.get("bankai_used", 0) == 1:
        bankai = battle.get("bankai_data", {})
        text += f"\n⚔️ Bankai: {bankai.get('name', '')}"
        atk_b = battle.get("bankai_atk_current", 0)
        dodge_b = battle.get("bankai_dodge_current", 0)
        if atk_b:
            text += f" (ATK +{atk_b}٪"
            if dodge_b:
                text += f"، دوج +{dodge_b}٪)"
            else:
                text += ")"
        elif dodge_b:
            text += f" (دوج +{dodge_b}٪)"

    text += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n🎯 نوبت توئه!"
    return text


def finish_battle(uid, boss_name, won):
    if won:
        boss = get_boss_data(boss_name)
        reward = boss["reward"] if boss else 5000
        add_coins(uid, reward)
        update_quest_progress(uid, "win_3_bosses")
        update_quest_progress(uid, "win_5_bosses")
        if boss_name == "Saitama Phase 1":
            update_quest_progress(uid, "kill_saitama")
        if boss_name.startswith("Goku"):
            update_quest_progress(uid, "kill_goku")

        # 🏰 XP کلن
        try:
            from guild import give_guild_xp
            xp_amount = 5  # پیش‌فرض
            if boss:
                boss_hp = boss.get("hp", 0)
                if boss_hp >= 40000:
                    xp_amount = 20  # قوی
                elif boss_hp >= 20000:
                    xp_amount = 10  # متوسط
                elif boss_hp >= 5000:
                    xp_amount = 5   # ضعیف
                else:
                    xp_amount = 2   # فادر
            give_guild_xp(uid, xp_amount)
        except Exception:
            pass

        return reward
    return 0