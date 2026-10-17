# ============================================================
# HUNTER X HUNTER DATA
# ============================================================

CHARACTERS_HXH = {
    "S": {
        "Gon Freecss": "Nen Prodigy",
        "Killua Zoldyck": "Lightning Assassin",
        "Isaac Netero": "Hunter Association Chairman",
        "Meruem": "Chimera Ant King",
        "Neferpitou": "Royal Guard",
        "Menthuthuyoupi": "Royal Guard",
        "Shaiapouf": "Royal Guard",
        "Hisoka Morow": "Magician",
        "Chrollo Lucilfer": "Phantom Troupe Leader",
        "Ging Freecss": "Legendary Hunter",
    },
    "A": {
        "Kurapika": "Chain User",
        "Leorio Paradinight": "Future Doctor",
        "Illumi Zoldyck": "Master Assassin",
        "Feitan Portor": "Phantom Troupe",
        "Phinks Magcub": "Phantom Troupe",
        "Shalnark": "Phantom Troupe",
        "Machi Komachine": "Phantom Troupe",
        "Nobunaga Hazama": "Phantom Troupe",
        "Franklin Bordeau": "Phantom Troupe",
        "Shizuku Murasaki": "Phantom Troupe",
    },
    "B": {
        "Biscuit Krueger": "Nen Master",
        "Knov": "Hunter",
        "Morel Mackernasey": "Hunter",
        "Knuckle Bine": "Beast Hunter",
        "Shoot McMahon": "Hunter",
        "Kite": "Ging's Student",
        "Hanzo": "Ninja Hunter",
        "Zushi": "Nen Student",
        "Wing": "Nen Teacher",
        "Tonpa": "Rookie Crusher",
    },
}

