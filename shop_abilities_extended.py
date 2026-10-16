# ============================================================
# EXTENDED SHOP ABILITIES — 5 Anime
# ============================================================

# ============================================================
# ATTACK ON TITAN SHOP
# ============================================================
AOT_ABILITIES_SHOP = {
    "ODM Gear Boost": {
        "effect": "DODGE +40% (2 turns)",
        "effect_fa": "جاخالی +۴۰٪ (۲ راند)",
        "price": 22000,
    },
    "Thunder Spear": {
        "effect": "ATK x3.5",
        "effect_fa": "نیزه رعد ۳.۵x",
        "price": 25000,
    },
    "Titan Shifter Form": {
        "effect": "ATK x5 + 15% HP",
        "effect_fa": "فرم تایتان ۵x + ۱۵٪ HP",
        "price": 45000,
    },
    "Hardening Crystal": {
        "effect": "DEF +50% (2 turns)",
        "effect_fa": "کریستال سخت +۵۰٪ دفاع",
        "price": 28000,
    },
    "The Rumbling": {
        "effect": "ATK x6 + no dodge",
        "effect_fa": "رامبلینگ ۶x + جاخالی ممنوع",
        "price": 50000,
    },
}

# ============================================================
# BLACK CLOVER SHOP
# ============================================================
BLACKCLOVER_ABILITIES_SHOP = {
    "Mana Zone": {
        "effect": "ATK x4",
        "effect_fa": "مانا زون ۴x",
        "price": 30000,
    },
    "Anti-Magic Slash": {
        "effect": "ATK x5 + remove enemy buffs",
        "effect_fa": "ضربه آنتی‌مجیک ۵x + حذف باف دشمن",
        "price": 38000,
    },
    "Spirit Dive": {
        "effect": "ATK +50% (2 turns)",
        "effect_fa": "اسپیریت دایو +۵۰٪ (۲ راند)",
        "price": 32000,
    },
    "Grimoire Awakening": {
        "effect": "ATK x6",
        "effect_fa": "بیداری گریمور ۶x",
        "price": 48000,
    },
    "Devil Union": {
        "effect": "ATK x7 (1 time)",
        "effect_fa": "اتحاد شیطان ۷x (۱ بار)",
        "price": 55000,
    },
}

# ============================================================
# BERSERK SHOP
# ============================================================
BERSERK_ABILITIES_SHOP = {
    "Dragon Slayer Swing": {
        "effect": "ATK x3.5",
        "effect_fa": "ضربه کشنده اژدها ۳.۵x",
        "price": 24000,
    },
    "Cannon Arm": {
        "effect": "ATK x4 + enemy -20% DEF",
        "effect_fa": "بازوی توپ ۴x + دفاع دشمن -۲۰٪",
        "price": 30000,
    },
    "Berserker Armor": {
        "effect": "ATK +60% + self 10% dmg",
        "effect_fa": "زره برزرکر +۶۰٪ + ۱۰٪ آسیب به خود",
        "price": 40000,
    },
    "Behelit Sacrifice": {
        "effect": "ATK x6",
        "effect_fa": "قربانی بهلیت ۶x",
        "price": 50000,
    },
    "Skull Knight Blade": {
        "effect": "ATK x7 (1 time)",
        "effect_fa": "شمشیر شوالیه جمجمه ۷x (۱ بار)",
        "price": 55000,
    },
}

# ============================================================
# DEMON SLAYER SHOP
# ============================================================
DEMONSLAYER_ABILITIES_SHOP = {
    "Water Breathing": {
        "effect": "ATK x3",
        "effect_fa": "تنفس آب ۳x",
        "price": 20000,
    },
    "Hinokami Kagura": {
        "effect": "ATK x5 + no dodge",
        "effect_fa": "هینوکامی کاگورا ۵x + جاخالی ممنوع",
        "price": 35000,
    },
    "Total Concentration": {
        "effect": "ATK +40% + DODGE +20%",
        "effect_fa": "تمرکز کامل +۴۰٪ حمله + ۲۰٪ جاخالی",
        "price": 28000,
    },
    "Mark of the Demon Slayer": {
        "effect": "ATK x6",
        "effect_fa": "نشان شیطان‌کش ۶x",
        "price": 45000,
    },
    "Sun Breathing 13th": {
        "effect": "ATK x8 (1 time)",
        "effect_fa": "تنفس خورشید فرم ۱۳ ۸x (۱ بار)",
        "price": 60000,
    },
}

