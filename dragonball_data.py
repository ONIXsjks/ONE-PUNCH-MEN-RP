# ============================================================
# DRAGON BALL DATA
# ============================================================

CHARACTERS_DRAGONBALL = {
    "S": {
        "Son Goku": "Legendary Super Saiyan",
        "Vegeta": "Prince of Saiyans",
        "Gohan": "Ultimate Gohan",
        "Frieza": "Emperor of Universe 7",
        "Cell": "Perfect Android",
        "Majin Buu": "Innocent Buu",
        "Beerus": "God of Destruction",
        "Whis": "Angel Attendant",
        "Broly": "Legendary Super Saiyan",
        "Jiren": "Pride Trooper",
    },
    "A": {
        "Piccolo": "Namekian Warrior",
        "Trunks": "Future Warrior",
        "Goten": "Saiyan Prodigy",
        "Krillin": "Strongest Human",
        "Android 18": "Infinite Energy Android",
        "Android 17": "Ranger Android",
        "Hit": "Legendary Assassin",
        "Goku Black": "Evil Goku",
        "Zamasu": "Immortal Kai",
        "Toppo": "Pride Trooper",
    },
    "B": {
        "Yamcha": "Desert Bandit",
        "Tien Shinhan": "Crane Student",
        "Chiaotzu": "Psychic Warrior",
        "Master Roshi": "Turtle Hermit",
        "Videl": "Satan City Hero",
        "Pan": "Saiyan Child",
        "Bardock": "Saiyan Father",
        "Raditz": "Low-Class Saiyan",
        "Nappa": "Saiyan Elite",
        "Captain Ginyu": "Ginyu Force Captain",
    },
}

