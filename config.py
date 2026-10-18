import os
from dotenv import load_dotenv
load_dotenv()

# ============================================================
# IMPORTS — Old Animes (JJK, Bleach, OPM)
# ============================================================
from jjk_data import (
    CHARACTERS_JJK, CHAR_PRICES_JJK, ABILITIES_JJK,
    DOMAINS_JJK, BOSSES_JJK, FODDER_JJK, COOLDOWNS_JJK
)
from bleach_data import (
    CHARACTERS_BLEACH, CHAR_PRICES_BLEACH, BLEACH_ABILITIES_SHOP,
    BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER, ABILITIES_BLEACH
)
from opm_data import (
    CHARACTERS_OPM, ABILITIES_OPM, BOSSES_OPM
)

# ============================================================
# IMPORTS — 7 Animes (AOT, Black Clover, Berserk, Demon Slayer, Chainsaw Man, Naruto, SDS)
# ============================================================
from aot_data import (
    CHARACTERS_AOT, CHAR_PRICES_AOT, ABILITIES_AOT,
    AOT_BOSSES, AOT_FODDER
)
from blackclover_data import (
    CHARACTERS_BLACKCLOVER, CHAR_PRICES_BLACKCLOVER, ABILITIES_BLACKCLOVER,
    BLACKCLOVER_BOSSES, BLACKCLOVER_FODDER
)
from berserk_data import (
    CHARACTERS_BERSERK, CHAR_PRICES_BERSERK, ABILITIES_BERSERK,
    BERSERK_BOSSES, BERSERK_FODDER
)
from demonslayer_data import (
    CHARACTERS_DEMONSLAYER, CHAR_PRICES_DEMONSLAYER, ABILITIES_DEMONSLAYER,
    DEMONSLAYER_BOSSES, DEMONSLAYER_FODDER
)
from chainsawman_data import (
    CHARACTERS_CHAINSAWMAN, CHAR_PRICES_CHAINSAWMAN, ABILITIES_CHAINSAWMAN,
    CHAINSAWMAN_BOSSES, CHAINSAWMAN_FODDER
)
from naruto_data import (
    CHARACTERS_NARUTO, CHAR_PRICES_NARUTO, ABILITIES_NARUTO,
    NARUTO_BOSSES, NARUTO_FODDER
)
from sevendeadlysins_data import (
    CHARACTERS_SDS, CHAR_PRICES_SDS, ABILITIES_SDS,
    SDS_BOSSES, SDS_FODDER
)

# ============================================================
# IMPORTS — 🆕 8 Animes NEW
# ============================================================
from onepiece_data import (
    CHARACTERS_ONEPIECE, CHAR_PRICES_ONEPIECE, ABILITIES_ONEPIECE,
    ONEPIECE_BOSSES, ONEPIECE_FODDER
)
from dragonball_data import (
    CHARACTERS_DRAGONBALL, CHAR_PRICES_DRAGONBALL, ABILITIES_DRAGONBALL,
    DRAGONBALL_BOSSES, DRAGONBALL_FODDER
)
from hxh_data import (
    CHARACTERS_HXH, CHAR_PRICES_HXH, ABILITIES_HXH,
    HXH_BOSSES, HXH_FODDER
)
from sakamoto_data import (
    CHARACTERS_SAKAMOTO, CHAR_PRICES_SAKAMOTO, ABILITIES_SAKAMOTO,
    SAKAMOTO_BOSSES, SAKAMOTO_FODDER
)
from sololeveling_data import (
    CHARACTERS_SOLOLEVELING, CHAR_PRICES_SOLOLEVELING, ABILITIES_SOLOLEVELING,
    SOLOLEVELING_BOSSES, SOLOLEVELING_FODDER
)
from mushoku_data import (
    CHARACTERS_MUSHOKU, CHAR_PRICES_MUSHOKU, ABILITIES_MUSHOKU,
    MUSHOKU_BOSSES, MUSHOKU_FODDER
)
from codegeass_data import (
    CHARACTERS_CODEGEASS, CHAR_PRICES_CODEGEASS, ABILITIES_CODEGEASS,
    CODEGEASS_BOSSES, CODEGEASS_FODDER
)
from tokyoghoul_data import (
    CHARACTERS_TOKYOGHOUL, CHAR_PRICES_TOKYOGHOUL, ABILITIES_TOKYOGHOUL,
    TOKYOGHOUL_BOSSES, TOKYOGHOUL_FODDER
)

