# ============================================================
# NARUTO DATA
# ============================================================

CHARACTERS_NARUTO = {
    "S": {
        "Naruto Uzumaki": "Seventh Hokage",
        "Sasuke Uchiha": "Shadow Hokage",
        "Madara Uchiha": "Ghost of the Uchiha",
        "Kaguya Otsutsuki": "Rabbit Goddess",
        "Hagoromo Otsutsuki": "Sage of Six Paths",
        "Itachi Uchiha": "Clan Slayer",
        "Hashirama Senju": "God of Shinobi",
        "Obito Uchiha": "Masked Man",
        "Minato Namikaze": "Yellow Flash",
        "Pain": "Akatsuki Leader",
    },
    "A": {
        "Kakashi Hatake": "Copy Ninja",
        "Sakura Haruno": "Medical Ninja",
        "Gaara": "Fifth Kazekage",
        "Killer Bee": "Eight Tails Jinchuriki",
        "Might Guy": "Taijutsu Master",
        "Tsunade": "Fifth Hokage",
        "Jiraiya": "Pervy Sage",
        "Orochimaru": "Snake Sannin",
        "Kabuto Yakushi": "Dragon Sage",
        "Shikamaru Nara": "Shadow Strategist",
    },
    "B": {
        "Rock Lee": "Taijutsu Specialist",
        "Hinata Hyuga": "Byakugan Princess",
        "Neji Hyuga": "Prodigy",
        "Kiba Inuzuka": "Beast Ninja",
        "Shino Aburame": "Insect Ninja",
        "Choji Akimichi": "Akamichi Heir",
        "Ino Yamanaka": "Mind Ninja",
        "Tenten": "Weapon Specialist",
        "Sai": "Root Member",
        "Konohamaru Sarutobi": "Third Hokage's Grandson",
    },
}

CHAR_PRICES_NARUTO = {"S": 5000000, "A": 600000, "B": 150000}

