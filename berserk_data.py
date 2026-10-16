# ============================================================
# BERSERK DATA
# ============================================================

CHARACTERS_BERSERK = {
    "S": {
        "Guts": "Berserker Armor",
        "Griffith": "Femto",
        "Skull Knight": "Sword of Actuation",
        "Zodd": "Immortal Apostle",
        "Emperor Ganishka": "Shiva Form",
        "Grunbeld": "Dragon Apostle",
        "Locus": "Moonlight Knight",
        "Irvine": "Archer Apostle",
        "Rakshas": "Shadow Apostle",
        "Void": "God Hand",
    },
    "A": {
        "Slan": "God Hand",
        "Ubik": "God Hand",
        "Conrad": "God Hand",
        "Casca": "Band of the Hawk",
        "Farnese": "Knight Commander",
        "Serpico": "Wind Swordsman",
        "Isidro": "Bandit Ace",
        "Schierke": "Astral Witch",
        "Puck": "Elf Companion",
        "Ivalera": "Elf Companion",
    },
    "B": {
        "Silat": "Bakiraka Leader",
        "Daiba": "Kushan Sorcerer",
        "Sonia": "Kushan Guard",
        "Mule": "Kushan Guard",
        "Charlotte": "Midland Princess",
        "Julius": "Midland Knight",
        "Adon": "Snake Baron",
        "Boscone": "Snake Baron",
        "Mozgus": "Inquisitor Apostle",
        "Emperor's Mage": "Kushan Sorcerer",
    },
}

CHAR_PRICES_BERSERK = {"S": 2000000, "A": 500000, "B": 150000}