# ============================================================
# CHAINSAW MAN SHOP
# ============================================================
CHAINSAWMAN_ABILITIES_SHOP = {
    "Chainsaw Rush": {
        "effect": "ATK x3.5",
        "effect_fa": "حمله اره‌برقی ۳.۵x",
        "price": 24000,
    },
    "Blood Frenzy": {
        "effect": "ATK x4 + 10% HP",
        "effect_fa": "دیوانگی خون ۴x + ۱۰٪ HP",
        "price": 30000,
    },
    "Devil Contract": {
        "effect": "ATK +50% (2 turns)",
        "effect_fa": "قرارداد شیطان +۵۰٪ (۲ راند)",
        "price": 32000,
    },
    "Hybrid Form": {
        "effect": "ATK x6",
        "effect_fa": "فرم هیبرید ۶x",
        "price": 48000,
    },
    "Hero of Hell": {
        "effect": "ATK x8 (1 time)",
        "effect_fa": "قهرمان جهنم ۸x (۱ بار)",
        "price": 60000,
    },
}

# ============================================================
# MERGED DICT — برای اضافه‌کردن به ABILITIES توی config
# ============================================================
EXTENDED_SHOP_ABILITIES = {}
EXTENDED_SHOP_ABILITIES.update(AOT_ABILITIES_SHOP)
EXTENDED_SHOP_ABILITIES.update(BLACKCLOVER_ABILITIES_SHOP)
EXTENDED_SHOP_ABILITIES.update(BERSERK_ABILITIES_SHOP)
EXTENDED_SHOP_ABILITIES.update(DEMONSLAYER_ABILITIES_SHOP)
EXTENDED_SHOP_ABILITIES.update(CHAINSAWMAN_ABILITIES_SHOP)

# ============================================================
# FA (فارسی) — برای نمایش در Shop
# ============================================================
EXTENDED_SHOP_ABILITIES_FA = {
    # AOT
    "ODM Gear Boost": "باف چرخ‌دنده ODM",
    "Thunder Spear": "نیزه رعد",
    "Titan Shifter Form": "فرم تایتان شیفتر",
    "Hardening Crystal": "کریستال سخت",
    "The Rumbling": "رامبلینگ",
    # Black Clover
    "Mana Zone": "مانا زون",
    "Anti-Magic Slash": "ضربه آنتی‌مجیک",
    "Spirit Dive": "اسپیریت دایو",
    "Grimoire Awakening": "بیداری گریمور",
    "Devil Union": "اتحاد شیطان",
    # Berserk
    "Dragon Slayer Swing": "ضربه کشنده اژدها",
    "Cannon Arm": "بازوی توپ",
    "Berserker Armor": "زره برزرکر",
    "Behelit Sacrifice": "قربانی بهلیت",
    "Skull Knight Blade": "شمشیر شوالیه جمجمه",
    # Demon Slayer
    "Water Breathing": "تنفس آب",
    "Hinokami Kagura": "هینوکامی کاگورا",
    "Total Concentration": "تمرکز کامل",
    "Mark of the Demon Slayer": "نشان شیطان‌کش",
    "Sun Breathing 13th": "تنفس خورشید فرم ۱۳",
    # Chainsaw Man
    "Chainsaw Rush": "حمله اره‌برقی",
    "Blood Frenzy": "دیوانگی خون",
    "Devil Contract": "قرارداد شیطان",
    "Hybrid Form": "فرم هیبرید",
    "Hero of Hell": "قهرمان جهنم",
}