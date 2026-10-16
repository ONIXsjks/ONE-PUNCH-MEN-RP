# ============================================================
# ANIME REGISTRY — Central Registry for All 8 Animes
# ============================================================

# ============ OPM ============
from opm_data import (
    CHARACTERS_OPM, ABILITIES_OPM, BOSSES_OPM
)
try:
    from opm_data import OPM_FODDER
except ImportError:
    OPM_FODDER = None

# ============ JJK ============
from jjk_data import (
    CHARACTERS_JJK, ABILITIES_JJK, BOSSES_JJK,
    FODDER_JJK, DOMAINS_JJK
)

# ============ BLEACH ============
from bleach_data import (
    CHARACTERS_BLEACH, ABILITIES_BLEACH, BLEACH_BOSSES,
    BLEACH_FODDER, BLEACH_BANKAI, BLEACH_ABILITIES_SHOP
)

# ============ AOT ============
from aot_data import (
    CHARACTERS_AOT, ABILITIES_AOT, AOT_BOSSES,
    AOT_FODDER, CHAR_PRICES_AOT
)

# ============ BLACK CLOVER ============
from blackclover_data import (
    CHARACTERS_BLACKCLOVER, ABILITIES_BLACKCLOVER,
    BLACKCLOVER_BOSSES, BLACKCLOVER_FODDER,
    CHAR_PRICES_BLACKCLOVER
)

# ============ BERSERK ============
from berserk_data import (
    CHARACTERS_BERSERK, ABILITIES_BERSERK,
    BERSERK_BOSSES, BERSERK_FODDER,
    CHAR_PRICES_BERSERK
)

# ============ DEMON SLAYER ============
from demonslayer_data import (
    CHARACTERS_DEMONSLAYER, ABILITIES_DEMONSLAYER,
    DEMONSLAYER_BOSSES, DEMONSLAYER_FODDER,
    CHAR_PRICES_DEMONSLAYER
)

# ============ CHAINSAW MAN ============
from chainsawman_data import (
    CHARACTERS_CHAINSAWMAN, ABILITIES_CHAINSAWMAN,
    CHAINSAWMAN_BOSSES, CHAINSAWMAN_FODDER,
    CHAR_PRICES_CHAINSAWMAN
)

# ============ EXTENDED SHOP ABILITIES ============
from shop_abilities_extended import (
    AOT_ABILITIES_SHOP,
    BLACKCLOVER_ABILITIES_SHOP,
    BERSERK_ABILITIES_SHOP,
    DEMONSLAYER_ABILITIES_SHOP,
    CHAINSAWMAN_ABILITIES_SHOP,
    EXTENDED_SHOP_ABILITIES,
    EXTENDED_SHOP_ABILITIES_FA,
)


