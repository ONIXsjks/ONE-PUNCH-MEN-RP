import os
from dotenv import load_dotenv

load_dotenv()

from jjk_data import (
    CHARACTERS_JJK, CHAR_PRICES_JJK, ABILITIES_JJK,
    DOMAINS_JJK, BOSSES_JJK, FODDER_JJK, COOLDOWNS_JJK
)

from bleach_data import (
    CHARACTERS_BLEACH, CHAR_PRICES_BLEACH, BLEACH_ABILITIES_SHOP,
    BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER
)

from opm_data import (
    CHARACTERS_OPM, ABILITIES_OPM, BOSSES_OPM
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = "/data/game.db"

START_COINS = 0
DAILY_REWARD = 100
PERFECT_DODGE = 20
COMBO_BONUS = 50
COOP_WIN = 200
GROUP_BOSS_WIN = 400

RANK_STATS = {
    "S": {"hp": 1500, "atk": 300, "def": 100, "dodge": 25, "slots": 8},
    "A": {"hp": 1000, "atk": 200, "def": 70,  "dodge": 20, "slots": 7},
    "B": {"hp": 700,  "atk": 120, "def": 40,  "dodge": 15, "slots": 6},
    "C": {"hp": 400,  "atk": 60,  "def": 20,  "dodge": 10, "slots": 5},
}

FREE_SLOTS = 3

# ============ LEVEL COST (پله‌ای، هر ۱۰ لول دو برابر) ============
LEVEL_COST = [
    (1, 10, 2000),
    (10, 20, 5000),
    (20, 30, 12000),
    (30, 40, 25000),
    (40, 50, 50000),
    (50, 60, 100000),
    (60, 70, 200000),
    (70, 80, 400000),
    (80, 90, 800000),
    (90, 100, 1500000),
    (100, 120, 3000000),
    (120, 150, 6000000),
    (150, 200, 12000000),
    (200, 300, 30000000),
    (300, 400, 70000000),
    (400, 500, 150000000),
]

SLOT_PRICES = {4: 5000, 5: 10000, 6: 18000, 7: 28000, 8: 40000}

ABILITIES = {
    "Iron Skin":       {"effect": "DEF +50",           "effect_fa": "دفاع +۵۰",              "price": 5000},
    "Shadow Step":     {"effect": "DODGE +15%",          "effect_fa": "جاخالی +۱۵٪",            "price": 6000},
    "Counter Attack":  {"effect": "2x after dodge",      "effect_fa": "بعد جاخالی ۲x",          "price": 10000},
    "Heal Pulse":      {"effect": "HP +200 every 3",     "effect_fa": "هر ۳ راند HP +۲۰۰",      "price": 9000},
    "Critical Eye":    {"effect": "20% chance 3x",       "effect_fa": "۲۰٪ شانس ۳x",            "price": 12000},
    "Time Slow":       {"effect": "enemy dodge -20%",    "effect_fa": "جاخالی حریف -۲۰٪",       "price": 15000},
    "Berserker":       {"effect": "ATK +100 (HP<30%)",   "effect_fa": "حمله +۱۰۰ وقتی HP<۳۰٪", "price": 18000},
    "One Punch Dodge": {"effect": "90% dodge Saitama",   "effect_fa": "۹۰٪ جاخالی از سایتاما",  "price": 50000},
    "Mana Shield":     {"effect": "absorb 30%",          "effect_fa": "جذب ۳۰٪ آسیب",           "price": 11000},
    "Speed Boost":     {"effect": "attack first",        "effect_fa": "اول حمله",              "price": 7500},
    "Vampire":         {"effect": "20% dmg = HP",        "effect_fa": "۲۰٪ آسیب = HP",         "price": 14000},
    "Double Strike":   {"effect": "2 hits in 1 turn",    "effect_fa": "۲ ضربه در ۱ نوبت",       "price": 20000},
    "Phoenix Reborn":  {"effect": "revive 50% HP",       "effect_fa": "بازگشت با ۵۰٪ HP",      "price": 30000},
    "Dragon Fist":     {"effect": "ATK +250 (3 turns)",  "effect_fa": "حمله +۲۵۰ (۳ راند)",     "price": 22000},
}

ITEMS = {
    "Health Potion":  {"effect": "HP +500",           "effect_fa": "HP +۵۰۰",           "price": 1500},
    "Mega Potion":    {"effect": "HP +1500",          "effect_fa": "HP +۱۵۰۰",          "price": 3500},
    "Revive Stone":   {"effect": "revive",            "effect_fa": "بازگشت بعد مرگ",     "price": 8000},
    "Damage Boost":   {"effect": "ATK x2 (1 turn)",   "effect_fa": "حمله x۲ (۱ راند)",  "price": 4000},
    "Shield Scroll":  {"effect": "DEF x3 (2 turns)",  "effect_fa": "دفاع x۳ (۲ راند)",  "price": 5000},
    "Lucky Charm":    {"effect": "DODGE +30%",        "effect_fa": "جاخالی +۳۰٪",        "price": 6000},
    "Energy Drink":   {"effect": "extra turn",        "effect_fa": "نوبت اضافه",         "price": 4500},
    "Bomb":           {"effect": "500 damage",        "effect_fa": "۵۰۰ آسیب",           "price": 5500},
    "Smoke Bomb":     {"effect": "DODGE +50%",        "effect_fa": "جاخالی +۵۰٪",        "price": 7000},
}

BUFFS = {
    "HP Buff":        {"effect": "Max HP +500",     "effect_fa": "Max HP +۵۰۰",      "price": 8000},
    "Power Buff":     {"effect": "ATK +150",        "effect_fa": "حمله +۱۵۰",        "price": 9000},
    "Defense Buff":   {"effect": "DEF +80",         "effect_fa": "دفاع +۸۰",         "price": 7000},
    "Speed Buff":     {"effect": "DODGE +10%",      "effect_fa": "جاخالی +۱۰٪",      "price": 8000},
    "Critical Buff":  {"effect": "Crit +15%",       "effect_fa": "شانس کریتیکال +۱۵٪", "price": 10000},
    "Lifesteal Buff": {"effect": "10% dmg = HP",    "effect_fa": "۱۰٪ آسیب = HP",    "price": 11000},
    "Mega Buff":      {"effect": "all +20%",        "effect_fa": "همه +۲۰٪",         "price": 20000},
    "God Buff":       {"effect": "all +50% (1h)",   "effect_fa": "همه +۵۰٪ (۱ ساعت)", "price": 60000},
}

ABILITY_FA = {
    "Iron Skin": "پوست آهنین",
    "Shadow Step": "قدم سایه",
    "Counter Attack": "ضربه متقابل",
    "Heal Pulse": "پالس درمان",
    "Critical Eye": "چشم کریتیکال",
    "Time Slow": "کندی زمان",
    "Berserker": "برزرکر",
    "One Punch Dodge": "جاخالی یک‌ضربه‌ای",
    "Mana Shield": "سپر مانا",
    "Speed Boost": "افزایش سرعت",
    "Vampire": "خون‌آشام",
    "Double Strike": "ضربه دوگانه",
    "Phoenix Reborn": "تولد دوباره ققنوس",
    "Dragon Fist": "مشت اژدها",
}

ITEM_FA = {
    "Health Potion": "معجون کوچک",
    "Mega Potion": "معجون بزرگ",
    "Revive Stone": "سنگ احیا",
    "Damage Boost": "افزایش آسیب",
    "Shield Scroll": "اسکرول سپر",
    "Lucky Charm": "طلسم شانس",
    "Energy Drink": "نوشیدنی انرژی",
    "Bomb": "بمب",
    "Smoke Bomb": "بمب دود",
}

BUFF_FA = {
    "HP Buff": "باف HP",
    "Power Buff": "باف قدرت",
    "Defense Buff": "باف دفاع",
    "Speed Buff": "باف سرعت",
    "Critical Buff": "باف کریتیکال",
    "Lifesteal Buff": "باف خون‌آشام",
    "Mega Buff": "باف مگا",
    "God Buff": "باف خدا",
}

# ============ MERGE CHARACTERS (ادغام Rank ها) ============
CHARACTERS = {}

for rank, chars in CHARACTERS_JJK.items():
    if rank not in CHARACTERS:
        CHARACTERS[rank] = {}
    CHARACTERS[rank].update(chars)

for rank, chars in CHARACTERS_BLEACH.items():
    if rank not in CHARACTERS:
        CHARACTERS[rank] = {}
    CHARACTERS[rank].update(chars)

for rank, chars in CHARACTERS_OPM.items():
    if rank not in CHARACTERS:
        CHARACTERS[rank] = {}
    CHARACTERS[rank].update(chars)

# ============ MERGE CHAR PRICES ============
CHAR_PRICES = {"C": 50000, "B": 150000, "A": 500000, "S": 2000000}
CHAR_PRICES.update(CHAR_PRICES_JJK)
CHAR_PRICES.update(CHAR_PRICES_BLEACH)

# ============ MERGE BOSSES ============
BOSSES = {}
BOSSES.update(BOSSES_JJK)
BOSSES.update(BLEACH_BOSSES)
BOSSES.update(BOSSES_OPM)

# ============ MERGE ABILITIES ============
ABILITIES.update(BLEACH_ABILITIES_SHOP)
ABILITIES.update(ABILITIES_OPM)

# ============ ADMIN ============
ADMIN_IDS = [
    7023690411,
]