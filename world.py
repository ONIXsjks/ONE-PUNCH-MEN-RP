import random
from database import (get_world_progress, update_world_region, unlock_world_region,
                      increment_world_stat, add_world_treasure, get_world_treasures,
                      get_unlocked_regions, get_current_region, add_coins,
                      get_coins, get_username, get_char_image)


# ============================================================
# REGIONS
# ============================================================
REGIONS = {
    "forest": {
        "name": "🌲 جنگل",
        "level_range": "60-100",
        "min_level": 60,
        "rewards": {"min": 20000, "max": 100000},
        "enemies": ["Small Shadow", "Cursed Spirit", "Shadow Wolf"],
        "boss": "Mahito",
        "unlock": None,
        "emoji": "🌲",
        "color": "🟢",
    },
    "desert": {
        "name": "🏜️ بیابان",
        "level_range": "100-150",
        "min_level": 100,
        "rewards": {"min": 100000, "max": 400000},
        "enemies": ["Demon Fish", "Sky King", "Cursed Worm"],
        "boss": "Mahoraga",
        "unlock": "forest",
        "emoji": "🏜️",
        "color": "🟡",
    },
    "mountain": {
        "name": "🏔️ کوه",
        "level_range": "150-200",
        "min_level": 150,
        "rewards": {"min": 400000, "max": 1000000},
        "enemies": ["Adjuchas", "Weak Vasto Lorde", "Hell Spider"],
        "boss": "Sukuna Megumi",
        "unlock": "desert",
        "emoji": "🏔️",
        "color": "🟠",
    },
    "volcano": {
        "name": "🌋 آتشفشان",
        "level_range": "200-300",
        "min_level": 200,
        "rewards": {"min": 1000000, "max": 2000000},
        "enemies": ["Menos Grande", "Tiger Beast", "Volcanic Titan"], # 🆕 Goku Lv2 حذف شد و به جاش Volcanic Titan اضافه شد
        "boss": "Sukuna Heian",
        "unlock": "mountain",
        "emoji": "🌋",
        "color": "🔴",
    },
    "dungeon": {
        "name": "🏰 سیاه‌چال",
        "level_range": "300+",
        "min_level": 300,
        "rewards": {"min": 2000000, "max": 4000000},
        "enemies": ["Yhwach (Soul King)", "Aizen (Final Form)", "Shadow God"], # 🆕 Goku Lv3 حذف شد و به جاش Shadow God اضافه شد
        "boss": "Saitama Phase 1",
        "unlock": "volcano",
        "emoji": "🏰",
        "color": "⚫",
    },
}


# ============================================================
# TREASURES
# ============================================================
TREASURES = {
    "legendary_sword": {
        "name": "🗡️ شمشیر افسانه‌ای",
        "effect": "ATK +500 (permanent)",
        "type": "atk",
        "value": 500,
        "chance": 3,
    },
    "hero_shield": {
        "name": "🛡️ سپر قهرمان",
        "effect": "DEF +300 (permanent)",
        "type": "def",
        "value": 300,
        "chance": 3,
    },
    "speed_wings": {
        "name": "💨 بال سرعت",
        "effect": "DODGE +20% (permanent)",
        "type": "dodge",
        "value": 20,
        "chance": 4,
    },
    "dragon_heart": {
        "name": "❤️ قلب اژدها",
        "effect": "HP +2000 (permanent)",
        "type": "hp",
        "value": 2000,
        "chance": 4,
    },
    "gold_bag": {
        "name": "💰 کیسه طلا",
        "effect": "50,000 سکه",
        "type": "coins",
        "value": 50000,
        "chance": 20,
    },
    "gift_box": {
        "name": "🎁 صندوق هدیه",
        "effect": "یه آیتم تصادفی",
        "type": "item",
        "value": 0,
        "chance": 15,
    },
    "mega_coins": {
        "name": "💎 سکه مگا",
        "effect": "200,000 سکه",
        "type": "coins",
        "value": 200000,
        "chance": 5,
    },
}


