import sqlite3
from config import DB_NAME

def get_top_by_coins(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT username, coins FROM users
                 ORDER BY coins DESC LIMIT ?""", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_top_by_level(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT u.username, ch.char_name, ch.rank, ch.level
                 FROM characters ch
                 JOIN users u ON u.user_id = ch.user_id
                 ORDER BY ch.level DESC LIMIT ?""", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_top_by_rank(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT u.username, ch.char_name, ch.rank
                 FROM characters ch
                 JOIN users u ON u.user_id = ch.user_id
                 ORDER BY
                    CASE ch.rank
                        WHEN 'S' THEN 1
                        WHEN 'A' THEN 2
                        WHEN 'B' THEN 3
                        WHEN 'C' THEN 4
                    END ASC LIMIT ?""", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
