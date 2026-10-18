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
        is_active INTEGER DEFAULT 0,
        survival_wave INTEGER DEFAULT 1,
        cursed_energy INTEGER DEFAULT 120,
        max_cursed_energy INTEGER DEFAULT 120,
        reiatsu INTEGER DEFAULT 120,
        max_reiatsu INTEGER DEFAULT 120,
        geass_power INTEGER DEFAULT 120,
        max_geass_power INTEGER DEFAULT 120,
        haki INTEGER DEFAULT 120,
        max_haki INTEGER DEFAULT 120,
        naruto_chakra INTEGER DEFAULT 120,
        max_naruto_chakra INTEGER DEFAULT 120,
        dragonball_ki INTEGER DEFAULT 120,
        max_dragonball_ki INTEGER DEFAULT 120,
        sololeveling_mana INTEGER DEFAULT 120,
        max_sololeveling_mana INTEGER DEFAULT 120,
        hxh_nen INTEGER DEFAULT 120,
        max_hxh_nen INTEGER DEFAULT 120,
        mushoku_mana INTEGER DEFAULT 120,
        max_mushoku_mana INTEGER DEFAULT 120,
        tokyoghoul_rc INTEGER DEFAULT 120,
        max_tokyoghoul_rc INTEGER DEFAULT 120,
        sds_magic INTEGER DEFAULT 120,
        max_sds_magic INTEGER DEFAULT 120,
        sakamoto_stamina INTEGER DEFAULT 120,
        max_sakamoto_stamina INTEGER DEFAULT 120,
        aot_titan INTEGER DEFAULT 120,
        max_aot_titan INTEGER DEFAULT 120,
        blackclover_mana INTEGER DEFAULT 120,
        max_blackclover_mana INTEGER DEFAULT 120,
        berserk_bloodlust INTEGER DEFAULT 120,
        max_berserk_bloodlust INTEGER DEFAULT 120,
        demonslayer_breath INTEGER DEFAULT 120,
        max_demonslayer_breath INTEGER DEFAULT 120,
        chainsawman_blood INTEGER DEFAULT 120,
        max_chainsawman_blood INTEGER DEFAULT 120,
        opm_power INTEGER DEFAULT 120,
        max_opm_power INTEGER DEFAULT 120,
        castle_wave INTEGER DEFAULT 1,
        zombie_wave INTEGER DEFAULT 1,
        tower_wave INTEGER DEFAULT 1
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
        spam_state TEXT DEFAULT 'ability_1',
        goku_form INTEGER DEFAULT 0,
        luffy_form INTEGER DEFAULT 0,
        awaken_blue_used INTEGER DEFAULT 0,
        awaken_red_used INTEGER DEFAULT 0,
        awaken_purple_used INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

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

    c.execute("""CREATE TABLE IF NOT EXISTS admins (
        user_id INTEGER PRIMARY KEY,
        role TEXT DEFAULT 'admin',
        permissions TEXT DEFAULT '',
        added_by INTEGER,
        added_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS help_content (
        key TEXT PRIMARY KEY,
        text TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS char_images (
        char_name TEXT PRIMARY KEY,
        image_url TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS force_channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT UNIQUE,
        channel_name TEXT DEFAULT '',
        added_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS custom_quests (
        key TEXT PRIMARY KEY,
        desc_text TEXT,
        target INTEGER,
        reward INTEGER,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS world_progress (
        user_id INTEGER PRIMARY KEY,
        unlocked_regions TEXT DEFAULT 'forest',
        current_region TEXT DEFAULT 'forest',
        total_explores INTEGER DEFAULT 0,
        treasures_found INTEGER DEFAULT 0,
        bosses_killed INTEGER DEFAULT 0,
        best_region TEXT DEFAULT 'forest',
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS world_treasures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        treasure_name TEXT,
        found_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS shadows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        char_name TEXT,
        shadow_name TEXT,
        atk_bonus INTEGER DEFAULT 25,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    # 🆕 اضافه کردن ستون‌ها به جدول‌های قدیمی
    try: c.execute("ALTER TABLE active_battles ADD COLUMN spam_state TEXT DEFAULT 'ability_1'")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE active_battles ADD COLUMN goku_form INTEGER DEFAULT 0")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE active_battles ADD COLUMN luffy_form INTEGER DEFAULT 0")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE active_battles ADD COLUMN awaken_blue_used INTEGER DEFAULT 0")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE active_battles ADD COLUMN awaken_red_used INTEGER DEFAULT 0")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE active_battles ADD COLUMN awaken_purple_used INTEGER DEFAULT 0")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN survival_wave INTEGER DEFAULT 1")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN cursed_energy INTEGER DEFAULT 120")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN max_cursed_energy INTEGER DEFAULT 120")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN reiatsu INTEGER DEFAULT 120")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN max_reiatsu INTEGER DEFAULT 120")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN geass_power INTEGER DEFAULT 120")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN max_geass_power INTEGER DEFAULT 120")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN haki INTEGER DEFAULT 120")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN max_haki INTEGER DEFAULT 120")
    except sqlite3.OperationalError: pass

    # 🆕 ستون‌های انرژی جدید
    try: c.execute("ALTER TABLE characters ADD COLUMN naruto_chakra INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_naruto_chakra INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN dragonball_ki INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_dragonball_ki INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN sololeveling_mana INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_sololeveling_mana INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN hxh_nen INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_hxh_nen INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN mushoku_mana INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_mushoku_mana INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN tokyoghoul_rc INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_tokyoghoul_rc INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN sds_magic INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_sds_magic INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN sakamoto_stamina INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_sakamoto_stamina INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN aot_titan INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_aot_titan INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN blackclover_mana INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_blackclover_mana INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN berserk_bloodlust INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_berserk_bloodlust INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN demonslayer_breath INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_demonslayer_breath INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN chainsawman_blood INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_chainsawman_blood INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN opm_power INTEGER DEFAULT 120"); c.execute("ALTER TABLE characters ADD COLUMN max_opm_power INTEGER DEFAULT 120")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN castle_wave INTEGER DEFAULT 1")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN zombie_wave INTEGER DEFAULT 1")
    except: pass
    try: c.execute("ALTER TABLE characters ADD COLUMN tower_wave INTEGER DEFAULT 1")
    except: pass

    # 🆕 محدود کردن اتک و HP برای بالانس بازی
    try:
        c.execute("UPDATE characters SET atk = 25000 WHERE atk > 25000")
        c.execute("UPDATE characters SET hp = 50000 WHERE hp > 50000")
    except Exception as e:
        print(f"Balance Error: {e}")

    try:
        c.execute("UPDATE characters SET char_name = 'Harley Quinn' WHERE char_name = 'King'")
        c.execute("UPDATE abilities_owned SET char_name = 'Harley Quinn' WHERE char_name = 'King'")
        c.execute("UPDATE buffs SET char_name = 'Harley Quinn' WHERE char_name = 'King'")
        c.execute("UPDATE active_battles SET boss_name = 'Harley Quinn' WHERE boss_name = 'King'")
    except Exception as e:
        print(f"Rename DB error: {e}")

    conn.commit()
    conn.close()
# ============ USERS ============
def get_user(user_id, username=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    u = c.fetchone()
    if not u:
        c.execute("INSERT INTO users (user_id, username, coins) VALUES (?,?,0)", (user_id, username or "Player"))
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
    if "Survival" in boss_name:
        if "Castle" in boss_name: col = "castle_wave"
        elif "Zombie" in boss_name: col = "zombie_wave"
        elif "Tower" in boss_name: col = "tower_wave"
        else: col = "survival_wave"
        c.execute(f"SELECT {col} FROM characters WHERE user_id=? AND is_active=1", (user_id,))
        row = c.fetchone()
        wave = row[0] if row else 1
        base_hp = 10000
        growth = 1.047
        boss_hp = min(1000000, int(base_hp * (growth ** (wave - 1))))
    
    c.execute("DELETE FROM active_battles WHERE user_id=?", (user_id,))
    c.execute("""INSERT INTO active_battles
        (user_id, boss_name, player_hp, player_max_hp, boss_hp, boss_max_hp,
         turn, status, domain_used, boss_frozen, domain_active, domain_turns,
         domain_name, domain_atk_boost, spam_state, goku_form, luffy_form, awaken_blue_used, awaken_red_used, awaken_purple_used)
        VALUES (?,?,?,?,?,?,0,'active',0,0,0,0,'',0,'ability_1',0,0,0,0,0)""",
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
                        domain_name, domain_atk_boost, spam_state, goku_form, luffy_form,
                        awaken_blue_used, awaken_red_used, awaken_purple_used
                 FROM active_battles WHERE user_id=? AND status='active'""", (user_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0], "uid": row[1], "boss_name": row[2],
        "php": row[3], "pmax": row[4], "bhp": row[5], "bmax": row[6],
        "defending": row[7], "turn": row[8], "status": row[9],
        "domain_used": row[10], "boss_frozen": row[11], "domain_active": row[12],
        "domain_turns": row[13], "domain_name": row[14], "domain_atk_boost": row[15],
        "spam_state": row[16] if len(row) > 16 and row[16] else "ability_1",
        "goku_form": row[17] if len(row) > 17 and row[17] else 0,
        "luffy_form": row[18] if len(row) > 18 and row[18] else 0,
        "awaken_blue_used": row[19] if len(row) > 19 and row[19] else 0,
        "awaken_red_used": row[20] if len(row) > 20 and row[20] else 0,
        "awaken_purple_used": row[21] if len(row) > 21 and row[21] else 0,
    }