from shop_abilities_extended import (
    AOT_ABILITIES_SHOP, BLACKCLOVER_ABILITIES_SHOP, BERSERK_ABILITIES_SHOP,
    DEMONSLAYER_ABILITIES_SHOP, CHAINSAWMAN_ABILITIES_SHOP,
    EXTENDED_SHOP_ABILITIES, EXTENDED_SHOP_ABILITIES_FA,
)

# ============================================================
# BOT CONFIG
# ============================================================
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
    (1, 10, 2000), (10, 20, 5000), (20, 30, 12000), (30, 40, 25000),
    (40, 50, 50000), (50, 60, 100000), (60, 70, 200000), (70, 80, 400000),
    (80, 90, 800000), (90, 100, 1500000), (100, 120, 3000000),
    (120, 150, 6000000), (150, 200, 12000000), (200, 300, 30000000),
    (300, 400, 70000000), (400, 500, 150000000),
]
SLOT_PRICES = {4: 5000, 5: 10000, 6: 18000, 7: 28000, 8: 40000}

# ============================================================
# 🆕 ENERGY SYSTEMS
# ============================================================
# JJK
JJK_CE_MAX_BASE = 120
JJK_CE_MAX_CAP = 500
JJK_CE_COST_ABILITY_1 = 20
JJK_CE_COST_ABILITY_2 = 20
JJK_CE_COST_ABILITY_3 = 40
JJK_CE_COST_DOMAIN = 50

# Bleach
BLEACH_REI_MAX_BASE = 120
BLEACH_REI_MAX_CAP = 500
BLEACH_REI_COST_ABILITY_1 = 20
BLEACH_REI_COST_ABILITY_2 = 20
BLEACH_REI_COST_ABILITY_3 = 40
BLEACH_REI_COST_BANKAI = 50

# Code Geass
GEASS_MAX_BASE = 120
GEASS_MAX_CAP = 500
GEASS_COST_ABILITY_1 = 20
GEASS_COST_ABILITY_2 = 20
GEASS_COST_ABILITY_3 = 40
GEASS_COST_ULTIMATE = 50

# One Piece
HAKI_MAX_BASE = 120
HAKI_MAX_CAP = 500
HAKI_COST_ABILITY_1 = 20
HAKI_COST_ABILITY_2 = 20
HAKI_COST_ABILITY_3 = 40

# Naruto
NARUTO_CHAKRA_MAX_BASE = 120
NARUTO_CHAKRA_MAX_CAP = 500
NARUTO_CHAKRA_COST_ABILITY_1 = 20
NARUTO_CHAKRA_COST_ABILITY_2 = 20
NARUTO_CHAKRA_COST_ABILITY_3 = 40

# Dragon Ball
DRAGONBALL_KI_MAX_BASE = 120
DRAGONBALL_KI_MAX_CAP = 500
DRAGONBALL_KI_COST_ABILITY_1 = 20
DRAGONBALL_KI_COST_ABILITY_2 = 20
DRAGONBALL_KI_COST_ABILITY_3 = 40

# Solo Leveling
SOLOLEVELING_MANA_MAX_BASE = 120
SOLOLEVELING_MANA_MAX_CAP = 500
SOLOLEVELING_MANA_COST_ABILITY_1 = 20
SOLOLEVELING_MANA_COST_ABILITY_2 = 20
SOLOLEVELING_MANA_COST_ABILITY_3 = 40

# HxH
HXH_NEN_MAX_BASE = 120
HXH_NEN_MAX_CAP = 500
HXH_NEN_COST_ABILITY_1 = 20
HXH_NEN_COST_ABILITY_2 = 20
HXH_NEN_COST_ABILITY_3 = 40

# Mushoku
MUSHOKU_MANA_MAX_BASE = 120
MUSHOKU_MANA_MAX_CAP = 500
MUSHOKU_MANA_COST_ABILITY_1 = 20
MUSHOKU_MANA_COST_ABILITY_2 = 20
MUSHOKU_MANA_COST_ABILITY_3 = 40

# Tokyo Ghoul
TOKYOGHOUL_RC_MAX_BASE = 120
TOKYOGHOUL_RC_MAX_CAP = 500
TOKYOGHOUL_RC_COST_ABILITY_1 = 20
TOKYOGHOUL_RC_COST_ABILITY_2 = 20
TOKYOGHOUL_RC_COST_ABILITY_3 = 40

