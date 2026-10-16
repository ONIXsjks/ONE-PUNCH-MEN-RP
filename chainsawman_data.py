# ============================================================
# CHAINSAW MAN DATA
# ============================================================

CHARACTERS_CHAINSAWMAN = {
    "S": {
        "Makima": "Control Devil",
        "Darkness Devil": "Primal Fear",
        "Pochita": "Hero of Hell",
        "Denji": "Chainsaw Man",
        "Gun Devil": "Devil of Fear",
        "War Devil (Yoru)": "Horseman of War",
        "Falling Devil": "Primal Fear",
        "Famine Devil": "Horseman of Famine",
        "Death Devil": "Horseman of Death",
        "Quanxi": "Crossbow Hybrid",
    },
    "A": {
        "Kishibe": "Devil Hunter",
        "Aki Hayakawa": "Curse Devil Contract",
        "Power": "Blood Devil",
        "Reze": "Bomb Devil Hybrid",
        "Angel Devil": "Angel Devil",
        "Himeno": "Ghost Devil Contract",
        "Kobeni": "Secret Knife",
        "Beam": "Shark Devil",
        "Princi": "Spider Devil",
        "Galgali": "Stone Devil",
    },
    "B": {
        "Violence Devil": "Violence Devil",
        "Shark Devil": "Shark Devil",
        "Future Devil": "Future Devil",
        "Fox Devil": "Fox Devil",
        "Curse Devil": "Curse Devil",
        "Bomb Devil": "Bomb Devil",
        "Katana Man": "Katana Hybrid",
        "Sawatari": "Snake Devil",
        "Santa Claus": "Doll Devil",
        "Yakuza Boss": "Gang Leader",
    },
}

CHAR_PRICES_CHAINSAWMAN = {"S": 2000000, "A": 500000, "B": 150000}

