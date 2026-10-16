# ============================================================
# BLACK CLOVER DATA
# ============================================================

CHARACTERS_BLACKCLOVER = {
    "S": {
        "Asta": "Devil Union",
        "Yuno": "Spirit of Zephyr",
        "Julius Novachrono": "Wizard King",
        "Mereoleona Vermillion": "Crimson Lion",
        "Yami Sukehiro": "Black Bulls Captain",
        "Nozel Silva": "Silver Eagle",
        "Fuegoleon Vermillion": "Crimson Lion Captain",
        "Noelle Silva": "Valkyrie Dress",
        "Charlotte Roselei": "Briar Queen",
        "William Vangeance": "Golden Dawn Captain",
    },
    "A": {
        "Jack the Ripper": "Slash Magic",
        "Patry": "Light Magic",
        "Licht": "Demon Light",
        "Zagred": "Demon King",
        "Luck Voltia": "Lightning God",
        "Mimosa Vermillion": "Plant Magic",
        "Klaus Lunettes": "Steel Magic",
        "Magna Swing": "Flame Magic",
        "Finral Roulacase": "Spatial Magic",
        "Vanessa Enoteca": "Fate Witch",
    },
    "B": {
        "Charmy Pappitson": "Wolf in Sheep",
        "Grey": "Transmutation",
        "Gauche Adlai": "Mirror Magic",
        "Gordon Agrippa": "Poison Magic",
        "Zora Ideale": "Trap Magic",
        "Nero": "Sealing Magic",
        "Secre Swallowtail": "Anti-Magic Wing",
        "Rhya": "Copy Magic",
        "Fana": "Fire Spirit",
        "Vetto": "Beast Magic",
    },
}

CHAR_PRICES_BLACKCLOVER = {"S": 2000000, "A": 500000, "B": 150000}