# Seven Deadly Sins
SDS_MAGIC_MAX_BASE = 120
SDS_MAGIC_MAX_CAP = 500
SDS_MAGIC_COST_ABILITY_1 = 20
SDS_MAGIC_COST_ABILITY_2 = 20
SDS_MAGIC_COST_ABILITY_3 = 40

# Sakamoto
SAKAMOTO_STAMINA_MAX_BASE = 120
SAKAMOTO_STAMINA_MAX_CAP = 500
SAKAMOTO_STAMINA_COST_ABILITY_1 = 20
SAKAMOTO_STAMINA_COST_ABILITY_2 = 20
SAKAMOTO_STAMINA_COST_ABILITY_3 = 40

# AOT
AOT_TITAN_MAX_BASE = 120
AOT_TITAN_MAX_CAP = 500
AOT_TITAN_COST_ABILITY_1 = 20
AOT_TITAN_COST_ABILITY_2 = 20
AOT_TITAN_COST_ABILITY_3 = 40

# Black Clover
BLACKCLOVER_MANA_MAX_BASE = 120
BLACKCLOVER_MANA_MAX_CAP = 500
BLACKCLOVER_MANA_COST_ABILITY_1 = 20
BLACKCLOVER_MANA_COST_ABILITY_2 = 20
BLACKCLOVER_MANA_COST_ABILITY_3 = 40

# Berserk
BERSERK_BLOODLUST_MAX_BASE = 120
BERSERK_BLOODLUST_MAX_CAP = 500
BERSERK_BLOODLUST_COST_ABILITY_1 = 20
BERSERK_BLOODLUST_COST_ABILITY_2 = 20
BERSERK_BLOODLUST_COST_ABILITY_3 = 40

# Demon Slayer
DEMONSLAYER_BREATH_MAX_BASE = 120
DEMONSLAYER_BREATH_MAX_CAP = 500
DEMONSLAYER_BREATH_COST_ABILITY_1 = 20
DEMONSLAYER_BREATH_COST_ABILITY_2 = 20
DEMONSLAYER_BREATH_COST_ABILITY_3 = 40

# Chainsaw Man
CHAINSAWMAN_BLOOD_MAX_BASE = 120
CHAINSAWMAN_BLOOD_MAX_CAP = 500
CHAINSAWMAN_BLOOD_COST_ABILITY_1 = 20
CHAINSAWMAN_BLOOD_COST_ABILITY_2 = 20
CHAINSAWMAN_BLOOD_COST_ABILITY_3 = 40

# OPM
OPM_POWER_MAX_BASE = 120
OPM_POWER_MAX_CAP = 500
OPM_POWER_COST_ABILITY_1 = 20
OPM_POWER_COST_ABILITY_2 = 20
OPM_POWER_COST_ABILITY_3 = 40

# ============================================================
# 🆕 SHOP DATA
# ============================================================
ABILITIES = {
    "Iron Skin": {"effect": "DEF +50", "effect_fa": "دفاع +۵۰", "price": 5000},
    "Shadow Step": {"effect": "DODGE +15%", "effect_fa": "جاخالی +۱۵٪", "price": 6000},
    "Counter Attack": {"effect": "2x after dodge", "effect_fa": "بعد جاخالی ۲x", "price": 10000},
    "Heal Pulse": {"effect": "HP +200 every 3", "effect_fa": "هر ۳ راند HP +۲۰۰", "price": 9000},
    "Critical Eye": {"effect": "20% chance 3x", "effect_fa": "۲۰٪ شانس ۳x", "price": 12000},
    "Time Slow": {"effect": "enemy dodge -20%", "effect_fa": "جاخالی حریف -۲۰٪", "price": 15000},
    "Berserker": {"effect": "ATK +100 (HP<30%)", "effect_fa": "حمله +۱۰۰ وقتی HP<۳۰٪", "price": 18000},
    "One Punch Dodge": {"effect": "90% dodge Saitama", "effect_fa": "۹۰٪ جاخالی از سایتاما", "price": 50000},
    "Mana Shield": {"effect": "absorb 30%", "effect_fa": "جذب ۳۰٪ آسیب", "price": 11000},
    "Speed Boost": {"effect": "attack first", "effect_fa": "اول حمله", "price": 7500},
    "Vampire": {"effect": "20% dmg = HP", "effect_fa": "۲۰٪ آسیب = HP", "price": 14000},
    "Double Strike": {"effect": "2 hits in 1 turn", "effect_fa": "۲ ضربه در ۱ نوبت", "price": 20000},
    "Phoenix Reborn": {"effect": "revive 50% HP", "effect_fa": "بازگشت با ۵۰٪ HP", "price": 30000},
    "Dragon Fist": {"effect": "ATK +250 (3 turns)", "effect_fa": "حمله +۲۵۰ (۳ راند)", "price": 22000},
}

