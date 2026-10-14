import sqlite3
from config import DB_NAME


# ============ INIT ============

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

    # ============ GUILD TABLES ============
    c.execute("""CREATE TABLE IF NOT EXISTS guilds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        leader_id INTEGER,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        treasury INTEGER DEFAULT 0,
        members_count INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS guild_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        user_id INTEGER UNIQUE,
        role TEXT DEFAULT 'member',
        joined_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()


# ============ USERS ============

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
    else:
        if username and (not u[1] or u[1] == "Player"):
            c.execute("UPDATE users SET username=? WHERE user_id=?", (username, user_id))
            conn.commit()
            c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
            u = c.fetchone()

    conn.close()
    return u


def get_username(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()

    if row and row[0] and row[0] != "Player":
        return f"@{row[0]}"
    return "ناشناس"


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


# ============ ABILITIES & ITEMS ============

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


# ============ GUILD ============

def get_guild_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM guilds WHERE name=?", (name,))
    row = c.fetchone()
    conn.close()
    return row


def get_guild_by_id(guild_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM guilds WHERE id=?", (guild_id,))
    row = c.fetchone()
    conn.close()
    return row


def get_user_guild(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT g.id, g.name, g.leader_id, g.level, g.xp,
                        g.treasury, g.members_count
                 FROM guilds g
                 JOIN guild_members gm ON g.id = gm.guild_id
                 WHERE gm.user_id=?""", (user_id,))
    row = c.fetchone()
    conn.close()
    return row


def create_guild(name, leader_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO guilds (name, leader_id, treasury, members_count) VALUES (?,?,0,1)",
              (name, leader_id))
    gid = c.lastrowid
    c.execute("INSERT INTO guild_members (guild_id, user_id, role) VALUES (?,?,?)",
              (gid, leader_id, "leader"))
    conn.commit()
    conn.close()
    return gid


def join_guild(guild_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO guild_members (guild_id, user_id) VALUES (?,?)",
              (guild_id, user_id))
    c.execute("UPDATE guilds SET members_count = members_count + 1 WHERE id=?",
              (guild_id,))
    conn.commit()
    conn.close()


def leave_guild(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT guild_id, role FROM guild_members WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False
    gid, role = row[0], row[1]
    c.execute("DELETE FROM guild_members WHERE user_id=?", (user_id,))
    c.execute("UPDATE guilds SET members_count = members_count - 1 WHERE id=?",
              (gid,))
    # اگه لیدر بود، کلن رو حذف کن
    if role == "leader":
        c.execute("DELETE FROM guild_members WHERE guild_id=?", (gid,))
        c.execute("DELETE FROM guilds WHERE id=?", (gid,))
    conn.commit()
    conn.close()
    return True


def get_guild_members(guild_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, role FROM guild_members WHERE guild_id=?",
              (guild_id,))
    rows = c.fetchall()
    conn.close()
    return rows


def donate_to_guild(guild_id, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE guilds SET treasury = treasury + ? WHERE id=?",
              (amount, guild_id))
    conn.commit()
    conn.close()


def add_guild_xp(guild_id, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE guilds SET xp = xp + ? WHERE id=?", (amount, guild_id))
    conn.commit()
    conn.close()


def upgrade_guild(guild_id, new_level, xp_cost, coin_cost):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""UPDATE guilds SET level=?, treasury = treasury - ?,
                 xp = xp - ? WHERE id=?""",
              (new_level, coin_cost, xp_cost, guild_id))
    conn.commit()
    conn.close()


def spend_guild_treasury(guild_id, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE guilds SET treasury = treasury - ? WHERE id=?",
              (amount, guild_id))
    conn.commit()
    conn.close()


def get_all_guilds():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, leader_id, level, xp, treasury, members_count FROM guilds ORDER BY treasury DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return rows


def kick_guild_member(guild_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM guild_members WHERE guild_id=? AND user_id=?",
              (guild_id, user_id))
    c.execute("UPDATE guilds SET members_count = members_count - 1 WHERE id=?",
              (guild_id,))
    conn.commit()
    conn.close()
# ============ GUILD HELPERS ============

GUILD_MAX_MEMBERS = {
    1: 5, 2: 10, 3: 15, 4: 20, 5: 30,
    6: 40, 7: 50, 8: 75, 9: 100, 10: 150,
}

GUILD_UPGRADE_COST = {
    1: (5000, 1000000),
    2: (10000, 2500000),
    3: (20000, 5000000),
    4: (40000, 10000000),
    5: (80000, 20000000),
    6: (150000, 50000000),
    7: (300000, 100000000),
    8: (500000, 250000000),
    9: (1000000, 500000000),
}

GUILD_MAX_TREASURY = {
    1: 5000000, 2: 10000000, 3: 25000000, 4: 50000000,
    5: 100000000, 6: 200000000, 7: 500000000,
    8: 1000000000, 9: 2500000000, 10: 5000000000,
}


def get_guild_max_members(level):
    return GUILD_MAX_MEMBERS.get(level, 5)


def get_guild_upgrade_req(level):
    """(xp_needed, coin_cost)"""
    return GUILD_UPGRADE_COST.get(level, None)


def get_guild_max_treasury(level):
    return GUILD_MAX_TREASURY.get(level, 5000000)


def is_guild_leader(guild_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT leader_id FROM guilds WHERE id=?", (guild_id,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == user_id


def can_upgrade_guild(guild_id):
    """چک کن کلن می‌تونه ارتقا بده یا نه"""
    guild = get_guild_by_id(guild_id)
    if not guild:
        return False, "کلن پیدا نشد"
    level = guild[3]
    if level >= 10:
        return False, "کلن در حداکثر سطحه!"
    req = get_guild_upgrade_req(level)
    if not req:
        return False, "خطا در محاسبه هزینه"
    xp_needed, coin_cost = req
    xp = guild[4]
    treasury = guild[5]
    if xp < xp_needed:
        return False, f"❌ XP کافی نیست!\n⚡ لازم: {xp_needed:,}\n💫 داری: {xp:,}"
    if treasury < coin_cost:
        return False, f"❌ خزانه کافی نیست!\n💰 لازم: {coin_cost:,}\n💵 داری: {treasury:,}"
    return True, ""


def search_guilds(query):
    """جستجوی کلن با اسم مشابه"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, level, members_count FROM guilds WHERE name LIKE ? LIMIT 10",
              (f"%{query}%",))
    rows = c.fetchall()
    conn.close()
    return rows


def get_top_guilds(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT id, name, leader_id, level, xp, treasury, members_count
                 FROM guilds ORDER BY level DESC, treasury DESC LIMIT ?""",
              (limit,))
    rows = c.fetchall()
    conn.close()
    return rows