def update_battle(battle, status='active'):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT goku_form, luffy_form, awaken_blue_used, awaken_red_used, awaken_purple_used FROM active_battles WHERE id=?", (battle["id"],))
    row = c.fetchone()
    goku_f = battle.get("goku_form", 0)
    luffy_f = battle.get("luffy_form", 0)
    blue_u = battle.get("awaken_blue_used", 0)
    red_u = battle.get("awaken_red_used", 0)
    purple_u = battle.get("awaken_purple_used", 0)
    if row:
        if row[0] is not None and row[0] > goku_f: goku_f = row[0]
        if row[1] is not None and row[1] > luffy_f: luffy_f = row[1]
        if row[2] is not None and row[2] > blue_u: blue_u = row[2]
        if row[3] is not None and row[3] > red_u: red_u = row[3]
        if row[4] is not None and row[4] > purple_u: purple_u = row[4]
    c.execute("""UPDATE active_battles SET
        player_hp=?, boss_hp=?, turn=?, player_defending=?, status=?,
        domain_used=?, boss_frozen=?, domain_active=?, domain_turns=?,
        domain_name=?, domain_atk_boost=?, spam_state=?, goku_form=?, luffy_form=?, awaken_blue_used=?, awaken_red_used=?, awaken_purple_used=? WHERE id=?""",
        (battle["php"], battle["bhp"], battle["turn"],
         battle["defending"], status,
         battle["domain_used"], battle["boss_frozen"],
         battle["domain_active"], battle["domain_turns"],
         battle["domain_name"], battle["domain_atk_boost"],
         battle.get("spam_state", "ability_1"),
         goku_f, luffy_f, blue_u, red_u, purple_u, battle["id"]))
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
    c.execute("SELECT ability_name FROM abilities_owned WHERE user_id=? AND char_name=?", (user_id, char_name))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def remove_user_ability(user_id, char_name, ability_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM abilities_owned WHERE user_id=? AND char_name=? AND ability_name=?", (user_id, char_name, ability_name))
    conn.commit()
    conn.close()

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

# ============ BUFFS ============
def get_user_buffs(user_id, char_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT buff_name FROM buffs WHERE user_id=? AND char_name=?", (user_id, char_name))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def remove_user_buff(user_id, char_name, buff_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM buffs WHERE user_id=? AND char_name=? AND buff_name=?", (user_id, char_name, buff_name))
    conn.commit()
    conn.close()

# ============ SHADOWS (Arise System) ============
def add_shadow(user_id, char_name, shadow_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO shadows (user_id, char_name, shadow_name, atk_bonus) VALUES (?,?,?,25)", (user_id, char_name, shadow_name))
    conn.commit()
    conn.close()

def get_user_shadows(user_id, char_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT shadow_name, atk_bonus FROM shadows WHERE user_id=? AND char_name=?", (user_id, char_name))
    rows = c.fetchall()
    conn.close()
    return rows

def get_shadows_count(user_id, char_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM shadows WHERE user_id=? AND char_name=?", (user_id, char_name))
    count = c.fetchone()[0]
    conn.close()
    return count

def get_shadows_atk_bonus(user_id, char_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(atk_bonus), 0) FROM shadows WHERE user_id=? AND char_name=?", (user_id, char_name))
    total = c.fetchone()[0]
    conn.close()
    return total

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
                 FROM guilds g JOIN guild_members gm ON g.id = gm.guild_id
                 WHERE gm.user_id=?""", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_guilds():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, leader_id, level, xp, treasury, members_count FROM guilds ORDER BY level DESC, treasury DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def search_guilds(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, leader_id, level, xp, treasury, members_count FROM guilds WHERE name LIKE ? ORDER BY level DESC", (f"%{query}%",))
    rows = c.fetchall()
    conn.close()
    return rows

def create_guild(name, leader_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO guilds (name, leader_id, treasury, members_count) VALUES (?,?,0,1)", (name, leader_id))
    gid = c.lastrowid
    c.execute("INSERT INTO guild_members (guild_id, user_id, role) VALUES (?,?,?)", (gid, leader_id, "leader"))
    conn.commit()
    conn.close()
    return gid

def join_guild(guild_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO guild_members (guild_id, user_id) VALUES (?,?)", (guild_id, user_id))
    c.execute("UPDATE guilds SET members_count = members_count + 1 WHERE id=?", (guild_id,))
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
    c.execute("UPDATE guilds SET members_count = members_count - 1 WHERE id=?", (gid,))
    if role == "leader":
        c.execute("DELETE FROM guild_members WHERE guild_id=?", (gid,))
        c.execute("DELETE FROM guilds WHERE id=?", (gid,))
    conn.commit()
    conn.close()
    return True

def get_guild_members(guild_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, role FROM guild_members WHERE guild_id=?", (guild_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def donate_to_guild(guild_id, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE guilds SET treasury = treasury + ? WHERE id=?", (amount, guild_id))
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
    c.execute("UPDATE guilds SET level=?, treasury = treasury - ?, xp = xp - ? WHERE id=?", (new_level, coin_cost, xp_cost, guild_id))
    conn.commit()
    conn.close()

def get_top_guilds(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, leader_id, level, xp, treasury, members_count FROM guilds ORDER BY level DESC, treasury DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
def kick_guild_member(guild_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM guild_members WHERE guild_id=? AND user_id=?", (guild_id, user_id))
    c.execute("UPDATE guilds SET members_count = members_count - 1 WHERE id=?", (guild_id,))
    conn.commit()
    conn.close()

def is_guild_leader(guild_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT leader_id FROM guilds WHERE id=?", (guild_id,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == user_id

# ============ ADMIN ============
def add_admin_db(user_id, role="admin", permissions="", added_by=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO admins (user_id, role, permissions, added_by) VALUES (?,?,?,?)", (user_id, role, permissions, added_by))
    conn.commit()
    conn.close()

def remove_admin_db(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM admins WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_admin_db(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, role, permissions FROM admins WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_admins_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, role, permissions FROM admins ORDER BY added_at")
    rows = c.fetchall()
    conn.close()
    return rows

def set_admin_perms_db(user_id, permissions):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE admins SET permissions=? WHERE user_id=?", (permissions, user_id))
    conn.commit()
    conn.close()

# ============ HELP ============
def set_help_db(key, text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO help_content (key, text, updated_at) VALUES (?,?,CURRENT_TIMESTAMP)", (key, text))
    conn.commit()
    conn.close()

def get_help_db(key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT text FROM help_content WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_help_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT key, text FROM help_content")
    rows = c.fetchall()
    conn.close()
    return rows

# ============ CHAR IMAGES ============
def set_char_image_db(char_name, image_url):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO char_images (char_name, image_url, updated_at) VALUES (?,?,CURRENT_TIMESTAMP)", (char_name, image_url))
    conn.commit()
    conn.close()

def get_char_image_db(char_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT image_url FROM char_images WHERE char_name=?", (char_name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_char_image(char_name):
    return get_char_image_db(char_name)

# ============ FORCE CHANNELS ============
def add_force_channel_db(channel_id, channel_name=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO force_channels (channel_id, channel_name) VALUES (?,?)", (channel_id, channel_name))
    conn.commit()
    conn.close()

def remove_force_channel_db(channel_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM force_channels WHERE channel_id=?", (channel_id,))
    conn.commit()
    conn.close()

def get_force_channels_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT channel_id, channel_name FROM force_channels")
    rows = c.fetchall()
    conn.close()
    return rows

# ============ CUSTOM QUESTS ============
def set_custom_quest_db(key, desc_text, target, reward):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO custom_quests (key, desc_text, target, reward, updated_at) VALUES (?,?,?,?,CURRENT_TIMESTAMP)", (key, desc_text, target, reward))
    conn.commit()
    conn.close()

def get_custom_quests_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT key, desc_text, target, reward FROM custom_quests")
    rows = c.fetchall()
    conn.close()
    return rows

def get_custom_quest_db(key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT key, desc_text, target, reward FROM custom_quests WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row

# ============ WORLD ============
def get_world_progress(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM world_progress WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO world_progress (user_id) VALUES (?)", (user_id,))
        conn.commit()
        c.execute("SELECT * FROM world_progress WHERE user_id=?", (user_id,))
        row = c.fetchone()
    conn.close()
    return row

def update_world_region(user_id, region):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE world_progress SET current_region=? WHERE user_id=?", (region, user_id))
    conn.commit()
    conn.close()

def unlock_world_region(user_id, region):
    progress = get_world_progress(user_id)
    unlocked = progress[1] or "forest"
    regions = unlocked.split(",")
    if region not in regions:
        regions.append(region)
        new_unlocked = ",".join(regions)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE world_progress SET unlocked_regions=? WHERE user_id=?", (new_unlocked, user_id))
        conn.commit()
        conn.close()
        return True
    return False

def increment_world_stat(user_id, stat):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if stat == "explores":
        c.execute("UPDATE world_progress SET total_explores = total_explores + 1 WHERE user_id=?", (user_id,))
    elif stat == "treasures":
        c.execute("UPDATE world_progress SET treasures_found = treasures_found + 1 WHERE user_id=?", (user_id,))
    elif stat == "bosses":
        c.execute("UPDATE world_progress SET bosses_killed = bosses_killed + 1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def add_world_treasure(user_id, treasure_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO world_treasures (user_id, treasure_name) VALUES (?,?)", (user_id, treasure_name))
    conn.commit()
    conn.close()

def get_world_treasures(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT treasure_name, found_at FROM world_treasures WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_world_leaderboard(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, total_explores, treasures_found, bosses_killed FROM world_progress ORDER BY total_explores DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_unlocked_regions(user_id):
    progress = get_world_progress(user_id)
    unlocked = progress[1] or "forest"
    return unlocked.split(",")

def get_current_region(user_id):
    progress = get_world_progress(user_id)
    return progress[2] or "forest"

# ============ GUILD HELPERS ============
GUILD_MAX_MEMBERS = {1: 5, 2: 10, 3: 15, 4: 20, 5: 30, 6: 40, 7: 50, 8: 75, 9: 100, 10: 150}
GUILD_UPGRADE_COST = {1: (5000, 1000000), 2: (10000, 2500000), 3: (20000, 5000000), 4: (40000, 10000000), 5: (80000, 20000000), 6: (150000, 50000000), 7: (300000, 100000000), 8: (500000, 250000000), 9: (1000000, 500000000)}
GUILD_MAX_TREASURY = {1: 5000000, 2: 10000000, 3: 25000000, 4: 50000000, 5: 100000000, 6: 200000000, 7: 500000000, 8: 1000000000, 9: 2500000000, 10: 5000000000}

def get_guild_max_members(level):
    return GUILD_MAX_MEMBERS.get(level, 5)

def get_guild_upgrade_req(level):
    return GUILD_UPGRADE_COST.get(level, None)

def get_guild_max_treasury(level):
    return GUILD_MAX_TREASURY.get(level, 5000000)

def can_upgrade_guild(guild_id):
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
    if guild[4] < xp_needed:
        return False, f"❌ XP کافی نیست!\n⚡ لازم: {xp_needed:,}\n💫 داری: {guild[4]:,}"
    if guild[5] < coin_cost:
        return False, f"❌ خزانه کافی نیست!\n💰 لازم: {coin_cost:,}\n💵 داری: {guild[5]:,}"
    return True, ""

PERMISSIONS_LIST = ["manage_admins", "manage_coins", "manage_chars", "manage_quests", "manage_channels", "manage_help", "manage_images", "ban_users"]

def has_permission_db(user_id, permission):
    admin = get_admin_db(user_id)
    if not admin:
        return False
    perms = admin[2] or ""
    if "all" in perms:
        return True
    return permission in perms

def get_admin_perms_list(user_id):
    admin = get_admin_db(user_id)
    if not admin:
        return []
    perms = admin[2] or ""
    if "all" in perms:
        return PERMISSIONS_LIST
    return [p for p in perms.split(",") if p]

# ============ HELP KEYS ============
HELP_KEYS = ["welcome", "main_menu", "battle_help", "shop_help", "guild_help", "quest_help", "jjk_help", "opm_help", "world_help", "general"]

def get_default_help(key):
    defaults = {
        "welcome": "🎮 به BANG BANG RP خوش اومدی!",
        "main_menu": "منوی اصلی — یکی از دستورات رو انتخاب کن:",
        "battle_help": "⚔️ برای نبرد: /battle بزن",
        "shop_help": "🏪 برای شاپ: /shop بزن",
        "guild_help": "🏰 برای کلن: /guild بزن",
        "quest_help": "📜 برای کوئست: /quests بزن",
        "jjk_help": "🌀 برای جوجوتسو: /jjk بزن",
        "opm_help": "💪 برای One-Punch: /opm بزن",
        "world_help": "🗺️ برای دنیای آزاد: /world بزن",
        "general": "برای راهنما: /help",
    }
    return defaults.get(key, "")

# ============ OWNER RESET ============
def reset_all_players():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM users")
        total = c.fetchone()[0]
        c.execute("UPDATE users SET coins = 0")
        c.execute("DELETE FROM characters")
        c.execute("DELETE FROM abilities_owned")
        c.execute("DELETE FROM buffs")
        c.execute("DELETE FROM active_battles")
        c.execute("DELETE FROM shadows")
        conn.commit()
        return total
    except Exception as e:
        conn.rollback()
        print(f"Reset all error: {e}")
        return 0
    finally:
        conn.close()

def get_total_users_count():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count

def get_shadow_slots(user_id, char_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM shadows WHERE user_id=? AND char_name=?", (user_id, char_name))
    count = c.fetchone()[0]
    conn.close()
    return count