ITEMS = {
    "Health Potion": {"effect": "HP +500", "effect_fa": "HP +۵۰۰", "price": 1500},
    "Mega Potion": {"effect": "HP +1500", "effect_fa": "HP +۱۵۰۰", "price": 3500},
    "Revive Stone": {"effect": "revive", "effect_fa": "بازگشت بعد مرگ", "price": 8000},
    "Damage Boost": {"effect": "ATK x2 (1 turn)", "effect_fa": "حمله x۲ (۱ راند)", "price": 4000},
    "Shield Scroll": {"effect": "DEF x3 (2 turns)", "effect_fa": "دفاع x۳ (۲ راند)", "price": 5000},
    "Lucky Charm": {"effect": "DODGE +30%", "effect_fa": "جاخالی +۳۰٪", "price": 6000},
    "Energy Drink": {"effect": "extra turn", "effect_fa": "نوبت اضافه", "price": 4500},
    "Bomb": {"effect": "500 damage", "effect_fa": "۵۰۰ آسیب", "price": 5500},
    "Smoke Bomb": {"effect": "DODGE +50%", "effect_fa": "جاخالی +۵۰٪", "price": 7000},
    "Jinwoo Sword": {"effect": "ATK +50% (3 turns)", "effect_fa": "ATK +۵۰٪ (۳ راند)", "price": 75000},
    "Shadow Stone": {"effect": "arise boss", "effect_fa": "تبدیل باس به سایه", "price": 50000},
    "Magic Bean": {"effect": "full HP restore", "effect_fa": "پر کردن کامل HP", "price": 45000},
    "Saiyan Crystal": {"effect": "ATK +100% (2 turns)", "effect_fa": "ATK +۱۰۰٪ (۲ راند)", "price": 85000},
    "Lelouch Geass": {"effect": "enemy skip 1 turn", "effect_fa": "دشمن ۱ نوبت محروم", "price": 90000},
    "Zero Mask": {"effect": "DEF +50% (3 turns)", "effect_fa": "DEF +۵۰٪ (۳ راند)", "price": 40000},
    "Sakamoto Chopsticks": {"effect": "double attack 1 turn", "effect_fa": "دابل حمله (۱ نوبت)", "price": 60000},
    "Secret Candy": {"effect": "restore 50% HP", "effect_fa": "بازیابی ۵۰٪ HP", "price": 25000},
    "Kurapika Chain": {"effect": "freeze enemy 1 turn", "effect_fa": "فریز دشمن (۱ نوبت)", "price": 70000},
    "Hisoka Card": {"effect": "double ATK 1 turn", "effect_fa": "دابل ATK (۱ نوبت)", "price": 55000},
    "Sea Meat": {"effect": "restore 70% HP", "effect_fa": "بازیابی ۷۰٪ HP", "price": 35000},
    "One Piece Fragment": {"effect": "ATK+75% DEF+50% 2turn", "effect_fa": "ATK+۷۵٪ DEF+۵۰٪ (۲ راند)", "price": 95000},
    "Kaneki Mask": {"effect": "DEF +75% (2 turns)", "effect_fa": "DEF +۷۵٪ (۲ راند)", "price": 65000},
    "Kaneki Kagune": {"effect": "ATK +80% (3 turns)", "effect_fa": "ATK +۸۰٪ (۳ راند)", "price": 80000},
}

BUFFS = {
    "HP Buff": {"effect": "Max HP +500", "effect_fa": "Max HP +۵۰۰", "price": 8000},
    "Power Buff": {"effect": "ATK +150", "effect_fa": "حمله +۱۵۰", "price": 9000},
    "Defense Buff": {"effect": "DEF +80", "effect_fa": "دفاع +۸۰", "price": 7000},
    "Speed Buff": {"effect": "DODGE +10%", "effect_fa": "جاخالی +۱۰٪", "price": 8000},
    "Critical Buff": {"effect": "Crit +15%", "effect_fa": "شانس کریتیکال +۱۵٪", "price": 10000},
    "Lifesteal Buff": {"effect": "10% dmg = HP", "effect_fa": "۱۰٪ آسیب = HP", "price": 11000},
    "Mega Buff": {"effect": "all +20%", "effect_fa": "همه +۲۰٪", "price": 20000},
    "God Buff": {"effect": "all +50% (1h)", "effect_fa": "همه +۵۰٪ (۱ ساعت)", "price": 60000},
}

