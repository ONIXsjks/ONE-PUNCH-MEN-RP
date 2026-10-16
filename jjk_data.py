# ============================================================
# JJK DATA - Jujutsu Kaisen Characters, Abilities, Domains
# ============================================================

CHARACTERS_JJK = {
    "S": {
        "Gojo Satoru": "The Strongest",
        "Yuta Okkotsu": "Special Grade",
        "Kenjaku": "The Ancient Sorcerer",
        "Yuki Tsukumo": "Special Grade",
        "Suguru Geto": "Curse User",
        "Toji Fushiguro": "Sorcerer Killer",
        "Kinji Hakari": "Gambler",
        "Hiromi Higuruma": "Lawyer",
        "Hajime Kashimo": "Thunder God",
        "Yuji Modulo": "Modulo Form",
        "Uraume": "Ice Sorcerer",
        "SUKUNA ITADORI BODY": "King of Curses",
    },
    "A": {
        "Yuji Itadori": "Vessel",
        "Megumi Fushiguro": "Ten Shadows",
        "Maki Zenin": "Heavenly Restriction",
        "Kento Nanami": "Ratio Sorcerer",
        "Mei Mei": "Bird User",
        "Aoi Todo": "Boogie Woogie",
        "Choso": "Death Painting",
        "Naoya Zenin": "Projection Sorcery",
    },
    "B": {
        "Nobara Kugisaki": "Straw Doll",
        "Toge Inumaki": "Cursed Speech",
        "Kirara Hoshi": "Love Rendezvous",
        "Hana Kurusu": "Angel",
    },
}

CHAR_PRICES_JJK = {
    "S": 2000000,
    "A": 500000,
    "B": 150000,
    "C": 50000,
}