ABILITIES_BLACKCLOVER = {
    # ============ S RANK ============
    "Asta": {
        "ability_1": {"name": "Demon-Slayer Slash", "mult": 3},
        "ability_2": {"name": "Black Slash", "mult": 5},
        "ability_3": {"name": "Devil Union", "mult": 10, "once": True},
    },
    "Yuno": {
        "ability_1": {"name": "Wind Blade", "mult": 3},
        "ability_2": {"name": "Spirit Storm", "mult": 5},
        "ability_3": {"name": "Spirit of Zephyr", "mult": 10, "once": True},
    },
    "Julius Novachrono": {
        "ability_1": {"name": "Time Slash", "mult": 3},
        "ability_2": {"name": "Time Prison", "mult": 5},
        "ability_3": {"name": "Chrono Stasis", "mult": 10, "once": True},
    },
    "Mereoleona Vermillion": {
        "ability_1": {"name": "Flame Fist", "mult": 3},
        "ability_2": {"name": "Hellfire Rush", "mult": 5},
        "ability_3": {"name": "Mana Zone: Flame", "mult": 10, "once": True},
    },
    "Yami Sukehiro": {
        "ability_1": {"name": "Dark Slash", "mult": 3},
        "ability_2": {"name": "Dark Cloaked Blade", "mult": 5},
        "ability_3": {"name": "Dimension Slash", "mult": 10, "once": True},
    },
    "Nozel Silva": {
        "ability_1": {"name": "Silver Spear", "mult": 3},
        "ability_2": {"name": "Mercury Rain", "mult": 5},
        "ability_3": {"name": "Silver Eagle", "mult": 10, "once": True},
    },
    "Fuegoleon Vermillion": {
        "ability_1": {"name": "Flame Punch", "mult": 3},
        "ability_2": {"name": "Crimson Lion", "mult": 5},
        "ability_3": {"name": "Salamander", "mult": 10, "once": True},
    },
    "Noelle Silva": {
        "ability_1": {"name": "Water Ball", "mult": 3},
        "ability_2": {"name": "Sea Dragon's Roar", "mult": 5},
        "ability_3": {"name": "Valkyrie Dress", "mult": 10, "once": True},
    },
    "Charlotte Roselei": {
        "ability_1": {"name": "Briar Whip", "mult": 3},
        "ability_2": {"name": "Blue Rose", "mult": 5},
        "ability_3": {"name": "Briar Queen", "mult": 10, "once": True},
    },
    "William Vangeance": {
        "ability_1": {"name": "World Tree", "mult": 3},
        "ability_2": {"name": "Golden Dawn", "mult": 5},
        "ability_3": {"name": "Yggdrasil", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Jack the Ripper": {
        "ability_1": {"name": "Slash Cut", "mult": 3},
        "ability_2": {"name": "Sever Slash", "mult": 5},
        "ability_3": {"name": "Slash Magic Full", "mult": 10, "once": True},
    },
    "Patry": {
        "ability_1": {"name": "Light Blade", "mult": 3},
        "ability_2": {"name": "Light Whip", "mult": 5},
        "ability_3": {"name": "Light Speed", "mult": 10, "once": True},
    },
    "Licht": {
        "ability_1": {"name": "Demon Light", "mult": 3},
        "ability_2": {"name": "Demon Sword", "mult": 5},
        "ability_3": {"name": "Demon Light Full", "mult": 10, "once": True},
    },
    "Zagred": {
        "ability_1": {"name": "Word Soul", "mult": 3},
        "ability_2": {"name": "Demon Tongue", "mult": 5},
        "ability_3": {"name": "Demon King Form", "mult": 10, "once": True},
    },
    "Luck Voltia": {
        "ability_1": {"name": "Lightning Punch", "mult": 3},
        "ability_2": {"name": "Thunder Rush", "mult": 5},
        "ability_3": {"name": "Lightning God", "mult": 10, "once": True},
    },
    "Mimosa Vermillion": {
        "ability_1": {"name": "Plant Heal", "mult": 3},
        "ability_2": {"name": "Flower Shield", "mult": 5},
        "ability_3": {"name": "Plant Magic Full", "mult": 10, "once": True},
    },
    "Klaus Lunettes": {
        "ability_1": {"name": "Steel Spear", "mult": 3},
        "ability_2": {"name": "Steel Wall", "mult": 5},
        "ability_3": {"name": "Steel Magic Full", "mult": 10, "once": True},
    },
    "Magna Swing": {
        "ability_1": {"name": "Flame Ball", "mult": 3},
        "ability_2": {"name": "Fire Punch", "mult": 5},
        "ability_3": {"name": "Flame Magic Full", "mult": 10, "once": True},
    },
    "Finral Roulacase": {
        "ability_1": {"name": "Portal Kick", "mult": 3},
        "ability_2": {"name": "Spatial Warp", "mult": 5},
        "ability_3": {"name": "Fallen Angel", "mult": 10, "once": True},
    },
    "Vanessa Enoteca": {
        "ability_1": {"name": "Thread Bind", "mult": 3},
        "ability_2": {"name": "Red Thread", "mult": 5},
        "ability_3": {"name": "Fate Witch", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Charmy Pappitson": {
        "ability_1": {"name": "Sheep Strike", "mult": 3},
        "ability_2": {"name": "Cotton Blast", "mult": 5},
        "ability_3": {"name": "Wolf in Sheep", "mult": 10, "once": True},
    },
    "Grey": {
        "ability_1": {"name": "Transmute", "mult": 3},
        "ability_2": {"name": "Stone Golem", "mult": 5},
        "ability_3": {"name": "Transmutation Full", "mult": 10, "once": True},
    },
    "Gauche Adlai": {
        "ability_1": {"name": "Mirror Shot", "mult": 3},
        "ability_2": {"name": "Mirror Clone", "mult": 5},
        "ability_3": {"name": "Mirror Magic Full", "mult": 10, "once": True},
    },
    "Gordon Agrippa": {
        "ability_1": {"name": "Poison Cloud", "mult": 3},
        "ability_2": {"name": "Curse Hex", "mult": 5},
        "ability_3": {"name": "Poison Magic Full", "mult": 10, "once": True},
    },
    "Zora Ideale": {
        "ability_1": {"name": "Trap Rune", "mult": 3},
        "ability_2": {"name": "Counter Trap", "mult": 5},
        "ability_3": {"name": "Trap Magic Full", "mult": 10, "once": True},
    },
    "Nero": {
        "ability_1": {"name": "Seal Strike", "mult": 3},
        "ability_2": {"name": "Anti-Magic Seal", "mult": 5},
        "ability_3": {"name": "Sealing Magic Full", "mult": 10, "once": True},
    },
    "Secre Swallowtail": {
        "ability_1": {"name": "Seal Strike", "mult": 3},
        "ability_2": {"name": "Anti-Magic Wing", "mult": 5},
        "ability_3": {"name": "Sealing Magic Full", "mult": 10, "once": True},
    },
    "Rhya": {
        "ability_1": {"name": "Copy Slash", "mult": 3},
        "ability_2": {"name": "Copy Magic", "mult": 5},
        "ability_3": {"name": "Copy Full", "mult": 10, "once": True},
    },
    "Fana": {
        "ability_1": {"name": "Flame Bird", "mult": 3},
        "ability_2": {"name": "Salamander", "mult": 5},
        "ability_3": {"name": "Fire Spirit Full", "mult": 10, "once": True},
    },
    "Vetto": {
        "ability_1": {"name": "Beast Punch", "mult": 3},
        "ability_2": {"name": "Beast Claw", "mult": 5},
        "ability_3": {"name": "Beast Magic Full", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
BLACKCLOVER_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Mars": {"display_name": "مارس", "hp": 1000, "atk": 80, "reward": 50000},
    "Vetto": {"display_name": "وتو", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Fana": {"display_name": "فانا", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Rhya": {"display_name": "ریا", "hp": 90000, "atk": 4400, "reward": 200000},
    "Licht": {"display_name": "لیخت", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Zagred": {"display_name": "زاگرید", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
BLACKCLOVER_FODDER = {
    "Lesser Mage": {"display_name": "جادوگر ضعیف", "hp": 400, "atk": 30, "reward": 5000},
    "Mars": {"display_name": "مارس", "hp": 1000, "atk": 80, "reward": 5000},
    "Vetto": {"display_name": "وتو", "hp": 1200, "atk": 90, "reward": 5000},
    "Fana": {"display_name": "فانا", "hp": 2000, "atk": 150, "reward": 5000},
}