ABILITY_FA = {
    "Iron Skin": "پوست آهنین", "Shadow Step": "قدم سایه", "Counter Attack": "ضربه متقابل",
    "Heal Pulse": "پالس درمان", "Critical Eye": "چشم کریتیکال", "Time Slow": "کندی زمان",
    "Berserker": "برزرکر", "One Punch Dodge": "جاخالی یک‌ضربه‌ای", "Mana Shield": "سپر مانا",
    "Speed Boost": "افزایش سرعت", "Vampire": "خون‌آشام", "Double Strike": "ضربه دوگانه",
    "Phoenix Reborn": "تولد دوباره ققنوس", "Dragon Fist": "مشت اژدها",
}
ITEM_FA = {
    "Health Potion": "معجون کوچک", "Mega Potion": "معجون بزرگ", "Revive Stone": "سنگ احیا",
    "Damage Boost": "افزایش آسیب", "Shield Scroll": "اسکرول سپر", "Lucky Charm": "طلسم شانس",
    "Energy Drink": "نوشیدنی انرژی", "Bomb": "بمب", "Smoke Bomb": "بمب دود",
    "Jinwoo Sword": "شمشیر جین‌وو", "Shadow Stone": "سنگ سایه", "Magic Bean": "لوبیای جادویی",
    "Saiyan Crystal": "کریستال سایان", "Lelouch Geass": "گِیاس لولوش", "Zero Mask": "ماسک زیرو",
    "Sakamoto Chopsticks": "چاپ‌استیک ساکاموتو", "Secret Candy": "آب‌نبات مخفی",
    "Kurapika Chain": "زنجیر کوراپیکا", "Hisoka Card": "کارت هیسوکا", "Sea Meat": "گوشت دریایی",
    "One Piece Fragment": "قطعه‌ی وان‌پیس", "Kaneki Mask": "ماسک کانکی", "Kaneki Kagune": "کاگونِه کانکی",
}
BUFF_FA = {
    "HP Buff": "باف HP", "Power Buff": "باف قدرت", "Defense Buff": "باف دفاع",
    "Speed Buff": "باف سرعت", "Critical Buff": "باف کریتیکال", "Lifesteal Buff": "باف خون‌آشام",
    "Mega Buff": "باف مگا", "God Buff": "باف خدا",
}

# ============================================================
# MERGE ALL DATA
# ============================================================
CHARACTERS = {}
for char_dict in [CHARACTERS_JJK, CHARACTERS_BLEACH, CHARACTERS_OPM, CHARACTERS_AOT, 
                  CHARACTERS_BLACKCLOVER, CHARACTERS_BERSERK, CHARACTERS_DEMONSLAYER,
                  CHARACTERS_CHAINSAWMAN, CHARACTERS_NARUTO, CHARACTERS_SDS,
                  CHARACTERS_ONEPIECE, CHARACTERS_DRAGONBALL, CHARACTERS_HXH,
                  CHARACTERS_SAKAMOTO, CHARACTERS_SOLOLEVELING, CHARACTERS_MUSHOKU,
                  CHARACTERS_CODEGEASS, CHARACTERS_TOKYOGHOUL]:
    for rank, chars in char_dict.items():
        if rank not in CHARACTERS: CHARACTERS[rank] = {}
        CHARACTERS[rank].update(chars)

CHAR_PRICES = {"C": 50000, "B": 150000, "A": 500000, "S": 2000000}
CHAR_PRICES.update(CHAR_PRICES_JJK)
CHAR_PRICES.update(CHAR_PRICES_BLEACH)

BOSSES = {}
for boss_dict in [BOSSES_OPM, BOSSES_JJK, BLEACH_BOSSES, AOT_BOSSES, BLACKCLOVER_BOSSES,
                  BERSERK_BOSSES, DEMONSLAYER_BOSSES, CHAINSAWMAN_BOSSES, NARUTO_BOSSES,
                  SDS_BOSSES, ONEPIECE_BOSSES, DRAGONBALL_BOSSES, HXH_BOSSES, SAKAMOTO_BOSSES,
                  SOLOLEVELING_BOSSES, MUSHOKU_BOSSES, CODEGEASS_BOSSES, TOKYOGHOUL_BOSSES]:
    BOSSES.update(boss_dict)

