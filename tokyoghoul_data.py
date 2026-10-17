# ============================================================
# TOKYO GHOUL DATA
# ============================================================

CHARACTERS_TOKYOGHOUL = {
    "S": {
        "Ken Kaneki": "One-Eyed King",
        "Eto Yoshimura": "One-Eyed Owl",
        "Touka Kirishima": "Rabbit",
        "Ayato Kirishima": "Black Rabbit",
        "Rize Kamishiro": "Binge Eater",
        "Yoshimura": "Manager",
        "Renji Yomo": "Raven",
        "Uta": "Clown Mask",
        "Kishou Arima": "CCG Reaper",
        "Furuta Nimura": "Kichimura Washuu",
    },
    "A": {
        "Shuu Tsukiyama": "Gourmet",
        "Hinami Fueguchi": "Rabbit",
        "Nishiki Nishio": "Nishio",
        "Kureo Mado": "CCG Investigator",
        "Akira Mado": "CCG Investigator",
        "Koutarou Amon": "CCG Investigator",
        "Juuzou Suzuya": "CCG Investigator",
        "Seidou Takizawa": "Owl",
        "Tooru Mutsuki": "CCG Investigator",
        "Kuki Urie": "CCG Investigator",
    },
    "B": {
        "Hideyoshi Nagachika": "Hide",
        "Kimmy": "Ghoul",
        "Yamori": "Jason",
        "Nico": "Clown",
        "Itori": "Clown",
        "Roma Hoito": "Clown",
        "Hooguro": "Aogiri",
        "Shousei Idera": "Aogiri",
        "Miza Kusakari": "Aogiri",
        "Kurona Yasuhisa": "Aogiri",
    },
}

CHAR_PRICES_TOKYOGHOUL = {"S": 5000000, "A": 600000, "B": 150000}