CHAR_PRICES_DRAGONBALL = {"S": 5000000, "A": 600000, "B": 150000}
ABILITIES_DRAGONBALL = {
    # ============ S RANK ============
    "Son Goku": {
        "ability_1": {"name": "Kamehameha", "mult": 3},
        "ability_2": {"name": "Super Saiyan Blue Kaio-ken", "mult": 5},
        "ability_3": {"name": "Ultra Instinct: Silver", "mult": 10, "once": True},
    },
    "Vegeta": {
        "ability_1": {"name": "Galick Gun", "mult": 3},
        "ability_2": {"name": "Final Flash", "mult": 5},
        "ability_3": {"name": "Ultra Ego", "mult": 10, "once": True},
    },
    "Gohan": {
        "ability_1": {"name": "Masenko", "mult": 3},
        "ability_2": {"name": "Father-Son Kamehameha", "mult": 5},
        "ability_3": {"name": "Beast Mode", "mult": 10, "once": True},
    },
    "Frieza": {
        "ability_1": {"name": "Death Beam", "mult": 3},
        "ability_2": {"name": "Death Ball", "mult": 5},
        "ability_3": {"name": "Golden Frieza", "mult": 10, "once": True},
    },
    "Cell": {
        "ability_1": {"name": "Kamehameha", "mult": 3},
        "ability_2": {"name": "Solar Kamehameha", "mult": 5},
        "ability_3": {"name": "Perfect Cell Full", "mult": 10, "once": True},
    },
    "Majin Buu": {
        "ability_1": {"name": "Chocolate Beam", "mult": 3},
        "ability_2": {"name": "Vanishing Ball", "mult": 5},
        "ability_3": {"name": "Kid Buu Form", "mult": 10, "once": True},
    },
    "Beerus": {
        "ability_1": {"name": "Hakai Sphere", "mult": 3},
        "ability_2": {"name": "Beerus Punch", "mult": 5},
        "ability_3": {"name": "Hakai: Destruction", "mult": 10, "once": True},
    },
    "Whis": {
        "ability_1": {"name": "Angel Staff Strike", "mult": 3},
        "ability_2": {"name": "Time Rewind", "mult": 5},
        "ability_3": {"name": "Ultra Instinct Whis", "mult": 10, "once": True},
    },
    "Broly": {
        "ability_1": {"name": "Gigantic Roar", "mult": 3},
        "ability_2": {"name": "Gigantic Impact", "mult": 5},
        "ability_3": {"name": "Legendary Super Saiyan Full", "mult": 10, "once": True},
    },
    "Jiren": {
        "ability_1": {"name": "Power Impact", "mult": 3},
        "ability_2": {"name": "Heatwave", "mult": 5},
        "ability_3": {"name": "Full Power Jiren", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Piccolo": {
        "ability_1": {"name": "Special Beam Cannon", "mult": 3},
        "ability_2": {"name": "Light Grenade", "mult": 5},
        "ability_3": {"name": "Orange Piccolo", "mult": 10, "once": True},
    },
    "Trunks": {
        "ability_1": {"name": "Burning Attack", "mult": 3},
        "ability_2": {"name": "Final Flash", "mult": 5},
        "ability_3": {"name": "Sword of Hope", "mult": 10, "once": True},
    },
    "Goten": {
        "ability_1": {"name": "Kamehameha", "mult": 3},
        "ability_2": {"name": "Gotenks Fusion", "mult": 5},
        "ability_3": {"name": "Super Ghost Kamikaze", "mult": 10, "once": True},
    },
    "Krillin": {
        "ability_1": {"name": "Destructo Disk", "mult": 3},
        "ability_2": {"name": "Solar Flare", "mult": 5},
        "ability_3": {"name": "Kamehameha Full", "mult": 10, "once": True},
    },
    "Android 18": {
        "ability_1": {"name": "Infinity Bullet", "mult": 3},
        "ability_2": {"name": "Energy Blast", "mult": 5},
        "ability_3": {"name": "Android Full Power", "mult": 10, "once": True},
    },
    "Android 17": {
        "ability_1": {"name": "Barrier Punch", "mult": 3},
        "ability_2": {"name": "Photon Flash", "mult": 5},
        "ability_3": {"name": "Super 17 Form", "mult": 10, "once": True},
    },
    "Hit": {
        "ability_1": {"name": "Time Skip", "mult": 3},
        "ability_2": {"name": "Vital Point Attack", "mult": 5},
        "ability_3": {"name": "Time Cage", "mult": 10, "once": True},
    },
    "Goku Black": {
        "ability_1": {"name": "Black Kamehameha", "mult": 3},
        "ability_2": {"name": "Divine Retribution", "mult": 5},
        "ability_3": {"name": "Rosé Full Power", "mult": 10, "once": True},
    },
    "Zamasu": {
        "ability_1": {"name": "Holy Wrath", "mult": 3},
        "ability_2": {"name": "Light of Justice", "mult": 5},
        "ability_3": {"name": "Fused Zamasu", "mult": 10, "once": True},
    },
    "Toppo": {
        "ability_1": {"name": "Justice Flash", "mult": 3},
        "ability_2": {"name": "Justice Rush", "mult": 5},
        "ability_3": {"name": "God of Destruction Mode", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Yamcha": {
        "ability_1": {"name": "Wolf Fang Fist", "mult": 3},
        "ability_2": {"name": "Spirit Ball", "mult": 5},
        "ability_3": {"name": "Wolf Fang Full", "mult": 10, "once": True},
    },
    "Tien Shinhan": {
        "ability_1": {"name": "Dodon Ray", "mult": 3},
        "ability_2": {"name": "Tri-Beam", "mult": 5},
        "ability_3": {"name": "Four Witches Technique", "mult": 10, "once": True},
    },
    "Chiaotzu": {
        "ability_1": {"name": "Psychic Blast", "mult": 3},
        "ability_2": {"name": "Telekinesis", "mult": 5},
        "ability_3": {"name": "Self-Destruct", "mult": 10, "once": True},
    },
    "Master Roshi": {
        "ability_1": {"name": "Kamehameha", "mult": 3},
        "ability_2": {"name": "Mafuba", "mult": 5},
        "ability_3": {"name": "Max Power Form", "mult": 10, "once": True},
    },
    "Videl": {
        "ability_1": {"name": "High Kick", "mult": 3},
        "ability_2": {"name": "Flying Kick", "mult": 5},
        "ability_3": {"name": "Satan Style", "mult": 10, "once": True},
    },
    "Pan": {
        "ability_1": {"name": "Ki Blast", "mult": 3},
        "ability_2": {"name": "Kamehameha", "mult": 5},
        "ability_3": {"name": "Saiyan Child Power", "mult": 10, "once": True},
    },
    "Bardock": {
        "ability_1": {"name": "Final Spirit Cannon", "mult": 3},
        "ability_2": {"name": "Final Revenger", "mult": 5},
        "ability_3": {"name": "Super Saiyan Bardock", "mult": 10, "once": True},
    },
    "Raditz": {
        "ability_1": {"name": "Double Sunday", "mult": 3},
        "ability_2": {"name": "Saturday Crash", "mult": 5},
        "ability_3": {"name": "Great Ape Form", "mult": 10, "once": True},
    },
    "Nappa": {
        "ability_1": {"name": "Bomber DX", "mult": 3},
        "ability_2": {"name": "Volcano Explosion", "mult": 5},
        "ability_3": {"name": "Great Ape Nappa", "mult": 10, "once": True},
    },
    "Captain Ginyu": {
        "ability_1": {"name": "Body Change", "mult": 3},
        "ability_2": {"name": "Milky Cannon", "mult": 5},
        "ability_3": {"name": "Ginyu Force Pose", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
DRAGONBALL_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Raditz": {"display_name": "رادیتز", "hp": 1000, "atk": 80, "reward": 50000},
    "Nappa": {"display_name": "ناپا", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Captain Ginyu": {"display_name": "کاپیتان گینیو", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Perfect Cell": {"display_name": "سل کامل", "hp": 90000, "atk": 4400, "reward": 200000},
    "Majin Buu (Kid)": {"display_name": "ماجین بو (کید)", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Jiren (Full Power)": {"display_name": "جیرن (قدرت کامل)", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
DRAGONBALL_FODDER = {
    "Saibaman": {"display_name": "سایبامن", "hp": 400, "atk": 30, "reward": 5000},
    "Raditz": {"display_name": "رادیتز", "hp": 1000, "atk": 80, "reward": 5000},
    "Nappa": {"display_name": "ناپا", "hp": 1200, "atk": 90, "reward": 5000},
    "Captain Ginyu": {"display_name": "کاپیتان گینیو", "hp": 2000, "atk": 150, "reward": 5000},
}