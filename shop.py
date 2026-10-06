from config import ABILITIES, ITEMS, BUFFS, SLOT_PRICES, LEVEL_COST, DB_NAME
from database import spend_coins
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

def upgrade_character(user_id, char_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT level, hp, atk, def, dodge FROM characters WHERE id=? AND user_id=?",
              (char_id, user_id))
    row = c.fetchone()
    if not row:
        conn.close()
        return "Character not found."
    level, hp, atk, dfn, dodge = row
    if level >= 100:
        conn.close()
        return "Already Level 100."

    cost = 0
    for lo, hi, price in LEVEL_COST:
        if lo <= level < hi:
            cost = price
            break

    if not spend_coins(user_id, cost):
        conn.close()
        return f"Not enough coins. Need: {cost}"

    c.execute("""UPDATE characters SET level=?, hp=?, atk=?, def=?, dodge=?
                 WHERE id=?""",
              (level + 1, hp + 50, atk + 10, dfn + 5, dodge + 0.5, char_id))
    conn.commit()
    conn.close()
    return f"Upgraded to Level {level + 1}! Cost: {cost}"
