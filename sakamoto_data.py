# ============================================================
# SAKAMOTO DAYS DATA
# ============================================================

CHARACTERS_SAKAMOTO = {
    "S": {
        "Taro Sakamoto": "Legendary Hitman",
        "Shin Asakura": "Psychic Assassin",
        "Lu Shaotang": "Mafia Heiress",
        "Yoichi Nagumo": "Order Member", # 🆕 از A به S منتقل شد
        "Slur": "Slur's Leader",
        "Gaku": "Slur's Right Hand",
        "Order Leader": "Head of Order",
        "Hybrid": "Order Member",
        "Kumanomi": "Slur's Member",
        "Akao": "Slur's Member",
    },
    "A": {
        "Piisuke": "Sakamoto's Ally",
        "Boiled": "Assassin",
        "Obayashi": "Hitman",
        "Son Hee": "Slur's Member",
        "Bach": "Slur's Member",
        "Osaragi": "Order Member",
        "Shishiba": "Order Member",
        "Kanaguri": "Order Member",
        "Kaji": "Order Member",
        "Kashima": "Assassin", # 🆕 از B به A منتقل شد
        "Satoru Yotsumura": "Hitman", # 🆕 از B به A منتقل شد
    },
    "B": {
        "Hana Sakamoto": "Sakamoto's Daughter",
        "Aoi Sakamoto": "Sakamoto's Wife",
        "Akira Akao": "Hitman",
        "Amane": "Assassin",
        "Tatsu": "Hitman",
        "Shinaya": "Assassin",
        "Mad Horiguchi": "Hitman",
        "Tanaka": "Store Owner",
        "Nagumo's Shadow": "Shadow Assassin", # 🆕 کاراکتر جدید
        "Silent Blade": "Silent Assassin", # 🆕 کاراکتر جدید
    },
}

CHAR_PRICES_SAKAMOTO = {"S": 5000000, "A": 600000, "B": 150000}

