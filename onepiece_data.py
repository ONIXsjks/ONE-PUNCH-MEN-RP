# ============================================================
# ONE PIECE DATA
# ============================================================

CHARACTERS_ONEPIECE = {
    "S": {
        "Monkey D. Luffy": "Straw Hat Captain",
        "Roronoa Zoro": "Pirate Hunter",
        "Sanji": "Black Leg",
        "Nami": "Cat Burglar",
        "Usopp": "God Usopp",
        "Nico Robin": "Devil Child",
        "Trafalgar D. Water Law": "Surgeon of Death",
        "Marshall D. Teach": "Blackbeard",
        "Shanks": "Red-Haired Emperor",
        "Kaido": "King of Beasts",
    },
    "A": {
        "Portgas D. Ace": "Fire Fist",
        "Sabo": "Revolutionary Chief",
        "Charlotte Katakuri": "Sweet Commander",
        "Marco the Phoenix": "Whitebeard Commander",
        "Boa Hancock": "Pirate Empress",
        "Smoker": "White Hunter",
        "Crocodile": "Desert King",
        "Doflamingo": "Heavenly Yaksha",
        "King the Wildfire": "All-Star",
        "Queen the Plague": "All-Star",
    },
    "B": {
        "Vinsmoke Reiju": "Poison Pink",
        "Carrot": "Mink Warrior",
        "Brook": "Soul King",
        "Franky": "Cyborg",
        "Jinbe": "Knight of the Sea",
        "Tony Tony Chopper": "Cotton Candy Lover",
        "Perona": "Ghost Princess",
        "Buggy": "Genius Jester",
        "Coby": "Marine Hero",
        "Helmeppo": "Marine Officer",
    },
}

