# ============================================================
# MUSHOKU TENSEI DATA
# ============================================================

CHARACTERS_MUSHOKU = {
    "S": {
        "Rudeus Greyrat": "Quagmire Rudeus",
        "Orsted": "Dragon God",
        "Eris Boreas Greyrat": "Sword King",
        "Ruijerd Superdia": "Superd Warrior",
        "Ghislaine Dedoldia": "Sword King",
        "Paul Greyrat": "Sword Saint",
        "Roxy Migurdia": "Water Saint",
        "Sylphiette": "Silent Fittoa",
        "Perugius Dola": "Armored Dragon King",
        "Kishirika Kishirisu": "Demon Emperor",
    },
    "A": {
        "Zanoba Shirone": "Doll Maker",
        "Cliff Grimoire": "Mage",
        "Elinalise Dragonroad": "Elf Warrior",
        "Talhand": "Dwarf Warrior",
        "Badigadi": "Immortal Demon King",
        "Aisha Greyrat": "Rudeus' Sister",
        "Norn Greyrat": "Rudeus' Sister",
        "Lara Greyrat": "Rudeus' Daughter",
        "Sieghart Saladin Greyrat": "Rudeus' Son",
        "Lucy Greyrat": "Rudeus' Daughter",
    },
    "B": {
        "Zenith Greyrat": "Rudeus' Mother",
        "Lilia Greyrat": "Servant",
        "Sauros Boreas Greyrat": "Eris' Father",
        "Philip Boreas Greyrat": "Eris' Father",
        "Hilda Boreas Greyrat": "Eris' Mother",
        "Gyllene Dedoldia": "Ghislaine's Sister",
        "Gisu Dedoldia": "Beast Warrior",
        "Almanfi": "Fire Spirit",
        "Rinia Dedoldia": "Beast Warrior",
        "Pursena Adoldia": "Beast Warrior",
    },
}

CHAR_PRICES_MUSHOKU = {"S": 5000000, "A": 600000, "B": 150000}

