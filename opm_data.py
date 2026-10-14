# ============================================================
# OPM DATA - One Punch Man Characters, Abilities, Bosses
# ============================================================

CHARACTERS_OPM = {
    "S": {
        "Saitama": "One Punch Man",
        "Blast": "Legendary Hero",
        "Boros": "Space Destroyer",
        "Garou": "Monster Hunter",
        "Tatsumaki": "Terror Sister",
        "Orochi": "Monster King",
        "Psykos": "Heavenly General",
        "Metal Bat": "CQC",
        "Zomnking": "Brutal",
    },
    "A": {
        "Suiryu": "Masked",
        "Bang": "Explosive Engine",
        "Gouketsu": "Former Champion",
        "Amai Mask": "Silver Mask",
        "Genos": "Vengeful Cyborg",
    },
    "B": {
        "Wacsmann": "Tatsumaki's Disciple",
        "Sonic": "Speed Ninja",
        "Mumen Rider": "Justice",
    },
    "C": {
        "Fubuki": "Sweet Talker",
        "King": "Coward Hero",
        "Pri-Pri Prisoner": "Prisoner",
    },
}

# ============================================================
# ABILITIES (2 per character)
# ============================================================
ABILITIES_OPM = {
    # ============ S RANK ============
    "Saitama": {
        "ability_1": {"name": "Normal Punch", "effect": "ATK x4", "type": "damage"},
        "ability_2": {"name": "Serious Punch", "effect": "ATK x7", "type": "damage"},
    },
    "Blast": {
        "ability_1": {"name": "Gravity Knuckle", "effect": "ATK x4", "type": "damage"},
        "ability_2": {"name": "Dimensional Gate", "effect": "DODGE +30% (permanent)", "type": "buff"},
    },
    "Boros": {
        "ability_1": {"name": "Meteoric Burst", "effect": "ATK x4", "type": "damage"},
        "ability_2": {"name": "Collapsing Star", "effect": "ATK x6", "type": "damage"},
    },
    "Garou": {
        "ability_1": {"name": "Whirlwind Fist", "effect": "3 hits x1.5 ATK", "type": "multi"},
        "ability_2": {"name": "Monster Calamity", "effect": "ATK x5", "type": "damage"},
    },
    "Tatsumaki": {
        "ability_1": {"name": "Psychic Wave", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Psychic Crush", "effect": "ATK x4 + enemy DODGE -30%", "type": "damage"},
    },
    "Orochi": {
        "ability_1": {"name": "Monster Cannon", "effect": "ATK x4", "type": "damage"},
        "ability_2": {"name": "Horn Drill", "effect": "ATK x5", "type": "damage"},
    },
    "Psykos": {
        "ability_1": {"name": "Psychic Blast", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Ruin Wave", "effect": "ATK x4", "type": "damage"},
    },
    "Metal Bat": {
        "ability_1": {"name": "Fighting Spirit", "effect": "ATK +100 (2 turns)", "type": "buff"},
        "ability_2": {"name": "Home Run", "effect": "ATK x5", "type": "damage"},
    },
    "Zomnking": {
        "ability_1": {"name": "Savage Roar", "effect": "Enemy ATK -25%", "type": "debuff"},
        "ability_2": {"name": "Berserk", "effect": "ATK x4", "type": "damage"},
    },

    # ============ A RANK ============
    "Suiryu": {
        "ability_1": {"name": "Void Fist", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Crushing Kick", "effect": "ATK x4", "type": "damage"},
    },
    "Bang": {
        "ability_1": {"name": "Flowing Water", "effect": "ATK x3 + DODGE +20%", "type": "damage"},
        "ability_2": {"name": "Fist of Roar", "effect": "ATK x5", "type": "damage"},
    },
    "Gouketsu": {
        "ability_1": {"name": "Monster Strength", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Meteor Kick", "effect": "ATK x4", "type": "damage"},
    },
    "Amai Mask": {
        "ability_1": {"name": "Handsome Blow", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Monster Form", "effect": "ATK +100 (3 turns)", "type": "buff"},
    },
    "Genos": {
        "ability_1": {"name": "Machine Gun Blow", "effect": "3 hits x1.5 ATK", "type": "multi"},
        "ability_2": {"name": "Incinerate", "effect": "ATK x4", "type": "damage"},
    },

    # ============ B RANK ============
    "Wacsmann": {
        "ability_1": {"name": "Love Attack", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Charm", "effect": "Enemy ATK -20%", "type": "debuff"},
    },
    "Sonic": {
        "ability_1": {"name": "Speed Slash", "effect": "ATK x3", "type": "damage"},
        "ability_2": {"name": "Wind Blade Kick", "effect": "ATK x3.5", "type": "damage"},
    },
    "Mumen Rider": {
        "ability_1": {"name": "Justice Punch", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Justice Crash", "effect": "ATK x2.5", "type": "damage"},
    },

    # ============ C RANK ============
    "Fubuki": {
        "ability_1": {"name": "Psychic Push", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Hell Storm", "effect": "ATK x3", "type": "damage"},
    },
    "King": {
        "ability_1": {"name": "King Engine", "effect": "Enemy frozen (1 turn)", "type": "freeze"},
        "ability_2": {"name": "Ultimate Hellfire", "effect": "ATK x3", "type": "damage"},
    },
    "Pri-Pri Prisoner": {
        "ability_1": {"name": "Angel Rush", "effect": "ATK x2", "type": "damage"},
        "ability_2": {"name": "Prisoner Love", "effect": "ATK x3", "type": "damage"},
    },
}

# ============================================================
# BOSSES (OPM)
# ============================================================
BOSSES_OPM = {
    "Wolf Monster": {
        "display_name": "گرگ هیولا",
        "hp": 500,
        "atk": 40,
        "reward": 100000,
    },
    "Tiger Beast": {
        "display_name": "ببر وحشی",
        "hp": 1200,
        "atk": 80,
        "reward": 100000,
    },
    "Demon Fish": {
        "display_name": "ماهی شیطانی",
        "hp": 2500,
        "atk": 150,
        "reward": 100000,
    },
    "Sky King": {
        "display_name": "پادشاه آسمان",
        "hp": 4000,
        "atk": 250,
        "reward": 100000,
    },
    "Deep Sea King": {
        "display_name": "پادشاه اعماق دریا",
        "hp": 6000,
        "atk": 350,
        "reward": 100000,
    },
    "Elder Centipede": {
        "display_name": "هزارپای بزرگ",
        "hp": 9000,
        "atk": 500,
        "reward": 130000,
    },
    "Monster Garou": {
        "display_name": "گارو هیولا",
        "hp": 12000,
        "atk": 700,
        "reward": 130000,
    },
    "Saitama Phase 1": {
        "display_name": "سایتاما (فاز ۱)",
        "hp": 5000,
        "atk": 9999,
        "reward": 150000,
    },
    "Goku Lv1": {
        "display_name": "گوکو سطح ۱",
        "hp": 1500,
        "atk": 150,
        "reward": 100000,
    },
    "Goku Lv2": {
        "display_name": "گوکو سطح ۲",
        "hp": 3000,
        "atk": 300,
        "reward": 130000,
    },
    "Goku Lv3": {
        "display_name": "گوکو سطح ۳",
        "hp": 5000,
        "atk": 500,
        "reward": 130000,
    },
    "Saitama + Goku": {
        "display_name": "سایتاما + گوکو",
        "hp": 7000,
        "atk": 9999,
        "reward": 150000,
    },
}