# ============================================================
# REGISTRY — همه انیمه‌ها به صورت جداگانه
# ============================================================
ANIME_REGISTRY = {
    "opm": {
        "name": "One Punch Man",
        "name_fa": "وان پانچ من",
        "emoji": "🥊",
        "characters": CHARACTERS_OPM,
        "abilities": ABILITIES_OPM,
        "bosses": BOSSES_OPM,
        "fodder": OPM_FODDER,
        "prices": {"S": 2000000, "A": 500000, "B": 150000, "C": 50000},
        "shop_abilities": {},  # OPM shop جدا نداره، از ABILITIES عمومی استفاده می‌کنه
        "has_domain": False,
        "has_bankai": False,
    },
    "jjk": {
        "name": "Jujutsu Kaisen",
        "name_fa": "جوجوتسو کایزن",
        "emoji": "🌀",
        "characters": CHARACTERS_JJK,
        "abilities": ABILITIES_JJK,
        "bosses": BOSSES_JJK,
        "fodder": FODDER_JJK,
        "domains": DOMAINS_JJK,
        "prices": {"S": 2000000, "A": 500000, "B": 150000, "C": 50000},
        "shop_abilities": {},
        "has_domain": True,
        "has_bankai": False,
    },
    "bleach": {
        "name": "Bleach",
        "name_fa": "بلیچ",
        "emoji": "⚔️",
        "characters": CHARACTERS_BLEACH,
        "abilities": ABILITIES_BLEACH,
        "bosses": BLEACH_BOSSES,
        "fodder": BLEACH_FODDER,
        "bankai": BLEACH_BANKAI,
        "prices": {"S": 2000000, "A": 500000, "B": 150000, "C": 50000},
        "shop_abilities": BLEACH_ABILITIES_SHOP,
        "has_domain": False,
        "has_bankai": True,
    },
    "aot": {
        "name": "Attack on Titan",
        "name_fa": "اتک آن تایتان",
        "emoji": "🗡️",
        "characters": CHARACTERS_AOT,
        "abilities": ABILITIES_AOT,
        "bosses": AOT_BOSSES,
        "fodder": AOT_FODDER,
        "prices": CHAR_PRICES_AOT,
        "shop_abilities": AOT_ABILITIES_SHOP,
        "has_domain": False,
        "has_bankai": False,
    },
    "blackclover": {
        "name": "Black Clover",
        "name_fa": "بلک کلوور",
        "emoji": "🍀",
        "characters": CHARACTERS_BLACKCLOVER,
        "abilities": ABILITIES_BLACKCLOVER,
        "bosses": BLACKCLOVER_BOSSES,
        "fodder": BLACKCLOVER_FODDER,
        "prices": CHAR_PRICES_BLACKCLOVER,
        "shop_abilities": BLACKCLOVER_ABILITIES_SHOP,
        "has_domain": False,
        "has_bankai": False,
    },
    "berserk": {
        "name": "Berserk",
        "name_fa": "برزرک",
        "emoji": "🩸",
        "characters": CHARACTERS_BERSERK,
        "abilities": ABILITIES_BERSERK,
        "bosses": BERSERK_BOSSES,
        "fodder": BERSERK_FODDER,
        "prices": CHAR_PRICES_BERSERK,
        "shop_abilities": BERSERK_ABILITIES_SHOP,
        "has_domain": False,
        "has_bankai": False,
    },
    "demonslayer": {
        "name": "Demon Slayer",
        "name_fa": "دیمن اسلیر",
        "emoji": "🌸",
        "characters": CHARACTERS_DEMONSLAYER,
        "abilities": ABILITIES_DEMONSLAYER,
        "bosses": DEMONSLAYER_BOSSES,
        "fodder": DEMONSLAYER_FODDER,
        "prices": CHAR_PRICES_DEMONSLAYER,
        "shop_abilities": DEMONSLAYER_ABILITIES_SHOP,
        "has_domain": False,
        "has_bankai": False,
    },
    "chainsawman": {
        "name": "Chainsaw Man",
        "name_fa": "چینساو من",
        "emoji": "🪚",
        "characters": CHARACTERS_CHAINSAWMAN,
        "abilities": ABILITIES_CHAINSAWMAN,
        "bosses": CHAINSAWMAN_BOSSES,
        "fodder": CHAINSAWMAN_FODDER,
        "prices": CHAR_PRICES_CHAINSAWMAN,
        "shop_abilities": CHAINSAWMAN_ABILITIES_SHOP,
        "has_domain": False,
        "has_bankai": False,
    },
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_anime(anime_key):
    """گرفتن اطلاعات یه انیمه"""
    return ANIME_REGISTRY.get(anime_key)


def get_anime_list():
    """لیست همه انیمه‌ها برای منو"""
    return [
        (key, data["emoji"], data["name"], data["name_fa"])
        for key, data in ANIME_REGISTRY.items()
    ]


def get_characters_by_anime(anime_key, rank):
    """کاراکترهای یه انیمه توی یه رنک"""
    anime = ANIME_REGISTRY.get(anime_key)
    if not anime:
        return {}
    return anime["characters"].get(rank, {})


def get_char_price_by_anime(anime_key, rank):
    """قیمت کاراکتر بر اساس انیمه و رنک"""
    anime = ANIME_REGISTRY.get(anime_key)
    if not anime:
        return 0
    return anime["prices"].get(rank, 8000)


def find_char_anime(char_name):
    """پیدا کردن انیمه‌ی یه کاراکتر بر اساس اسمش"""
    for anime_key, data in ANIME_REGISTRY.items():
        for rank, chars in data["characters"].items():
            if char_name in chars:
                return anime_key, rank
    return None, None


def get_char_abilities(char_name):
    """گرفتن Abilityهای یه کاراکتر از هر انیمه‌ای"""
    for anime_key, data in ANIME_REGISTRY.items():
        if char_name in data["abilities"]:
            return data["abilities"][char_name]
    return None


def get_anime_bosses(anime_key):
    """گرفتن باس‌های یه انیمه"""
    anime = ANIME_REGISTRY.get(anime_key)
    if not anime:
        return {}
    return anime["bosses"]


def get_anime_shop_abilities(anime_key):
    """گرفتن Abilityهای Shop یه انیمه"""
    anime = ANIME_REGISTRY.get(anime_key)
    if not anime:
        return {}
    return anime["shop_abilities"]