from functools import lru_cache
import requests


# نگاشت اسم‌های خاص به اسم‌های MyAnimeList
NAME_MAP = {
    # OPM
    "Saitama": "Saitama",
    "Genos": "Genos",
    "Garou": "Garou",
    "Boros": "Boros",
    "Tatsumaki": "Tatsumaki",
    "Blast": "Blast",
    "Sonic": "Sonic",
    "Metal Bat": "Metal Bat",
    "Mumen Rider": "Mumen Rider",
    "King": "King",
    "Fubuki": "Fubuki",
    "Bang": "Bang",
    "Bomb": "Bomb",
    "Suiryu": "Suiryu",
    "Amai Mask": "Amai Mask",
    "Gouketsu": "Gouketsu",
    "Orochi": "Orochi",
    "Psykos": "Psykos",
    "Zomnking": "Zombieman",
    "Pri-Pri Prisoner": "Puri-Puri Prisoner",
    "Wacsmann": "Wacsmann",
    "Blast": "Blast",

    # JJK
    "Gojo Satoru": "Satoru Gojo",
    "Yuta Okkotsu": "Yuta Okkotsu",
    "Kenjaku": "Kenjaku",
    "Yuki Tsukumo": "Yuki Tsukumo",
    "Suguru Geto": "Suguru Geto",
    "Toji Fushiguro": "Toji Fushiguro",
    "Kinji Hakari": "Kinji Hakari",
    "Hiromi Higuruma": "Hiromi Higuruma",
    "Hajime Kashimo": "Hajime Kashimo",
    "Yuji Modulo": "Yuji Itadori",
    "Uraume": "Uraume",
    "Yuji Itadori": "Yuji Itadori",
    "Megumi Fushiguro": "Megumi Fushiguro",
    "Maki Zenin": "Maki Zenin",
    "Kento Nanami": "Kento Nanami",
    "Mei Mei": "Mei Mei",
    "Aoi Todo": "Aoi Todo",
    "Choso": "Choso",
    "Naoya Zenin": "Naoya Zenin",
    "Nobara Kugisaki": "Nobara Kugisaki",
    "Toge Inumaki": "Toge Inumaki",
    "Kirara Hoshi": "Kirara Hoshi",
    "Hana Kurusu": "Hana Kurusu",

    # Bosses JJK
    "Sukuna Heian": "Ryomen Sukuna",
    "Sukuna Megumi": "Ryomen Sukuna",
    "Mahoraga": "Mahoraga",
    "Mahito": "Mahito",
    "Dabura": "Dabura",
}


@lru_cache(maxsize=500)
def get_anime_image(char_name):
    """گرفتن عکس کاراکتر از Jikan API (MyAnimeList)"""
    search_name = NAME_MAP.get(char_name, char_name)

    try:
        url = f"https://api.jikan.moe/v4/characters?q={search_name}&limit=1"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        data = response.json()
        if data.get("data") and len(data["data"]) > 0:
            img_url = data["data"][0]["images"]["jpg"]["image_url"]
            return img_url
    except Exception:
        pass

    return None
