import sqlite3
from config import DB_NAME, ADMIN_IDS
from database import add_coins, get_coins


def is_admin(user_id):
    return user_id in ADMIN_IDS


def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, username, coins FROM users ORDER BY coins DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def get_user_stats(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, coins FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    c.execute("SELECT char_name, rank, level FROM characters WHERE user_id=?", (user_id,))
    chars = c.fetchall()
    conn.close()
    return user, chars


def give_coins(user_id, amount):
    add_coins(user_id, amount)


def take_coins(user_id, amount):
    current = get_coins(user_id)
    if current < amount:
        return False
    add_coins(user_id, -amount)
    return True


def reset_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM characters WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM abilities_owned WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM items WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM buffs WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM active_battles WHERE user_id=?", (user_id,))
    c.execute("UPDATE users SET coins=0 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()


def ban_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET banned=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()


def unban_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET banned=0 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()


def is_banned(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT banned FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == 1:
        return True
    return False
