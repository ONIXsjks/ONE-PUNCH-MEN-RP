# ============================================================
# OPM DATA - One Punch Man
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
# ABILITIES - هر کاراکتر ۳ Ability
# ============================================================
ABILITIES_OPM = {
    # ============ S RANK ============
    "Saitama": {
        "ability_1": {"name": "Normal Punch", "mult": 3},
        "ability_2": {"name": "Serious Punch", "mult": 5},
        "ability_3": {"name": "Serious Punch (Full Power)", "mult": 10, "once": True},
    },
    "Blast": {
        "ability_1": {"name": "Gravity Knuckle", "mult": 3},
        "ability_2": {"name": "Dimensional Gate", "mult": 5},
        "ability_3": {"name": "Gravity Wave", "mult": 10, "once": True},
    },
    "Boros": {
        "ability_1": {"name": "Meteoric Burst", "mult": 3},
        "ability_2": {"name": "Collapsing Star", "mult": 5},
        "ability_3": {"name": "Roaring Cannon", "mult": 10, "once": True},
    },
    "Garou": {
        "ability_1": {"name": "Whirlwind Fist", "mult": 3},
        "ability_2": {"name": "Monster Calamity", "mult": 5},
        "ability_3": {"name": "God Slayer", "mult": 10, "once": True},
    },
    "Tatsumaki": {
        "ability_1": {"name": "Psychic Wave", "mult": 3},
        "ability_2": {"name": "Psychic Crush", "mult": 5},
        "ability_3": {"name": "Full Power", "mult": 10, "once": True},
    },
    "Orochi": {
        "ability_1": {"name": "Monster Cannon", "mult": 3},
        "ability_2": {"name": "Horn Drill", "mult": 5},
        "ability_3": {"name": "Gaia Cannon", "mult": 10, "once": True},
    },
    "Psykos": {
        "ability_1": {"name": "Psychic Blast", "mult": 3},
        "ability_2": {"name": "Ruin Wave", "mult": 5},
        "ability_3": {"name": "Fusion Form", "mult": 10, "once": True},
    },
    "Metal Bat": {
        "ability_1": {"name": "Fighting Spirit", "mult": 3},
        "ability_2": {"name": "Home Run", "mult": 5},
        "ability_3": {"name": "Full Swing", "mult": 10, "once": True},
    },
    "Zomnking": {
        "ability_1": {"name": "Savage Roar", "mult": 3},
        "ability_2": {"name": "Berserk", "mult": 5},
        "ability_3": {"name": "Rampage", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Suiryu": {
        "ability_1": {"name": "Void Fist", "mult": 3},
        "ability_2": {"name": "Crushing Kick", "mult": 5},
        "ability_3": {"name": "Void Shower", "mult": 10, "once": True},
    },
    "Bang": {
        "ability_1": {"name": "Flowing Water", "mult": 3},
        "ability_2": {"name": "Fist of Roar", "mult": 5},
        "ability_3": {"name": "Awakening Breath", "mult": 10, "once": True},
    },
    "Gouketsu": {
        "ability_1": {"name": "Monster Strength", "mult": 3},
        "ability_2": {"name": "Meteor Kick", "mult": 5},
        "ability_3": {"name": "Rampage", "mult": 10, "once": True},
    },
    "Amai Mask": {
        "ability_1": {"name": "Handsome Blow", "mult": 3},
        "ability_2": {"name": "Monster Form", "mult": 5},
        "ability_3": {"name": "True Form", "mult": 10, "once": True},
    },
    "Genos": {
        "ability_1": {"name": "Machine Gun Blow", "mult": 3},
        "ability_2": {"name": "Incinerate", "mult": 5},
        "ability_3": {"name": "True Spiral Incineration", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Wacsmann": {
        "ability_1": {"name": "Love Attack", "mult": 3},
        "ability_2": {"name": "Charm", "mult": 5},
        "ability_3": {"name": "Heart Break", "mult": 10, "once": True},
    },
    "Sonic": {
        "ability_1": {"name": "Speed Slash", "mult": 3},
        "ability_2": {"name": "Wind Blade Kick", "mult": 5},
        "ability_3": {"name": "Explosive Shuriken", "mult": 10, "once": True},
    },
    "Mumen Rider": {
        "ability_1": {"name": "Justice Punch", "mult": 3},
        "ability_2": {"name": "Justice Crash", "mult": 5},
        "ability_3": {"name": "Justice Tackle", "mult": 10, "once": True},
    },

    # ============ C RANK ============
    "Fubuki": {
        "ability_1": {"name": "Psychic Push", "mult": 3},
        "ability_2": {"name": "Hell Storm", "mult": 5},
        "ability_3": {"name": "Psychic Whirlwind", "mult": 10, "once": True},
    },
    "King": {
        "ability_1": {"name": "King Engine", "mult": 3},
        "ability_2": {"name": "Ultimate Hellfire", "mult": 5},
        "ability_3": {"name": "King's Presence", "mult": 10, "once": True},
    },
    "Pri-Pri Prisoner": {
        "ability_1": {"name": "Angel Rush", "mult": 3},
        "ability_2": {"name": "Prisoner Love", "mult": 5},
        "ability_3": {"name": "Angel Style", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES (مرتب‌شده بر اساس قدرت)
# ============================================================
BOSSES_OPM = {
    # 🟢 ضعیف (HP < 5k، ATK < 300) — جایزه: 50,000
    "Wolf Monster": {"display_name": "گرگ هیولا", "hp": 500, "atk": 40, "reward": 50000},
    "Tiger Beast": {"display_name": "ببر وحشی", "hp": 1200, "atk": 80, "reward": 50000},
    "Mosquito Girl": {"display_name": "پشه‌دختر", "hp": 2000, "atk": 150, "reward": 50000},
    "Demon Fish": {"display_name": "ماهی شیطانی", "hp": 2500, "atk": 150, "reward": 50000},

    # 🟡 متوسط (HP 5k-20k، ATK 300-800) — جایزه: 100,000
    "Sky King": {"display_name": "پادشاه آسمان", "hp": 8000, "atk": 500, "reward": 100000},
    "Deep Sea King": {"display_name": "پادشاه اعماق دریا", "hp": 12000, "atk": 700, "reward": 100000},
    "Carnage Kabuto": {"display_name": "کارنیج کابوتو", "hp": 16000, "atk": 1200, "reward": 100000},
    "Elder Centipede": {"display_name": "هزارپای بزرگ", "hp": 18000, "atk": 1000, "reward": 100000},
    "Beefcake": {"display_name": "کیک‌گوشتی", "hp": 24000, "atk": 1400, "reward": 100000},

    # 🔴 افسانه‌ای (HP 50k+، ATK 2k+) — جایزه: 500,000
    "Monster Garou": {"display_name": "گارو هیولا", "hp": 160000, "atk": 5000, "reward": 500000},
    "Saitama Phase 1": {"display_name": "سایتاما (فاز ۱)", "hp": 180000, "atk": 6000, "reward": 500000},
}