ABILITIES.update(BLEACH_ABILITIES_SHOP)
ABILITIES.update(EXTENDED_SHOP_ABILITIES)

ABILITIES_3 = {}
for abs_dict in [ABILITIES_JJK, ABILITIES_BLEACH, ABILITIES_OPM, ABILITIES_AOT,
                 ABILITIES_BLACKCLOVER, ABILITIES_BERSERK, ABILITIES_DEMONSLAYER,
                 ABILITIES_CHAINSAWMAN, ABILITIES_NARUTO, ABILITIES_SDS,
                 ABILITIES_ONEPIECE, ABILITIES_DRAGONBALL, ABILITIES_HXH, ABILITIES_SAKAMOTO,
                 ABILITIES_SOLOLEVELING, ABILITIES_MUSHOKU, ABILITIES_CODEGEASS, ABILITIES_TOKYOGHOUL]:
    ABILITIES_3.update(abs_dict)

DOMAINS = {}
DOMAINS.update(DOMAINS_JJK)
BANKAI = {}
BANKAI.update(BLEACH_BANKAI)

ULTIMATE_GEASS = {
    "Lelouch Lamperouge": {"name": "Geass of Absolute Command", "effect": "skip_enemy_turn", "duration": 2},
    "Suzaku Kururugi": {"name": "Live Geass", "effect": "atk_boost", "value": 100, "duration": 3},
    "C.C.": {"name": "Immortal Witch's Curse", "effect": "heal", "value": 50, "duration": 1},
    "Charles zi Britannia": {"name": "Ragnarok Connection", "effect": "skip_enemy_turn", "duration": 2},
    "V.V.": {"name": "Geass Cult's Legacy", "effect": "def_boost", "value": 100, "duration": 3},
    "Schneizel el Britannia": {"name": "Checkmate", "effect": "atk_boost", "value": 75, "duration": 2},
    "Bismarck Waldstein": {"name": "Knight of One's Resolve", "effect": "atk_boost", "value": 80, "duration": 2},
    "Marianne vi Britannia": {"name": "Flash of Britannia", "effect": "dodge_boost", "value": 50, "duration": 3},
    "Kallen Stadtfeld": {"name": "Guren's Wrath", "effect": "atk_boost", "value": 90, "duration": 2},
    "Gino Weinberg": {"name": "Knight of Three's Charge", "effect": "atk_boost", "value": 70, "duration": 2},
    "Rolo Lamperouge": {"name": "Time Stop Geass", "effect": "skip_enemy_turn", "duration": 1},
    "Jeremiah Gottwald": {"name": "Orange's Loyalty", "effect": "def_boost", "value": 80, "duration": 2},
    "Anya Alstreim": {"name": "Mordred's Memory", "effect": "atk_boost", "value": 60, "duration": 2},
    "Cornelia li Britannia": {"name": "Witch's Command", "effect": "atk_boost", "value": 75, "duration": 2},
    "Diethard Ried": {"name": "Truth of the World", "effect": "atk_boost", "value": 50, "duration": 2},
}

ABILITY_MULTIPLIERS = {
    "ability_1": 3, "ability_2": 5, "ability_3": 10, "domain": 8, "bankai": 6, "simple": 1,
}

ADMIN_IDS = [7023690411]

# ============================================================
# 🆕 تابع قیمت‌گذاری ارتقای انرژی (بالانس شده)
# ============================================================
def get_energy_upgrade_cost(current_level):
    if current_level < 10: return 50000          # 50 هزار
    elif current_level < 20: return 100000       # 100 هزار
    elif current_level < 30: return 250000       # 250 هزار
    elif current_level < 40: return 500000       # 500 هزار
    elif current_level < 50: return 1000000      # 1 میلیون
    elif current_level < 60: return 2500000      # 2.5 میلیون
    elif current_level < 70: return 5000000      # 5 میلیون
    elif current_level < 80: return 10000000     # 10 میلیون
    elif current_level < 90: return 20000000     # 20 میلیون
    elif current_level < 100: return 35000000    # 35 میلیون
    else: return 50000000                        # 50 میلیون

# 🆕 هزینه فرم گوکو و لوفی
FORM_COST_GOKU = 30
FORM_COST_LUFFY = 30