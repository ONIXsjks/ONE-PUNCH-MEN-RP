from config import ABILITIES, ITEMS, BUFFS, SLOT_PRICES, LEVEL_COST, DB_NAME
from database import spend_coins, get_coins
import sqlite3


def buy_ability(user_id, char_name, ability_name):
    if ability_name not in ABILITIES:
        return "Ability not found."
    price = ABILITIES[ability_name]["price"]
    if not spend_coins(user_id, price):
        return f"Not enough coins. Need: {price}"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO abilities_owned (user_id, char_name, ability_name) VALUES (?,?,?)",
              (user_id, char_name, ability_name))
    conn.commit()
    conn.close()
    return f"Bought {ability_name}!"


def buy_item(user_id, item_name):
    if item_name not in ITEMS:
        return "Item not found."
    price = ITEMS[item_name]["price"]
    if not spend_coins(user_id, price):
        return f"Not enough coins. Need: {price}"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE user_id=? AND item_name=?", (user_id, item_name))
    row = c.fetchone()
    if row:
        c.execute("UPDATE items SET quantity = quantity + 1 WHERE id=?", (row[0],))
    else:
        c.execute("INSERT INTO items (user_id, item_name) VALUES (?,?)", (user_id, item_name))
    conn.commit()
    conn.close()
    return f"Bought {item_name}!"


def buy_buff(user_id, char_name, buff_name):
    if buff_name not in BUFFS:
        return "Buff not found."
    price = BUFFS[buff_name]["price"]
    if not spend_coins(user_id, price):
        return f"Not enough coins. Need: {price}"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO buffs (user_id, char_name, buff_name) VALUES (?,?,?)",
              (user_id, char_name, buff_name))
    conn.commit()
    conn.close()
    return f"{buff_name} activated!"


def buy_slot(user_id, char_id, slot_num):
    if slot_num not in SLOT_PRICES:
        return "Invalid slot."
    price = SLOT_PRICES[slot_num]
    if not spend_coins(user_id, price):
        return f"Not enough coins. Need: {price}"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE characters SET slots_unlocked=? WHERE id=? AND user_id=?",
              (slot_num, char_id, user_id))
    conn.commit()
    conn.close()
    return f"Slot {slot_num} unlocked!"


# ============ UPGRADE ============

def get_upgrade_cost(current_level, target_level):
    """محاسبه هزینه کل برای رسیدن از current_level به target_level"""
    total = 0
    for lvl in range(current_level, target_level):
        cost_per_level = 0
        for lo, hi, price in LEVEL_COST:
            if lo <= lvl < hi:
                cost_per_level = price
                break
        total += cost_per_level
    return total


def get_growth_rates(base_hp, base_atk, base_def, base_dodge):
    """ضریب رشد بر اساس آمار اولیه"""
    return {
        "hp": max(1, base_hp // 25),
        "atk": max(1, base_atk // 25),
        "def": max(1, base_def // 25),
        "dodge": base_dodge / 1000,
    }


def upgrade_character(user_id, char_id, target_level=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT level, hp, atk, def, dodge FROM characters WHERE id=? AND user_id=?",
              (char_id, user_id))
    row = c.fetchone()
    if not row:
        conn.close()
        return "Character not found."

    level, hp, atk, dfn, dodge = row

    # آمار پایه رو از stats بگیر
    c.execute("SELECT char_name, rank FROM characters WHERE id=?", (char_id,))
    char_row = c.fetchone()
    char_name = char_row[0]
    rank = char_row[1]

    # آمار اولیه
    from characters import get_char_stats
    base_stats = get_char_stats(char_name, rank)
    base_hp = base_stats.get("hp", 400)
    base_atk = base_stats.get("atk", 60)
    base_def = base_stats.get("def", 20)
    base_dodge = base_stats.get("dodge", 10)

    # ضریب رشد
    growth = get_growth_rates(base_hp, base_atk, base_def, base_dodge)

    if target_level is None:
        target_level = level + 1

    if target_level > 500:
        conn.close()
        return "❌ سقف لول ۵۰۰ هست!"

    if target_level <= level:
        conn.close()
        return f"❌ لول فعلی: {level} — هدف باید بالاتر باشه!"

    total_cost = get_upgrade_cost(level, target_level)

    coins = get_coins(user_id)
    if coins < total_cost:
        conn.close()
        return f"❌ پول کافی نداری!\n💰 لازم: {total_cost:,}\n💵 داری: {coins:,}"

    spend_coins(user_id, total_cost)

    levels_gained = target_level - level
    new_hp = hp + (growth["hp"] * levels_gained)
    new_atk = atk + (growth["atk"] * levels_gained)
    new_def = dfn + (growth["def"] * levels_gained)
    new_dodge = min(50, dodge + (growth["dodge"] * levels_gained))

    c.execute("""UPDATE characters SET level=?, hp=?, atk=?, def=?, dodge=?
                 WHERE id=?""",
              (target_level, int(new_hp), int(new_atk), int(new_def), round(new_dodge, 1), char_id))
    conn.commit()
    conn.close()
    return f"✅ لول {target_level} شدی!\n💰 هزینه: {total_cost:,} سکه"