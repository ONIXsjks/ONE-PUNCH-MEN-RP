import sqlite3
from config import DB_NAME
from database import get_coins, spend_coins, add_coins


def log_gift(from_id, to_id, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS gift_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INTEGER,
        to_id INTEGER,
        amount INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("INSERT INTO gift_log (from_id, to_id, amount) VALUES (?,?,?)",
              (from_id, to_id, amount))
    conn.commit()
    conn.close()


def send_gift(from_id, to_id, amount):
    if from_id == to_id:
        return "❌ نمی‌تونی به خودت هدیه بدی!"
    if amount <= 0:
        return "❌ مقدار باید بیشتر از ۰ باشه."

    coins = get_coins(from_id)
    if coins < amount:
        return f"❌ Coin کافی نداری. موجودی: {coins}"

    if not spend_coins(from_id, amount):
        return "❌ خطا در پرداخت."

    add_coins(to_id, amount)
    log_gift(from_id, to_id, amount)
    return f"✅ {amount} coin به کاربر {to_id} هدیه دادی!"


def get_gift_history(user_id, limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT from_id, to_id, amount, created_at
                 FROM gift_log
                 WHERE from_id=? OR to_id=?
                 ORDER BY id DESC LIMIT ?""",
              (user_id, user_id, limit))
    rows = c.fetchall()
    conn.close()
    return rows


def get_top_givers(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT from_id, SUM(amount) as total
                 FROM gift_log
                 GROUP BY from_id
                 ORDER BY total DESC LIMIT ?""", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
