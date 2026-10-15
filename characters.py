from config import RANK_STATS, FREE_SLOTS, DB_NAME, CHAR_PRICES
import sqlite3
from database import get_coins, spend_coins


# ============ STATS LOADER ============

def get_char_stats(char_name, rank):
    """آمار کاراکتر رو از فایل‌های stats می‌خونه"""
    try:
        from jjk_stats import JJK_STATS
        if char_name in JJK_STATS:
            return JJK_STATS[char_name]
    except Exception:
        pass

    try:
        from bleach_stats import BLEACH_STATS
        if char_name in BLEACH_STATS:
            return BLEACH_STATS[char_name]
    except Exception:
        pass

    try:
        from opm_stats import OPM_STATS
        if char_name in OPM_STATS:
            return OPM_STATS[char_name]
    except Exception:
        pass

    # پیش‌فرض: RANK_STATS
    return RANK_STATS.get(rank, RANK_STATS["C"])


def get_char_price(char_name, rank):
    """قیمت کاراکتر رو از stats می‌خونه"""
    stats = get_char_stats(char_name, rank)
    if "price" in stats:
        return stats["price"]
    return CHAR_PRICES.get(rank, 8000)


# ============ CHARACTERS ============

def create_character(user_id, char_name, rank):
    stats = get_char_stats(char_name, rank)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""INSERT INTO characters
        (user_id, char_name, rank, level, hp, atk, def, dodge, slots_unlocked, is_active)
        VALUES (?,?,?,1,?,?,?,?,?,0)""",
        (user_id, char_name, rank,
         stats.get("hp", 400),
         stats.get("atk", 60),
         stats.get("def", 20),
         stats.get("dodge", 10),
         FREE_SLOTS))
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
    price = get_char_price(char_name, rank)
    if not spend_coins(user_id, price):
        return f"Not enough coins. Need: {price}"
    create_character(user_id, char_name, rank)
    return f"Bought {char_name} ({rank} Rank) for {price} coins!"