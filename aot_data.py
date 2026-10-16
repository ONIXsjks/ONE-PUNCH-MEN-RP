# ============================================================
# ATTACK ON TITAN DATA
# ============================================================

CHARACTERS_AOT = {
    "S": {
        "Eren Yeager": "Founding Titan",
        "Levi Ackerman": "Humanity's Strongest",
        "Mikasa Ackerman": "Ackerman Bloodline",
        "Zeke Yeager": "Beast Titan",
        "Reiner Braun": "Armored Titan",
        "Bertholdt Hoover": "Colossal Titan",
        "Annie Leonhart": "Female Titan",
        "Kenny Ackerman": "Anti-Personnel Squad",
        "Armin Arlert": "Colossal Titan Inheritor",
        "Rod Reiss": "Titan Lord",
    },
    "A": {
        "Erwin Smith": "Survey Corps Commander",
        "Hange Zoë": "Titan Researcher",
        "Pieck Finger": "Cart Titan",
        "Porco Galliard": "Jaw Titan",
        "Marcel Galliard": "Former Jaw Titan",
        "Ymir": "Dancing Titan",
        "Jean Kirstein": "Squad Leader",
        "Falco Grice": "Jaw Titan Inheritor",
        "Gabi Braun": "Warrior Candidate",
        "Yelena": "Volunteer Commander",
    },
    "B": {
        "Sasha Blouse": "Hunter",
        "Connie Springer": "Scout",
        "Historia Reiss": "Queen",
        "Floch Forster": "Yeagerist Leader",
        "Colt Grice": "Warrior Candidate",
        "Udo": "Warrior Candidate",
        "Zofia": "Warrior Candidate",
        "Onyankopon": "Volunteer",
        "Niccolo": "Marleyan Chef",
        "Kiyomi Azumabito": "Hizuru Leader",
    },
}

CHAR_PRICES_AOT = {"S": 2000000, "A": 500000, "B": 150000}

