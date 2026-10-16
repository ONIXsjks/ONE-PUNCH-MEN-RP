# ============================================================
# BLEACH DATA
# ============================================================

CHARACTERS_BLEACH = {
    "S": {
        "Ichigo Kurosaki": "Substitute Soul Reaper",
        "Sosuke Aizen": "Former Captain",
        "Yhwach": "Quincy King",
        "Genryusai Yamamoto": "Captain Commander",
        "Kenpachi Zaraki": "11th Division Captain",
        "Byakuya Kuchiki": "6th Division Captain",
        "Toshiro Hitsugaya": "10th Division Captain",
        "Shunsui Kyoraku": "8th Division Captain",
        "Kisuke Urahara": "Former Captain",
        "Ichibe Hyosube": "Royal Guard",
        "White Zangetsu": "Ichigo's Hollow",
        "Ulquiorra Cifer": "Arrancar",
    },
    "A": {
        "Renji Abarai": "6th Division Lieutenant",
        "Rukia Kuchiki": "13th Division",
        "Ikkaku Madarame": "11th Division",
        "Yumichika Ayasegawa": "11th Division",
        "Shuhei Hisagi": "9th Division Lieutenant",
        "Kensei Muguruma": "9th Division Captain",
        "Rojuro Otoribashi": "3rd Division Captain",
        "Love Aikawa": "Former Captain",
        "Grimmjow Jaegerjaquez": "Arrancar",
        "Nelliel Tu": "Former Espada",
    },
    "B": {
        "Yasutora Sado": "Ichigo's Friend",
        "Orihime Inoue": "Ichigo's Friend",
        "Uryu Ishida": "Quincy",
        "Tier Harribel": "Espada",
        "Coyote Starrk": "Primera Espada",
        "Baraggan Louisenbairn": "Segunda Espada",
        "Soi Fon": "2nd Division Captain",
        "Yoruichi Shihoin": "Former Captain",
        "Retsu Unohana": "4th Division Captain",
        "Marechiyo Omaeda": "2nd Division Lieutenant",
    },
}

CHAR_PRICES_BLEACH = {"S": 2000000, "A": 500000, "B": 150000}

BLEACH_ABILITIES_SHOP = {
    "Getsuga Tensho": {"effect": "ATK x4", "effect_fa": "ضربه ماه‌شکن ۴x", "price": 25000},
    "Cero": {"effect": "ATK x5 + no dodge", "effect_fa": "سرخ ۵x + جاخالی ممنوع", "price": 35000},
    "Bankai Boost": {"effect": "ATK +50% for 2 turns", "effect_fa": "باف بانکای +۵۰٪", "price": 30000},
    "Shunpo": {"effect": "DODGE +40% (2 turns)", "effect_fa": "قدم سریع جاخالی +۴۰٪", "price": 22000},
    "Kido Blast": {"effect": "ATK x3 + enemy -20% DEF", "effect_fa": "جادو ضربه ۳x", "price": 20000},
    "Hollow Mask": {"effect": "ATK +30% + DODGE +20%", "effect_fa": "ماسک هالو", "price": 28000},
    "Quincy Arrow": {"effect": "ATK x3.5", "effect_fa": "تیر کوئینسی ۳.۵x", "price": 18000},
    "Flash Step": {"effect": "Extra turn", "effect_fa": "نوبت اضافه", "price": 32000},
    "Reiatsu Wave": {"effect": "ATK x2.5 + enemy ATK -25%", "effect_fa": "موج روحی", "price": 24000},
    "Final Getsuga": {"effect": "ATK x6 + self 20% HP", "effect_fa": "گتسوگا نهایی", "price": 50000},
}