ABILITIES_MUSHOKU = {
    # ============ S RANK ============
    "Rudeus Greyrat": {
        "ability_1": {"name": "Water Ball", "mult": 3},
        "ability_2": {"name": "Quagmire", "mult": 5},
        "ability_3": {"name": "Nuclear Explosion", "mult": 10, "once": True},
    },
    "Orsted": {
        "ability_1": {"name": "Dragon God Strike", "mult": 3},
        "ability_2": {"name": "Cursed Time Loop", "mult": 5},
        "ability_3": {"name": "Dragon God Full Power", "mult": 10, "once": True},
    },
    "Eris Boreas Greyrat": {
        "ability_1": {"name": "Sword God Strike", "mult": 3},
        "ability_2": {"name": "Sword King Rush", "mult": 5},
        "ability_3": {"name": "Longsword of Light", "mult": 10, "once": True},
    },
    "Ruijerd Superdia": {
        "ability_1": {"name": "Spear Strike", "mult": 3},
        "ability_2": {"name": "Superd Rush", "mult": 5},
        "ability_3": {"name": "Superd Warrior Full", "mult": 10, "once": True},
    },
    "Ghislaine Dedoldia": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Beast Rush", "mult": 5},
        "ability_3": {"name": "Sword King Full", "mult": 10, "once": True},
    },
    "Paul Greyrat": {
        "ability_1": {"name": "Sword Strike", "mult": 3},
        "ability_2": {"name": "Sword Saint Slash", "mult": 5},
        "ability_3": {"name": "Sword Saint Full", "mult": 10, "once": True},
    },
    "Roxy Migurdia": {
        "ability_1": {"name": "Water Ball", "mult": 3},
        "ability_2": {"name": "Ice Smash", "mult": 5},
        "ability_3": {"name": "Water Saint Full", "mult": 10, "once": True},
    },
    "Sylphiette": {
        "ability_1": {"name": "Wind Blade", "mult": 3},
        "ability_2": {"name": "Silent Cast", "mult": 5},
        "ability_3": {"name": "Silent Fittoa Full", "mult": 10, "once": True},
    },
    "Perugius Dola": {
        "ability_1": {"name": "Familiar Strike", "mult": 3},
        "ability_2": {"name": "Armored Dragon Attack", "mult": 5},
        "ability_3": {"name": "Armored Dragon King Full", "mult": 10, "once": True},
    },
    "Kishirika Kishirisu": {
        "ability_1": {"name": "Demon Eye", "mult": 3},
        "ability_2": {"name": "Demon Emperor Curse", "mult": 5},
        "ability_3": {"name": "Demon Emperor Full", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Zanoba Shirone": {
        "ability_1": {"name": "Doll Strike", "mult": 3},
        "ability_2": {"name": "Golem Punch", "mult": 5},
        "ability_3": {"name": "Doll Maker Full", "mult": 10, "once": True},
    },
    "Cliff Grimoire": {
        "ability_1": {"name": "Fire Ball", "mult": 3},
        "ability_2": {"name": "Magic Burst", "mult": 5},
        "ability_3": {"name": "Grimoire Full", "mult": 10, "once": True},
    },
    "Elinalise Dragonroad": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Elf Rush", "mult": 5},
        "ability_3": {"name": "Elf Warrior Full", "mult": 10, "once": True},
    },
    "Talhand": {
        "ability_1": {"name": "Axe Strike", "mult": 3},
        "ability_2": {"name": "Dwarf Rush", "mult": 5},
        "ability_3": {"name": "Dwarf Warrior Full", "mult": 10, "once": True},
    },
    "Badigadi": {
        "ability_1": {"name": "Demon Punch", "mult": 3},
        "ability_2": {"name": "Immortal Rush", "mult": 5},
        "ability_3": {"name": "Demon King Full", "mult": 10, "once": True},
    },
    "Aisha Greyrat": {
        "ability_1": {"name": "Magic Bolt", "mult": 3},
        "ability_2": {"name": "Fire Ball", "mult": 5},
        "ability_3": {"name": "Aisha's Power", "mult": 10, "once": True},
    },
    "Norn Greyrat": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Sword Rush", "mult": 5},
        "ability_3": {"name": "Norn's Resolve", "mult": 10, "once": True},
    },
    "Lara Greyrat": {
        "ability_1": {"name": "Magic Bolt", "mult": 3},
        "ability_2": {"name": "Water Ball", "mult": 5},
        "ability_3": {"name": "Lara's Power", "mult": 10, "once": True},
    },
    "Sieghart Saladin Greyrat": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Sword Rush", "mult": 5},
        "ability_3": {"name": "Sieghart's Resolve", "mult": 10, "once": True},
    },
    "Lucy Greyrat": {
        "ability_1": {"name": "Magic Bolt", "mult": 3},
        "ability_2": {"name": "Fire Ball", "mult": 5},
        "ability_3": {"name": "Lucy's Power", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Zenith Greyrat": {
        "ability_1": {"name": "Heal Pulse", "mult": 3},
        "ability_2": {"name": "Holy Light", "mult": 5},
        "ability_3": {"name": "Mother's Love", "mult": 10, "once": True},
    },
    "Lilia Greyrat": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Servant Rush", "mult": 5},
        "ability_3": {"name": "Lilia's Resolve", "mult": 10, "once": True},
    },
    "Sauros Boreas Greyrat": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Noble Rush", "mult": 5},
        "ability_3": {"name": "Boreas Power", "mult": 10, "once": True},
    },
    "Philip Boreas Greyrat": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Noble Rush", "mult": 5},
        "ability_3": {"name": "Boreas Power", "mult": 10, "once": True},
    },
    "Hilda Boreas Greyrat": {
        "ability_1": {"name": "Magic Bolt", "mult": 3},
        "ability_2": {"name": "Noble Magic", "mult": 5},
        "ability_3": {"name": "Boreas Magic", "mult": 10, "once": True},
    },
    "Gyllene Dedoldia": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Beast Rush", "mult": 5},
        "ability_3": {"name": "Beast Warrior Full", "mult": 10, "once": True},
    },
    "Gisu Dedoldia": {
        "ability_1": {"name": "Claw Strike", "mult": 3},
        "ability_2": {"name": "Beast Rush", "mult": 5},
        "ability_3": {"name": "Beast Warrior Full", "mult": 10, "once": True},
    },
    "Almanfi": {
        "ability_1": {"name": "Fire Ball", "mult": 3},
        "ability_2": {"name": "Flame Rush", "mult": 5},
        "ability_3": {"name": "Fire Spirit Full", "mult": 10, "once": True},
    },
    "Rinia Dedoldia": {
        "ability_1": {"name": "Claw Strike", "mult": 3},
        "ability_2": {"name": "Beast Rush", "mult": 5},
        "ability_3": {"name": "Beast Warrior Full", "mult": 10, "once": True},
    },
    "Pursena Adoldia": {
        "ability_1": {"name": "Claw Strike", "mult": 3},
        "ability_2": {"name": "Beast Rush", "mult": 5},
        "ability_3": {"name": "Beast Warrior Full", "mult": 10, "once": True},
    },
}
# ============================================================
# BOSSES
# ============================================================
MUSHOKU_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Gisu Dedoldia": {"display_name": "گیسو ددولдия", "hp": 1000, "atk": 80, "reward": 50000},
    "Almanfi": {"display_name": "آلمانفی", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Badigadi": {"display_name": "بادگادی", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Ghislaine Dedoldia": {"display_name": "گیسلین", "hp": 90000, "atk": 4400, "reward": 200000},
    "Ruijerd Superdia": {"display_name": "رویجرد", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Orsted": {"display_name": "اورستد", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
MUSHOKU_FODDER = {
    "Goblin": {"display_name": "گابلین", "hp": 400, "atk": 30, "reward": 5000},
    "Gisu Dedoldia": {"display_name": "گیسو", "hp": 1000, "atk": 80, "reward": 5000},
    "Almanfi": {"display_name": "آلمانفی", "hp": 1200, "atk": 90, "reward": 5000},
    "Badigadi": {"display_name": "بادگادی", "hp": 2000, "atk": 150, "reward": 5000},
}