CHAR_PRICES_HXH = {"S": 5000000, "A": 600000, "B": 150000}
ABILITIES_HXH = {
    # ============ S RANK ============
    "Gon Freecss": {
        "ability_1": {"name": "Rock", "mult": 3},
        "ability_2": {"name": "Paper", "mult": 5},
        "ability_3": {"name": "Adult Gon Form", "mult": 10, "once": True},
    },
    "Killua Zoldyck": {
        "ability_1": {"name": "Lightning Palm", "mult": 3},
        "ability_2": {"name": "Thunderbolt", "mult": 5},
        "ability_3": {"name": "Godspeed: Speed of Lightning", "mult": 10, "once": True},
    },
    "Isaac Netero": {
        "ability_1": {"name": "100-Type Guanyin Bodhisattva", "mult": 3},
        "ability_2": {"name": "Zero Hand", "mult": 5},
        "ability_3": {"name": "Rose Bomb", "mult": 10, "once": True},
    },
    "Meruem": {
        "ability_1": {"name": "Aura Synthesis", "mult": 3},
        "ability_2": {"name": "Photon Tail", "mult": 5},
        "ability_3": {"name": "Metamorphosis: Full", "mult": 10, "once": True},
    },
    "Neferpitou": {
        "ability_1": {"name": "Terpsichora", "mult": 3},
        "ability_2": {"name": "Doctor Blythe", "mult": 5},
        "ability_3": {"name": "Puppeteer Mode", "mult": 10, "once": True},
    },
    "Menthuthuyoupi": {
        "ability_1": {"name": "Rage Blast", "mult": 3},
        "ability_2": {"name": "Metamorphosis", "mult": 5},
        "ability_3": {"name": "Centaur Form", "mult": 10, "once": True},
    },
    "Shaiapouf": {
        "ability_1": {"name": "Spiritual Message", "mult": 3},
        "ability_2": {"name": "Scale Powder", "mult": 5},
        "ability_3": {"name": "Butterfly Form", "mult": 10, "once": True},
    },
    "Hisoka Morow": {
        "ability_1": {"name": "Bungee Gum", "mult": 3},
        "ability_2": {"name": "Texture Surprise", "mult": 5},
        "ability_3": {"name": "Bloodlust Awakening", "mult": 10, "once": True},
    },
    "Chrollo Lucilfer": {
        "ability_1": {"name": "Skill Hunter", "mult": 3},
        "ability_2": {"name": "Sun and Moon", "mult": 5},
        "ability_3": {"name": "Bookmark: Full Power", "mult": 10, "once": True},
    },
    "Ging Freecss": {
        "ability_1": {"name": "Aura Copy", "mult": 3},
        "ability_2": {"name": "Prediction", "mult": 5},
        "ability_3": {"name": "Top 5 Nen User", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Kurapika": {
        "ability_1": {"name": "Chain Jail", "mult": 3},
        "ability_2": {"name": "Holy Chain", "mult": 5},
        "ability_3": {"name": "Emperor Time", "mult": 10, "once": True},
    },
    "Leorio Paradinight": {
        "ability_1": {"name": "Warping Punch", "mult": 3},
        "ability_2": {"name": "Remote Punch", "mult": 5},
        "ability_3": {"name": "Doctor's Resolve", "mult": 10, "once": True},
    },
    "Illumi Zoldyck": {
        "ability_1": {"name": "Needle People", "mult": 3},
        "ability_2": {"name": "Illusion Needles", "mult": 5},
        "ability_3": {"name": "Zoldyck Assassin Mode", "mult": 10, "once": True},
    },
    "Feitan Portor": {
        "ability_1": {"name": "Rising Sun", "mult": 3},
        "ability_2": {"name": "Pain Packer", "mult": 5},
        "ability_3": {"name": "Sun Full Power", "mult": 10, "once": True},
    },
    "Phinks Magcub": {
        "ability_1": {"name": "Ripper Cyclotron", "mult": 3},
        "ability_2": {"name": "Wind-Up Punch", "mult": 5},
        "ability_3": {"name": "Max Wind-Up", "mult": 10, "once": True},
    },
    "Shalnark": {
        "ability_1": {"name": "Black Voice", "mult": 3},
        "ability_2": {"name": "Cell Phone Control", "mult": 5},
        "ability_3": {"name": "Autopilot Mode", "mult": 10, "once": True},
    },
    "Machi Komachine": {
        "ability_1": {"name": "Nen Stitches", "mult": 3},
        "ability_2": {"name": "Puppet Strings", "mult": 5},
        "ability_3": {"name": "Heart Strings", "mult": 10, "once": True},
    },
    "Nobunaga Hazama": {
        "ability_1": {"name": "Iaido Slash", "mult": 3},
        "ability_2": {"name": "En Circle", "mult": 5},
        "ability_3": {"name": "Samurai Full Power", "mult": 10, "once": True},
    },
    "Franklin Bordeau": {
        "ability_1": {"name": "Double Machine Gun", "mult": 3},
        "ability_2": {"name": "Nen Bullets", "mult": 5},
        "ability_3": {"name": "Full Barrage", "mult": 10, "once": True},
    },
    "Shizuku Murasaki": {
        "ability_1": {"name": "Blinky Vacuum", "mult": 3},
        "ability_2": {"name": "Deme-chan", "mult": 5},
        "ability_3": {"name": "Bloody Mary", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Biscuit Krueger": {
        "ability_1": {"name": "Cookie Punch", "mult": 3},
        "ability_2": {"name": "Nen Bath", "mult": 5},
        "ability_3": {"name": "True Form", "mult": 10, "once": True},
    },
    "Knov": {
        "ability_1": {"name": "Hide and Seek", "mult": 3},
        "ability_2": {"name": "Scream", "mult": 5},
        "ability_3": {"name": "4th Floor", "mult": 10, "once": True},
    },
    "Morel Mackernasey": {
        "ability_1": {"name": "Deep Purple", "mult": 3},
        "ability_2": {"name": "Smoky Jail", "mult": 5},
        "ability_3": {"name": "Smoke Troopers Full", "mult": 10, "once": True},
    },
    "Knuckle Bine": {
        "ability_1": {"name": "Potclean", "mult": 3},
        "ability_2": {"name": "Hakoware", "mult": 5},
        "ability_3": {"name": "Bankruptcy", "mult": 10, "once": True},
    },
    "Shoot McMahon": {
        "ability_1": {"name": "Floating Hand", "mult": 3},
        "ability_2": {"name": "Cage of Three", "mult": 5},
        "ability_3": {"name": "Hotel Rafflesia", "mult": 10, "once": True},
    },
    "Kite": {
        "ability_1": {"name": "Crazy Slots", "mult": 3},
        "ability_2": {"name": "Scythe", "mult": 5},
        "ability_3": {"name": "Number 3: Mace", "mult": 10, "once": True},
    },
    "Hanzo": {
        "ability_1": {"name": "Ninja Dash", "mult": 3},
        "ability_2": {"name": "Shadow Clone", "mult": 5},
        "ability_3": {"name": "Ninja Full Power", "mult": 10, "once": True},
    },
    "Zushi": {
        "ability_1": {"name": "Nen Punch", "mult": 3},
        "ability_2": {"name": "Ten Defense", "mult": 5},
        "ability_3": {"name": "Nen Awakening", "mult": 10, "once": True},
    },
    "Wing": {
        "ability_1": {"name": "Nen Palm", "mult": 3},
        "ability_2": {"name": "Ten Barrier", "mult": 5},
        "ability_3": {"name": "Nen Master", "mult": 10, "once": True},
    },
    "Tonpa": {
        "ability_1": {"name": "Poison Drink", "mult": 3},
        "ability_2": {"name": "Trick Juice", "mult": 5},
        "ability_3": {"name": "Rookie Crusher", "mult": 10, "once": True},
    },
}
# ============================================================
# BOSSES
# ============================================================
HXH_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Tonpa": {"display_name": "تونپا", "hp": 1000, "atk": 80, "reward": 50000},
    "Zushi": {"display_name": "زوشی", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Hisoka Morow": {"display_name": "هیسوکا", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Chrollo Lucilfer": {"display_name": "کرولو", "hp": 90000, "atk": 4400, "reward": 200000},
    "Neferpitou": {"display_name": "نفرپیتو", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Meruem": {"display_name": "مروئم", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
HXH_FODDER = {
    "Hunter Applicant": {"display_name": "متقاضی هانتر", "hp": 400, "atk": 30, "reward": 5000},
    "Tonpa": {"display_name": "تونپا", "hp": 1000, "atk": 80, "reward": 5000},
    "Zushi": {"display_name": "زوشی", "hp": 1200, "atk": 90, "reward": 5000},
    "Hisoka Morow": {"display_name": "هیسوکا", "hp": 2000, "atk": 150, "reward": 5000},
}