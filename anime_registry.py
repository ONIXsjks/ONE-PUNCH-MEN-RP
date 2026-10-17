# ============================================================
# ANIME REGISTRY — Central Registry for All 18 Animes
# ============================================================

# ============ OLD ANIMES ============
from opm_data import (
    CHARACTERS_OPM, ABILITIES_OPM, BOSSES_OPM
)
try:
    from opm_data import OPM_FODDER
except ImportError:
    OPM_FODDER = None

from jjk_data import (
    CHARACTERS_JJK, ABILITIES_JJK, BOSSES_JJK,
    FODDER_JJK, DOMAINS_JJK
)

from bleach_data import (
    CHARACTERS_BLEACH, ABILITIES_BLEACH, BLEACH_BOSSES,
    BLEACH_FODDER, BLEACH_BANKAI, BLEACH_ABILITIES_SHOP
)

# ============ 7 ANIMES (AOT, BC, Berserk, DS, CSM, Naruto, SDS) ============
from aot_data import (
    CHARACTERS_AOT, ABILITIES_AOT, AOT_BOSSES,
    AOT_FODDER, CHAR_PRICES_AOT
)

from blackclover_data import (
    CHARACTERS_BLACKCLOVER, ABILITIES_BLACKCLOVER,
    BLACKCLOVER_BOSSES, BLACKCLOVER_FODDER,
    CHAR_PRICES_BLACKCLOVER
)

from berserk_data import (
    CHARACTERS_BERSERK, ABILITIES_BERSERK,
    BERSERK_BOSSES, BERSERK_FODDER,
    CHAR_PRICES_BERSERK
)

from demonslayer_data import (
    CHARACTERS_DEMONSLAYER, ABILITIES_DEMONSLAYER,
    DEMONSLAYER_BOSSES, DEMONSLAYER_FODDER,
    CHAR_PRICES_DEMONSLAYER
)

from chainsawman_data import (
    CHARACTERS_CHAINSAWMAN, ABILITIES_CHAINSAWMAN,
    CHAINSAWMAN_BOSSES, CHAINSAWMAN_FODDER,
    CHAR_PRICES_CHAINSAWMAN
)

from naruto_data import (
    CHARACTERS_NARUTO, ABILITIES_NARUTO,
    NARUTO_BOSSES, NARUTO_FODDER,
    CHAR_PRICES_NARUTO
)

from sevendeadlysins_data import (
    CHARACTERS_SDS, ABILITIES_SDS,
    SDS_BOSSES, SDS_FODDER,
    CHAR_PRICES_SDS
)

# ============ 🆕 8 ANIMES NEW ============
from onepiece_data import (
    CHARACTERS_ONEPIECE, ABILITIES_ONEPIECE,
    ONEPIECE_BOSSES, ONEPIECE_FODDER,
    CHAR_PRICES_ONEPIECE
)

from dragonball_data import (
    CHARACTERS_DRAGONBALL, ABILITIES_DRAGONBALL,
    DRAGONBALL_BOSSES, DRAGONBALL_FODDER,
    CHAR_PRICES_DRAGONBALL
)

from hxh_data import (
    CHARACTERS_HXH, ABILITIES_HXH,
    HXH_BOSSES, HXH_FODDER,
    CHAR_PRICES_HXH
)

from sakamoto_data import (
    CHARACTERS_SAKAMOTO, ABILITIES_SAKAMOTO,
    SAKAMOTO_BOSSES, SAKAMOTO_FODDER,
    CHAR_PRICES_SAKAMOTO
)

from sololeveling_data import (
    CHARACTERS_SOLOLEVELING, ABILITIES_SOLOLEVELING,
    SOLOLEVELING_BOSSES, SOLOLEVELING_FODDER,
    CHAR_PRICES_SOLOLEVELING
)

from mushoku_data import (
    CHARACTERS_MUSHOKU, ABILITIES_MUSHOKU,
    MUSHOKU_BOSSES, MUSHOKU_FODDER,
    CHAR_PRICES_MUSHOKU
)

from codegeass_data import (
    CHARACTERS_CODEGEASS, ABILITIES_CODEGEASS,
    CODEGEASS_BOSSES, CODEGEASS_FODDER,
    CHAR_PRICES_CODEGEASS
)

