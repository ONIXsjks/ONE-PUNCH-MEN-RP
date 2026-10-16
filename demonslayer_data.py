# ============================================================
# DEMON SLAYER DATA
# ============================================================

CHARACTERS_DEMONSLAYER = {
    "S": {
        "Muzan Kibutsuji": "Demon King",
        "Kokushibo": "Upper Moon One",
        "Doma": "Upper Moon Two",
        "Akaza": "Upper Moon Three",
        "Gyomei Himejima": "Stone Hashira",
        "Sanemi Shinazugawa": "Wind Hashira",
        "Kyojuro Rengoku": "Flame Hashira",
        "Giyu Tomioka": "Water Hashira",
        "Muichiro Tokito": "Mist Hashira",
        "Tanjiro Kamado": "Sun Breathing",
    },
    "A": {
        "Shinobu Kocho": "Insect Hashira",
        "Mitsuri Kanroji": "Love Hashira",
        "Obanai Iguro": "Serpent Hashira",
        "Tengen Uzui": "Sound Hashira",
        "Nezuko Kamado": "Demon Form",
        "Zenitsu Agatsuma": "Thunder Breathing",
        "Inosuke Hashibira": "Beast Breathing",
        "Kanao Tsuyuri": "Flower Breathing",
        "Genya Shinazugawa": "Demon Slayer",
        "Hantengu": "Upper Moon Four",
    },
    "B": {
        "Gyokko": "Upper Moon Five",
        "Nakime": "Upper Moon Four",
        "Kaigaku": "Upper Moon Six",
        "Enmu": "Lower Moon One",
        "Rui": "Lower Moon Five",
        "Kagaya Ubuyashiki": "Demon Slayer Leader",
        "Murata": "Demon Slayer",
        "Sakonji Urokodaki": "Water Breathing Trainer",
        "Jigoro Kuwajima": "Thunder Breathing Trainer",
        "Shinjuro Rengoku": "Former Flame Hashira",
    },
}

CHAR_PRICES_DEMONSLAYER = {"S": 2000000, "A": 500000, "B": 150000}

