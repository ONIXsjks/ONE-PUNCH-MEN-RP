from datetime import datetime
import sqlite3
from config import DB_NAME
from database import add_coins

QUESTS = {
    "win_3_bosses":    {"desc": "Win 3 boss fights",     "target": 3,  "reward": 500},
    "win_5_bosses":    {"desc": "Win 5 boss fights",     "target": 5,  "reward": 1000},
    "kill_saitama":    {"desc": "Defeat Saitama (P1)",   "target": 1,  "reward": 1500},
    "kill_goku":       {"desc": "Defeat Goku (any lv)",  "target": 1,  "reward": 1200},
    "win_1_coop":      {"desc": "Win 1 co-op battle",    "target": 1,  "reward": 800},
    "win_1_pvp":       {"desc": "Win 1 PvP match",       "target": 1,  "reward": 1000},
    "buy_1_ability":   {"desc": "Buy 1 ability",         "target": 1,  "reward": 600},
    "level_up_1":      {"desc": "Level up 1 time",       "target": 1,  "reward": 400},
    "login":           {"desc": "Login today",           "target": 1,  "reward": 200},
}

def init_quests_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS quests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        quest_key TEXT,
        progress INTEGER DEFAULT 0,
        completed INTEGER DEFAULT 0,
        claimed INTEGER DEFAULT 0,
        date TEXT
    )""")
    conn.commit()
    conn.close()

def reset_daily_quests(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM quests WHERE user_id=? AND date=?", (user_id, today))
    count = c.fetchone()[0]
    if count == 0:
        c.execute("DELETE FROM quests WHERE user_id=?", (user_id,))
        for key in QUESTS:
            c.execute("""INSERT INTO quests (user_id, quest_key, progress, date)
                         VALUES (?,?,0,?)""", (user_id, key, today))
        conn.commit()
    conn.close()

def update_quest_progress(user_id, quest_key, amount=1):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT id, progress, completed FROM quests
                 WHERE user_id=? AND quest_key=? AND date=?""",
              (user_id, quest_key, today))
    row = c.fetchone()
    if not row:
        conn.close()
        return
    qid, prog, completed = row
    if completed:
        conn.close()
        return
    new_prog = prog + amount
    target = QUESTS[quest_key]["target"]
    done = 1 if new_prog >= target else 0
    c.execute("""UPDATE quests SET progress=?, completed=?
                 WHERE id=?""", (new_prog, done, qid))
    conn.commit()
    conn.close()

def get_user_quests(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT quest_key, progress, completed, claimed FROM quests
                 WHERE user_id=? AND date=?""", (user_id, today))
    rows = c.fetchall()
    conn.close()
    return rows

def claim_quest(user_id, quest_key):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT id, completed, claimed FROM quests
                 WHERE user_id=? AND quest_key=? AND date=?""",
              (user_id, quest_key, today))
    row = c.fetchone()
    if not row:
        conn.close()
        return "Quest not found."
    qid, completed, claimed = row
    if not completed:
        conn.close()
        return "Quest not completed yet."
    if claimed:
        conn.close()
        return "Already claimed."
    reward = QUESTS[quest_key]["reward"]
    c.execute("UPDATE quests SET claimed=1 WHERE id=?", (qid,))
    conn.commit()
    conn.close()
    add_coins(user_id, reward)
    return f"Claimed! +{reward} coins"
