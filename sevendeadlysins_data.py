# ============================================================
# SEVEN DEADLY SINS DATA
# ============================================================

CHARACTERS_SDS = {
    "S": {
        "Meliodas": "Dragon's Sin of Wrath",
        "Escanor": "Lion's Sin of Pride",
        "Ban": "Fox's Sin of Greed",
        "King": "Grizzly's Sin of Sloth",
        "Merlin": "Boar's Sin of Gluttony",
        "Diane": "Serpent's Sin of Envy",
        "Gowther": "Goat's Sin of Lust",
        "Elizabeth Liones": "Goddess Reincarnation",
        "Estarossa": "Ten Commandments",
        "Demon King": "Ruler of Purgatory",
    },
    "A": {
        "Zeldris": "Ten Commandments Leader",
        "Chandler": "Demon Master",
        "Cusack": "Sword Demon",
        "Galand": "Ten Commandments",
        "Grayroad": "Ten Commandments",
        "Gloxinia": "Fairy King",
        "Drole": "Giant King",
        "Monspeet": "Ten Commandments",
        "Derieri": "Ten Commandments",
        "Hendrickson": "Holy Knight",
    },
    "B": {
        "Gilthunder": "Holy Knight",
        "Howzer": "Holy Knight",
        "Griamore": "Holy Knight",
        "Hauser": "Holy Knight",
        "Gilfrost": "Mage",
        "Vivian": "Mage",
        "Bartra Liones": "King of Liones",
        "Margaret Liones": "Princess",
        "Veronica Liones": "Princess",
        "Elaine": "Fairy",
    },
}

CHAR_PRICES_SDS = {"S": 5000000, "A": 600000, "B": 150000}