CHAR_PRICES_ONEPIECE = {"S": 5000000, "A": 600000, "B": 150000}
ABILITIES_ONEPIECE = {
    # ============ S RANK ============
    "Monkey D. Luffy": {
        "ability_1": {"name": "Gum-Gum Pistol", "mult": 3},
        "ability_2": {"name": "Gear 4: Bounceman", "mult": 5},
        "ability_3": {"name": "Gear 5: Sun God Nika", "mult": 10, "once": True},
    },
    "Roronoa Zoro": {
        "ability_1": {"name": "Oni Giri", "mult": 3},
        "ability_2": {"name": "Ashura", "mult": 5},
        "ability_3": {"name": "King of Hell", "mult": 10, "once": True},
    },
    "Sanji": {
        "ability_1": {"name": "Diable Jambe", "mult": 3},
        "ability_2": {"name": "Ifrit Jambe", "mult": 5},
        "ability_3": {"name": "Exoskeleton Awakening", "mult": 10, "once": True},
    },
    "Nami": {
        "ability_1": {"name": "Clima-Tact", "mult": 3},
        "ability_2": {"name": "Thunderbolt Tempo", "mult": 5},
        "ability_3": {"name": "Zeus Breeze Tempo", "mult": 10, "once": True},
    },
    "Usopp": {
        "ability_1": {"name": "Lead Star", "mult": 3},
        "ability_2": {"name": "Firebird Star", "mult": 5},
        "ability_3": {"name": "God Usopp Snipe", "mult": 10, "once": True},
    },
    "Nico Robin": {
        "ability_1": {"name": "Mil Fleur", "mult": 3},
        "ability_2": {"name": "Gigantesco Mano", "mult": 5},
        "ability_3": {"name": "Demonio Fleur", "mult": 10, "once": True},
    },
    "Trafalgar D. Water Law": {
        "ability_1": {"name": "Room", "mult": 3},
        "ability_2": {"name": "Shambles", "mult": 5},
        "ability_3": {"name": "K-ROOM: Injection Shot", "mult": 10, "once": True},
    },
    "Marshall D. Teach": {
        "ability_1": {"name": "Dark Matter", "mult": 3},
        "ability_2": {"name": "Black Vortex", "mult": 5},
        "ability_3": {"name": "Liberation", "mult": 10, "once": True},
    },
    "Shanks": {
        "ability_1": {"name": "Conqueror's Haki", "mult": 3},
        "ability_2": {"name": "Divine Departure", "mult": 5},
        "ability_3": {"name": "Kamusari", "mult": 10, "once": True},
    },
    "Kaido": {
        "ability_1": {"name": "Bolo Breath", "mult": 3},
        "ability_2": {"name": "Thunder Bagua", "mult": 5},
        "ability_3": {"name": "Blast Breath: Full Power", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Portgas D. Ace": {
        "ability_1": {"name": "Fire Fist", "mult": 3},
        "ability_2": {"name": "Flame Commandment", "mult": 5},
        "ability_3": {"name": "Entei", "mult": 10, "once": True},
    },
    "Sabo": {
        "ability_1": {"name": "Dragon Claw", "mult": 3},
        "ability_2": {"name": "Flame Emperor", "mult": 5},
        "ability_3": {"name": "Hiken: Fire Fist", "mult": 10, "once": True},
    },
    "Charlotte Katakuri": {
        "ability_1": {"name": "Mochi Thrust", "mult": 3},
        "ability_2": {"name": "Power Mochi", "mult": 5},
        "ability_3": {"name": "Buzz Cut Mochi", "mult": 10, "once": True},
    },
    "Marco the Phoenix": {
        "ability_1": {"name": "Phoenix Kick", "mult": 3},
        "ability_2": {"name": "Blue Flame Rush", "mult": 5},
        "ability_3": {"name": "Phoenix Rebirth", "mult": 10, "once": True},
    },
    "Boa Hancock": {
        "ability_1": {"name": "Pistol Kiss", "mult": 3},
        "ability_2": {"name": "Perfume Femur", "mult": 5},
        "ability_3": {"name": "Love Arrow", "mult": 10, "once": True},
    },
    "Smoker": {
        "ability_1": {"name": "White Blow", "mult": 3},
        "ability_2": {"name": "White Snake", "mult": 5},
        "ability_3": {"name": "White Out", "mult": 10, "once": True},
    },
    "Crocodile": {
        "ability_1": {"name": "Desert Spada", "mult": 3},
        "ability_2": {"name": "Sables", "mult": 5},
        "ability_3": {"name": "Ground Death", "mult": 10, "once": True},
    },
    "Doflamingo": {
        "ability_1": {"name": "Five Color Strings", "mult": 3},
        "ability_2": {"name": "Overheat", "mult": 5},
        "ability_3": {"name": "God Thread", "mult": 10, "once": True},
    },
    "King the Wildfire": {
        "ability_1": {"name": "Flame Slash", "mult": 3},
        "ability_2": {"name": "Pteranodon Rush", "mult": 5},
        "ability_3": {"name": "Lunarian Flame", "mult": 10, "once": True},
    },
    "Queen the Plague": {
        "ability_1": {"name": "Brachio Bomber", "mult": 3},
        "ability_2": {"name": "Ice Oni Virus", "mult": 5},
        "ability_3": {"name": "Black Coffee", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Vinsmoke Reiju": {
        "ability_1": {"name": "Poison Pink", "mult": 3},
        "ability_2": {"name": "Purple Pheromone", "mult": 5},
        "ability_3": {"name": "Poison Kiss", "mult": 10, "once": True},
    },
    "Carrot": {
        "ability_1": {"name": "Electro Claw", "mult": 3},
        "ability_2": {"name": "Sulong Rush", "mult": 5},
        "ability_3": {"name": "Full Moon Sulong", "mult": 10, "once": True},
    },
    "Brook": {
        "ability_1": {"name": "Soul Solid", "mult": 3},
        "ability_2": {"name": "Chills of the Underworld", "mult": 5},
        "ability_3": {"name": "Soul King Concert", "mult": 10, "once": True},
    },
    "Franky": {
        "ability_1": {"name": "Strong Right", "mult": 3},
        "ability_2": {"name": "Coup de Vent", "mult": 5},
        "ability_3": {"name": "Radical Beam", "mult": 10, "once": True},
    },
    "Jinbe": {
        "ability_1": {"name": "Fishman Karate", "mult": 3},
        "ability_2": {"name": "Shark Brick Fist", "mult": 5},
        "ability_3": {"name": "Ocean Current Shoulder Throw", "mult": 10, "once": True},
    },
    "Tony Tony Chopper": {
        "ability_1": {"name": "Kung Fu Point", "mult": 3},
        "ability_2": {"name": "Monster Point", "mult": 5},
        "ability_3": {"name": "Rumble Ball: Full", "mult": 10, "once": True},
    },
    "Perona": {
        "ability_1": {"name": "Negative Hollow", "mult": 3},
        "ability_2": {"name": "Mini Hollow", "mult": 5},
        "ability_3": {"name": "Ghost Princess", "mult": 10, "once": True},
    },
    "Buggy": {
        "ability_1": {"name": "Chop Chop Cannon", "mult": 3},
        "ability_2": {"name": "Muggy Ball", "mult": 5},
        "ability_3": {"name": "Cross Country", "mult": 10, "once": True},
    },
    "Coby": {
        "ability_1": {"name": "Soru", "mult": 3},
        "ability_2": {"name": "Rokushiki Combo", "mult": 5},
        "ability_3": {"name": "Observation Haki", "mult": 10, "once": True},
    },
    "Helmeppo": {
        "ability_1": {"name": "Dual Swords", "mult": 3},
        "ability_2": {"name": "Sword Rush", "mult": 5},
        "ability_3": {"name": "Marine Justice", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
ONEPIECE_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Alvida": {"display_name": "آلویدا", "hp": 1000, "atk": 80, "reward": 50000},
    "Buggy (East Blue)": {"display_name": "باگی (ایست بلو)", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Crocodile": {"display_name": "کروکودایل", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Doflamingo": {"display_name": "دوفلامینگو", "hp": 90000, "atk": 4400, "reward": 200000},
    "Charlotte Katakuri": {"display_name": "کاتاکوری", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Kaido": {"display_name": "کایدو", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
ONEPIECE_FODDER = {
    "Marine Recruit": {"display_name": "سرباز تازه‌کار", "hp": 400, "atk": 30, "reward": 5000},
    "Alvida": {"display_name": "آلویدا", "hp": 1000, "atk": 80, "reward": 5000},
    "Buggy (East Blue)": {"display_name": "باگی (ایست بلو)", "hp": 1200, "atk": 90, "reward": 5000},
    "Crocodile": {"display_name": "کروکودایل", "hp": 2000, "atk": 150, "reward": 5000},
}