ABILITIES_BERSERK = {
    # ============ S RANK ============
    "Guts": {
        "ability_1": {"name": "Dragon Slayer", "mult": 3},
        "ability_2": {"name": "Cannon Arm", "mult": 5},
        "ability_3": {"name": "Berserker Armor", "mult": 10, "once": True},
    },
    "Griffith": {
        "ability_1": {"name": "Saber Slash", "mult": 3},
        "ability_2": {"name": "Falcon Strike", "mult": 5},
        "ability_3": {"name": "Femto Form", "mult": 10, "once": True},
    },
    "Skull Knight": {
        "ability_1": {"name": "Sword of Actuation", "mult": 3},
        "ability_2": {"name": "Behelit Sword", "mult": 5},
        "ability_3": {"name": "Skull Knight Full", "mult": 10, "once": True},
    },
    "Zodd": {
        "ability_1": {"name": "Axe Swing", "mult": 3},
        "ability_2": {"name": "Beast Rush", "mult": 5},
        "ability_3": {"name": "Apostle Form", "mult": 10, "once": True},
    },
    "Emperor Ganishka": {
        "ability_1": {"name": "Lightning Strike", "mult": 3},
        "ability_2": {"name": "Storm Call", "mult": 5},
        "ability_3": {"name": "Shiva Form", "mult": 10, "once": True},
    },
    "Grunbeld": {
        "ability_1": {"name": "Hammer Smash", "mult": 3},
        "ability_2": {"name": "Corundum Shield", "mult": 5},
        "ability_3": {"name": "Dragon Form", "mult": 10, "once": True},
    },
    "Locus": {
        "ability_1": {"name": "Lance Charge", "mult": 3},
        "ability_2": {"name": "Iron Rush", "mult": 5},
        "ability_3": {"name": "Apostle Form", "mult": 10, "once": True},
    },
    "Irvine": {
        "ability_1": {"name": "Arrow Shot", "mult": 3},
        "ability_2": {"name": "Bow Barrage", "mult": 5},
        "ability_3": {"name": "Apostle Form", "mult": 10, "once": True},
    },
    "Rakshas": {
        "ability_1": {"name": "Assassin Slash", "mult": 3},
        "ability_2": {"name": "Shadow Strike", "mult": 5},
        "ability_3": {"name": "Apostle Form", "mult": 10, "once": True},
    },
    "Void": {
        "ability_1": {"name": "Space Warp", "mult": 3},
        "ability_2": {"name": "Void Slash", "mult": 5},
        "ability_3": {"name": "God Hand Power", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Slan": {
        "ability_1": {"name": "Whip Strike", "mult": 3},
        "ability_2": {"name": "Pain Lash", "mult": 5},
        "ability_3": {"name": "God Hand Power", "mult": 10, "once": True},
    },
    "Ubik": {
        "ability_1": {"name": "Mirror Slash", "mult": 3},
        "ability_2": {"name": "Illusion Strike", "mult": 5},
        "ability_3": {"name": "God Hand Power", "mult": 10, "once": True},
    },
    "Conrad": {
        "ability_1": {"name": "Rat Swarm", "mult": 3},
        "ability_2": {"name": "Plague Strike", "mult": 5},
        "ability_3": {"name": "God Hand Power", "mult": 10, "once": True},
    },
    "Casca": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Bandit Rush", "mult": 5},
        "ability_3": {"name": "Warrior Spirit", "mult": 10, "once": True},
    },
    "Farnese": {
        "ability_1": {"name": "Whip Strike", "mult": 3},
        "ability_2": {"name": "Knight Charge", "mult": 5},
        "ability_3": {"name": "Knight Full", "mult": 10, "once": True},
    },
    "Serpico": {
        "ability_1": {"name": "Wind Sword", "mult": 3},
        "ability_2": {"name": "Sylph Blade", "mult": 5},
        "ability_3": {"name": "Sylph Full", "mult": 10, "once": True},
    },
    "Isidro": {
        "ability_1": {"name": "Dagger Slash", "mult": 3},
        "ability_2": {"name": "Fire Bomb", "mult": 5},
        "ability_3": {"name": "Bandit Ace", "mult": 10, "once": True},
    },
    "Schierke": {
        "ability_1": {"name": "Fire Spell", "mult": 3},
        "ability_2": {"name": "Astral Walk", "mult": 5},
        "ability_3": {"name": "Astral Projection", "mult": 10, "once": True},
    },
    "Puck": {
        "ability_1": {"name": "Elf Punch", "mult": 3},
        "ability_2": {"name": "Healing Burst", "mult": 5},
        "ability_3": {"name": "Elf Form", "mult": 10, "once": True},
    },
    "Ivalera": {
        "ability_1": {"name": "Elf Punch", "mult": 3},
        "ability_2": {"name": "Healing Dust", "mult": 5},
        "ability_3": {"name": "Elf Full", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Silat": {
        "ability_1": {"name": "Tapasa Strike", "mult": 3},
        "ability_2": {"name": "Kusarigama", "mult": 5},
        "ability_3": {"name": "Bakiraka Full", "mult": 10, "once": True},
    },
    "Daiba": {
        "ability_1": {"name": "Fire Spell", "mult": 3},
        "ability_2": {"name": "Serpent Call", "mult": 5},
        "ability_3": {"name": "Sorcerer Full", "mult": 10, "once": True},
    },
    "Sonia": {
        "ability_1": {"name": "Dagger Slash", "mult": 3},
        "ability_2": {"name": "Kushan Strike", "mult": 5},
        "ability_3": {"name": "Kushan Guard", "mult": 10, "once": True},
    },
    "Mule": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Kushan Rush", "mult": 5},
        "ability_3": {"name": "Kushan Guard", "mult": 10, "once": True},
    },
    "Charlotte": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Noble Strike", "mult": 5},
        "ability_3": {"name": "Midland Guard", "mult": 10, "once": True},
    },
    "Julius": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Knight Rush", "mult": 5},
        "ability_3": {"name": "Midland Guard", "mult": 10, "once": True},
    },
    "Adon": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Cobra Strike", "mult": 5},
        "ability_3": {"name": "Snake Baron", "mult": 10, "once": True},
    },
    "Boscone": {
        "ability_1": {"name": "Axe Swing", "mult": 3},
        "ability_2": {"name": "Chain Strike", "mult": 5},
        "ability_3": {"name": "Snake Baron", "mult": 10, "once": True},
    },
    "Mozgus": {
        "ability_1": {"name": "Book Smash", "mult": 3},
        "ability_2": {"name": "Fire Breath", "mult": 5},
        "ability_3": {"name": "Apostle Form", "mult": 10, "once": True},
    },
    "Emperor's Mage": {
        "ability_1": {"name": "Fire Spell", "mult": 3},
        "ability_2": {"name": "Storm Call", "mult": 5},
        "ability_3": {"name": "Sorcerer Full", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
BERSERK_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Adon": {"display_name": "آدون", "hp": 1000, "atk": 80, "reward": 50000},
    "Mozgus": {"display_name": "موزگوس", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Zodd": {"display_name": "زود", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Grunbeld": {"display_name": "گرانبلت", "hp": 90000, "atk": 4400, "reward": 200000},
    "Emperor Ganishka": {"display_name": "امپراتور گانیشکا", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Femto Griffith": {"display_name": "فمتو گریفیث", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
BERSERK_FODDER = {
    "Lesser Apostle": {"display_name": "رسول ضعیف", "hp": 400, "atk": 30, "reward": 5000},
    "Adon": {"display_name": "آدون", "hp": 1000, "atk": 80, "reward": 5000},
    "Mozgus": {"display_name": "موزگوس", "hp": 1200, "atk": 90, "reward": 5000},
    "Zodd": {"display_name": "زود", "hp": 2000, "atk": 150, "reward": 5000},
}