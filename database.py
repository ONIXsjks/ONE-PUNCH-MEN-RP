import sqlite3
from config import DB_NAME


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        coins INTEGER DEFAULT 0,
        daily_claimed TEXT DEFAULT '',
        banned INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        char_name TEXT,
        rank TEXT,
        level INTEGER DEFAULT 1,
        hp INTEGER,
        atk INTEGER,
        def INTEGER,
        dodge REAL,
        slots_unlocked INTEGER DEFAULT 3,
        is_active INTEGER DEFAULT 0
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS abilities_owned (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        char_name TEXT,
        ability_name TEXT,
        equipped INTEGER DEFAULT 0
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        quantity INTEGER DEFAULT 1
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS buffs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        char_name TEXT,
        buff_name TEXT
    )""")

    # پاک کردن جدول قبلی برای اضافه شدن ستون‌های جدید
    c.execute("DROP TABLE IF EXISTS active_battles")

    c.execute("""CREATE TABLE IF NOT EXISTS active_battles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        boss_name TEXT,
        player_hp INTEGER,
        player_max_hp INTEGER,
        boss_hp INTEGER,
        boss_max_hp INTEGER,
        player_defending INTEGER DEFAULT 0,
        turn INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active',
        domain_used INTEGER DEFAULT 0,
        boss_frozen INTEGER DEFAULT 0,
        domain_active INTEGER DEFAULT 0,
        domain_turns INTEGER DEFAULT 0,
        domain_name TEXT DEFAULT '',
        domain_atk_boost INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()


def get_user(user_id, username=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    u = c.fetchone()
    if not u:
        c.execute("INSERT INTO users (user_id, username, coins) VALUES (?,?,0)",
                  (user_id, username or "Player"))
        conn.commit()
        c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        u = c.fetchone()
    conn.close()
    return u


def add_coins(user_id, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET coins = coins + ? WHERE user_id=?", (amount, user_id))
    conn.commit()
    conn.close()


def get_coins(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT coins FROM users WHERE user_id=?", (user_id,))
    r = c.fetchone()
    conn.close()
    return r[0] if r else 0


def spend_coins(user_id, amount):
    coins = get_coins(user_id)
    if coins < amount:
        return False
    add_coins(user_id, -amount)
    return True


# ============ ACTIVE BATTLES ============

def create_battle(user_id, boss_name, player_hp, boss_hp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM active_battles WHERE user_id=?", (user_id,))
    c.execute("""INSERT INTO active_battles
        (user_id, boss_name, player_hp, player_max_hp, boss_hp, boss_max_hp,
         turn, status, domain_used, boss_frozen, domain_active, domain_turns,
         domain_name, domain_atk_boost)
        VALUES (?,?,?,?,?,?,0,'active',0,0,0,0,'',0)""",
        (user_id, boss_name, player_hp, player_hp, boss_hp, boss_hp))
    bid = c.lastrowid
    conn.commit()
    conn.close()
    return bid


def get_battle(user_id):
    """برگرداندن dict بجای tuple"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT id, user_id, boss_name, player_hp, player_max_hp,
                        boss_hp, boss_max_hp, player_defending, turn, status,
                        domain_used, boss_frozen, domain_active, domain_turns,
                        domain_name, domain_atk_boost
                 FROM active_battles WHERE user_id=? AND status='active'""", (user_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "uid": row[1],
        "boss_name": row[2],
        "php": row[3],
        "pmax": row[4],
        "bhp": row[5],
        "bmax": row[6],
        "defending": row[7],
        "turn": row[8],
        "status": row[9],
        "domain_used": row[10],
        "boss_frozen": row[11],
        "domain_active": row[12],
        "domain_turns": row[13],
        "domain_name": row[14],
        "domain_atk_boost": row[15],
    }


def update_battle(battle, status='active'):
    """برگرداندن dict"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""UPDATE active_battles SET
        player_hp=?, boss_hp=?, turn=?, player_defending=?, status=?,
        domain_used=?, boss_frozen=?, domain_active=?, domain_turns=?,
        domain_name=?, domain_atk_boost=?
        WHERE id=?""",
        (battle["php"], battle["bhp"], battle["turn"],
         battle["defending"], status,
         battle["domain_used"], battle["boss_frozen"],
         battle["domain_active"], battle["domain_turns"],
         battle["domain_name"], battle["domain_atk_boost"],
         battle["id"]))
    conn.commit()
    conn.close()


def end_battle(battle_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM active_battles WHERE id=?", (battle_id,))
    conn.commit()
    conn.close()


def get_abilities(user_id, char_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT ability_name FROM abilities_owned
                 WHERE user_id=? AND char_name=?""", (user_id, char_name))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_items(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT item_name, quantity FROM items WHERE user_id=? AND quantity>0", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows


def use_item(user_id, item_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, quantity FROM items WHERE user_id=? AND item_name=?", (user_id, item_name))
    row = c.fetchone()
    if not row or row[1] <= 0:
        conn.close()
        return False
    if row[1] == 1:
        c.execute("DELETE FROM items WHERE id=?", (row[0],))
    else:
        c.execute("UPDATE items SET quantity = quantity - 1 WHERE id=?", (row[0],))
    conn.commit()
    conn.close()
    return True