ABILITIES_CHAINSAWMAN = {
    # ============ S RANK ============
    "Makima": {
        "ability_1": {"name": "Control Chain", "mult": 3},
        "ability_2": {"name": "Domination", "mult": 5},
        "ability_3": {"name": "Conquest Full", "mult": 10, "once": True},
    },
    "Darkness Devil": {
        "ability_1": {"name": "Dark Slash", "mult": 3},
        "ability_2": {"name": "Void Grasp", "mult": 5},
        "ability_3": {"name": "Darkness Full", "mult": 10, "once": True},
    },
    "Pochita": {
        "ability_1": {"name": "Chainsaw Slash", "mult": 3},
        "ability_2": {"name": "Hero Rush", "mult": 5},
        "ability_3": {"name": "Hero of Hell", "mult": 10, "once": True},
    },
    "Denji": {
        "ability_1": {"name": "Chainsaw Slash", "mult": 3},
        "ability_2": {"name": "Blood Frenzy", "mult": 5},
        "ability_3": {"name": "Chainsaw Devil Full", "mult": 10, "once": True},
    },
    "Gun Devil": {
        "ability_1": {"name": "Bullet Shot", "mult": 3},
        "ability_2": {"name": "Gun Barrage", "mult": 5},
        "ability_3": {"name": "Gun Devil Full", "mult": 10, "once": True},
    },
    "War Devil (Yoru)": {
        "ability_1": {"name": "Bomb Drop", "mult": 3},
        "ability_2": {"name": "War Blade", "mult": 5},
        "ability_3": {"name": "Nuclear Punch", "mult": 10, "once": True},
    },
    "Falling Devil": {
        "ability_1": {"name": "Gravity Push", "mult": 3},
        "ability_2": {"name": "Fallen Rush", "mult": 5},
        "ability_3": {"name": "Falling Full", "mult": 10, "once": True},
    },
    "Famine Devil": {
        "ability_1": {"name": "Hunger Chain", "mult": 3},
        "ability_2": {"name": "Starve Touch", "mult": 5},
        "ability_3": {"name": "Famine Full", "mult": 10, "once": True},
    },
    "Death Devil": {
        "ability_1": {"name": "Scythe Slash", "mult": 3},
        "ability_2": {"name": "Soul Reap", "mult": 5},
        "ability_3": {"name": "Death Full", "mult": 10, "once": True},
    },
    "Quanxi": {
        "ability_1": {"name": "Crossbow Shot", "mult": 3},
        "ability_2": {"name": "Arrow Rush", "mult": 5},
        "ability_3": {"name": "Hybrid Full", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Kishibe": {
        "ability_1": {"name": "Knife Slash", "mult": 3},
        "ability_2": {"name": "Devil Hunter", "mult": 5},
        "ability_3": {"name": "Hunter Full", "mult": 10, "once": True},
    },
    "Aki Hayakawa": {
        "ability_1": {"name": "Katana Slash", "mult": 3},
        "ability_2": {"name": "Curse Nail", "mult": 5},
        "ability_3": {"name": "Curse Devil Full", "mult": 10, "once": True},
    },
    "Power": {
        "ability_1": {"name": "Blood Hammer", "mult": 3},
        "ability_2": {"name": "Blood Frenzy", "mult": 5},
        "ability_3": {"name": "Blood Devil Full", "mult": 10, "once": True},
    },
    "Reze": {
        "ability_1": {"name": "Bomb Kick", "mult": 3},
        "ability_2": {"name": "Explosion", "mult": 5},
        "ability_3": {"name": "Bomb Devil Full", "mult": 10, "once": True},
    },
    "Angel Devil": {
        "ability_1": {"name": "Spear Throw", "mult": 3},
        "ability_2": {"name": "Life Drain", "mult": 5},
        "ability_3": {"name": "Angel Full", "mult": 10, "once": True},
    },
    "Himeno": {
        "ability_1": {"name": "Ghost Hand", "mult": 3},
        "ability_2": {"name": "Curse Pull", "mult": 5},
        "ability_3": {"name": "Ghost Devil Full", "mult": 10, "once": True},
    },
    "Kobeni": {
        "ability_1": {"name": "Knife Stab", "mult": 3},
        "ability_2": {"name": "Panic Rush", "mult": 5},
        "ability_3": {"name": "Secret Knife", "mult": 10, "once": True},
    },
    "Beam": {
        "ability_1": {"name": "Shark Rush", "mult": 3},
        "ability_2": {"name": "Fin Slash", "mult": 5},
        "ability_3": {"name": "Shark Devil Full", "mult": 10, "once": True},
    },
    "Princi": {
        "ability_1": {"name": "Spider Thread", "mult": 3},
        "ability_2": {"name": "Web Trap", "mult": 5},
        "ability_3": {"name": "Spider Devil Full", "mult": 10, "once": True},
    },
    "Galgali": {
        "ability_1": {"name": "Stone Punch", "mult": 3},
        "ability_2": {"name": "Rock Rush", "mult": 5},
        "ability_3": {"name": "Stone Devil Full", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Violence Devil": {
        "ability_1": {"name": "Fist Rush", "mult": 3},
        "ability_2": {"name": "Rage Punch", "mult": 5},
        "ability_3": {"name": "Violence Full", "mult": 10, "once": True},
    },
    "Shark Devil": {
        "ability_1": {"name": "Fin Slash", "mult": 3},
        "ability_2": {"name": "Blood Bite", "mult": 5},
        "ability_3": {"name": "Shark Full", "mult": 10, "once": True},
    },
    "Future Devil": {
        "ability_1": {"name": "Future Sight", "mult": 3},
        "ability_2": {"name": "Time Slash", "mult": 5},
        "ability_3": {"name": "Future Full", "mult": 10, "once": True},
    },
    "Fox Devil": {
        "ability_1": {"name": "Fox Bite", "mult": 3},
        "ability_2": {"name": "Head Crush", "mult": 5},
        "ability_3": {"name": "Fox Full", "mult": 10, "once": True},
    },
    "Curse Devil": {
        "ability_1": {"name": "Nail Curse", "mult": 3},
        "ability_2": {"name": "Curse Pull", "mult": 5},
        "ability_3": {"name": "Curse Full", "mult": 10, "once": True},
    },
    "Bomb Devil": {
        "ability_1": {"name": "Bomb Drop", "mult": 3},
        "ability_2": {"name": "Explosion", "mult": 5},
        "ability_3": {"name": "Bomb Full", "mult": 10, "once": True},
    },
    "Katana Man": {
        "ability_1": {"name": "Katana Slash", "mult": 3},
        "ability_2": {"name": "Iai Strike", "mult": 5},
        "ability_3": {"name": "Katana Hybrid Full", "mult": 10, "once": True},
    },
    "Sawatari": {
        "ability_1": {"name": "Snake Summon", "mult": 3},
        "ability_2": {"name": "Snake Bite", "mult": 5},
        "ability_3": {"name": "Snake Devil Full", "mult": 10, "once": True},
    },
    "Santa Claus": {
        "ability_1": {"name": "Doll Army", "mult": 3},
        "ability_2": {"name": "Curse Doll", "mult": 5},
        "ability_3": {"name": "Doll Devil Full", "mult": 10, "once": True},
    },
    "Yakuza Boss": {
        "ability_1": {"name": "Knife Slash", "mult": 3},
        "ability_2": {"name": "Yakuza Rush", "mult": 5},
        "ability_3": {"name": "Gang Leader", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
CHAINSAWMAN_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Katana Man": {"display_name": "کاتانا من", "hp": 1000, "atk": 80, "reward": 50000},
    "Bomb Devil": {"display_name": "شیطان بمب", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Gun Devil": {"display_name": "شیطان تفنگ", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Santa Claus": {"display_name": "سانتا کلاوس", "hp": 90000, "atk": 4400, "reward": 200000},
    "Darkness Devil": {"display_name": "شیطان تاریکی", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Makima": {"display_name": "ماکیما", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
CHAINSAWMAN_FODDER = {
    "Lesser Devil": {"display_name": "شیطان ضعیف", "hp": 400, "atk": 30, "reward": 5000},
    "Katana Man": {"display_name": "کاتانا من", "hp": 1000, "atk": 80, "reward": 5000},
    "Bomb Devil": {"display_name": "شیطان بمب", "hp": 1200, "atk": 90, "reward": 5000},
    "Gun Devil": {"display_name": "شیطان تفنگ", "hp": 2000, "atk": 150, "reward": 5000},
}