# ============================================================
# ABILITIES - هر کاراکتر ۳ Ability
# ============================================================
ABILITIES_BLEACH = {
    # ============ S RANK ============
    "Ichigo Kurosaki": {
        "ability_1": {"name": "Getsuga Tensho", "mult": 3},
        "ability_2": {"name": "Bankai Getsuga", "mult": 5},
        "ability_3": {"name": "Mugetsu", "mult": 10, "once": True},
    },
    "Sosuke Aizen": {
        "ability_1": {"name": "Kyoka Suigetsu", "mult": 3},
        "ability_2": {"name": "Fragor", "mult": 5},
        "ability_3": {"name": "Hogyoku Fusion", "mult": 10, "once": True},
    },
    "Yhwach": {
        "ability_1": {"name": "Sankt Altar", "mult": 3},
        "ability_2": {"name": "Auswahlen", "mult": 5},
        "ability_3": {"name": "The Almighty", "mult": 10, "once": True},
    },
    "Genryusai Yamamoto": {
        "ability_1": {"name": "Ryujin Jakka", "mult": 3},
        "ability_2": {"name": "Zanka no Tachi", "mult": 5},
        "ability_3": {"name": "Ennetsu Jigoku", "mult": 10, "once": True},
    },
    "Kenpachi Zaraki": {
        "ability_1": {"name": "Nozarashi", "mult": 3},
        "ability_2": {"name": "Kendo", "mult": 5},
        "ability_3": {"name": "Bankai: Nozarashi", "mult": 10, "once": True},
    },
    "Byakuya Kuchiki": {
        "ability_1": {"name": "Senbonzakura", "mult": 3},
        "ability_2": {"name": "Kageyoshi", "mult": 5},
        "ability_3": {"name": "Ikka Senjinka", "mult": 10, "once": True},
    },
    "Toshiro Hitsugaya": {
        "ability_1": {"name": "Hyorinmaru", "mult": 3},
        "ability_2": {"name": "Daiguren Hyorinmaru", "mult": 5},
        "ability_3": {"name": "Hyoten Hyakkaso", "mult": 10, "once": True},
    },
    "Shunsui Kyoraku": {
        "ability_1": {"name": "Katen Kyokotsu", "mult": 3},
        "ability_2": {"name": "Irooni", "mult": 5},
        "ability_3": {"name": "Kageoni", "mult": 10, "once": True},
    },
    "Kisuke Urahara": {
        "ability_1": {"name": "Benihime", "mult": 3},
        "ability_2": {"name": "Kannonbiraki", "mult": 5},
        "ability_3": {"name": "Bankai: Kannonbiraki", "mult": 10, "once": True},
    },
    "Ichibe Hyosube": {
        "ability_1": {"name": "Ichimonji", "mult": 3},
        "ability_2": {"name": "Shirafude Ichimonji", "mult": 5},
        "ability_3": {"name": "Futen Taisatsuryo", "mult": 10, "once": True},
    },
    "White Zangetsu": {
        "ability_1": {"name": "Cero", "mult": 3},
        "ability_2": {"name": "Vasto Lorde", "mult": 5},
        "ability_3": {"name": "Full Hollowfication", "mult": 10, "once": True},
    },
    "Ulquiorra Cifer": {
        "ability_1": {"name": "Cero Oscuras", "mult": 3},
        "ability_2": {"name": "Lanza del Relampago", "mult": 5},
        "ability_3": {"name": "Segunda Etapa", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Renji Abarai": {
        "ability_1": {"name": "Zabimaru", "mult": 3},
        "ability_2": {"name": "Hihio Zabimaru", "mult": 5},
        "ability_3": {"name": "So'o Zabimaru", "mult": 10, "once": True},
    },
    "Rukia Kuchiki": {
        "ability_1": {"name": "Sode no Shirayuki", "mult": 3},
        "ability_2": {"name": "Some no Mai", "mult": 5},
        "ability_3": {"name": "Hakka no Togame", "mult": 10, "once": True},
    },
    "Ikkaku Madarame": {
        "ability_1": {"name": "Hozukimaru", "mult": 3},
        "ability_2": {"name": "Bankai: Ryumon", "mult": 5},
        "ability_3": {"name": "Ryumon Hozukimaru", "mult": 10, "once": True},
    },
    "Yumichika Ayasegawa": {
        "ability_1": {"name": "Fujikujaku", "mult": 3},
        "ability_2": {"name": "Ruri'iro Kujaku", "mult": 5},
        "ability_3": {"name": "Kujaku's Wrath", "mult": 10, "once": True},
    },
    "Shuhei Hisagi": {
        "ability_1": {"name": "Kazeshini", "mult": 3},
        "ability_2": {"name": "Reaper's Dance", "mult": 5},
        "ability_3": {"name": "Kazeshini's Fury", "mult": 10, "once": True},
    },
    "Kensei Muguruma": {
        "ability_1": {"name": "Tachikaze", "mult": 3},
        "ability_2": {"name": "Tekken Tachikaze", "mult": 5},
        "ability_3": {"name": "Explosion Fist", "mult": 10, "once": True},
    },
    "Rojuro Otoribashi": {
        "ability_1": {"name": "Kinshara", "mult": 3},
        "ability_2": {"name": "Kinshara Butodan", "mult": 5},
        "ability_3": {"name": "Dance of Sound", "mult": 10, "once": True},
    },
    "Love Aikawa": {
        "ability_1": {"name": "Tengumaru", "mult": 3},
        "ability_2": {"name": "Hifuki no Koduchi", "mult": 5},
        "ability_3": {"name": "Tengumaru's Wrath", "mult": 10, "once": True},
    },
    "Grimmjow Jaegerjaquez": {
        "ability_1": {"name": "Darts", "mult": 3},
        "ability_2": {"name": "Desgarron", "mult": 5},
        "ability_3": {"name": "Pantera", "mult": 10, "once": True},
    },
    "Nelliel Tu": {
        "ability_1": {"name": "Cero Doble", "mult": 3},
        "ability_2": {"name": "Lanzador Verde", "mult": 5},
        "ability_3": {"name": "Gamuza", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Yasutora Sado": {
        "ability_1": {"name": "Right Arm of the Giant", "mult": 3},
        "ability_2": {"name": "Left Arm of the Devil", "mult": 5},
        "ability_3": {"name": "Fullbring: Brazo", "mult": 10, "once": True},
    },
    "Orihime Inoue": {
        "ability_1": {"name": "Koten Zanshun", "mult": 3},
        "ability_2": {"name": "Santen Kesshun", "mult": 5},
        "ability_3": {"name": "Shiten Koshun", "mult": 10, "once": True},
    },
    "Uryu Ishida": {
        "ability_1": {"name": "Heilig Pfeil", "mult": 3},
        "ability_2": {"name": "Sprenger", "mult": 5},
        "ability_3": {"name": "Vollständig", "mult": 10, "once": True},
    },
    "Tier Harribel": {
        "ability_1": {"name": "Hirviendo", "mult": 3},
        "ability_2": {"name": "Cascada", "mult": 5},
        "ability_3": {"name": "Tiburon", "mult": 10, "once": True},
    },
    "Coyote Starrk": {
        "ability_1": {"name": "Cero Metralleta", "mult": 3},
        "ability_2": {"name": "Los Lobos", "mult": 5},
        "ability_3": {"name": "Cero Metralleta (Full)", "mult": 10, "once": True},
    },
    "Baraggan Louisenbairn": {
        "ability_1": {"name": "Respiro", "mult": 3},
        "ability_2": {"name": "Gran Caida", "mult": 5},
        "ability_3": {"name": "Arrogante", "mult": 10, "once": True},
    },
    "Soi Fon": {
        "ability_1": {"name": "Suzumebachi", "mult": 3},
        "ability_2": {"name": "Nigeki Kessatsu", "mult": 5},
        "ability_3": {"name": "Jakuhō Raikōben", "mult": 10, "once": True},
    },
    "Yoruichi Shihoin": {
        "ability_1": {"name": "Shunko", "mult": 3},
        "ability_2": {"name": "Raijin Senkei", "mult": 5},
        "ability_3": {"name": "Shunko: Full Power", "mult": 10, "once": True},
    },
    "Retsu Unohana": {
        "ability_1": {"name": "Minazuki", "mult": 3},
        "ability_2": {"name": "Bankai: Minazuki", "mult": 5},
        "ability_3": {"name": "Kenpachi Mode", "mult": 10, "once": True},
    },
    "Marechiyo Omaeda": {
        "ability_1": {"name": "Gegetsuburi", "mult": 3},
        "ability_2": {"name": "Jizo Engaku", "mult": 5},
        "ability_3": {"name": "Omaeda's Wrath", "mult": 10, "once": True},
    },
}

# ============================================================
# BANKAI
# ============================================================
BLEACH_BANKAI = {
    "Ichigo Kurosaki": {"name": "Tensa Zangetsu", "atk_per_round": 10, "dodge_per_round": 6, "max_atk": 50, "max_dodge": 30},
    "Sosuke Aizen": {"name": "Kyoka Suigetsu", "atk_per_round": 9, "dodge_per_round": 6, "max_atk": 45, "max_dodge": 30},
    "Yhwach": {"name": "The Almighty", "atk_per_round": 10, "dodge_per_round": 5, "max_atk": 50, "max_dodge": 25},
    "Genryusai Yamamoto": {"name": "Zanka no Tachi", "atk_per_round": 9, "bleed_per_round": 2, "max_atk": 45, "max_bleed": 8},
    "Kenpachi Zaraki": {"name": "Nozarashi", "atk_per_round": 10, "self_dmg_per_round": 2, "max_atk": 50, "max_self_dmg": 8},
    "Byakuya Kuchiki": {"name": "Senbonzakura Kageyoshi", "atk_per_round": 8, "extra_hit_chance": 20, "max_atk": 40},
    "Toshiro Hitsugaya": {"name": "Daiguren Hyorinmaru", "atk_per_round": 8, "freeze_chance": 15, "max_atk": 40},
    "Shunsui Kyoraku": {"name": "Katen Kyokotsu", "atk_per_round": 9, "crit_chance": 20, "max_atk": 45},
    "Kisuke Urahara": {"name": "Benihime Aratame", "atk_per_round": 8, "heal_per_round": 5, "max_atk": 40, "max_heal": 20},
    "Ichibe Hyosube": {"name": "Shirafude Ichimonji", "atk_per_round": 9, "enemy_atk_debuff": 4, "max_atk": 45, "max_enemy_debuff": 20},
    "White Zangetsu": {"name": "Vasto Lorde Form", "atk_per_round": 10, "heal_per_round": 4, "max_atk": 50, "max_heal": 15},
    "Ulquiorra Cifer": {"name": "Resurrección: Segunda Etapa", "atk_per_round": 10, "crit_chance": 25, "max_atk": 50},
    "Renji Abarai": {"name": "So'o Zabimaru", "atk_per_round": 7, "extra_hit_chance": 20, "max_atk": 35},
    "Rukia Kuchiki": {"name": "Hakka no Togame", "atk_per_round": 6, "freeze_chance": 15, "max_atk": 30},
    "Ikkaku Madarame": {"name": "Ryumon Hozukimaru", "atk_per_round": 8, "dodge_debuff": 5, "max_atk": 40},
    "Yumichika Ayasegawa": {"name": "Ruri'iro Kujaku", "atk_per_round": 6, "heal_per_round": 4, "max_atk": 30, "max_heal": 15},
    "Shuhei Hisagi": {"name": "Kazeshini", "atk_per_round": 6, "bleed_per_round": 2, "max_atk": 30, "max_bleed": 8},
    "Kensei Muguruma": {"name": "Tekken Tachikaze", "atk_per_round": 7, "crit_chance": 15, "max_atk": 35},
    "Rojuro Otoribashi": {"name": "Kinshara Butodan", "atk_per_round": 7, "bleed_per_round": 2, "max_atk": 35, "max_bleed": 8},
    "Love Aikawa": {"name": "Tengumaru", "atk_per_round": 7, "extra_hit_chance": 20, "max_atk": 35},
    "Grimmjow Jaegerjaquez": {"name": "Pantera", "atk_per_round": 8, "dodge_per_round": 4, "max_atk": 40, "max_dodge": 20},
    "Nelliel Tu": {"name": "Gamuza", "atk_per_round": 7, "heal_per_round": 4, "max_atk": 35, "max_heal": 15},
    "Yasutora Sado": {"name": "Brazo Izquierda del Diablo", "atk_per_round": 5, "dodge_debuff": 3, "max_atk": 25},
    "Orihime Inoue": {"name": "Koten Zanshun", "atk_per_round": 3, "heal_per_round": 6, "dodge_per_round": 4, "max_atk": 15, "max_heal": 25, "max_dodge": 20},
    "Uryu Ishida": {"name": "Vollständig: Antithesis", "atk_per_round": 5, "extra_hit_chance": 20, "max_atk": 25},
    "Tier Harribel": {"name": "Tiburon", "atk_per_round": 5, "freeze_chance": 15, "max_atk": 25},
    "Coyote Starrk": {"name": "Los Lobos", "atk_per_round": 5, "extra_hit_chance": 15, "max_atk": 25},
    "Baraggan Louisenbairn": {"name": "Arrogante", "atk_per_round": 5, "bleed_per_round": 2, "max_atk": 25, "max_bleed": 8},
    "Soi Fon": {"name": "Jakuhō Raikōben", "atk_per_round": 7, "crit_chance": 20, "max_atk": 35},
    "Yoruichi Shihoin": {"name": "Shunkō: Raijin Senkei", "atk_per_round": 5, "dodge_per_round": 5, "max_atk": 25, "max_dodge": 25},
    "Retsu Unohana": {"name": "Minazuki", "atk_per_round": 6, "heal_per_round": 5, "max_atk": 30, "max_heal": 20},
    "Marechiyo Omaeda": {"name": "Jizō Engaku", "atk_per_round": 4, "dodge_per_round": 3, "max_atk": 20, "max_dodge": 15},
}

# ============================================================
# BOSSES (مرتب‌شده بر اساس قدرت)
# ============================================================
BLEACH_BOSSES = {
    # 🟢 ضعیف (HP < 5k، ATK < 300) — جایزه: 50,000
    "Hollow": {"display_name": "هالو", "hp": 500, "atk": 40, "reward": 50000},
    "Menos Grande": {"display_name": "منوس گرانده", "hp": 800, "atk": 60, "reward": 50000},
    "Adjuchas": {"display_name": "آدجوچاس", "hp": 1200, "atk": 90, "reward": 50000},

    # 🟡 متوسط (HP 5k-20k، ATK 300-800) — جایزه: 100,000
    "Weak Vasto Lorde": {"display_name": "واستو لرد ضعیف", "hp": 4000, "atk": 300, "reward": 100000},

    # 🟠 قوی (HP 20k-50k، ATK 800-2k) — جایزه: 200,000
    "Ulquiorra (Segunda Etapa)": {"display_name": "اولکویورا (مرحله دوم)", "hp": 80000, "atk": 4000, "reward": 200000},
    "Ichigo (Vasto Lorde)": {"display_name": "ایچیگو (واستو لرد)", "hp": 90000, "atk": 4400, "reward": 200000},
    "Yamamoto (Bankai)": {"display_name": "یاماموتو (بانکای)", "hp": 100000, "atk": 4800, "reward": 200000},
    "Aizen (Final Form)": {"display_name": "آیزن (فرم نهایی)", "hp": 120000, "atk": 5000, "reward": 200000},

    # 🔴 افسانه‌ای (HP 50k+، ATK 2k+) — جایزه: 500,000
    "Gerard Valkyrie": {"display_name": "جرارد (معجزه)", "hp": 170000, "atk": 4600, "reward": 500000},
    "Yhwach (Soul King)": {"display_name": "یاوخ (پادشاه روح)", "hp": 200000, "atk": 5600, "reward": 500000},
}

# ============================================================
# FODDER
# ============================================================
BLEACH_FODDER = {
    "Hollow": {"display_name": "هالو", "hp": 500, "atk": 40, "reward": 5000},
    "Menos Grande": {"display_name": "منوس گرانده", "hp": 800, "atk": 60, "reward": 5000},
    "Adjuchas": {"display_name": "آدجوچاس", "hp": 1200, "atk": 90, "reward": 5000},
    "Weak Vasto Lorde": {"display_name": "واستو لرد ضعیف", "hp": 2000, "atk": 150, "reward": 5000},
}