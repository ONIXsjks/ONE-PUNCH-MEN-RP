import random
import sqlite3
from config import DB_NAME
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ============================================================
# 🧠 SOUL SYSTEM - سیستم شخصیت با اراده
# ============================================================

# دیتای شخصیت‌ها (چون بخش جداست، اینجا تعریف می‌کنیم)
CHARACTER_SOULS = {
    "Sukuna": {"obedience": 10, "pride": 100, "fear": 0, "title": "پادشاه نفرین‌ها"},
    "Gojo Satoru": {"obedience": 30, "pride": 95, "fear": 0, "title": "قوی‌ترین جوجوتسو سورسرر"},
    "Levi Ackerman": {"obedience": 90, "pride": 40, "fear": 10, "title": "قوی‌ترین سرباز بشریت"},
    "Zenitsu Agatsuma": {"obedience": 80, "pride": 10, "fear": 95, "title": "شمشیرزن ترسو"},
    "Saitama": {"obedience": 20, "pride": 100, "fear": 0, "title": "قهرمان کچل"},
    "Monkey D. Luffy": {"obedience": 80, "pride": 90, "fear": 10, "title": "پادشاه دزدان دریایی"},
    "Ichigo Kurosaki": {"obedience": 75, "pride": 70, "fear": 20, "title": "جایگزین شینیگامی"},
    "Naruto Uzumaki": {"obedience": 85, "pride": 60, "fear": 15, "title": "هوکاگه هفتم"},
    "Eren Yeager": {"obedience": 40, "pride": 85, "fear": 20, "title": "تایتان حمله"},
    "Sung Jin-Woo": {"obedience": 70, "pride": 80, "fear": 5, "title": "پادشاه سایه‌ها"},
    # بقیه کاراکترها به صورت پیش‌فرض این مقادیر رو می‌گیرن
}

DEFAULT_SOUL = {"obedience": 70, "pride": 50, "fear": 30, "title": "مبارز ناشناس"}

def init_soul_db():
    """ساخت جدول اختصاصی سیستم روح"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS char_souls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        char_name TEXT,
        obedience INTEGER DEFAULT 70,
        pride INTEGER DEFAULT 50,
        fear INTEGER DEFAULT 30,
        trust INTEGER DEFAULT 50,
        UNIQUE(user_id, char_name)
    )""")
    conn.commit()
    conn.close()

def get_soul(user_id, char_name):
    """گرفتن اطلاعات روح کاراکتر (اگه نبود، می‌سازه)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT obedience, pride, fear, trust FROM char_souls WHERE user_id=? AND char_name=?", (user_id, char_name))
    row = c.fetchone()
    if not row:
        # اگه کاراکتر توی لیست بود، از لیست بگیر، وگرنه پیش‌فرض
        base = CHARACTER_SOULS.get(char_name, DEFAULT_SOUL)
        c.execute("INSERT INTO char_souls (user_id, char_name, obedience, pride, fear, trust) VALUES (?,?,?,?,?,50)",
                  (user_id, char_name, base["obedience"], base["pride"], base["fear"]))
        conn.commit()
        row = (base["obedience"], base["pride"], base["fear"], 50)
    conn.close()
    return {"obedience": row[0], "pride": row[1], "fear": row[2], "trust": row[3]}

def update_trust(user_id, char_name, amount):
    """کم و زیاد کردن اعتماد"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE char_souls SET trust = MAX(0, MIN(100, trust + ?)) WHERE user_id=? AND char_name=?", (amount, user_id, char_name))
    conn.commit()
    conn.close()

def check_obedience(user_id, char_name, command, current_hp, max_hp):
    """
    بررسی اینکه آیا کاراکتر دستور رو اجرا می‌کنه یا نه
    خروجی: (obeyed: bool, final_command: str, message: str, trust_change: int)
    """
    soul = get_soul(user_id, char_name)
    
    # شانس پایه اطاعت
    obey_chance = soul["obedience"] / 100.0
    
    # اعتماد تاثیر داره
    obey_chance += (soul["trust"] - 50) / 200.0
    
    # غرور: اگه دستور دفاع باشه، غرور کمش می‌کنه
    if command in ["defend", "dodge"]:
        obey_chance -= (soul["pride"] / 250.0)
    
    # ترس: اگه HP کم باشه و دستور حمله باشه، ترس باعث فرار می‌شه
    if command == "attack" and current_hp < (max_hp * 0.3):
        obey_chance -= (soul["fear"] / 200.0)
    
    # محدود کردن شانس
    obey_chance = max(0.05, min(0.95, obey_chance))
    
    if random.random() < obey_chance:
        return True, command, "", 0  # اطاعت کرد
    
    # === نافرمانی ===
    trust_change = -3  # نافرمانی اعتماد رو کم می‌کنه
    
    if soul["pride"] > 60 and command in ["defend", "dodge"]:
        return False, "attack", f"😤 **{char_name} از دستور تو سرپیچی کرد!**\n«{soul['title']} هرگز عقب نمی‌کشه!»\n\n", trust_change
    elif soul["fear"] > 60 and command == "attack":
        return False, "defend", f"😨 **{char_name} ترسید و عقب کشید!**\n«{soul['title']} از این مبارزه می‌ترسه...»\n\n", trust_change
    else:
        rebel_move = random.choice(["attack", "dodge", "defend"])
        return False, rebel_move, f"🤬 **{char_name} به حرفت گوش نداد و خودسرانه عمل کرد!**\n\n", trust_change

def get_soul_view(user_id, char_name):
    """نمایش کارت روح کاراکتر"""
    soul = get_soul(user_id, char_name)
    base = CHARACTER_SOULS.get(char_name, DEFAULT_SOUL)
    title = base.get("title", "مبارز")
    
    def bar(val, length=10):
        filled = int((val / 100) * length)
        return "█" * filled + "░" * (length - filled)
    
    text = f"╔══════════════════════════╗\n"
    text += f"║  🧠 روح {char_name[:15].center(15)} ║\n"
    text += f"╚══════════════════════════╝\n\n"
    text += f"🎭 {title}\n\n"
    text += f"🛡️ اطاعت:  [{bar(soul['obedience'])}] {soul['obedience']}%\n"
    text += f"👑 غرور:   [{bar(soul['pride'])}] {soul['pride']}%\n"
    text += f"😨 ترس:    [{bar(soul['fear'])}] {soul['fear']}%\n"
    text += f"🤝 اعتماد: [{bar(soul['trust'])}] {soul['trust']}%\n\n"
    
    # تفسیر
    if soul['trust'] < 30:
        text += "⚠️ کاراکترت بهت اعتماد نداره! ممکنه نافرمانی کنه."
    elif soul['trust'] > 80:
        text += "💚 کاراکترت کاملاً بهت اعتماد داره و مطیعه."
    else:
        text += "🤔 رابطه‌تون عادیه."
    
    return text

def soul_menu_callback_data(char_name):
    """ساخت دکمه‌های منوی روح"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 پروفایل روح", callback_data=f"soul_view_{char_name}")],
        [InlineKeyboardButton("🤝 آموزش (افزایش اعتماد)", callback_data=f"soul_train_{char_name}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="soul_back")]
    ])