ABILITIES_SAKAMOTO = {
    # ============ S RANK ============
    "Taro Sakamoto": {
        "ability_1": {"name": "Legendary Reflex", "mult": 3},
        "ability_2": {"name": "Pencil Takedown", "mult": 5},
        "ability_3": {"name": "Hitman Awakening", "mult": 10, "once": True},
    },
    "Shin Asakura": {
        "ability_1": {"name": "Mind Reading", "mult": 3},
        "ability_2": {"name": "Precognition", "mult": 5},
        "ability_3": {"name": "Future Sight Full", "mult": 10, "once": True},
    },
    "Lu Shaotang": {
        "ability_1": {"name": "Mafia Kick", "mult": 3},
        "ability_2": {"name": "Shaotang Style", "mult": 5},
        "ability_3": {"name": "Heiress Awakening", "mult": 10, "once": True},
    },
    "Yoichi Nagumo": { # 🆕 از A به S منتقل شد
        "ability_1": {"name": "Ally Strike", "mult": 3},
        "ability_2": {"name": "Team Combo", "mult": 5},
        "ability_3": {"name": "Nagumo's Resolve", "mult": 10, "once": True},
    },
    "Slur": {
        "ability_1": {"name": "Slur Strike", "mult": 3},
        "ability_2": {"name": "Chaos Fist", "mult": 5},
        "ability_3": {"name": "Slur's True Form", "mult": 10, "once": True},
    },
    "Gaku": {
        "ability_1": {"name": "Brute Force", "mult": 3},
        "ability_2": {"name": "Iron Fist", "mult": 5},
        "ability_3": {"name": "Monster Strength", "mult": 10, "once": True},
    },
    "Order Leader": {
        "ability_1": {"name": "Order Command", "mult": 3},
        "ability_2": {"name": "Elite Strike", "mult": 5},
        "ability_3": {"name": "Leader's Wrath", "mult": 10, "once": True},
    },
    "Hybrid": {
        "ability_1": {"name": "Dual Blade", "mult": 3},
        "ability_2": {"name": "Cross Slash", "mult": 5},
        "ability_3": {"name": "Hybrid Form", "mult": 10, "once": True},
    },
    "Kumanomi": {
        "ability_1": {"name": "Toxic Touch", "mult": 3},
        "ability_2": {"name": "Poison Cloud", "mult": 5},
        "ability_3": {"name": "Venom Frenzy", "mult": 10, "once": True},
    },
    "Akao": {
        "ability_1": {"name": "Sniper Shot", "mult": 3},
        "ability_2": {"name": "Precision Shot", "mult": 5},
        "ability_3": {"name": "Perfect Aim", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Piisuke": {
        "ability_1": {"name": "Quick Draw", "mult": 3},
        "ability_2": {"name": "Rapid Fire", "mult": 5},
        "ability_3": {"name": "Sniper's Focus", "mult": 10, "once": True},
    },
    "Boiled": {
        "ability_1": {"name": "Knife Slash", "mult": 3},
        "ability_2": {"name": "Bloodthirst", "mult": 5},
        "ability_3": {"name": "Berserk Mode", "mult": 10, "once": True},
    },
    "Obayashi": {
        "ability_1": {"name": "Hitman Strike", "mult": 3},
        "ability_2": {"name": "Silenced Shot", "mult": 5},
        "ability_3": {"name": "Perfect Kill", "mult": 10, "once": True},
    },
    "Son Hee": {
        "ability_1": {"name": "Twin Blade", "mult": 3},
        "ability_2": {"name": "Dual Slash", "mult": 5},
        "ability_3": {"name": "Blade Dance", "mult": 10, "once": True},
    },
    "Bach": {
        "ability_1": {"name": "Heavy Punch", "mult": 3},
        "ability_2": {"name": "Stone Fist", "mult": 5},
        "ability_3": {"name": "Titan Strength", "mult": 10, "once": True},
    },
    "Osaragi": {
        "ability_1": {"name": "Sharp Aim", "mult": 3},
        "ability_2": {"name": "Throw Master", "mult": 5},
        "ability_3": {"name": "Order Elite", "mult": 10, "once": True},
    },
    "Shishiba": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Iron Guard", "mult": 5},
        "ability_3": {"name": "Order Assassin", "mult": 10, "once": True},
    },
    "Kanaguri": {
        "ability_1": {"name": "Fast Kick", "mult": 3},
        "ability_2": {"name": "Speed Rush", "mult": 5},
        "ability_3": {"name": "Blur Form", "mult": 10, "once": True},
    },
    "Kaji": {
        "ability_1": {"name": "Fire Fist", "mult": 3},
        "ability_2": {"name": "Flame Burst", "mult": 5},
        "ability_3": {"name": "Inferno Blast", "mult": 10, "once": True},
    },
    "Kashima": { # 🆕 از B به A منتقل شد
        "ability_1": {"name": "Dagger Slash", "mult": 3},
        "ability_2": {"name": "Shadow Strike", "mult": 5},
        "ability_3": {"name": "Phantom Kill", "mult": 10, "once": True},
    },
    "Satoru Yotsumura": { # 🆕 از B به A منتقل شد
        "ability_1": {"name": "Hitman Punch", "mult": 3},
        "ability_2": {"name": "Deadly Grip", "mult": 5},
        "ability_3": {"name": "Berserk Strike", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Hana Sakamoto": {
        "ability_1": {"name": "Quick Slap", "mult": 3},
        "ability_2": {"name": "Surprise Punch", "mult": 5},
        "ability_3": {"name": "Daughter's Will", "mult": 10, "once": True},
    },
    "Aoi Sakamoto": {
        "ability_1": {"name": "Frying Pan Hit", "mult": 3},
        "ability_2": {"name": "Mother's Fury", "mult": 5},
        "ability_3": {"name": "Wife's Resolve", "mult": 10, "once": True},
    },
    "Akira Akao": {
        "ability_1": {"name": "Pistol Shot", "mult": 3},
        "ability_2": {"name": "Rapid Shot", "mult": 5},
        "ability_3": {"name": "Ace Shooter", "mult": 10, "once": True},
    },
    "Amane": {
        "ability_1": {"name": "Poison Dart", "mult": 3},
        "ability_2": {"name": "Venom Touch", "mult": 5},
        "ability_3": {"name": "Toxic Rush", "mult": 10, "once": True},
    },
    "Tatsu": {
        "ability_1": {"name": "Knife Slash", "mult": 3},
        "ability_2": {"name": "Silent Kill", "mult": 5},
        "ability_3": {"name": "Hitman Mode", "mult": 10, "once": True},
    },
    "Shinaya": {
        "ability_1": {"name": "Arrow Shot", "mult": 3},
        "ability_2": {"name": "Arrow Barrage", "mult": 5},
        "ability_3": {"name": "Sniper Mode", "mult": 10, "once": True},
    },
    "Mad Horiguchi": {
        "ability_1": {"name": "Fist Punch", "mult": 3},
        "ability_2": {"name": "Mad Rush", "mult": 5},
        "ability_3": {"name": "Frenzy Form", "mult": 10, "once": True},
    },
    "Tanaka": {
        "ability_1": {"name": "Store Broom Hit", "mult": 3},
        "ability_2": {"name": "Shopkeeper Fury", "mult": 5},
        "ability_3": {"name": "Hidden Strength", "mult": 10, "once": True},
    },
    "Nagumo's Shadow": { # 🆕 کاراکتر جدید
        "ability_1": {"name": "Shadow Strike", "mult": 3},
        "ability_2": {"name": "Dark Slash", "mult": 5},
        "ability_3": {"name": "Shadow Execution", "mult": 10, "once": True},
    },
    "Silent Blade": { # 🆕 کاراکتر جدید
        "ability_1": {"name": "Silent Cut", "mult": 3},
        "ability_2": {"name": "Assassin Rush", "mult": 5},
        "ability_3": {"name": "Death's Whisper", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES (دسته‌بندی جدید)
# ============================================================
SAKAMOTO_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Boiled": {"display_name": "بوئیلد", "hp": 1000, "atk": 80, "reward": 50000},
    "Obayashi": {"display_name": "اوبایاشی", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Kumanomi": {"display_name": "کومانومی", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Gaku": {"display_name": "گاکو", "hp": 90000, "atk": 4400, "reward": 200000},
    "Nagumo's Shadow": {"display_name": "سایه ناگومو", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Slur": {"display_name": "اسلر", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
SAKAMOTO_FODDER = {
    "Street Thug": {"display_name": "اراذل خیابانی", "hp": 400, "atk": 30, "reward": 5000},
    "Boiled": {"display_name": "بوئیلد", "hp": 1000, "atk": 80, "reward": 5000},
    "Obayashi": {"display_name": "اوبایاشی", "hp": 1200, "atk": 90, "reward": 5000},
    "Kumanomi": {"display_name": "کومانومی", "hp": 2000, "atk": 150, "reward": 5000},
}