# ============================================================
# EXPLORE EVENTS
# ============================================================
EXPLORE_EVENTS = [
    {"type": "enemy", "chance": 30, "name": "👹 دشمن ظاهر شد!"},
    {"type": "treasure", "chance": 25, "name": "🎁 یه صندوق پیدا کردی!"},
    {"type": "mine", "chance": 15, "name": "💎 معدن پیدا کردی!"},
    {"type": "gate", "chance": 10, "name": "🚪 یه دروازه پیدا کردی!"},
    {"type": "riddle", "chance": 10, "name": "❓ یه معما پیدا کردی!"},
    {"type": "rare_boss", "chance": 5, "name": "🌟 باس کمیاب!"},
    {"type": "trap", "chance": 5, "name": "💀 تله!"},
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_region(region_key):
    return REGIONS.get(region_key)


def get_region_name(region_key):
    r = REGIONS.get(region_key)
    return r["name"] if r else "❓ ناشناس"


def random_explore_event():
    roll = random.randint(1, 100)
    cumulative = 0
    for event in EXPLORE_EVENTS:
        cumulative += event["chance"]
        if roll <= cumulative:
            return event["type"]
    return "enemy"


def random_treasure():
    roll = random.randint(1, 100)
    cumulative = 0
    for key, treasure in TREASURES.items():
        cumulative += treasure["chance"]
        if roll <= cumulative:
            return key, treasure
    return None, None


def random_reward(region_key):
    """جایزه کمتر (نصف شد)"""
    region = REGIONS.get(region_key)
    if not region:
        return 500
    r = region["rewards"]
    return random.randint(r["min"] // 2, r["max"] // 2)


def can_unlock_region(user_id, region_key):
    """چک میکنه کاربر میتونه این منطقه رو باز کنه (با چک لول)"""
    region = REGIONS.get(region_key)
    if not region:
        return False, "منطقه پیدا نشد"
    unlocked = get_unlocked_regions(user_id)
    if region_key in unlocked:
        return True, "باز است"
    try:
        from characters import get_active_character
        char = get_active_character(user_id)
        if not char:
            return False, "❌ کاراکتر فعال نداری!"
        char_level = char[4]
        min_level = region.get("min_level", 1)
        if char_level < min_level:
            return False, f"❌ برای این منطقه به لول {min_level} نیاز داری!\n📊 لول فعلی: {char_level}"
    except Exception as e:
        return False, f"❌ خطا: {e}"
    parent = region.get("unlock")
    if parent and parent not in unlocked:
        return False, f"❌ اول باید {get_region_name(parent)} رو باز کنی!"
    return True, "می‌تونی باز کنی"


def get_player_region_view(user_id):
    unlocked = get_unlocked_regions(user_id)
    current = get_current_region(user_id)

    text = "🗺️ دنیای آزاد\n"
    text += "━━━━━━━━━━━━━━━━━━━\n\n"

    for key, region in REGIONS.items():
        if key in unlocked:
            status = "🎯" if key == current else "✅"
        else:
            status = "🔒"
        text += f"{status} {region['name']} (Level {region['level_range']})\n"

    text += f"\n🎯 منطقه فعلی: {get_region_name(current)}"
    return text


def get_region_view(user_id, region_key):
    region = REGIONS.get(region_key)
    if not region:
        return "❌ منطقه پیدا نشد"

    text = f"{region['emoji']} {region['name']}\n"
    text += f"📊 Level: {region['level_range']}\n"
    text += f"💰 جایزه: {region['rewards']['min']:,} - {region['rewards']['max']:,}\n"
    text += "━━━━━━━━━━━━━━━━━━━\n\n"
    text += "👹 دشمن‌ها:\n"
    for e in region["enemies"][:3]:
        text += f"  • {e}\n"
    text += f"\n👑 باس: {region['boss']}"
    return text


def format_treasure(treasure_key, treasure):
    return f"{treasure['name']}\n📝 {treasure['effect']}"


def format_world_progress(user_id):
    progress = get_world_progress(user_id)
    if not progress:
        return "❌ اطلاعاتی نیست"

    total_explores = progress[3] or 0
    treasures = progress[4] or 0
    bosses = progress[5] or 0

    text = "📊 پیشرفت تو در دنیای آزاد\n"
    text += "━━━━━━━━━━━━━━━━━━━\n\n"
    text += f"🚶 کل گشتن‌ها: {total_explores:,}\n"
    text += f"🎁 گنج‌های پیدا شده: {treasures:,}\n"
    text += f"👑 باس‌های کشته شده: {bosses:,}\n"
    text += f"\n🗺️ مناطق باز شده: {len(get_unlocked_regions(user_id))}/5"

    return text


def format_treasures_list(user_id):
    treasures = get_world_treasures(user_id)
    if not treasures:
        return "📭 هنوز هیچ گنجی پیدا نکردی!"

    text = "🏆 گنج‌های تو:\n"
    text += "━━━━━━━━━━━━━━━━━━━\n\n"

    for name, date in treasures[-20:]:
        text += f"✨ {name}\n"

    if len(treasures) > 20:
        text += f"\n... و {len(treasures) - 20} گنج دیگه"

    return text