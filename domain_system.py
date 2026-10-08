import random
from jjk_data import DOMAINS_JJK, COOLDOWNS_JJK


def get_domain(char_name):
    """گرفتن Domain یه کاراکتر"""
    return DOMAINS_JJK.get(char_name, None)


def has_domain(char_name):
    """چک کن کاراکتر Domain داره یا نه"""
    return char_name in DOMAINS_JJK


def start_domain(battle, char_name):
    """شروع گسترش قلمرو"""
    domain = get_domain(char_name)
    if not domain:
        return None

    return {
        "name": domain["name"],
        "type": domain["type"],
        "turns_left": domain["duration"],
        "cooldown": domain["cooldown"],
        "effects": domain["effects"],
        "caster": char_name,
    }


def can_use_domain(battle, char_name):
    """چک کن می‌تونه Domain بزنه"""
    if char_name not in DOMAINS_JJK:
        return False, "❌ این کاراکتر گسترش قلمرو نداره"

    cd_key = f"domain_cd_{char_name}"
    if battle.get(cd_key, 0) > 0:
        return False, f"⏱️ کول‌داون: {battle[cd_key]} راند مونده"

    if battle.get("domain_active"):
        return False, "🌀 یه Domain دیگه فعاله"

    return True, "✅"


def domain_targets(char_name, enemies):
    """انتخاب هدف‌های Domain"""
    domain = DOMAINS_JJK.get(char_name)
    if not domain:
        return []

    dtype = domain["type"]

    if dtype == "single":
        return [enemies[0]] if enemies else []
    elif dtype == "multi":
        return enemies[:2]
    elif dtype == "all":
        return enemies
    return []


def apply_domain_round(battle, player, enemies):
    """اعمال افکت‌های Domain در هر راند"""
    if not battle.get("domain_active"):
        return None

    if battle.get("domain_turns", 0) <= 0:
        battle["domain_active"] = False
        return "🌀 گسترش قلمرو بسته شد"

    effects = battle.get("domain_effects", {})
    log = []

    # هدف‌ها
    targets = domain_targets(battle.get("domain_caster", ""), enemies)

    for target in targets:
        # Bleed (HP drain)
        if "hp_drain" in effects:
            drain = int(target.get("max_hp", target.get("hp", 100)) * effects["hp_drain"] / 100)
            target["hp"] = max(0, target["hp"] - drain)
            log.append(f"💀 {target.get('name', 'دشمن')}: -{drain} HP")

        # Freeze
        if "freeze" in effects:
            target["frozen"] = effects["freeze"]
            log.append(f"❄️ {target.get('name', 'دشمن')} فریز شد")

        # Dodge debuff
        if "dodge_debuff" in effects:
            target["dodge_debuff"] = effects["dodge_debuff"]

    # ATK boost برای خودت
    if "atk_boost" in effects:
        player["atk_boost"] = effects["atk_boost"]
        log.append(f"⚔️ ATK تو +{effects['atk_boost']}٪")

    # Heal
    if "heal_per_turn" in effects:
        heal = int(player.get("max_hp", player["hp"]) * effects["heal_per_turn"] / 100)
        player["hp"] = min(player.get("max_hp", player["hp"]), player["hp"] + heal)
        log.append(f"💚 {heal} HP برگشت")

    # کاهش راند
    battle["domain_turns"] -= 1

    if battle["domain_turns"] <= 0:
        battle["domain_active"] = False
        caster = battle.get("domain_caster", "")
        cd = DOMAINS_JJK.get(caster, {}).get("cooldown", 3)
        battle[f"domain_cd_{caster}"] = cd
        log.append(f"🌀 قلمرو بسته شد — کول‌داون {cd} راند")

    return "\n".join(log) if log else None


def tick_cooldowns(battle):
    """هر راند کول‌داون‌ها رو کم کن"""
    keys = [k for k in battle.keys() if k.startswith("domain_cd_") or k.startswith("cd_")]
    for key in keys:
        if battle[key] > 0:
            battle[key] -= 1
    return battle


def set_cooldown(battle, ability_name, cooldown):
    """تنظیم کول‌داون برای یه Ability"""
    battle[f"cd_{ability_name}"] = cooldown
    return battle


def is_ability_on_cooldown(battle, ability_name):
    """چک کن Ability کول‌داون داره"""
    return battle.get(f"cd_{ability_name}", 0) > 0


def get_cooldown_turns(battle, ability_name):
    """چند راند کول‌داون مونده"""
    return battle.get(f"cd_{ability_name}", 0)
