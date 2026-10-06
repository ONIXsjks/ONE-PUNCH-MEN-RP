from config import RANK_STATS, FREE_SLOTS, DB_NAME, CHAR_PRICES
import sqlite3
from database import get_coins, spend_coins

def create_character(user_id, char_name, rank):
    stats = RANK_STATS[rank]
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""INSERT INTO characters
        (user_id, char_name, rank, level, hp, atk, def, dodge, slots_unlocked, is_active)
        VALUES (?,?,?,1,?,?,?,?,?,0)""",
        (user_id, char_name, rank, stats["hp"], stats["atk"],
         stats["def"], stats["dodge"], FREE_SLOTS))
    conn.commit()
    conn.close()

def get_user_characters(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM characters WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_active_character(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM characters WHERE user_id=? AND is_active=1", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def set_active(user_id, char_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE characters SET is_active=0 WHERE user_id=?", (user_id,))
    c.execute("UPDATE characters SET is_active=1 WHERE id=? AND user_id=?", (char_id, user_id))
    conn.commit()
    conn.close()

def buy_character(user_id, char_name, rank):
    price = CHAR_PRICES[rank]
    if not spend_coins(user_id, price):
        return f"Not enough coins. Need: {price}"
    create_character(user_id, char_name, rank)
    return f"Bought {char_name} ({rank} Rank) for {price} coins!"
