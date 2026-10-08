# ============================================================
# JJK DATA - Jujutsu Kaisen Characters, Abilities, Domains
# ============================================================

# ============================================================
# CHARACTERS (23 characters)
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
    "S": 200000,
    "A": 140000,
    "B": 70000,
}

# ============================================================
# ABILITIES (2 per character, no Domain)
# ============================================================
ABILITIES_JJK = {
    # ============ S RANK ============
    "Gojo Satoru": {
        "ability_1": {"name": "Limitless", "effect": "DODGE 90% (1 turn)", "type": "dodge"},
        "ability_2": {"name": "Hollow Purple", "effect": "ATK x5", "type": "damage"},
    },
    "Yuta Okkotsu": {
        "ability_1": {"name": "Copy Technique", "effect": "Copy enemy attack", "type": "copy"},
        "ability_2": {"name": "Cursed Energy Blast", "effect": "ATK x3", "type": "damage"},
    },
    "Kenjaku": {
        "ability_1": {"name": "Brain Transplant", "effect": "Enemy -25% ATK (1 turn)", "type": "debuff"},
        "ability_2": {"name": "Cursed Spirit Army", "effect": "2 spirits x2 ATK", "type": "multi"},
    },
    "Yuki Tsukumo": {
        "ability_1": {"name": "Star Rage", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Mass Punch", "effect": "ATK x4", "type": "damage"},
    },
    "Suguru Geto": {
        "ability_1": {"name": "Cursed Spirit Army", "effect": "3 hits x1 ATK", "type": "multi"},
        "ability_2": {"name": "Uzumaki", "effect": "ATK x4", "type": "damage"},
    },
    "Toji Fushiguro": {
        "ability_1": {"name": "Inverted Spear", "effect": "Ignore DEF", "type": "damage"},
        "ability_2": {"name": "Heavenly Restriction", "effect": "DODGE +25% (permanent)", "type": "buff"},
    },
    "Kinji Hakari": {
        "ability_1": {"name": "Jackpot", "effect": "50% chance 4x ATK", "type": "gamble"},
        "ability_2": {"name": "Pure Love Train", "effect": "ATK x3 + DODGE +20%", "type": "damage"},
    },
    "Hiromi Higuruma": {
        "ability_1": {"name": "Judgeman", "effect": "Enemy -30% ATK (1 turn)", "type": "debuff"},
        "ability_2": {"name": "Confiscation", "effect": "Disable 1 enemy ability", "type": "disable"},
    },
    "Hajime Kashimo": {
        "ability_1": {"name": "Mythical Beast Amber", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Lightning Discharge", "effect": "50% chance 5x ATK", "type": "gamble"},
    },
    "Yuji Modulo": {
        "ability_1": {"name": "Divergent Fist", "effect": "2 hits in 1 turn", "type": "multi"},
        "ability_2": {"name": "Shrine", "effect": "ATK x4", "type": "damage"},
    },
    "Uraume": {
        "ability_1": {"name": "Ice Formation", "effect": "Enemy -25% ATK", "type": "debuff"},
        "ability_2": {"name": "Frost Strike", "effect": "ATK x3 + no dodge", "type": "damage"},
    },

    # ============ A RANK ============
    "Yuji Itadori": {
        "ability_1": {"name": "Divergent Fist", "effect": "2 hits in 1 turn", "type": "multi"},
        "ability_2": {"name": "Black Flash", "effect": "25% chance 4x ATK", "type": "gamble"},
    },
    "Megumi Fushiguro": {
        "ability_1": {"name": "Divine Dogs", "effect": "2 dogs x1.5 ATK", "type": "multi"},
        "ability_2": {"name": "Max Elephant", "effect": "ATK x3", "type": "damage"},
    },
    "Maki Zenin": {
        "ability_1": {"name": "Cursed Tool Mastery", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Heavenly Restriction", "effect": "DODGE +25% (permanent)", "type": "buff"},
    },
    "Kento Nanami": {
        "ability_1": {"name": "Ratio Technique 7:3", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Overtime", "effect": "ATK +100 (2 turns)", "type": "buff"},
    },
    "Mei Mei": {
        "ability_1": {"name": "Black Bird Manipulation", "effect": "2 birds x1 ATK", "type": "multi"},
        "ability_2": {"name": "Bird Attack", "effect": "ATK x3", "type": "damage"},
    },
    "Aoi Todo": {
        "ability_1": {"name": "Boogie Woogie", "effect": "DODGE 100% (1 turn)", "type": "dodge"},
        "ability_2": {"name": "Divergent Fist", "effect": "ATK x3", "type": "damage"},
    },
    "Choso": {
        "ability_1": {"name": "Blood Manipulation", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Piercing Blood", "effect": "ATK x4 + 10% HP", "type": "damage"},
    },
    "Naoya Zenin": {
        "ability_1": {"name": "Projection Sorcery", "effect": "24 frames (2 hits)", "type": "multi"},
        "ability_2": {"name": "Speed Strike", "effect": "ATK x3", "type": "damage"},
    },

    # ============ B RANK ============
    "Nobara Kugisaki": {
        "ability_1": {"name": "Straw Doll Technique", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Resonance", "effect": "20% direct HP damage", "type": "damage"},
    },
    "Toge Inumaki": {
        "ability_1": {"name": "Cursed Speech", "effect": "Enemy frozen (1 turn)", "type": "freeze"},
        "ability_2": {"name": "Don't Move", "effect": "Enemy dodge 0 (1 turn)", "type": "debuff"},
    },
    "Kirara Hoshi": {
        "ability_1": {"name": "Love Rendezvous", "effect": "DODGE +20% (permanent)", "type": "buff"},
        "ability_2": {"name": "Star Shot", "effect": "ATK x3", "type": "damage"},
    },
    "Hana Kurusu": {
        "ability_1": {"name": "Jacob's Ladder", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Divine Flame", "effect": "ATK x4", "type": "damage"},
    },
}

# ============================================================
# DOMAINS (Domain Expansion)
# ============================================================
DOMAINS_JJK = {
    # ============ S RANK ============
    "Gojo Satoru": {
        "name": "Unlimited Void",
        "type": "single",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "freeze": 3,
            "hp_drain": 25,
            "atk_boost": 40,
            "heal": 50,
        },
    },
    "Yuta Okkotsu": {
        "name": "Authentic Mutual Love",
        "type": "single",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "atk_boost": 50,
            "dodge_boost": 30,
            "hp_drain": 10,
            "heal_per_turn": 15,
        },
    },
    "Kenjaku": {
        "name": "Womb Profusion",
        "type": "multi",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "spirits": 3,
            "dodge_debuff": 40,
            "hp_drain": 5,
        },
    },
    "Kinji Hakari": {
        "name": "Idle Death Gamble",
        "type": "multi",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "gamble": 50,
            "atk_boost": 30,
            "heal_per_turn": 20,
        },
    },
    "Hiromi Higuruma": {
        "name": "Deadly Sentencing",
        "type": "multi",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "no_defense": True,
            "disable_ability": 1,
            "atk_boost": 40,
        },
    },
    "Yuji Modulo": {
        "name": "Unnamed Domain",
        "type": "multi",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "atk_boost": 50,
            "freeze": 2,
            "dodge_debuff": 30,
        },
    },

    # ============ A RANK ============
    "Yuji Itadori": {
        "name": "Unnamed Domain",
        "type": "single",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "atk_boost": 40,
            "heal": 50,
            "hp_drain": 5,
        },
    },
    "Megumi Fushiguro": {
        "name": "Chimera Shadow Garden",
        "type": "single",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "shadows": 3,
            "dodge_debuff": 30,
            "hp_drain": 10,
            "heal_per_turn": 15,
        },
    },
    "Naoya Zenin": {
        "name": "Time Cell Moon Palace",
        "type": "single",
        "duration": 3,
        "cooldown": 3,
        "effects": {
            "freeze": 2,
            "frames": 3,
            "dodge_boost": 25,
        },
    },
}