from tokyoghoul_data import (
    CHARACTERS_TOKYOGHOUL, ABILITIES_TOKYOGHOUL,
    TOKYOGHOUL_BOSSES, TOKYOGHOUL_FODDER,
    CHAR_PRICES_TOKYOGHOUL
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
# REGISTRY — همه ۱۸ انیمه به صورت جداگانه
# ============================================================
ANIME_REGISTRY = {

    # ============ ۳ انیمه قدیمی ============
    "opm": {
        "name": "One Punch Man",
        "name_fa": "وان پانچ من",
        "emoji": "🥊",
        "characters": CHARACTERS_OPM,
        "abilities": ABILITIES_OPM,
        "bosses": BOSSES_OPM,
        "fodder": OPM_FODDER,
        "prices": {"S": 2000000, "A": 500000, "B": 150000, "C": 50000},
        "shop_abilities": {},
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

    # ============ ۷ انیمه اول ============
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
    "naruto": {
        "name": "Naruto",
        "name_fa": "ناروتو",
        "emoji": "🍥",
        "characters": CHARACTERS_NARUTO,
        "abilities": ABILITIES_NARUTO,
        "bosses": NARUTO_BOSSES,
        "fodder": NARUTO_FODDER,
        "prices": CHAR_PRICES_NARUTO,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
    "sds": {
        "name": "Seven Deadly Sins",
        "name_fa": "هفت گناه کبیره",
        "emoji": "⚔️",
        "characters": CHARACTERS_SDS,
        "abilities": ABILITIES_SDS,
        "bosses": SDS_BOSSES,
        "fodder": SDS_FODDER,
        "prices": CHAR_PRICES_SDS,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
}
# ============================================================
# 🆕 8 ANIMES NEW — اضافه به registry
# ============================================================
ANIME_REGISTRY.update({
    "onepiece": {
        "name": "One Piece",
        "name_fa": "وان پیس",
        "emoji": "🏴‍☠️",
        "characters": CHARACTERS_ONEPIECE,
        "abilities": ABILITIES_ONEPIECE,
        "bosses": ONEPIECE_BOSSES,
        "fodder": ONEPIECE_FODDER,
        "prices": CHAR_PRICES_ONEPIECE,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
    "dragonball": {
        "name": "Dragon Ball",
        "name_fa": "دراگون بال",
        "emoji": "🐉",
        "characters": CHARACTERS_DRAGONBALL,
        "abilities": ABILITIES_DRAGONBALL,
        "bosses": DRAGONBALL_BOSSES,
        "fodder": DRAGONBALL_FODDER,
        "prices": CHAR_PRICES_DRAGONBALL,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
    "hxh": {
        "name": "Hunter x Hunter",
        "name_fa": "هانتر × هانتر",
        "emoji": "🎯",
        "characters": CHARACTERS_HXH,
        "abilities": ABILITIES_HXH,
        "bosses": HXH_BOSSES,
        "fodder": HXH_FODDER,
        "prices": CHAR_PRICES_HXH,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
    "sakamoto": {
        "name": "Sakamoto Days",
        "name_fa": "ساکاموتو دیز",
        "emoji": "🍡",
        "characters": CHARACTERS_SAKAMOTO,
        "abilities": ABILITIES_SAKAMOTO,
        "bosses": SAKAMOTO_BOSSES,
        "fodder": SAKAMOTO_FODDER,
        "prices": CHAR_PRICES_SAKAMOTO,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
    "sololeveling": {
        "name": "Solo Leveling",
        "name_fa": "سولو لولینگ",
        "emoji": "🗡️",
        "characters": CHARACTERS_SOLOLEVELING,
        "abilities": ABILITIES_SOLOLEVELING,
        "bosses": SOLOLEVELING_BOSSES,
        "fodder": SOLOLEVELING_FODDER,
        "prices": CHAR_PRICES_SOLOLEVELING,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
    "mushoku": {
        "name": "Mushoku Tensei",
        "name_fa": "موشوکو تنسی",
        "emoji": "🌀",
        "characters": CHARACTERS_MUSHOKU,
        "abilities": ABILITIES_MUSHOKU,
        "bosses": MUSHOKU_BOSSES,
        "fodder": MUSHOKU_FODDER,
        "prices": CHAR_PRICES_MUSHOKU,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
    "codegeass": {
        "name": "Code Geass",
        "name_fa": "کد گیاس",
        "emoji": "♟️",
        "characters": CHARACTERS_CODEGEASS,
        "abilities": ABILITIES_CODEGEASS,
        "bosses": CODEGEASS_BOSSES,
        "fodder": CODEGEASS_FODDER,
        "prices": CHAR_PRICES_CODEGEASS,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
    "tokyoghoul": {
        "name": "Tokyo Ghoul",
        "name_fa": "توکیو غول",
        "emoji": "👁️",
        "characters": CHARACTERS_TOKYOGHOUL,
        "abilities": ABILITIES_TOKYOGHOUL,
        "bosses": TOKYOGHOUL_BOSSES,
        "fodder": TOKYOGHOUL_FODDER,
        "prices": CHAR_PRICES_TOKYOGHOUL,
        "shop_abilities": {},
        "has_domain": False,
        "has_bankai": False,
    },
})


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_anime(anime_key):
    return ANIME_REGISTRY.get(anime_key)


def get_anime_list():
    return [
        (key, data["emoji"], data["name"], data["name_fa"])
        for key, data in ANIME_REGISTRY.items()
    ]


def get_characters_by_anime(anime_key, rank):
    anime = ANIME_REGISTRY.get(anime_key)
    if not anime:
        return {}
    return anime["characters"].get(rank, {})


def get_char_price_by_anime(anime_key, rank):
    anime = ANIME_REGISTRY.get(anime_key)
    if not anime:
        return 0
    return anime["prices"].get(rank, 8000)


def find_char_anime(char_name):
    for anime_key, data in ANIME_REGISTRY.items():
        for rank, chars in data["characters"].items():
            if char_name in chars:
                return anime_key, rank
    return None, None


def get_char_abilities(char_name):
    for anime_key, data in ANIME_REGISTRY.items():
        if char_name in data["abilities"]:
            return data["abilities"][char_name]
    return None


def get_anime_bosses(anime_key):
    anime = ANIME_REGISTRY.get(anime_key)
    if not anime:
        return {}
    return anime["bosses"]


def get_anime_shop_abilities(anime_key):
    anime = ANIME_REGISTRY.get(anime_key)
    if not anime:
        return {}
    return anime["shop_abilities"]