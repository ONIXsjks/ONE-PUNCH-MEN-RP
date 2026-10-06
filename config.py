شششششimport os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "8908872734:AAEexZRr4WQeKeqMtc5sP_MVXXb4vS2nULk"
DB_NAME = "game.db"

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
    (1, 10, 500),
    (11, 30, 1500),
    (31, 50, 4000),
    (51, 70, 10000),
    (71, 90, 25000),
    (91, 100, 50000),
]

SLOT_PRICES = {4: 10000, 5: 20000, 6: 35000, 7: 55000, 8: 80000}

ABILITIES = {
    "Iron Skin":       {"effect": "DEF +50",           "price": 10000},
    "Shadow Step":     {"effect": "DODGE +15%",          "price": 12500},
    "Counter Attack":  {"effect": "after dodge 2x",      "price": 20000},
    "Heal Pulse":      {"effect": "HP +200 every 3",     "price": 17500},
    "Critical Eye":    {"effect": "20% chance 3x",       "price": 25000},
    "Time Slow":       {"effect": "enemy dodge -20%",    "price": 30000},
    "Berserker":       {"effect": "ATK +100 (HP<30%)",   "price": 35000},
    "God Mode":        {"effect": "1x immortal",         "price": 75000},
    "One Punch Dodge": {"effect": "90% dodge Saitama",   "price": 100000},
    "Mana Shield":     {"effect": "absorb 30%",          "price": 22500},
    "Speed Boost":     {"effect": "attack first",        "price": 15000},
    "Vampire":         {"effect": "20% dmg = HP",        "price": 27500},
    "Double Strike":   {"effect": "2 hits in 1 turn",    "price": 40000},
    "Phoenix Reborn":  {"effect": "revive 50% HP",       "price": 60000},
    "Dragon Fist":     {"effect": "ATK +250 (3 turns)",  "price": 45000},
}

ITEMS = {
    "Health Potion":  {"effect": "HP +500",           "price": 2500},
    "Mega Potion":    {"effect": "HP +1500",          "price": 6000},
    "Revive Stone":   {"effect": "revive",            "price": 15000},
    "Damage Boost":   {"effect": "ATK x2 (1 turn)",   "price": 7500},
    "Shield Scroll":  {"effect": "DEF x3 (2 turns)",  "price": 10000},
    "Lucky Charm":    {"effect": "DODGE +30%",        "price": 12500},
    "Energy Drink":   {"effect": "extra turn",        "price": 9000},
    "Bomb":           {"effect": "500 damage",        "price": 11000},
    "Smoke Bomb":     {"effect": "DODGE +50%",        "price": 14000},
}

BUFFS = {
    "HP Buff":        {"effect": "Max HP +500",     "price": 15000},
    "Power Buff":     {"effect": "ATK +150",        "price": 17500},
    "Defense Buff":   {"effect": "DEF +80",         "price": 14000},
    "Speed Buff":     {"effect": "DODGE +10%",      "price": 16000},
    "Critical Buff":  {"effect": "Crit +15%",       "price": 20000},
    "Lifesteal Buff": {"effect": "10% dmg = HP",    "price": 22500},
    "Mega Buff":      {"effect": "all +20%",        "price": 40000},
    "God Buff":       {"effect": "all +50% (1h)",   "price": 125000},
}

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

CHAR_PRICES = {"C": 15000, "B": 40000, "A": 100000, "S": 250000}

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