# ============================================================
# BOSSES_JJK (6 Special Bosses - NPC, not purchasable)
# ============================================================
BOSSES_JJK = {
    "Sukuna Heian": {
        "display_name": "Sukuna (Heian Form)",
        "hp": 50000,
        "atk": 2000,
        "reward": 10000,
        "fodder": ["Small Shadow", "Cursed Spirit", "Cursed Spirit"],
        "ability_1": {"name": "Dismantle", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Cleave", "effect": "ATK x5", "type": "damage"},
        "domain": {
            "name": "Malevolent Shrine",
            "type": "all",
            "duration": 3,
            "cooldown": 3,
            "effects": {
                "atk_boost": 60,
                "hp_drain": 15,
                "dodge_debuff": 50,
                "no_defense": True,
            },
        },
    },
    "Sukuna Megumi": {
        "display_name": "Sukuna (Megumi's Body)",
        "hp": 45000,
        "atk": 1800,
        "reward": 10000,
        "fodder": ["Small Shadow", "Shadow Wolf", "Cursed Spirit"],
        "ability_1": {"name": "Dismantle", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Ten Shadows", "effect": "2 shadows x2 ATK", "type": "multi"},
        "domain": {
            "name": "Malevolent Shrine",
            "type": "all",
            "duration": 3,
            "cooldown": 3,
            "effects": {
                "atk_boost": 50,
                "freeze": 2,
                "hp_drain": 10,
            },
        },
    },
    "Mahoraga": {
        "display_name": "Divine General Mahoraga",
        "hp": 40000,
        "atk": 2500,
        "reward": 10000,
        "fodder": ["Shadow Wolf", "Shadow Wolf"],
        "ability_1": {"name": "Adaptation Wheel", "effect": "ATK +100 per turn", "type": "buff"},
        "ability_2": {"name": "Sword of Extermination", "effect": "ATK x5 (ignore DEF)", "type": "damage"},
        "domain": {
            "name": "Divine Judgment",
            "type": "single",
            "duration": 3,
            "cooldown": 3,
            "effects": {
                "hp_drain": 50,
                "atk_boost": 40,
            },
        },
    },
    "Mahito": {
        "display_name": "Mahito",
        "hp": 35000,
        "atk": 1500,
        "reward": 10000,
        "fodder": ["Cursed Spirit", "Cursed Spirit", "Small Shadow", "Small Shadow"],
        "ability_1": {"name": "Idle Transfiguration", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Soul Manipulation", "effect": "20% HP damage", "type": "damage"},
        "domain": {
            "name": "Self-Embodiment of Perfection",
            "type": "single",
            "duration": 3,
            "cooldown": 3,
            "effects": {
                "dodge_debuff": 100,
                "atk_boost": 50,
                "hp_drain": 20,
            },
        },
    },
    "Uraume": {
        "display_name": "Uraume",
        "hp": 30000,
        "atk": 1300,
        "reward": 10000,
        "fodder": ["Small Shadow", "Cursed Spirit"],
        "ability_1": {"name": "Frozen Domain", "effect": "Freeze enemy (1 turn)", "type": "freeze"},
        "ability_2": {"name": "Ice Tomb", "effect": "ATK x4", "type": "damage"},
        "domain": {
            "name": "Absolute Zero",
            "type": "single",
            "duration": 3,
            "cooldown": 3,
            "effects": {
                "freeze": 2,
                "atk_boost": 40,
                "hp_drain": 15,
                "no_defense": True,
            },
        },
    },
    "Dabura": {
        "display_name": "Dabura",
        "hp": 28000,
        "atk": 1200,
        "reward": 10000,
        "fodder": ["Small Shadow", "Small Shadow", "Cursed Spirit"],
        "ability_1": {"name": "Cursed Energy Blast", "effect": "ATK x4", "type": "damage"},
        "ability_2": {"name": "Dark Rift", "effect": "25% HP damage", "type": "damage"},
        "domain": {
            "name": "Void Shrine",
            "type": "all",
            "duration": 3,
            "cooldown": 3,
            "effects": {
                "atk_boost": 50,
                "dodge_debuff": 40,
                "hp_drain": 10,
            },
        },
    },
}

# ============================================================
# FODDER (6 weak enemies - coin farm)
# ============================================================
FODDER_JJK = {
    "Small Shadow": {
        "display_name": "سایه کوچک",
        "hp": 500,
        "atk": 40,
        "reward": 100,
    },
    "Cursed Spirit": {
        "display_name": "روح سرگردان",
        "hp": 800,
        "atk": 60,
        "reward": 200,
    },
    "Shadow Wolf": {
        "display_name": "گرگ سایه",
        "hp": 1200,
        "atk": 90,
        "reward": 350,
    },
    "Weak Curse": {
        "display_name": "نفرین‌شده ضعیف",
        "hp": 2000,
        "atk": 150,
        "reward": 600,
    },
    "Cursed Worm": {
        "display_name": "کرم نفرین‌شده",
        "hp": 3000,
        "atk": 200,
        "reward": 900,
    },
    "Hell Spider": {
        "display_name": "عنکبوت جهنمی",
        "hp": 4000,
        "atk": 250,
        "reward": 1200,
    },
}

# ============================================================
# COOLDOWNS
# ============================================================
COOLDOWNS_JJK = {
    "ability_1": 1,
    "ability_2": 2,
    "domain": 3,
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_char_abilities(char_name):
    """Get abilities for a specific character"""
    return ABILITIES_JJK.get(char_name, {})


def get_char_domain(char_name):
    """Get domain for a specific character"""
    return DOMAINS_JJK.get(char_name, None)


def get_boss_data(boss_name):
    """Get boss data"""
    return BOSSES_JJK.get(boss_name, None)


def get_fodder_data(fodder_name):
    """Get fodder data"""
    return FODDER_JJK.get(fodder_name, None)


def is_jjk_character(char_name):
    """Check if character is from JJK"""
    for rank in CHARACTERS_JJK:
        if char_name in CHARACTERS_JJK[rank]:
            return True
    return False


def is_jjk_boss(boss_name):
    """Check if boss is from JJK"""
    return boss_name in BOSSES_JJK


def has_domain(char_name):
    """Check if character has a domain"""
    return char_name in DOMAINS_JJK


def get_character_rank(char_name):
    """Get rank of a JJK character"""
    for rank in CHARACTERS_JJK:
        if char_name in CHARACTERS_JJK[rank]:
            return rank
    return None
