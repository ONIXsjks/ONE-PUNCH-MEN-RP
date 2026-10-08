import os
from dotenv import load_dotenv

load_dotenv()

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

LEVEL_COST = [
    (1, 10, 300),
    (11, 30, 800),
    (31, 50, 2000),
    (51, 70, 5000),
    (71, 90, 12000),
    (91, 100, 25000),
]

SLOT_PRICES = {4: 5000, 5: 10000, 6: 18000, 7: 28000, 8: 40000}

# ============ ABILITIES ============
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

# ============ ITEMS ============
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

# ============ BUFFS ============
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

# ============ TRANSLATIONS ============
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

# ============ CHARACTERS ============
CHARACTERS = {
    "S": {
        "Blast": "Legendary Hero",
        "Boros": "Space Destroyer",
        "Psykos": "Heavenly General",
        "Orochi": "Monster King",
        "Zomnking": "Brutal",
        "Garou": "Monster Hunter",
        "Metal Bat": "CQC",
        "Tatsumaki": "Terror Sister",
    },
    "A": {
        "Suiryu": "Masked",
        "Bang": "Explosive Engine",
        "Gouketsu": "Former Champion",
        "Amai Mask": "Silver Mask",
        "Genos": "Vengeful Cyborg",
    },
    "B": {
        "Wacsmann": "Tatsumaki's Disciple",
        "Sonic": "Speed Ninja",
        "Mumen Rider": "Justice",
    },
    "C": {
        "Fubuki": "Sweet Talker",
        "King": "Coward Hero",
        "Pri-Pri Prisoner": "Prisoner",
    },
}

CHAR_PRICES = {"C": 8000, "B": 20000, "A": 50000, "S": 120000}

BOSSES = {
    "Wolf Monster":     {"hp": 500,  "atk": 40,  "entry": 0,    "reward": 50},
    "Tiger Beast":      {"hp": 1200, "atk": 80,  "entry": 0,    "reward": 120},
    "Demon Fish":       {"hp": 2500, "atk": 150, "entry": 500,  "reward": 250},
    "Sky King":         {"hp": 4000, "atk": 250, "entry": 1000, "reward": 450},
    "Deep Sea King":    {"hp": 6000, "atk": 350, "entry": 1500, "reward": 750},
    "Elder Centipede":  {"hp": 9000, "atk": 500, "entry": 2500, "reward": 1200},
    "Monster Garou":    {"hp": 12000,"atk": 700, "entry": 4000, "reward": 2000},
    "Saitama Phase 1":  {"hp": 5000, "atk": 9999,"entry": 5000, "reward": 2500},
    "Goku Lv1":         {"hp": 1500, "atk": 150, "entry": 2500, "reward": 1000},
    "Goku Lv2":         {"hp": 3000, "atk": 300, "entry": 4000, "reward": 1500},
    "Goku Lv3":         {"hp": 5000, "atk": 500, "entry": 6000, "reward": 2500},
    "Saitama + Goku":   {"hp": 7000, "atk": 9999,"entry": 10000,"reward": 5000},
}

# ============ ADMIN ============
ADMIN_IDS = [
    7023690411,
]
