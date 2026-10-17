# ============================================================
# SOLO LEVELING DATA
# ============================================================

CHARACTERS_SOLOLEVELING = {
    "S": {
        "Sung Jin-Woo": "Shadow Monarch",
        "Antares": "Dragon King",
        "Thomas Andre": "Goliath",
        "Liu Zhigang": "China's Strongest",
        "Bellion": "Grand Marshal",
        "Beru": "Ant King",
        "Igris": "Blood-Red Commander",
        "Ashborn": "Original Shadow Monarch",
        "Frost Monarch": "Ice King",
        "Beast Monarch": "King of Beasts",
    },
    "A": {
        "Cha Hae-In": "Dancer",
        "Choi Jong-In": "Fire Mage",
        "Baek Yoon-Ho": "White Tiger",
        "Go Gun-Hee": "Hunter Association Chairman",
        "Hwang Dong-Su": "S-Rank Hunter",
        "Kargalgan": "High Orc Shaman",
        "Kaisel": "Wyvern",
        "Iron": "Shadow Soldier",
        "Tank": "Shadow Bear",
        "Fangs": "Shadow Wolf",
    },
    "B": {
        "Yoo Jin-Ho": "Jin-Woo's Friend",
        "Lee Joo-Hee": "Healer",
        "Song Chi-Yul": "Hunter",
        "Kim Sang-Shik": "Hunter",
        "Jung Yoon-Tae": "Hunter",
        "Park Hee-Jin": "Hunter",
        "Baran": "Demon King",
        "Kang Tae-Shik": "Hunter",
        "Min Byung-Gu": "Healer",
        "Hwang Dong-Soo": "S-Rank Hunter",
    },
}

CHAR_PRICES_SOLOLEVELING = {"S": 5000000, "A": 600000, "B": 150000}