ABILITIES_SDS = {
    # ============ S RANK ============
    "Meliodas": {
        "ability_1": {"name": "Full Counter", "mult": 3},
        "ability_2": {"name": "Revenge Counter", "mult": 5},
        "ability_3": {"name": "Assault Mode", "mult": 10, "once": True},
    },
    "Escanor": {
        "ability_1": {"name": "Cruel Sun", "mult": 3},
        "ability_2": {"name": "Sunshine", "mult": 5},
        "ability_3": {"name": "The One", "mult": 10, "once": True},
    },
    "Ban": {
        "ability_1": {"name": "Snatch", "mult": 3},
        "ability_2": {"name": "Fox Hunt", "mult": 5},
        "ability_3": {"name": "Hunter Fest", "mult": 10, "once": True},
    },
    "King": {
        "ability_1": {"name": "Chastiefol", "mult": 3},
        "ability_2": {"name": "True Spirit Spear", "mult": 5},
        "ability_3": {"name": "Sunflower Form", "mult": 10, "once": True},
    },
    "Merlin": {
        "ability_1": {"name": "Infinity", "mult": 3},
        "ability_2": {"name": "Exterminate Ray", "mult": 5},
        "ability_3": {"name": "Aldan", "mult": 10, "once": True},
    },
    "Diane": {
        "ability_1": {"name": "Gideon", "mult": 3},
        "ability_2": {"name": "Mother Catastrophe", "mult": 5},
        "ability_3": {"name": "Drole's Dance", "mult": 10, "once": True},
    },
    "Gowther": {
        "ability_1": {"name": "Invasion", "mult": 3},
        "ability_2": {"name": "Nightmare Teller", "mult": 5},
        "ability_3": {"name": "Rewrite Light", "mult": 10, "once": True},
    },
    "Elizabeth Liones": {
        "ability_1": {"name": "Ark", "mult": 3},
        "ability_2": {"name": "Healing Prayer", "mult": 5},
        "ability_3": {"name": "Goddess Blessing", "mult": 10, "once": True},
    },
    "Estarossa": {
        "ability_1": {"name": "Full Counter", "mult": 3},
        "ability_2": {"name": "Darkness Slash", "mult": 5},
        "ability_3": {"name": "Mael Form", "mult": 10, "once": True},
    },
    "Demon King": {
        "ability_1": {"name": "Ruler", "mult": 3},
        "ability_2": {"name": "The Ruler", "mult": 5},
        "ability_3": {"name": "Indura Form", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Zeldris": {
        "ability_1": {"name": "Ominous Nebula", "mult": 3},
        "ability_2": {"name": "God Slash", "mult": 5},
        "ability_3": {"name": "Demon King Power", "mult": 10, "once": True},
    },
    "Chandler": {
        "ability_1": {"name": "Absolute Cancel", "mult": 3},
        "ability_2": {"name": "Full Counter", "mult": 5},
        "ability_3": {"name": "True Form", "mult": 10, "once": True},
    },
    "Cusack": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Resonant", "mult": 5},
        "ability_3": {"name": "Indura Form", "mult": 10, "once": True},
    },
    "Galand": {
        "ability_1": {"name": "Critical Over", "mult": 3},
        "ability_2": {"name": "Counter", "mult": 5},
        "ability_3": {"name": "Truth", "mult": 10, "once": True},
    },
    "Grayroad": {
        "ability_1": {"name": "Curse", "mult": 3},
        "ability_2": {"name": "Faith", "mult": 5},
        "ability_3": {"name": "Pacifism", "mult": 10, "once": True},
    },
    "Gloxinia": {
        "ability_1": {"name": "Basquias", "mult": 3},
        "ability_2": {"name": "Disaster", "mult": 5},
        "ability_3": {"name": "Form One: Moon Rose", "mult": 10, "once": True},
    },
    "Drole": {
        "ability_1": {"name": "Giga Crush", "mult": 3},
        "ability_2": {"name": "Giga Fall", "mult": 5},
        "ability_3": {"name": "Drole Dance", "mult": 10, "once": True},
    },
    "Monspeet": {
        "ability_1": {"name": "Trick Star", "mult": 3},
        "ability_2": {"name": "Hellblaze", "mult": 5},
        "ability_3": {"name": "Indura Form", "mult": 10, "once": True},
    },
    "Derieri": {
        "ability_1": {"name": "Combo Star", "mult": 3},
        "ability_2": {"name": "Heavy Blow", "mult": 5},
        "ability_3": {"name": "Indura Form", "mult": 10, "once": True},
    },
    "Hendrickson": {
        "ability_1": {"name": "Acid", "mult": 3},
        "ability_2": {"name": "Dark Snow", "mult": 5},
        "ability_3": {"name": "Demon Form", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Gilthunder": {
        "ability_1": {"name": "Lightning Slash", "mult": 3},
        "ability_2": {"name": "Lightning Ball", "mult": 5},
        "ability_3": {"name": "Full Lightning", "mult": 10, "once": True},
    },
    "Howzer": {
        "ability_1": {"name": "Whirlwind", "mult": 3},
        "ability_2": {"name": "Wind Blade", "mult": 5},
        "ability_3": {"name": "Rising Tornado", "mult": 10, "once": True},
    },
    "Griamore": {
        "ability_1": {"name": "Wall", "mult": 3},
        "ability_2": {"name": "Shield Bash", "mult": 5},
        "ability_3": {"name": "Fortress", "mult": 10, "once": True},
    },
    "Hauser": {
        "ability_1": {"name": "Sword Slash", "mult": 3},
        "ability_2": {"name": "Battle Cry", "mult": 5},
        "ability_3": {"name": "Holy Knight Oath", "mult": 10, "once": True},
    },
    "Gilfrost": {
        "ability_1": {"name": "Ice Shard", "mult": 3},
        "ability_2": {"name": "Ice Wall", "mult": 5},
        "ability_3": {"name": "Frozen Heart", "mult": 10, "once": True},
    },
    "Vivian": {
        "ability_1": {"name": "Teleport", "mult": 3},
        "ability_2": {"name": "Dark Wave", "mult": 5},
        "ability_3": {"name": "Dimension Rift", "mult": 10, "once": True},
    },
    "Bartra Liones": {
        "ability_1": {"name": "Vision", "mult": 3},
        "ability_2": {"name": "Royal Decree", "mult": 5},
        "ability_3": {"name": "Kingdom's Blessing", "mult": 10, "once": True},
    },
    "Margaret Liones": {
        "ability_1": {"name": "Noble Slash", "mult": 3},
        "ability_2": {"name": "Grace", "mult": 5},
        "ability_3": {"name": "Goddess Power", "mult": 10, "once": True},
    },
    "Veronica Liones": {
        "ability_1": {"name": "Spear Thrust", "mult": 3},
        "ability_2": {"name": "Royal Guard", "mult": 5},
        "ability_3": {"name": "Liones Spirit", "mult": 10, "once": True},
    },
    "Elaine": {
        "ability_1": {"name": "Fairy Wind", "mult": 3},
        "ability_2": {"name": "Nature's Blessing", "mult": 5},
        "ability_3": {"name": "Fairy King's Sister", "mult": 10, "once": True},
    },
}

# ============================================================
# BOSSES
# ============================================================
SDS_BOSSES = {
    # 🟢 ضعیف — Reward: 50,000
    "Hendrickson": {"display_name": "هندریکسون", "hp": 1000, "atk": 80, "reward": 50000},
    "Fraudrin": {"display_name": "فرادرین", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط — Reward: 100,000
    "Galand": {"display_name": "گالند", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی — Reward: 200,000
    "Estarossa": {"display_name": "استاروسا", "hp": 90000, "atk": 4400, "reward": 200000},
    "Meliodas (Assault Mode)": {"display_name": "ملیوداس (حالت حمله)", "hp": 100000, "atk": 4800, "reward": 200000},

    # 🔴 افسانه‌ای — Reward: 500,000
    "Demon King": {"display_name": "پادشاه شیاطین", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
SDS_FODDER = {
    "Holy Knight Apprentice": {"display_name": "شوالیه مقدس تازه‌کار", "hp": 400, "atk": 30, "reward": 5000},
    "Hendrickson": {"display_name": "هندریکسون", "hp": 1000, "atk": 80, "reward": 5000},
    "Fraudrin": {"display_name": "فرادرین", "hp": 1200, "atk": 90, "reward": 5000},
    "Galand": {"display_name": "گالند", "hp": 2000, "atk": 150, "reward": 5000},
}