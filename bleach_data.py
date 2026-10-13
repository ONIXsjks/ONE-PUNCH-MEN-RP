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

# ============================================================
# BLEACH ABILITIES (شاپ)
# ============================================================
BLEACH_ABILITIES_SHOP = {
    "Getsuga Tensho": {
        "effect": "ATK x4",
        "effect_fa": "ضربه ماه‌شکن ۴x",
        "price": 25000,
    },
    "Cero": {
        "effect": "ATK x5 + no dodge",
        "effect_fa": "سرخ ۵x + جاخالی ممنوع",
        "price": 35000,
    },
    "Bankai Boost": {
        "effect": "ATK +50% for 2 turns",
        "effect_fa": "باف بانکای +۵۰٪ برای ۲ راند",
        "price": 30000,
    },
    "Shunpo": {
        "effect": "DODGE +40% (2 turns)",
        "effect_fa": "قدم سریع جاخالی +۴۰٪",
        "price": 22000,
    },
    "Kido Blast": {
        "effect": "ATK x3 + enemy -20% DEF",
        "effect_fa": "جادو ضربه ۳x + دفاع دشمن -۲۰٪",
        "price": 20000,
    },
    "Hollow Mask": {
        "effect": "ATK +30% + DODGE +20% (2 turns)",
        "effect_fa": "ماسک هالو +۳۰٪ حمله +۲۰٪ جاخالی",
        "price": 28000,
    },
    "Quincy Arrow": {
        "effect": "ATK x3.5",
        "effect_fa": "تیر کوئینسی ۳.۵x",
        "price": 18000,
    },
    "Flash Step": {
        "effect": "Extra turn",
        "effect_fa": "نوبت اضافه",
        "price": 32000,
    },
    "Reiatsu Wave": {
        "effect": "ATK x2.5 + enemy ATK -25% (2 turns)",
        "effect_fa": "موج روحی ۲.۵x + حمله دشمن -۲۵٪",
        "price": 24000,
    },
    "Final Getsuga": {
        "effect": "ATK x6 + self 20% HP",
        "effect_fa": "گتسوگا نهایی ۶x + خودت ۲۰٪ HP",
        "price": 50000,
    },
}

