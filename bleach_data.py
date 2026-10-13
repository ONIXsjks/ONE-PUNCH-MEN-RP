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

CHAR_PRICES_BLEACH = {
    "S": 250000,
    "A": 180000,
    "B": 100000,
}

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

BLEACH_BOSSES = {
    "Aizen (Final Form)": {"display_name": "Sosuke Aizen (Final)", "hp": 60000, "atk": 2500, "reward": 15000},
    "Yhwach (Soul King)": {"display_name": "Yhwach (Soul King)", "hp": 70000, "atk": 2800, "reward": 15000},
    "Ichigo (Vasto Lorde)": {"display_name": "Ichigo (Vasto Lorde)", "hp": 45000, "atk": 2200, "reward": 15000},
    "Yamamoto (Bankai)": {"display_name": "Yamamoto (Bankai)", "hp": 50000, "atk": 2400, "reward": 15000},
    "Ulquiorra (Segunda Etapa)": {"display_name": "Ulquiorra (2nd Etapa)", "hp": 40000, "atk": 2000, "reward": 15000},
    "Gerard Valkyrie": {"display_name": "Gerard (Miracle)", "hp": 55000, "atk": 2300, "reward": 15000},
}

BLEACH_FODDER = {
    "Hollow": {"display_name": "هالو", "hp": 500, "atk": 40, "reward": 5000},
    "Menos Grande": {"display_name": "منوس گرانده", "hp": 800, "atk": 60, "reward": 5000},
    "Adjuchas": {"display_name": "آدجوچاس", "hp": 1200, "atk": 90, "reward": 5000},
    "Weak Vasto Lorde": {"display_name": "واستو لرد ضعیف", "hp": 2000, "atk": 150, "reward": 5000},
}