ABILITIES_DEMONSLAYER = {
    # ============ S RANK ============
    "Muzan Kibutsuji": {
        "ability_1": {"name": "Blood Whip", "mult": 3},
        "ability_2": {"name": "Flesh Claw", "mult": 5},
        "ability_3": {"name": "Demon King Form", "mult": 10, "once": True},
    },
    "Kokushibo": {
        "ability_1": {"name": "Moon Slash", "mult": 3},
        "ability_2": {"name": "Moon Breathing", "mult": 5},
        "ability_3": {"name": "14th Form", "mult": 10, "once": True},
    },
    "Doma": {
        "ability_1": {"name": "Ice Breath", "mult": 3},
        "ability_2": {"name": "Frozen Lotus", "mult": 5},
        "ability_3": {"name": "Ice Buddha", "mult": 10, "once": True},
    },
    "Akaza": {
        "ability_1": {"name": "Destructive Fist", "mult": 3},
        "ability_2": {"name": "Annihilation Type", "mult": 5},
        "ability_3": {"name": "Compass Needle", "mult": 10, "once": True},
    },
    "Gyomei Himejima": {
        "ability_1": {"name": "Stone Flail", "mult": 3},
        "ability_2": {"name": "Stone Pillar", "mult": 5},
        "ability_3": {"name": "Stone Breathing Full", "mult": 10, "once": True},
    },
    "Sanemi Shinazugawa": {
        "ability_1": {"name": "Wind Slash", "mult": 3},
        "ability_2": {"name": "Gale Rush", "mult": 5},
        "ability_3": {"name": "Wind Breathing Full", "mult": 10, "once": True},
    },
    "Kyojuro Rengoku": {
        "ability_1": {"name": "Flame Slash", "mult": 3},
        "ability_2": {"name": "Flame Tiger", "mult": 5},
        "ability_3": {"name": "9th Form: Rengoku", "mult": 10, "once": True},
    },
    "Giyu Tomioka": {
        "ability_1": {"name": "Water Slash", "mult": 3},
        "ability_2": {"name": "Dead Calm", "mult": 5},
        "ability_3": {"name": "11th Form", "mult": 10, "once": True},
    },
    "Muichiro Tokito": {
        "ability_1": {"name": "Mist Slash", "mult": 3},
        "ability_2": {"name": "Mist Cloud", "mult": 5},
        "ability_3": {"name": "7th Form: Obscuring", "mult": 10, "once": True},
    },
    "Tanjiro Kamado": {
        "ability_1": {"name": "Water Slash", "mult": 3},
        "ability_2": {"name": "Hinokami Kagura", "mult": 5},
        "ability_3": {"name": "Sun Breathing 13th", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Shinobu Kocho": {
        "ability_1": {"name": "Insect Stab", "mult": 3},
        "ability_2": {"name": "Wisteria Poison", "mult": 5},
        "ability_3": {"name": "Insect Breathing Full", "mult": 10, "once": True},
    },
    "Mitsuri Kanroji": {
        "ability_1": {"name": "Love Slash", "mult": 3},
        "ability_2": {"name": "Whip Blade", "mult": 5},
        "ability_3": {"name": "6th Form: Cat-Legged", "mult": 10, "once": True},
    },
    "Obanai Iguro": {
        "ability_1": {"name": "Serpent Slash", "mult": 3},
        "ability_2": {"name": "Snake Fang", "mult": 5},
        "ability_3": {"name": "9th Form: Serpent", "mult": 10, "once": True},
    },
    "Tengen Uzui": {
        "ability_1": {"name": "Sound Slash", "mult": 3},
        "ability_2": {"name": "Explosive Bomb", "mult": 5},
        "ability_3": {"name": "Musical Score", "mult": 10, "once": True},
    },
    "Nezuko Kamado": {
        "ability_1": {"name": "Blood Burn", "mult": 3},
        "ability_2": {"name": "Demon Kick", "mult": 5},
        "ability_3": {"name": "Exploding Blood", "mult": 10, "once": True},
    },
    "Zenitsu Agatsuma": {
        "ability_1": {"name": "Thunder Slash", "mult": 3},
        "ability_2": {"name": "Thunderclap", "mult": 5},
        "ability_3": {"name": "7th Form: Flaming", "mult": 10, "once": True},
    },
    "Inosuke Hashibira": {
        "ability_1": {"name": "Beast Slash", "mult": 3},
        "ability_2": {"name": "Fang Rush", "mult": 5},
        "ability_3": {"name": "Beast Breathing Full", "mult": 10, "once": True},
    },
    "Kanao Tsuyuri": {
        "ability_1": {"name": "Flower Slash", "mult": 3},
        "ability_2": {"name": "Final Form", "mult": 5},
        "ability_3": {"name": "Flower Breathing Full", "mult": 10, "once": True},
    },
    "Genya Shinazugawa": {
        "ability_1": {"name": "Shotgun Blast", "mult": 3},
        "ability_2": {"name": "Demon Bite", "mult": 5},
        "ability_3": {"name": "Demon Form", "mult": 10, "once": True},
    },
    "Hantengu": {
        "ability_1": {"name": "Emotion Clone", "mult": 3},
        "ability_2": {"name": "Zohakuten", "mult": 5},
        "ability_3": {"name": "Hatred Form", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Gyokko": {
        "ability_1": {"name": "Fish Punch", "mult": 3},
        "ability_2": {"name": "Water Prison", "mult": 5},
        "ability_3": {"name": "True Form", "mult": 10, "once": True},
    },
    "Nakime": {
        "ability_1": {"name": "Biwa Strike", "mult": 3},
        "ability_2": {"name": "Infinite Castle", "mult": 5},
        "ability_3": {"name": "Biwa Control", "mult": 10, "once": True},
    },
    "Kaigaku": {
        "ability_1": {"name": "Thunder Slash", "mult": 3},
        "ability_2": {"name": "Dark Thunder", "mult": 5},
        "ability_3": {"name": "5th Form", "mult": 10, "once": True},
    },
    "Enmu": {
        "ability_1": {"name": "Sleep Spell", "mult": 3},
        "ability_2": {"name": "Dream Trap", "mult": 5},
        "ability_3": {"name": "Dream Eater", "mult": 10, "once": True},
    },
    "Rui": {
        "ability_1": {"name": "Spider Thread", "mult": 3},
        "ability_2": {"name": "Steel Web", "mult": 5},
        "ability_3": {"name": "Spider Demon Full", "mult": 10, "once": True},
    },
    "Kagaya Ubuyashiki": {
        "ability_1": {"name": "Curse Mark", "mult": 3},
        "ability_2": {"name": "Final Plan", "mult": 5},
        "ability_3": {"name": "Ubuyashiki Will", "mult": 10, "once": True},
    },
    "Murata": {
        "ability_1": {"name": "Water Slash", "mult": 3},
        "ability_2": {"name": "Blade Rush", "mult": 5},
        "ability_3": {"name": "Water Breathing Full", "mult": 10, "once": True},
    },
    "Sakonji Urokodaki": {
        "ability_1": {"name": "Water Slash", "mult": 3},
        "ability_2": {"name": "Mask Strike", "mult": 5},
        "ability_3": {"name": "Water Breathing Full", "mult": 10, "once": True},
    },
    "Jigoro Kuwajima": {
        "ability_1": {"name": "Thunder Slash", "mult": 3},
        "ability_2": {"name": "Thunderclap", "mult": 5},
        "ability_3": {"name": "Thunder Breathing Full", "mult": 10, "once": True},
    },
    "Shinjuro Rengoku": {
        "ability_1": {"name": "Flame Slash", "mult": 3},
        "ability_2": {"name": "Flame Tiger", "mult": 5},
        "ability_3": {"name": "Flame Breathing Full", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
DEMONSLAYER_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Rui": {"display_name": "رویی", "hp": 1000, "atk": 80, "reward": 50000},
    "Enmu": {"display_name": "انمو", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Akaza": {"display_name": "آکازا", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Doma": {"display_name": "دوما", "hp": 90000, "atk": 4400, "reward": 200000},
    "Kokushibo": {"display_name": "کوکوشیبو", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Muzan Kibutsuji": {"display_name": "موزان کیبوتسوجی", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
DEMONSLAYER_FODDER = {
    "Lesser Demon": {"display_name": "شیطان ضعیف", "hp": 400, "atk": 30, "reward": 5000},
    "Rui": {"display_name": "رویی", "hp": 1000, "atk": 80, "reward": 5000},
    "Enmu": {"display_name": "انمو", "hp": 1200, "atk": 90, "reward": 5000},
    "Akaza": {"display_name": "آکازا", "hp": 2000, "atk": 150, "reward": 5000},
}