# ============================================================
# BLEACH BANKAI (۱ بار مصرف، متوسط)
# ============================================================
BLEACH_BANKAI = {
    # ============ S RANK ============
    "Ichigo Kurosaki": {
        "name": "Tensa Zangetsu",
        "atk_boost": 35,
        "dodge_boost": 20,
        "hp_drain": 10,
        "duration": 2,
    },
    "Sosuke Aizen": {
        "name": "Kyoka Suigetsu",
        "freeze": 1,
        "atk_boost": 30,
        "duration": 2,
    },
    "Yhwach": {
        "name": "The Almighty",
        "atk_boost": 40,
        "def_boost": 25,
        "hp_drain": 10,
        "duration": 2,
    },
    "Genryusai Yamamoto": {
        "name": "Zanka no Tachi",
        "hp_drain": 15,
        "atk_boost": 35,
        "duration": 3,
    },
    "Kenpachi Zaraki": {
        "name": "Nozarashi",
        "atk_boost": 50,
        "self_dmg": 15,
        "duration": 2,
    },
    "Byakuya Kuchiki": {
        "name": "Senbonzakura Kageyoshi",
        "multi_hits": 3,
        "dodge_debuff": 20,
        "duration": 2,
    },
    "Toshiro Hitsugaya": {
        "name": "Daiguren Hyorinmaru",
        "freeze": 1,
        "atk_boost": 25,
        "duration": 2,
    },
    "Shunsui Kyoraku": {
        "name": "Katen Kyokotsu: Karamatsu Shinju",
        "hp_drain": 12,
        "atk_boost": 20,
        "duration": 3,
    },
    "Kisuke Urahara": {
        "name": "Kannonbiraki Benihime Aratame",
        "atk_boost": 20,
        "heal_per_turn": 15,
        "duration": 2,
    },
    "Ichibe Hyosube": {
        "name": "Shirafude Ichimonji",
        "enemy_atk_debuff": 30,
        "duration": 2,
    },
    "White Zangetsu": {
        "name": "Vasto Lorde Form",
        "atk_boost": 40,
        "hp_drain": 15,
        "dodge_boost": 15,
        "duration": 2,
    },
    "Ulquiorra Cifer": {
        "name": "Resurrección: Segunda Etapa",
        "atk_boost": 40,
        "hp_drain": 15,
        "duration": 2,
    },

    # ============ A RANK ============
    "Renji Abarai": {
        "name": "So'o Zabimaru",
        "multi_hits": 3,
        "atk_boost": 25,
        "duration": 2,
    },
    "Rukia Kuchiki": {
        "name": "Hakka no Togame",
        "freeze": 1,
        "hp_drain": 12,
        "duration": 2,
    },
    "Ikkaku Madarame": {
        "name": "Ryumon Hozukimaru",
        "atk_boost": 45,
        "def_debuff": 15,
        "duration": 2,
    },
    "Yumichika Ayasegawa": {
        "name": "Ruri'iro Kujaku",
        "hp_drain": 20,
        "heal": 20,
        "duration": 1,
    },
    "Shuhei Hisagi": {
        "name": "Kazeshini",
        "freeze": 1,
        "hp_drain": 12,
        "duration": 2,
    },
    "Kensei Muguruma": {
        "name": "Tekken Tachikaze",
        "multi_hits": 2,
        "atk_boost": 25,
        "duration": 2,
    },
    "Rojuro Otoribashi": {
        "name": "Kinshara Butodan",
        "hp_drain": 8,
        "duration": 3,
    },
    "Love Aikawa": {
        "name": "Tengumaru",
        "atk_boost": 30,
        "duration": 2,
    },
    "Grimmjow Jaegerjaquez": {
        "name": "Resurrección: Pantera",
        "atk_boost": 30,
        "dodge_boost": 20,
        "duration": 2,
    },
    "Nelliel Tu": {
        "name": "Gamuza",
        "atk_boost": 25,
        "hp_drain": 12,
        "duration": 2,
    },

    # ============ B RANK ============
    "Yasutora Sado": {
        "name": "Brazo Izquierda del Diablo",
        "atk_boost": 30,
        "def_boost": 20,
        "duration": 2,
    },
    "Orihime Inoue": {
        "name": "Koten Zanshun",
        "heal": 40,
        "immortal": 1,
        "duration": 2,
    },
    "Uryu Ishida": {
        "name": "Vollständig: Antithesis",
        "atk_boost": 25,
        "duration": 2,
    },
    "Tier Harribel": {
        "name": "Resurrección: Tiburon",
        "multi_hits": 2,
        "atk_boost": 20,
        "duration": 2,
    },
    "Coyote Starrk": {
        "name": "Resurrección: Los Lobos",
        "multi_hits": 5,
        "dodge_debuff": 15,
        "duration": 2,
    },
    "Baraggan Louisenbairn": {
        "name": "Resurrección: Arrogante",
        "hp_drain": 10,
        "duration": 2,
    },
    "Soi Fon": {
        "name": "Bankai: Jakuhō Raikōben",
        "atk_boost": 35,
        "freeze": 1,
        "duration": 1,
    },
    "Yoruichi Shihoin": {
        "name": "Shunkō: Raijin Senkei",
        "atk_boost": 30,
        "dodge_boost": 25,
        "duration": 2,
    },
    "Retsu Unohana": {
        "name": "Bankai: Minazuki",
        "heal": 30,
        "atk_boost": 25,
        "duration": 2,
    },
    "Marechiyo Omaeda": {
        "name": "Bankai: Jizō Engaku",
        "def_boost": 30,
        "atk_boost": 15,
        "duration": 2,
    },
}

# ============================================================
# BLEACH BOSSES (۶ قوی)
# ============================================================
BLEACH_BOSSES = {
    "Aizen (Final Form)": {
        "display_name": "Sosuke Aizen (Final)",
        "hp": 60000,
        "atk": 2500,
        "reward": 15000,
    },
    "Yhwach (Soul King)": {
        "display_name": "Yhwach (Soul King)",
        "hp": 70000,
        "atk": 2800,
        "reward": 15000,
    },
    "Ichigo (Vasto Lorde)": {
        "display_name": "Ichigo (Vasto Lorde)",
        "hp": 45000,
        "atk": 2200,
        "reward": 15000,
    },
    "Yamamoto (Bankai)": {
        "display_name": "Yamamoto (Bankai)",
        "hp": 50000,
        "atk": 2400,
        "reward": 15000,
    },
    "Ulquiorra (Segunda Etapa)": {
        "display_name": "Ulquiorra (2nd Etapa)",
        "hp": 40000,
        "atk": 2000,
        "reward": 15000,
    },
    "Gerard Valkyrie": {
        "display_name": "Gerard (Miracle)",
        "hp": 55000,
        "atk": 2300,
        "reward": 15000,
    },
}

# ============================================================
# BLEACH FODDER (۴ ضعیف)
# ============================================================
BLEACH_FODDER = {
    "Hollow": {
        "display_name": "هالو",
        "hp": 500,
        "atk": 40,
        "reward": 5000,
    },
    "Menos Grande": {
        "display_name": "منوس گرانده",
        "hp": 800,
        "atk": 60,
        "reward": 5000,
    },
    "Adjuchas": {
        "display_name": "آدجوچاس",
        "hp": 1200,
        "atk": 90,
        "reward": 5000,
    },
    "Weak Vasto Lorde": {
        "display_name": "واستو لرد ضعیف",
        "hp": 2000,
        "atk": 150,
        "reward": 5000,
    },
}