ABILITIES_TOKYOGHOUL = {
    # ============ S RANK ============
    "Ken Kaneki": {
        "ability_1": {"name": "Rinkaku Kagune", "mult": 3},
        "ability_2": {"name": "Kakuja Form", "mult": 5},
        "ability_3": {"name": "One-Eyed King Awakening", "mult": 10, "once": True},
    },
    "Eto Yoshimura": {
        "ability_1": {"name": "Kakugan Stare", "mult": 3},
        "ability_2": {"name": "Owl Kagune", "mult": 5},
        "ability_3": {"name": "One-Eyed Owl Full", "mult": 10, "once": True},
    },
    "Touka Kirishima": {
        "ability_1": {"name": "Ukaku Shards", "mult": 3},
        "ability_2": {"name": "Rabbit Rush", "mult": 5},
        "ability_3": {"name": "Rabbit Full Power", "mult": 10, "once": True},
    },
    "Ayato Kirishima": {
        "ability_1": {"name": "Ukaku Blast", "mult": 3},
        "ability_2": {"name": "Black Rabbit Rush", "mult": 5},
        "ability_3": {"name": "Black Rabbit Full", "mult": 10, "once": True},
    },
    "Rize Kamishiro": {
        "ability_1": {"name": "Rinkaku Slash", "mult": 3},
        "ability_2": {"name": "Binge Eater Bite", "mult": 5},
        "ability_3": {"name": "Binge Eater Full", "mult": 10, "once": True},
    },
    "Yoshimura": {
        "ability_1": {"name": "Manager Strike", "mult": 3},
        "ability_2": {"name": "Kakuja Power", "mult": 5},
        "ability_3": {"name": "Manager Full", "mult": 10, "once": True},
    },
    "Renji Yomo": {
        "ability_1": {"name": "Raven Slash", "mult": 3},
        "ability_2": {"name": "Raven Rush", "mult": 5},
        "ability_3": {"name": "Raven Full", "mult": 10, "once": True},
    },
    "Uta": {
        "ability_1": {"name": "Mask Slash", "mult": 3},
        "ability_2": {"name": "Clown Strike", "mult": 5},
        "ability_3": {"name": "Clown Mask Full", "mult": 10, "once": True},
    },
    "Kishou Arima": {
        "ability_1": {"name": "IXA Strike", "mult": 3},
        "ability_2": {"name": "Narukami Lightning", "mult": 5},
        "ability_3": {"name": "CCG Reaper Full", "mult": 10, "once": True},
    },
    "Furuta Nimura": {
        "ability_1": {"name": "Rinkaku Slash", "mult": 3},
        "ability_2": {"name": "Rize Kagune", "mult": 5},
        "ability_3": {"name": "V Full Power", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Shuu Tsukiyama": {
        "ability_1": {"name": "Koukaku Slash", "mult": 3},
        "ability_2": {"name": "Gourmet Bite", "mult": 5},
        "ability_3": {"name": "Gourmet Full", "mult": 10, "once": True},
    },
    "Hinami Fueguchi": {
        "ability_1": {"name": "Rinkaku Strike", "mult": 3},
        "ability_2": {"name": "Rabbit Rush", "mult": 5},
        "ability_3": {"name": "Hinami Full", "mult": 10, "once": True},
    },
    "Nishiki Nishio": {
        "ability_1": {"name": "Koukaku Slash", "mult": 3},
        "ability_2": {"name": "Serpent Rush", "mult": 5},
        "ability_3": {"name": "Nishiki Full", "mult": 10, "once": True},
    },
    "Kureo Mado": {
        "ability_1": {"name": "Quinque Strike", "mult": 3},
        "ability_2": {"name": "Investigator Rush", "mult": 5},
        "ability_3": {"name": "Mado Full", "mult": 10, "once": True},
    },
    "Akira Mado": {
        "ability_1": {"name": "Quinque Slash", "mult": 3},
        "ability_2": {"name": "Investigator Rush", "mult": 5},
        "ability_3": {"name": "Akira Full", "mult": 10, "once": True},
    },
    "Koutarou Amon": {
        "ability_1": {"name": "Quinque Strike", "mult": 3},
        "ability_2": {"name": "Fist Rush", "mult": 5},
        "ability_3": {"name": "Amon Full", "mult": 10, "once": True},
    },
    "Juuzou Suzuya": {
        "ability_1": {"name": "Scissors Slash", "mult": 3},
        "ability_2": {"name": "Knife Rush", "mult": 5},
        "ability_3": {"name": "Suzuya Full", "mult": 10, "once": True},
    },
    "Seidou Takizawa": {
        "ability_1": {"name": "Kakugan Slash", "mult": 3},
        "ability_2": {"name": "Owl Rush", "mult": 5},
        "ability_3": {"name": "Takizawa Full", "mult": 10, "once": True},
    },
    "Tooru Mutsuki": {
        "ability_1": {"name": "Quinque Slash", "mult": 3},
        "ability_2": {"name": "Kagune Rush", "mult": 5},
        "ability_3": {"name": "Mutsuki Full", "mult": 10, "once": True},
    },
    "Kuki Urie": {
        "ability_1": {"name": "Quinque Strike", "mult": 3},
        "ability_2": {"name": "Rush Attack", "mult": 5},
        "ability_3": {"name": "Urie Full", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Hideyoshi Nagachika": {
        "ability_1": {"name": "Hide's Strike", "mult": 3},
        "ability_2": {"name": "Sneak Attack", "mult": 5},
        "ability_3": {"name": "Hide Full Power", "mult": 10, "once": True},
    },
    "Kimmy": {
        "ability_1": {"name": "Bikaku Strike", "mult": 3},
        "ability_2": {"name": "Ghoul Rush", "mult": 5},
        "ability_3": {"name": "Kimmy Full", "mult": 10, "once": True},
    },
    "Yamori": {
        "ability_1": {"name": "Pliers Crush", "mult": 3},
        "ability_2": {"name": "Jason Rush", "mult": 5},
        "ability_3": {"name": "Jason Full", "mult": 10, "once": True},
    },
    "Nico": {
        "ability_1": {"name": "Clown Slash", "mult": 3},
        "ability_2": {"name": "Clown Rush", "mult": 5},
        "ability_3": {"name": "Nico Full", "mult": 10, "once": True},
    },
    "Itori": {
        "ability_1": {"name": "Clown Strike", "mult": 3},
        "ability_2": {"name": "Clown Rush", "mult": 5},
        "ability_3": {"name": "Itori Full", "mult": 10, "once": True},
    },
    "Roma Hoito": {
        "ability_1": {"name": "Clown Slash", "mult": 3},
        "ability_2": {"name": "Clown Rush", "mult": 5},
        "ability_3": {"name": "Roma Full", "mult": 10, "once": True},
    },
    "Hooguro": {
        "ability_1": {"name": "Bikaku Strike", "mult": 3},
        "ability_2": {"name": "Aogiri Rush", "mult": 5},
        "ability_3": {"name": "Hooguro Full", "mult": 10, "once": True},
    },
    "Shousei Idera": {
        "ability_1": {"name": "Bikaku Strike", "mult": 3},
        "ability_2": {"name": "Aogiri Rush", "mult": 5},
        "ability_3": {"name": "Shousei Full", "mult": 10, "once": True},
    },
    "Miza Kusakari": {
        "ability_1": {"name": "Bikaku Strike", "mult": 3},
        "ability_2": {"name": "Aogiri Rush", "mult": 5},
        "ability_3": {"name": "Miza Full", "mult": 10, "once": True},
    },
    "Kurona Yasuhisa": {
        "ability_1": {"name": "Ukaku Blast", "mult": 3},
        "ability_2": {"name": "Aogiri Rush", "mult": 5},
        "ability_3": {"name": "Kurona Full", "mult": 10, "once": True},
    },
}
# ============================================================
# TOKYO GHOUL STATS - آمار کاراکترهای توکیو غول
# ============================================================

TOKYOGHOUL_STATS = {
    # ============ S RANK ============
    "Ken Kaneki": {
        "hp": 2500, "atk": 560, "def": 230, "dodge": 42,
        "price": 5000000,
    },
    "Eto Yoshimura": {
        "hp": 2500, "atk": 550, "def": 225, "dodge": 38,
        "price": 5000000,
    },
    "Touka Kirishima": {
        "hp": 2450, "atk": 530, "def": 220, "dodge": 40,
        "price": 4500000,
    },
    "Ayato Kirishima": {
        "hp": 2450, "atk": 525, "def": 220, "dodge": 40,
        "price": 4200000,
    },
    "Rize Kamishiro": {
        "hp": 2450, "atk": 530, "def": 215, "dodge": 38,
        "price": 4200000,
    },
    "Yoshimura": {
        "hp": 2500, "atk": 540, "def": 230, "dodge": 36,
        "price": 4500000,
    },
    "Renji Yomo": {
        "hp": 2400, "atk": 520, "def": 220, "dodge": 38,
        "price": 4000000,
    },
    "Uta": {
        "hp": 2400, "atk": 515, "def": 215, "dodge": 40,
        "price": 4000000,
    },
    "Kishou Arima": {
        "hp": 2500, "atk": 550, "def": 230, "dodge": 42,
        "price": 5000000,
    },
    "Furuta Nimura": {
        "hp": 2500, "atk": 540, "def": 225, "dodge": 40,
        "price": 4800000,
    },

    # ============ A RANK ============
    "Shuu Tsukiyama": {
        "hp": 1100, "atk": 225, "def": 82, "dodge": 26,
        "price": 600000,
    },
    "Hinami Fueguchi": {
        "hp": 1050, "atk": 215, "def": 75, "dodge": 26,
        "price": 560000,
    },
    "Nishiki Nishio": {
        "hp": 1080, "atk": 220, "def": 78, "dodge": 24,
        "price": 580000,
    },
    "Kureo Mado": {
        "hp": 1100, "atk": 225, "def": 80, "dodge": 24,
        "price": 600000,
    },
    "Akira Mado": {
        "hp": 1100, "atk": 225, "def": 80, "dodge": 25,
        "price": 600000,
    },
    "Koutarou Amon": {
        "hp": 1100, "atk": 225, "def": 82, "dodge": 22,
        "price": 600000,
    },
    "Juuzou Suzuya": {
        "hp": 1080, "atk": 220, "def": 78, "dodge": 28,
        "price": 580000,
    },
    "Seidou Takizawa": {
        "hp": 1100, "atk": 225, "def": 80, "dodge": 24,
        "price": 590000,
    },
    "Tooru Mutsuki": {
        "hp": 1080, "atk": 220, "def": 78, "dodge": 25,
        "price": 580000,
    },
    "Kuki Urie": {
        "hp": 1100, "atk": 225, "def": 80, "dodge": 24,
        "price": 590000,
    },

    # ============ B RANK ============
    "Hideyoshi Nagachika": {
        "hp": 700, "atk": 120, "def": 40, "dodge": 18,
        "price": 155000,
    },
    "Kimmy": {
        "hp": 680, "atk": 115, "def": 38, "dodge": 18,
        "price": 148000,
    },
    "Yamori": {
        "hp": 720, "atk": 125, "def": 42, "dodge": 16,
        "price": 160000,
    },
    "Nico": {
        "hp": 680, "atk": 118, "def": 38, "dodge": 17,
        "price": 150000,
    },
    "Itori": {
        "hp": 680, "atk": 115, "def": 38, "dodge": 18,
        "price": 150000,
    },
    "Roma Hoito": {
        "hp": 700, "atk": 122, "def": 40, "dodge": 17,
        "price": 155000,
    },
    "Hooguro": {
        "hp": 700, "atk": 120, "def": 40, "dodge": 16,
        "price": 150000,
    },
    "Shousei Idera": {
        "hp": 680, "atk": 118, "def": 38, "dodge": 16,
        "price": 148000,
    },
    "Miza Kusakari": {
        "hp": 680, "atk": 115, "def": 38, "dodge": 17,
        "price": 148000,
    },
    "Kurona Yasuhisa": {
        "hp": 700, "atk": 120, "def": 40, "dodge": 18,
        "price": 152000,
    },
}


# ============================================================
# BOSSES
# ============================================================
TOKYOGHOUL_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Yamori": {"display_name": "یاموری", "hp": 1000, "atk": 80, "reward": 50000},
    "Nishiki Nishio": {"display_name": "نیشیکی", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Juuzou Suzuya": {"display_name": "جوزو سوزویا", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Kishou Arima": {"display_name": "کیشو آریما", "hp": 90000, "atk": 4400, "reward": 200000},
    "Eto Yoshimura": {"display_name": "اتو یوشیمورا", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Furuta Nimura": {"display_name": "فوروتا نیومورا", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
TOKYOGHOUL_FODDER = {
    "Ghoul": {"display_name": "غول", "hp": 400, "atk": 30, "reward": 5000},
    "Yamori": {"display_name": "یاموری", "hp": 1000, "atk": 80, "reward": 5000},
    "Nishiki Nishio": {"display_name": "نیشیکی", "hp": 1200, "atk": 90, "reward": 5000},
    "Juuzou Suzuya": {"display_name": "جوزو سوزویا", "hp": 2000, "atk": 150, "reward": 5000},
}