# ============================================================
# ABILITIES - هر کاراکتر ۳ Ability (ability_1: ×3، ability_2: ×5، ability_3: ×10 یک بار)
# ============================================================
ABILITIES_JJK = {
    # ============ S RANK ============
    "Gojo Satoru": {
        "ability_1": {"name": "Blue", "mult": 3},
        "ability_2": {"name": "Red", "mult": 5},
        "ability_3": {"name": "Hollow Purple", "mult": 10, "once": True},
    },
    "Yuta Okkotsu": {
        "ability_1": {"name": "Cursed Energy Blast", "mult": 3},
        "ability_2": {"name": "Rika's Wrath", "mult": 5},
        "ability_3": {"name": "Copy: Ultimate", "mult": 10, "once": True},
    },
    "Kenjaku": {
        "ability_1": {"name": "Cursed Spirit Army", "mult": 3},
        "ability_2": {"name": "Uzumaki", "mult": 5},
        "ability_3": {"name": "Brain Transplant", "mult": 10, "once": True},
    },
    "Yuki Tsukumo": {
        "ability_1": {"name": "Star Rage", "mult": 3},
        "ability_2": {"name": "Mass Punch", "mult": 5},
        "ability_3": {"name": "Black Hole", "mult": 10, "once": True},
    },
    "Suguru Geto": {
        "ability_1": {"name": "Cursed Spirit Army", "mult": 3},
        "ability_2": {"name": "Uzumaki", "mult": 5},
        "ability_3": {"name": "Maximum Uzumaki", "mult": 10, "once": True},
    },
    "Toji Fushiguro": {
        "ability_1": {"name": "Inverted Spear", "mult": 3},
        "ability_2": {"name": "Heavenly Restriction", "mult": 5},
        "ability_3": {"name": "Split Soul Katana", "mult": 10, "once": True},
    },
    "Kinji Hakari": {
        "ability_1": {"name": "Jackpot", "mult": 3},
        "ability_2": {"name": "Pure Love Train", "mult": 5},
        "ability_3": {"name": "Idle Death Gamble", "mult": 10, "once": True},
    },
    "Hiromi Higuruma": {
        "ability_1": {"name": "Judgeman", "mult": 3},
        "ability_2": {"name": "Confiscation", "mult": 5},
        "ability_3": {"name": "Deadly Sentencing", "mult": 10, "once": True},
    },
    "Hajime Kashimo": {
        "ability_1": {"name": "Lightning Discharge", "mult": 3},
        "ability_2": {"name": "Mythical Beast Amber", "mult": 5},
        "ability_3": {"name": "Thunder God", "mult": 10, "once": True},
    },
    "Yuji Modulo": {
        "ability_1": {"name": "Divergent Fist", "mult": 3},
        "ability_2": {"name": "Shrine", "mult": 5},
        "ability_3": {"name": "Modulo Form", "mult": 10, "once": True},
    },
    "Uraume": {
        "ability_1": {"name": "Frost Strike", "mult": 3},
        "ability_2": {"name": "Ice Formation", "mult": 5},
        "ability_3": {"name": "Absolute Zero", "mult": 10, "once": True},
    },
    "SUKUNA ITADORI BODY": {
        "ability_1": {"name": "Dismantle", "mult": 3},
        "ability_2": {"name": "Cleave", "mult": 5},
        "ability_3": {"name": "Malevolent Shrine", "mult": 10, "once": True},
    },
    # ============ A RANK ============
    "Yuji Itadori": {
        "ability_1": {"name": "Divergent Fist", "mult": 3},
        "ability_2": {"name": "Black Flash", "mult": 5},
        "ability_3": {"name": "Sukuna's Awakening", "mult": 10, "once": True},
    },
    "Megumi Fushiguro": {
        "ability_1": {"name": "Divine Dogs", "mult": 3},
        "ability_2": {"name": "Max Elephant", "mult": 5},
        "ability_3": {"name": "Chimera Shadow Garden", "mult": 10, "once": True},
    },
    "Maki Zenin": {
        "ability_1": {"name": "Cursed Tool Mastery", "mult": 3},
        "ability_2": {"name": "Heavenly Restriction", "mult": 5},
        "ability_3": {"name": "Split Soul Katana", "mult": 10, "once": True},
    },
    "Kento Nanami": {
        "ability_1": {"name": "Ratio Technique 7:3", "mult": 3},
        "ability_2": {"name": "Overtime", "mult": 5},
        "ability_3": {"name": "Ratio: Critical", "mult": 10, "once": True},
    },
    "Mei Mei": {
        "ability_1": {"name": "Black Bird Manipulation", "mult": 3},
        "ability_2": {"name": "Bird Attack", "mult": 5},
        "ability_3": {"name": "Crow Strike", "mult": 10, "once": True},
    },
    "Aoi Todo": {
        "ability_1": {"name": "Boogie Woogie", "mult": 3},
        "ability_2": {"name": "Divergent Fist", "mult": 5},
        "ability_3": {"name": "Todo's Gambit", "mult": 10, "once": True},
    },
    "Choso": {
        "ability_1": {"name": "Blood Manipulation", "mult": 3},
        "ability_2": {"name": "Piercing Blood", "mult": 5},
        "ability_3": {"name": "Supernova", "mult": 10, "once": True},
    },
    "Naoya Zenin": {
        "ability_1": {"name": "Projection Sorcery", "mult": 3},
        "ability_2": {"name": "Speed Strike", "mult": 5},
        "ability_3": {"name": "Time Cell Moon Palace", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Nobara Kugisaki": {
        "ability_1": {"name": "Straw Doll Technique", "mult": 3},
        "ability_2": {"name": "Resonance", "mult": 5},
        "ability_3": {"name": "Black Flash", "mult": 10, "once": True},
    },
    "Toge Inumaki": {
        "ability_1": {"name": "Cursed Speech", "mult": 3},
        "ability_2": {"name": "Don't Move", "mult": 5},
        "ability_3": {"name": "Explode", "mult": 10, "once": True},
    },
    "Kirara Hoshi": {
        "ability_1": {"name": "Love Rendezvous", "mult": 3},
        "ability_2": {"name": "Star Shot", "mult": 5},
        "ability_3": {"name": "Star Fall", "mult": 10, "once": True},
    },
    "Hana Kurusu": {
        "ability_1": {"name": "Jacob's Ladder", "mult": 3},
        "ability_2": {"name": "Divine Flame", "mult": 5},
        "ability_3": {"name": "Angel's Wrath", "mult": 10, "once": True},
    },
}

# ============================================================
# DOMAINS
# ============================================================
DOMAINS_JJK = {
    "Gojo Satoru": {"name": "Unlimited Void", "type": "single", "duration": 2, "cooldown": 3,
        "effects": {"freeze": 1, "hp_drain": 10, "atk_boost": 15, "heal": 20}},
    "Yuta Okkotsu": {"name": "Authentic Mutual Love", "type": "single", "duration": 2, "cooldown": 3,
        "effects": {"atk_boost": 20, "dodge_boost": 15, "hp_drain": 5, "heal_per_turn": 5}},
    "Kenjaku": {"name": "Womb Profusion", "type": "multi", "duration": 2, "cooldown": 3,
        "effects": {"spirits": 2, "dodge_debuff": 15, "hp_drain": 3}},
    "Kinji Hakari": {"name": "Idle Death Gamble", "type": "multi", "duration": 2, "cooldown": 3,
        "effects": {"gamble": 50, "atk_boost": 15, "heal_per_turn": 8}},
    "Hiromi Higuruma": {"name": "Deadly Sentencing", "type": "multi", "duration": 2, "cooldown": 3,
        "effects": {"no_defense": True, "disable_ability": 1, "atk_boost": 15}},
    "Yuji Modulo": {"name": "Unnamed Domain", "type": "multi", "duration": 2, "cooldown": 3,
        "effects": {"atk_boost": 20, "freeze": 1, "dodge_debuff": 15}},
    "SUKUNA ITADORI BODY": {"name": "Malevolent Shrine", "type": "all", "duration": 2, "cooldown": 2,
        "effects": {"atk_boost": 20, "hp_drain": 8, "dodge_debuff": 15}},
    "Yuji Itadori": {"name": "Unnamed Domain", "type": "single", "duration": 2, "cooldown": 3,
        "effects": {"atk_boost": 15, "heal": 20, "hp_drain": 3}},
    "Megumi Fushiguro": {"name": "Chimera Shadow Garden", "type": "single", "duration": 2, "cooldown": 3,
        "effects": {"shadows": 2, "dodge_debuff": 15, "hp_drain": 5, "heal_per_turn": 5}},
    "Naoya Zenin": {"name": "Time Cell Moon Palace", "type": "single", "duration": 2, "cooldown": 3,
        "effects": {"freeze": 1, "frames": 2, "dodge_boost": 15}},
    "Sukuna Heian": {"name": "Malevolent Shrine", "type": "all", "duration": 3, "cooldown": 3,
        "effects": {"atk_boost": 30, "hp_drain": 8, "dodge_debuff": 25, "no_defense": True}},
    "Sukuna Megumi": {"name": "Malevolent Shrine", "type": "all", "duration": 3, "cooldown": 3,
        "effects": {"atk_boost": 25, "freeze": 1, "hp_drain": 5}},
    "Mahoraga": {"name": "Divine Judgment", "type": "single", "duration": 3, "cooldown": 3,
        "effects": {"hp_drain": 25, "atk_boost": 20}},
    "Mahito": {"name": "Self-Embodiment of Perfection", "type": "single", "duration": 3, "cooldown": 3,
        "effects": {"dodge_debuff": 50, "atk_boost": 25, "hp_drain": 10}},
    "Uraume": {"name": "Absolute Zero", "type": "single", "duration": 3, "cooldown": 3,
        "effects": {"freeze": 1, "atk_boost": 20, "hp_drain": 8, "no_defense": True}},
    "Dabura": {"name": "Void Shrine", "type": "all", "duration": 3, "cooldown": 3,
        "effects": {"atk_boost": 25, "dodge_debuff": 20, "hp_drain": 5}},
}

# ============================================================
# BOSSES (مرتب‌شده بر اساس قدرت)
# ============================================================
BOSSES_JJK = {
    # 🟢 ضعیف (HP < 5k، ATK < 300) — جایزه: 50,000
    "Small Shadow": {"display_name": "سایه کوچک", "hp": 500, "atk": 40, "reward": 50000},
    "Cursed Spirit": {"display_name": "روح سرگردان", "hp": 800, "atk": 60, "reward": 50000},
    "Shadow Wolf": {"display_name": "گرگ سایه", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط (HP 5k-20k، ATK 300-800) — جایزه: 100,000 (۲ برابر)
    "Cursed Worm": {"display_name": "کرم نفرین‌شده", "hp": 6000, "atk": 400, "reward": 100000},
    "Hell Spider": {"display_name": "عنکبوت جهنمی", "hp": 8000, "atk": 500, "reward": 100000},

    # 🟠 قوی (HP 20k-50k، ATK 800-2k) — جایزه: 200,000 (۲ برابر)
    "Uraume": {
        "display_name": "اوراومه", "hp": 60000, "atk": 2600, "reward": 200000,
        "fodder": ["Small Shadow", "Cursed Spirit"],
        "ability_1": {"name": "Frozen Domain", "effect": "Freeze enemy (1 turn)", "type": "freeze"},
        "ability_2": {"name": "Ice Tomb", "effect": "ATK x4", "type": "damage"},
    },
    "Mahito": {
        "display_name": "ماهیتو", "hp": 70000, "atk": 3000, "reward": 200000,
        "fodder": ["Cursed Spirit", "Cursed Spirit", "Small Shadow", "Small Shadow"],
        "ability_1": {"name": "Idle Transfiguration", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Soul Manipulation", "effect": "20% HP damage", "type": "damage"},
    },
    "Mahoraga": {
        "display_name": "ماهوراگا", "hp": 80000, "atk": 5000, "reward": 200000,
        "fodder": ["Shadow Wolf", "Shadow Wolf"],
        "ability_1": {"name": "Adaptation Wheel", "effect": "ATK +100 per turn", "type": "buff"},
        "ability_2": {"name": "Sword of Extermination", "effect": "ATK x5 (ignore DEF)", "type": "damage"},
    },
    "Sukuna Megumi": {
        "display_name": "سوکونا (بدن مگومی)", "hp": 90000, "atk": 3600, "reward": 200000,
        "fodder": ["Small Shadow", "Shadow Wolf", "Cursed Spirit"],
        "ability_1": {"name": "Dismantle", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Ten Shadows", "effect": "2 shadows x2 ATK", "type": "multi"},
    },

    # 🔴 افسانه‌ای (HP 50k+، ATK 2k+) — جایزه: 500,000 (۲ برابر)
    "Dabura": {
        "display_name": "دابورا", "hp": 190000, "atk": 5000, "reward": 500000,
        "fodder": ["Small Shadow", "Small Shadow", "Cursed Spirit"],
        "ability_1": {"name": "Cursed Energy Blast", "effect": "ATK x4", "type": "damage"},
        "ability_2": {"name": "Dark Rift", "effect": "25% HP damage", "type": "damage"},
    },
    "Sukuna Heian": {
        "display_name": "سوکونا (فرم هیان)", "hp": 200000, "atk": 6000, "reward": 500000,
        "fodder": ["Small Shadow", "Cursed Spirit", "Cursed Spirit"],
        "ability_1": {"name": "Dismantle", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Cleave", "effect": "ATK x5", "type": "damage"},
    },
}

# ============================================================
# FODDER
# ============================================================
FODDER_JJK = {
    "Small Shadow": {"display_name": "سایه کوچک", "hp": 500, "atk": 40, "reward": 5000},
    "Cursed Spirit": {"display_name": "روح سرگردان", "hp": 800, "atk": 60, "reward": 5000},
    "Shadow Wolf": {"display_name": "گرگ سایه", "hp": 1200, "atk": 90, "reward": 5000},
    "Weak Curse": {"display_name": "نفرین‌شده ضعیف", "hp": 2000, "atk": 150, "reward": 5000},
    "Cursed Worm": {"display_name": "کرم نفرین‌شده", "hp": 3000, "atk": 200, "reward": 5000},
    "Hell Spider": {"display_name": "عنکبوت جهنمی", "hp": 4000, "atk": 250, "reward": 5000},
}

# ============================================================
# COOLDOWNS
# ============================================================
COOLDOWNS_JJK = {"ability_1": 1, "ability_2": 2, "domain": 3}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_char_abilities(char_name):
    return ABILITIES_JJK.get(char_name, {})

def get_char_domain(char_name):
    return DOMAINS_JJK.get(char_name, None)

def get_boss_data(boss_name):
    return BOSSES_JJK.get(boss_name, None)

def get_fodder_data(fodder_name):
    return FODDER_JJK.get(fodder_name, None)

def is_jjk_character(char_name):
    for rank in CHARACTERS_JJK:
        if char_name in CHARACTERS_JJK[rank]:
            return True
    return False

def is_jjk_boss(boss_name):
    return boss_name in BOSSES_JJK

def has_domain(char_name):
    return char_name in DOMAINS_JJK

def get_character_rank(char_name):
    for rank in CHARACTERS_JJK:
        if char_name in CHARACTERS_JJK[rank]:
            return rank
    return None