ABILITIES_NARUTO = {
    # ============ S RANK ============
    "Naruto Uzumaki": {
        "ability_1": {"name": "Rasengan", "mult": 3},
        "ability_2": {"name": "Sage Art: Massive Rasengan", "mult": 5},
        "ability_3": {"name": "Six Paths: Truth-Seeking Ball", "mult": 10, "once": True},
    },
    "Sasuke Uchiha": {
        "ability_1": {"name": "Chidori", "mult": 3},
        "ability_2": {"name": "Amaterasu", "mult": 5},
        "ability_3": {"name": "Indra's Arrow", "mult": 10, "once": True},
    },
    "Madara Uchiha": {
        "ability_1": {"name": "Fire Style: Great Fireball", "mult": 3},
        "ability_2": {"name": "Perfect Susanoo", "mult": 5},
        "ability_3": {"name": "Infinite Tsukuyomi", "mult": 10, "once": True},
    },
    "Kaguya Otsutsuki": {
        "ability_1": {"name": "All-Killing Ash Bones", "mult": 3},
        "ability_2": {"name": "Dimensional Rift", "mult": 5},
        "ability_3": {"name": "Expansive Truth-Seeking Ball", "mult": 10, "once": True},
    },
    "Hagoromo Otsutsuki": {
        "ability_1": {"name": "Six Paths Strike", "mult": 3},
        "ability_2": {"name": "Banbutsu Sozo", "mult": 5},
        "ability_3": {"name": "Ninshu Creation", "mult": 10, "once": True},
    },
    "Itachi Uchiha": {
        "ability_1": {"name": "Tsukuyomi", "mult": 3},
        "ability_2": {"name": "Amaterasu", "mult": 5},
        "ability_3": {"name": "Totsuka Blade", "mult": 10, "once": True},
    },
    "Hashirama Senju": {
        "ability_1": {"name": "Wood Style: Forest", "mult": 3},
        "ability_2": {"name": "Wood Dragon", "mult": 5},
        "ability_3": {"name": "Sage Art: True Thousand Hands", "mult": 10, "once": True},
    },
    "Obito Uchiha": {
        "ability_1": {"name": "Kamui", "mult": 3},
        "ability_2": {"name": "Ten Tails Jinchuriki", "mult": 5},
        "ability_3": {"name": "Six Paths Form", "mult": 10, "once": True},
    },
    "Minato Namikaze": {
        "ability_1": {"name": "Rasengan", "mult": 3},
        "ability_2": {"name": "Flying Thunder God", "mult": 5},
        "ability_3": {"name": "KCM Sage Mode", "mult": 10, "once": True},
    },
    "Pain": {
        "ability_1": {"name": "Shinra Tensei", "mult": 3},
        "ability_2": {"name": "Chibaku Tensei", "mult": 5},
        "ability_3": {"name": "Six Paths Almighty Push", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Kakashi Hatake": {
        "ability_1": {"name": "Chidori", "mult": 3},
        "ability_2": {"name": "Kamui", "mult": 5},
        "ability_3": {"name": "DMS Perfect Susanoo", "mult": 10, "once": True},
    },
    "Sakura Haruno": {
        "ability_1": {"name": "Cherry Blossom Impact", "mult": 3},
        "ability_2": {"name": "Hundred Healings", "mult": 5},
        "ability_3": {"name": "Byakugou Release", "mult": 10, "once": True},
    },
    "Gaara": {
        "ability_1": {"name": "Sand Coffin", "mult": 3},
        "ability_2": {"name": "Sand Waterfall", "mult": 5},
        "ability_3": {"name": "Sand Tsunami", "mult": 10, "once": True},
    },
    "Killer Bee": {
        "ability_1": {"name": "Seven Swords Dance", "mult": 3},
        "ability_2": {"name": "Lariat", "mult": 5},
        "ability_3": {"name": "Tailed Beast Bomb", "mult": 10, "once": True},
    },
    "Might Guy": {
        "ability_1": {"name": "Leaf Whirlwind", "mult": 3},
        "ability_2": {"name": "Eight Gates Released", "mult": 5},
        "ability_3": {"name": "Night Guy", "mult": 10, "once": True},
    },
    "Tsunade": {
        "ability_1": {"name": "Heaven Kick", "mult": 3},
        "ability_2": {"name": "Hundred Healings", "mult": 5},
        "ability_3": {"name": "Byakugou Full Release", "mult": 10, "once": True},
    },
    "Jiraiya": {
        "ability_1": {"name": "Rasengan", "mult": 3},
        "ability_2": {"name": "Sage Mode", "mult": 5},
        "ability_3": {"name": "Sage Art: Goemon", "mult": 10, "once": True},
    },
    "Orochimaru": {
        "ability_1": {"name": "Striking Shadow Snake", "mult": 3},
        "ability_2": {"name": "Edo Tensei", "mult": 5},
        "ability_3": {"name": "Eight-Headed Serpent", "mult": 10, "once": True},
    },
    "Kabuto Yakushi": {
        "ability_1": {"name": "Chakra Scalpel", "mult": 3},
        "ability_2": {"name": "Sage Mode", "mult": 5},
        "ability_3": {"name": "Edo Tensei Army", "mult": 10, "once": True},
    },
    "Shikamaru Nara": {
        "ability_1": {"name": "Shadow Possession", "mult": 3},
        "ability_2": {"name": "Shadow Stitching", "mult": 5},
        "ability_3": {"name": "Shadow Strangle", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Rock Lee": {
        "ability_1": {"name": "Leaf Hurricane", "mult": 3},
        "ability_2": {"name": "Front Lotus", "mult": 5},
        "ability_3": {"name": "Eight Gates", "mult": 10, "once": True},
    },
    "Hinata Hyuga": {
        "ability_1": {"name": "Gentle Fist", "mult": 3},
        "ability_2": {"name": "Twin Lion Fists", "mult": 5},
        "ability_3": {"name": "Hamura's Chakra", "mult": 10, "once": True},
    },
    "Neji Hyuga": {
        "ability_1": {"name": "Eight Trigrams 64 Palms", "mult": 3},
        "ability_2": {"name": "Eight Trigrams Air Palm", "mult": 5},
        "ability_3": {"name": "Eight Trigrams Rotation", "mult": 10, "once": True},
    },
    "Kiba Inuzuka": {
        "ability_1": {"name": "Fang Passing Fang", "mult": 3},
        "ability_2": {"name": "Man-Beast Combination", "mult": 5},
        "ability_3": {"name": "Two-Headed Wolf", "mult": 10, "once": True},
    },
    "Shino Aburame": {
        "ability_1": {"name": "Insect Sphere", "mult": 3},
        "ability_2": {"name": "Insect Cloud", "mult": 5},
        "ability_3": {"name": "Insect Swarm", "mult": 10, "once": True},
    },
    "Choji Akimichi": {
        "ability_1": {"name": "Human Bullet Tank", "mult": 3},
        "ability_2": {"name": "Butterfly Mode", "mult": 5},
        "ability_3": {"name": "Butterfly Bomb", "mult": 10, "once": True},
    },
    "Ino Yamanaka": {
        "ability_1": {"name": "Mind Transfer", "mult": 3},
        "ability_2": {"name": "Mind Disturbance", "mult": 5},
        "ability_3": {"name": "Mind Body Switch", "mult": 10, "once": True},
    },
    "Tenten": {
        "ability_1": {"name": "Weapon Barrage", "mult": 3},
        "ability_2": {"name": "Rising Twin Dragons", "mult": 5},
        "ability_3": {"name": "Bashosen Fan", "mult": 10, "once": True},
    },
    "Sai": {
        "ability_1": {"name": "Super Beast Scroll", "mult": 3},
        "ability_2": {"name": "Ink Clone", "mult": 5},
        "ability_3": {"name": "Ink Giant", "mult": 10, "once": True},
    },
    "Konohamaru Sarutobi": {
        "ability_1": {"name": "Rasengan", "mult": 3},
        "ability_2": {"name": "Fire Style: Ash Pile", "mult": 5},
        "ability_3": {"name": "Sexy Jutsu", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
NARUTO_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Zabuza Momochi": {"display_name": "زابوزا", "hp": 1000, "atk": 80, "reward": 50000},
    "Haku": {"display_name": "هاکو", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Pain": {"display_name": "پین", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Obito Uchiha": {"display_name": "اوبیتو", "hp": 90000, "atk": 4400, "reward": 200000},
    "Madara Uchiha": {"display_name": "مادارا", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Kaguya Otsutsuki": {"display_name": "کاگویا", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
NARUTO_FODDER = {
    "Genin Ninja": {"display_name": "نینجای جونیور", "hp": 400, "atk": 30, "reward": 5000},
    "Zabuza Momochi": {"display_name": "زابوزا", "hp": 1000, "atk": 80, "reward": 5000},
    "Haku": {"display_name": "هاکو", "hp": 1200, "atk": 90, "reward": 5000},
    "Pain": {"display_name": "پین", "hp": 2000, "atk": 150, "reward": 5000},
}