ABILITIES_SOLOLEVELING = {
    # ============ S RANK ============
    "Sung Jin-Woo": {
        "ability_1": {"name": "Shadow Exchange", "mult": 3},
        "ability_2": {"name": "Ruler's Authority", "mult": 5},
        "ability_3": {"name": "Shadow Monarch Full", "mult": 10, "once": True},
    },
    "Antares": {
        "ability_1": {"name": "Dragon Breath", "mult": 3},
        "ability_2": {"name": "Flame of Destruction", "mult": 5},
        "ability_3": {"name": "Dragon King Form", "mult": 10, "once": True},
    },
    "Thomas Andre": {
        "ability_1": {"name": "Goliath Punch", "mult": 3},
        "ability_2": {"name": "Titan Crush", "mult": 5},
        "ability_3": {"name": "Goliath Awakening", "mult": 10, "once": True},
    },
    "Liu Zhigang": {
        "ability_1": {"name": "Martial Arts", "mult": 3},
        "ability_2": {"name": "Dragon Strike", "mult": 5},
        "ability_3": {"name": "China's Strongest", "mult": 10, "once": True},
    },
    "Bellion": {
        "ability_1": {"name": "Grand Marshal Strike", "mult": 3},
        "ability_2": {"name": "Shadow Army Charge", "mult": 5},
        "ability_3": {"name": "Bellion Full Power", "mult": 10, "once": True},
    },
    "Beru": {
        "ability_1": {"name": "Ant King Slash", "mult": 3},
        "ability_2": {"name": "Predator Fang", "mult": 5},
        "ability_3": {"name": "Ant King Full Power", "mult": 10, "once": True},
    },
    "Igris": {
        "ability_1": {"name": "Blood-Red Slash", "mult": 3},
        "ability_2": {"name": "Commander Charge", "mult": 5},
        "ability_3": {"name": "Igris Full Power", "mult": 10, "once": True},
    },
    "Ashborn": {
        "ability_1": {"name": "Shadow Strike", "mult": 3},
        "ability_2": {"name": "Death's Grasp", "mult": 5},
        "ability_3": {"name": "Original Monarch", "mult": 10, "once": True},
    },
    "Frost Monarch": {
        "ability_1": {"name": "Ice Spear", "mult": 3},
        "ability_2": {"name": "Frozen Hell", "mult": 5},
        "ability_3": {"name": "Frost King Form", "mult": 10, "once": True},
    },
    "Beast Monarch": {
        "ability_1": {"name": "Beast Claw", "mult": 3},
        "ability_2": {"name": "King's Roar", "mult": 5},
        "ability_3": {"name": "Beast King Form", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Cha Hae-In": {
        "ability_1": {"name": "Dancer Slash", "mult": 3},
        "ability_2": {"name": "Sword Dance", "mult": 5},
        "ability_3": {"name": "Dancer Full Power", "mult": 10, "once": True},
    },
    "Choi Jong-In": {
        "ability_1": {"name": "Fireball", "mult": 3},
        "ability_2": {"name": "Inferno Burst", "mult": 5},
        "ability_3": {"name": "Meteor Strike", "mult": 10, "once": True},
    },
    "Baek Yoon-Ho": {
        "ability_1": {"name": "White Tiger Strike", "mult": 3},
        "ability_2": {"name": "Tiger Roar", "mult": 5},
        "ability_3": {"name": "White Tiger Full", "mult": 10, "once": True},
    },
    "Go Gun-Hee": {
        "ability_1": {"name": "Chairman's Strike", "mult": 3},
        "ability_2": {"name": "Authority Blast", "mult": 5},
        "ability_3": {"name": "Power of the Rulers", "mult": 10, "once": True},
    },
    "Hwang Dong-Su": {
        "ability_1": {"name": "Hunter Punch", "mult": 3},
        "ability_2": {"name": "Berserk Rush", "mult": 5},
        "ability_3": {"name": "Dong-Su Full Power", "mult": 10, "once": True},
    },
    "Kargalgan": {
        "ability_1": {"name": "Orc Magic", "mult": 3},
        "ability_2": {"name": "Shaman Curse", "mult": 5},
        "ability_3": {"name": "High Orc Full", "mult": 10, "once": True},
    },
    "Kaisel": {
        "ability_1": {"name": "Wyvern Claw", "mult": 3},
        "ability_2": {"name": "Aerial Dive", "mult": 5},
        "ability_3": {"name": "Wyvern Full Power", "mult": 10, "once": True},
    },
    "Iron": {
        "ability_1": {"name": "Iron Punch", "mult": 3},
        "ability_2": {"name": "Steel Rush", "mult": 5},
        "ability_3": {"name": "Iron Full Power", "mult": 10, "once": True},
    },
    "Tank": {
        "ability_1": {"name": "Bear Swipe", "mult": 3},
        "ability_2": {"name": "Tank Charge", "mult": 5},
        "ability_3": {"name": "Tank Full Power", "mult": 10, "once": True},
    },
    "Fangs": {
        "ability_1": {"name": "Wolf Bite", "mult": 3},
        "ability_2": {"name": "Fang Rush", "mult": 5},
        "ability_3": {"name": "Fangs Full Power", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Yoo Jin-Ho": {
        "ability_1": {"name": "Support Strike", "mult": 3},
        "ability_2": {"name": "Team Combo", "mult": 5},
        "ability_3": {"name": "Jin-Ho's Resolve", "mult": 10, "once": True},
    },
    "Lee Joo-Hee": {
        "ability_1": {"name": "Heal Pulse", "mult": 3},
        "ability_2": {"name": "Holy Light", "mult": 5},
        "ability_3": {"name": "Healer's Prayer", "mult": 10, "once": True},
    },
    "Song Chi-Yul": {
        "ability_1": {"name": "Hunter Slash", "mult": 3},
        "ability_2": {"name": "Blade Rush", "mult": 5},
        "ability_3": {"name": "Chi-Yul Full Power", "mult": 10, "once": True},
    },
    "Kim Sang-Shik": {
        "ability_1": {"name": "Hunter Punch", "mult": 3},
        "ability_2": {"name": "Rush Attack", "mult": 5},
        "ability_3": {"name": "Sang-Shik Full", "mult": 10, "once": True},
    },
    "Jung Yoon-Tae": {
        "ability_1": {"name": "Blade Slash", "mult": 3},
        "ability_2": {"name": "Twin Slash", "mult": 5},
        "ability_3": {"name": "Yoon-Tae Full", "mult": 10, "once": True},
    },
    "Park Hee-Jin": {
        "ability_1": {"name": "Dagger Strike", "mult": 3},
        "ability_2": {"name": "Shadow Strike", "mult": 5},
        "ability_3": {"name": "Hee-Jin Full", "mult": 10, "once": True},
    },
    "Baran": {
        "ability_1": {"name": "Demon Strike", "mult": 3},
        "ability_2": {"name": "Hell Flame", "mult": 5},
        "ability_3": {"name": "Demon King Form", "mult": 10, "once": True},
    },
    "Kang Tae-Shik": {
        "ability_1": {"name": "Hunter Slash", "mult": 3},
        "ability_2": {"name": "Blade Rush", "mult": 5},
        "ability_3": {"name": "Tae-Shik Full", "mult": 10, "once": True},
    },
    "Min Byung-Gu": {
        "ability_1": {"name": "Heal Wave", "mult": 3},
        "ability_2": {"name": "Holy Shield", "mult": 5},
        "ability_3": {"name": "Byung-Gu's Blessing", "mult": 10, "once": True},
    },
    "Hwang Dong-Soo": {
        "ability_1": {"name": "Hunter Punch", "mult": 3},
        "ability_2": {"name": "Berserk Rush", "mult": 5},
        "ability_3": {"name": "Dong-Soo Full Power", "mult": 10, "once": True},
    },
}
# ============================================================
# BOSSES
# ============================================================
SOLOLEVELING_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Kargalgan": {"display_name": "کارگالگان", "hp": 1000, "atk": 80, "reward": 50000},
    "Baran": {"display_name": "باران", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Beru": {"display_name": "برو", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Igris": {"display_name": "ایگریس", "hp": 90000, "atk": 4400, "reward": 200000},
    "Thomas Andre": {"display_name": "توماس آندره", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Antares": {"display_name": "آنترس", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
SOLOLEVELING_FODDER = {
    "Goblin": {"display_name": "گابلین", "hp": 400, "atk": 30, "reward": 5000},
    "Kargalgan": {"display_name": "کارگالگان", "hp": 1000, "atk": 80, "reward": 5000},
    "Baran": {"display_name": "باران", "hp": 1200, "atk": 90, "reward": 5000},
    "Beru": {"display_name": "برو", "hp": 2000, "atk": 150, "reward": 5000},
}