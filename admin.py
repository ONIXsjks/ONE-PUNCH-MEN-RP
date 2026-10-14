import sqlite3
from config import DB_NAME, ADMIN_IDS
from database import (add_coins, get_coins, add_admin_db, remove_admin_db,
                      get_admin_db, get_all_admins_db, set_admin_perms_db,
                      has_permission_db, get_admin_perms_list,
                      set_help_db, get_help_db, get_all_help_db,
                      set_char_image_db, get_char_image_db,
                      add_force_channel_db, remove_force_channel_db,
                      get_force_channels_db,
                      set_custom_quest_db, get_custom_quests_db,
                      get_custom_quest_db, PERMISSIONS_LIST)


# ============ OWNER / ADMIN ============

def is_owner(user_id):
    """چک مالک اصلی"""
    return user_id in ADMIN_IDS


def is_admin(user_id):
    """چک ادمین (مالک یا ادمین اضافه شده)"""
    if user_id in ADMIN_IDS:
        return True
    return get_admin_db(user_id) is not None


def has_permission(user_id, permission):
    """چک دسترسی خاص"""
    if user_id in ADMIN_IDS:
        return True  # مالک همه دسترسی‌ها رو داره
    return has_permission_db(user_id, permission)


def get_user_perms(user_id):
    """لیست دسترسی‌های کاربر"""
    if user_id in ADMIN_IDS:
        return ["all"]
    return get_admin_perms_list(user_id)


def add_admin(user_id, permissions="all", added_by=None):
    """اضافه کردن ادمین جدید (فقط مالک)"""
    add_admin_db(user_id, "admin", permissions, added_by)
    return True


def remove_admin(user_id):
    """حذف ادمین (فقط مالک)"""
    if user_id in ADMIN_IDS:
        return False, "❌ نمی‌تونی مالک اصلی رو حذف کنی!"
    remove_admin_db(user_id)
    return True, "✅ ادمین حذف شد!"


def list_admins():
    """لیست همه ادمین‌ها"""
    return get_all_admins_db()


# ============ USERS ============

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


# ============ CHARACTERS ============

def give_character(user_id, char_name, rank, hp, atk, dfn, dodge):
    """دادن کاراکتر به کاربر (ادمین)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM characters WHERE user_id=? AND char_name=?",
              (user_id, char_name))
    if c.fetchone():
        conn.close()
        return False, "❌ کاربر این کاراکتر رو داره!"
    c.execute("""INSERT INTO characters
        (user_id, char_name, rank, level, hp, atk, def, dodge, slots_unlocked, is_active)
        VALUES (?,?,?,1,?,?,?,?,3,0)""",
        (user_id, char_name, rank, hp, atk, dfn, dodge))
    conn.commit()
    conn.close()
    return True, f"✅ کاراکتر {char_name} ({rank}) به کاربر داده شد!"


def reset_character(user_id):
    """ریست همه کاراکترهای کاربر"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM characters WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM abilities_owned WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM buffs WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    return True, "✅ کاراکترهای کاربر ریست شد!"


# ============ HELP ============

def set_help(key, text):
    set_help_db(key, text)
    return True, "✅ Help ذخیره شد!"


def get_help(key, default=""):
    text = get_help_db(key)
    return text if text else default


def get_all_help():
    return get_all_help_db()


# ============ CHAR IMAGES ============

def set_char_image(char_name, image_url):
    set_char_image_db(char_name, image_url)
    return True, f"✅ عکس {char_name} ذخیره شد!"


def get_char_image(char_name):
    return get_char_image_db(char_name)


# ============ FORCE CHANNELS ============

def add_force_channel(channel_id, channel_name=""):
    """اضافه کردن کانال جوین اجباری (حداکثر ۳)"""
    channels = get_force_channels_db()
    if len(channels) >= 3:
        return False, "❌ حداکثر ۳ کانال می‌شه اضافه کرد!"
    add_force_channel_db(channel_id, channel_name)
    return True, f"✅ کانال {channel_name or channel_id} اضافه شد!"


def remove_force_channel(channel_id):
    remove_force_channel_db(channel_id)
    return True, "✅ کانال حذف شد!"


def get_force_channels():
    return get_force_channels_db()


# ============ CUSTOM QUESTS ============

def set_custom_quest(key, desc_text, target, reward):
    set_custom_quest_db(key, desc_text, target, reward)
    return True, f"✅ کوئست {key} ذخیره شد!"


def get_custom_quest(key):
    return get_custom_quest_db(key)


def get_all_custom_quests():
    return get_custom_quests_db()