ABILITIES_AOT = {
    # ============ S RANK ============
    "Eren Yeager": {
        "ability_1": {"name": "Titan Punch", "mult": 3},
        "ability_2": {"name": "Hardening Fist", "mult": 5},
        "ability_3": {"name": "Founding Titan Roar", "mult": 10, "once": True},
    },
    "Levi Ackerman": {
        "ability_1": {"name": "ODM Slash", "mult": 3},
        "ability_2": {"name": "Spinning Blade", "mult": 5},
        "ability_3": {"name": "Ackerman Awakening", "mult": 10, "once": True},
    },
    "Mikasa Ackerman": {
        "ability_1": {"name": "Dual Blade Strike", "mult": 3},
        "ability_2": {"name": "Thunder Spear", "mult": 5},
        "ability_3": {"name": "Ackerman Bloodline", "mult": 10, "once": True},
    },
    "Zeke Yeager": {
        "ability_1": {"name": "Beast Throw", "mult": 3},
        "ability_2": {"name": "Scream Command", "mult": 5},
        "ability_3": {"name": "Royal Blood Titan", "mult": 10, "once": True},
    },
    "Reiner Braun": {
        "ability_1": {"name": "Armored Charge", "mult": 3},
        "ability_2": {"name": "Hardened Punch", "mult": 5},
        "ability_3": {"name": "Armored Titan Full", "mult": 10, "once": True},
    },
    "Bertholdt Hoover": {
        "ability_1": {"name": "Steam Burst", "mult": 3},
        "ability_2": {"name": "Colossal Kick", "mult": 5},
        "ability_3": {"name": "Colossal Titan Form", "mult": 10, "once": True},
    },
    "Annie Leonhart": {
        "ability_1": {"name": "Crystal Fist", "mult": 3},
        "ability_2": {"name": "Hardened Strike", "mult": 5},
        "ability_3": {"name": "Female Titan Full", "mult": 10, "once": True},
    },
    "Kenny Ackerman": {
        "ability_1": {"name": "Anti-Personnel Slash", "mult": 3},
        "ability_2": {"name": "Shotgun Blast", "mult": 5},
        "ability_3": {"name": "Ackerman Awakening", "mult": 10, "once": True},
    },
    "Armin Arlert": {
        "ability_1": {"name": "Blade Toss", "mult": 3},
        "ability_2": {"name": "Thunder Spear Barrage", "mult": 5},
        "ability_3": {"name": "Colossal Titan Nuke", "mult": 10, "once": True},
    },
    "Rod Reiss": {
        "ability_1": {"name": "Titan Crush", "mult": 3},
        "ability_2": {"name": "Titan Sweep", "mult": 5},
        "ability_3": {"name": "Rod Reiss Titan Full", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Erwin Smith": {
        "ability_1": {"name": "Charge Command", "mult": 3},
        "ability_2": {"name": "Final Gambit", "mult": 5},
        "ability_3": {"name": "Survey Corps Rally", "mult": 10, "once": True},
    },
    "Hange Zoë": {
        "ability_1": {"name": "Titan Research Trap", "mult": 3},
        "ability_2": {"name": "Explosive Blade", "mult": 5},
        "ability_3": {"name": "Mad Scientist Frenzy", "mult": 10, "once": True},
    },
    "Pieck Finger": {
        "ability_1": {"name": "Cart Rush", "mult": 3},
        "ability_2": {"name": "Jaw Bite", "mult": 5},
        "ability_3": {"name": "Cart Titan Form", "mult": 10, "once": True},
    },
    "Porco Galliard": {
        "ability_1": {"name": "Jaw Crush", "mult": 3},
        "ability_2": {"name": "Claw Strike", "mult": 5},
        "ability_3": {"name": "Jaw Titan Full", "mult": 10, "once": True},
    },
    "Marcel Galliard": {
        "ability_1": {"name": "Jaw Snap", "mult": 3},
        "ability_2": {"name": "Titan Fang", "mult": 5},
        "ability_3": {"name": "Jaw Titan Rampage", "mult": 10, "once": True},
    },
    "Ymir": {
        "ability_1": {"name": "Jaw Bite", "mult": 3},
        "ability_2": {"name": "Claw Slash", "mult": 5},
        "ability_3": {"name": "Dancing Titan Form", "mult": 10, "once": True},
    },
    "Jean Kirstein": {
        "ability_1": {"name": "ODM Cut", "mult": 3},
        "ability_2": {"name": "Thunder Spear", "mult": 5},
        "ability_3": {"name": "Squad Leader Charge", "mult": 10, "once": True},
    },
    "Falco Grice": {
        "ability_1": {"name": "Jaw Snap", "mult": 3},
        "ability_2": {"name": "Titan Claw", "mult": 5},
        "ability_3": {"name": "Jaw Titan Full", "mult": 10, "once": True},
    },
    "Gabi Braun": {
        "ability_1": {"name": "Rifle Shot", "mult": 3},
        "ability_2": {"name": "Anti-Titan Bomb", "mult": 5},
        "ability_3": {"name": "Warrior's Pride", "mult": 10, "once": True},
    },
    "Yelena": {
        "ability_1": {"name": "Pistol Shot", "mult": 3},
        "ability_2": {"name": "Anti-Titan Rifle", "mult": 5},
        "ability_3": {"name": "Volunteer Commander", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Sasha Blouse": {
        "ability_1": {"name": "Bow Shot", "mult": 3},
        "ability_2": {"name": "Arrow Barrage", "mult": 5},
        "ability_3": {"name": "Hunter's Instinct", "mult": 10, "once": True},
    },
    "Connie Springer": {
        "ability_1": {"name": "ODM Strike", "mult": 3},
        "ability_2": {"name": "Blade Rush", "mult": 5},
        "ability_3": {"name": "Scout Vanguard", "mult": 10, "once": True},
    },
    "Historia Reiss": {
        "ability_1": {"name": "Crystal Punch", "mult": 3},
        "ability_2": {"name": "Royal Strike", "mult": 5},
        "ability_3": {"name": "Queen's Resolve", "mult": 10, "once": True},
    },
    "Floch Forster": {
        "ability_1": {"name": "Rifle Shot", "mult": 3},
        "ability_2": {"name": "Fanatic Charge", "mult": 5},
        "ability_3": {"name": "Yeagerist Rally", "mult": 10, "once": True},
    },
    "Colt Grice": {
        "ability_1": {"name": "Blade Strike", "mult": 3},
        "ability_2": {"name": "Titan Assist", "mult": 5},
        "ability_3": {"name": "Beast Titan Guard", "mult": 10, "once": True},
    },
    "Udo": {
        "ability_1": {"name": "Blade Strike", "mult": 3},
        "ability_2": {"name": "Cadet Rush", "mult": 5},
        "ability_3": {"name": "Marleyan Guard", "mult": 10, "once": True},
    },
    "Zofia": {
        "ability_1": {"name": "Blade Strike", "mult": 3},
        "ability_2": {"name": "Cadet Rush", "mult": 5},
        "ability_3": {"name": "Marleyan Guard", "mult": 10, "once": True},
    },
    "Onyankopon": {
        "ability_1": {"name": "Pistol Shot", "mult": 3},
        "ability_2": {"name": "Supply Strike", "mult": 5},
        "ability_3": {"name": "Volunteer Ace", "mult": 10, "once": True},
    },
    "Niccolo": {
        "ability_1": {"name": "Knife Strike", "mult": 3},
        "ability_2": {"name": "Chef's Fury", "mult": 5},
        "ability_3": {"name": "Marleyan Chef", "mult": 10, "once": True},
    },
    "Kiyomi Azumabito": {
        "ability_1": {"name": "Guard Strike", "mult": 3},
        "ability_2": {"name": "Hizuru Blade", "mult": 5},
        "ability_3": {"name": "Azumabito Leader", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
AOT_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Pure Titan": {"display_name": "تایتان خالص", "hp": 800, "atk": 60, "reward": 50000},
    "Abnormal Titan": {"display_name": "تایتان غیرعادی", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Armored Titan": {"display_name": "تایتان زره‌پوش", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Colossal Titan": {"display_name": "تایتان غول‌پیکر", "hp": 90000, "atk": 4400, "reward": 200000},
    "Beast Titan": {"display_name": "تایتان وحش", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Founding Titan Eren": {"display_name": "تایتان بنیان‌گذار ارن", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
AOT_FODDER = {
    "Small Titan": {"display_name": "تایتان کوچک", "hp": 400, "atk": 30, "reward": 5000},
    "Pure Titan": {"display_name": "تایتان خالص", "hp": 800, "atk": 60, "reward": 5000},
    "Abnormal Titan": {"display_name": "تایتان غیرعادی", "hp": 1200, "atk": 90, "reward": 5000},
    "Wall Titan": {"display_name": "تایتان دیواری", "hp": 2000, "atk": 150, "reward": 5000},
}