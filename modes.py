# ============================================================
# MODES.PY — Castle Defense + Zombie Survival + Endless Tower
# ============================================================

import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import (add_coins, get_coins, get_battle, create_battle,
                      get_battle, update_battle, end_battle, get_active_character,
                      get_username, get_user_buffs)
from config import (ABILITIES_3, ABILITIES_JJK, ABILITIES_BLEACH, ABILITIES_OPM,
                    ABILITIES_AOT, ABILITIES_BLACKCLOVER, ABILITIES_BERSERK,
                    ABILITIES_DEMONSLAYER, ABILITIES_CHAINSAWMAN,
                    ABILITIES_NARUTO, ABILITIES_SDS)


# ============================================================
# SESSIONS
# ============================================================
CASTLE_SESSIONS = {}
ZOMBIE_SESSIONS = {}
TOWER_SESSIONS = {}


# ============================================================
# HELPERS
# ============================================================
def format_num(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def hp_bar(current, maximum, length=10):
    if maximum <= 0:
        return "💔 [" + "░" * length + "] ۰/۰"
    pct = current / maximum
    filled = int(pct * length)
    filled = max(0, min(length, filled))
    bar = "█" * filled + "░" * (length - filled)
    if pct > 0.6:
        icon = "❤️"
    elif pct > 0.3:
        icon = "🧡"
    else:
        icon = "💔"
    return f"{icon} [{bar}] {format_num(current)}/{format_num(maximum)}"


# ============================================================
# 🏰 CASTLE DEFENSE
# ============================================================
async def castle_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری. /start بزن.")
        return

    session_id = f"castle_{user_id}"
    CASTLE_SESSIONS[session_id] = {
        "host": user_id,
        "players": {user_id: {"name": get_username(user_id), "dmg": 0}},
        "wave": 0,
        "castle_hp": 5000,
        "castle_max_hp": 5000,
        "started": False,
        "last_wave_time": time.time(),
    }

    kb = [
        [InlineKeyboardButton("⚔️ شروع دفاع", callback_data=f"castle_start_{session_id}")],
        [InlineKeyboardButton("👥 دعوت دوستان", callback_data=f"castle_invite_{session_id}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
    ]
    text = (
        "🏰 **قلعه‌ی تو**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏰 HP قلعه: {format_num(5000)}/5000\n"
        f"👥 بازیکن‌ها: 1\n"
        f"🌊 موج: 0\n\n"
        "💡 هر ۱ ساعت و نیم، یه موج جدید میاد!\n"
        "🎯 دوستات رو دعوت کن تا با هم دفاع کنین.\n"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def castle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "modes_back":
        kb = [
            [InlineKeyboardButton("🏰 قلعه", callback_data="modes_castle")],
            [InlineKeyboardButton("🧟 زامبی", callback_data="modes_zombie")],
            [InlineKeyboardButton("🗼 برج", callback_data="modes_tower")],
        ]
        await q.edit_message_text("🎮 مودها:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("castle_start_"):
        session_id = data.replace("castle_start_", "")
        session = CASTLE_SESSIONS.get(session_id)
        if not session:
            await q.answer("❌ سشن پیدا نشد.", show_alert=True)
            return
        session["started"] = True
        session["wave"] = 1
        await castle_start_wave(q, session_id)
        return

    if data.startswith("castle_attack_"):
        session_id = data.replace("castle_attack_", "")
        session = CASTLE_SESSIONS.get(session_id)
        if not session:
            await q.answer("❌ سشن پیدا نشد.", show_alert=True)
            return
        await castle_player_attack(q, session_id, q.from_user.id)
        return

    if data.startswith("castle_invite_"):
        session_id = data.replace("castle_invite_", "")
        await q.message.reply_text(
            f"🔗 **لینک دعوت:**\n\n"
            f"دوستانت رو با این دستور دعوت کن:\n"
            f"`/joincastle {session_id}`\n\n"
            f"💰 هر کی بیاد، جایزه می‌گیره!"
        )
        return


async def join_castle_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /joincastle <session_id>")
        return
    session_id = ctx.args[0]
    session = CASTLE_SESSIONS.get(session_id)
    if not session:
        await update.message.reply_text("❌ سشن پیدا نشد.")
        return
    user_id = update.effective_user.id
    if user_id in session["players"]:
        await update.message.reply_text("✅ قبلاً تو این سشن هستی.")
        return
    session["players"][user_id] = {"name": get_username(user_id), "dmg": 0}
    await update.message.reply_text(
        f"✅ به قلعه‌ی {session['host']} پیوستی!\n"
        f"👥 تعداد: {len(session['players'])}"
    )


async def castle_start_wave(q, session_id):
    session = CASTLE_SESSIONS[session_id]
    wave = session["wave"]

    # HP دشمن هر موج +50%
    enemy_hp = int(1000 * (1.5 ** (wave - 1)))
    enemy_atk = int(50 * (1.4 ** (wave - 1)))

    session["enemy_hp"] = enemy_hp
    session["enemy_atk"] = enemy_atk
    session["enemy_max_hp"] = enemy_hp

    text = (
        f"🌊 **موج {wave}**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        f"👹 HP دشمن: {format_num(enemy_hp)}\n"
        f"⚔️ ATK دشمن: {format_num(enemy_atk)}\n\n"
        f"🏰 HP قلعه: {format_num(session['castle_hp'])}/{format_num(session['castle_max_hp'])}\n"
    )

    kb = []
    for pid, pdata in session["players"].items():
        kb.append([InlineKeyboardButton(
            f"⚔️ {pdata['name']} — حمله",
            callback_data=f"castle_attack_{session_id}_{pid}"
        )])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")])

    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def castle_player_attack(q, session_id, user_id):
    session = CASTLE_SESSIONS[session_id]
    if user_id not in session["players"]:
        await q.answer("❌ تو توی این سشن نیستی.", show_alert=True)
        return

    char = get_active_character(user_id)
    if not char:
        await q.answer("❌ کاراکتر فعال نداری.", show_alert=True)
        return

    atk = char[6]
    dmg = int(atk * random.uniform(0.9, 1.2))
    session["enemy_hp"] -= dmg
    session["players"][user_id]["dmg"] += dmg

    text = (
        f"⚔️ {get_username(user_id)} حمله کرد!\n"
        f"💥 {format_num(dmg)} آسیب\n\n"
    )

    if session["enemy_hp"] <= 0:
        # موج تموم شد
        wave = session["wave"]
        reward_pool = int(5000 * (1.6 ** (wave - 1)))

        # تقسیم جایزه بر اساس دمیج
        total_dmg = sum(p["dmg"] for p in session["players"].values())
        if total_dmg <= 0:
            total_dmg = 1

        reward_text = f"🏆 **موج {wave} تموم شد!**\n\n💰 جوایز:\n"
        for pid, pdata in session["players"].items():
            share = int(reward_pool * pdata["dmg"] / total_dmg)
            add_coins(pid, share)
            reward_text += f"👤 {pdata['name']}: +{format_num(share)} سکه\n"

        session["wave"] += 1
        session["last_wave_time"] = time.time()
        for p in session["players"].values():
            p["dmg"] = 0

        reward_text += f"\n⏳ موج بعدی: ۱ ساعت و نیم دیگه"

        kb = [[InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")]]
        try:
            await q.edit_message_text(reward_text, reply_markup=InlineKeyboardMarkup(kb))
        except Exception:
            await q.message.reply_text(reward_text, reply_markup=InlineKeyboardMarkup(kb))
        return

    # دشمن حمله می‌کنه
    enemy_dmg = session["enemy_atk"]
    session["castle_hp"] -= enemy_dmg

    if session["castle_hp"] <= 0:
        text += f"💥 دشمن قلعه رو نابود کرد!\n🏰 HP قلعه: 0"
        kb = [[InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")]]
        try:
            await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
        except Exception:
            await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    text += (
        f"👹 HP دشمن: {format_num(session['enemy_hp'])}/{format_num(session['enemy_max_hp'])}\n"
        f"🏰 HP قلعه: {format_num(session['castle_hp'])}/{format_num(session['castle_max_hp'])}\n\n"
        f"💥 دشمن حمله کرد! (-{format_num(enemy_dmg)})"
    )

    kb = []
    for pid, pdata in session["players"].items():
        kb.append([InlineKeyboardButton(
            f"⚔️ {pdata['name']} — حمله",
            callback_data=f"castle_attack_{session_id}_{pid}"
        )])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")])

    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
# ============================================================
# 🧟 ZOMBIE SURVIVAL
# ============================================================
async def zombie_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری. /start بزن.")
        return

    ZOMBIE_SESSIONS[user_id] = {
        "wave": 0,
        "hp": char[5],
        "max_hp": char[5],
        "char": char,
        "total_reward": 0,
        "active": False,
    }

    kb = [
        [InlineKeyboardButton("🧟 شروع موج ۱", callback_data=f"zombie_start_{user_id}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
    ]
    text = (
        "🧟 **زامبی مود (بقا)**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        f"❤️ HP: {format_num(char[5])}/{format_num(char[5])}\n"
        f"🌊 موج فعلی: 0\n"
        f"💰 جایزه‌ی کل: 0\n\n"
        "🎯 هر موج سخت‌تر، ولی جایزه بیشتر!\n"
        "🛑 سقف جایزه هر موج: 700,000\n"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def zombie_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "modes_back":
        kb = [
            [InlineKeyboardButton("🏰 قلعه", callback_data="modes_castle")],
            [InlineKeyboardButton("🧟 زامبی", callback_data="modes_zombie")],
            [InlineKeyboardButton("🗼 برج", callback_data="modes_tower")],
        ]
        await q.edit_message_text("🎮 مودها:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("zombie_start_"):
        user_id = int(data.replace("zombie_start_", ""))
        await zombie_start_wave(q, user_id)
        return

    if data.startswith("zombie_next_"):
        user_id = int(data.replace("zombie_next_", ""))
        await zombie_start_wave(q, user_id)
        return

    if data.startswith("zombie_attack_"):
        user_id = int(data.replace("zombie_attack_", ""))
        await zombie_attack(q, user_id)
        return

    if data.startswith("zombie_heal_"):
        user_id = int(data.replace("zombie_heal_", ""))
        await zombie_heal(q, user_id)
        return

    if data.startswith("zombie_flee_"):
        user_id = int(data.replace("zombie_flee_", ""))
        await zombie_flee(q, user_id)
        return


async def zombie_start_wave(q, user_id):
    session = ZOMBIE_SESSIONS.get(user_id)
    if not session:
        await q.answer("❌ سشن پیدا نشد.", show_alert=True)
        return

    session["wave"] += 1
    wave = session["wave"]

    # HP زامبی: هر موج +10%
    zombie_hp = int(1000 * (1.1 ** (wave - 1)))
    zombie_atk = int(50 * (1.1 ** (wave - 1)))

    session["zombie_hp"] = zombie_hp
    session["zombie_max_hp"] = zombie_hp
    session["zombie_atk"] = zombie_atk

    # جایزه: هر موج +10%، سقف 700,000
    base_reward = 5000
    reward = min(700000, int(base_reward * (1.1 ** (wave - 1))))
    session["wave_reward"] = reward

    text = (
        f"🧟 **موج {wave}**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        f"🧟 HP زامبی: {format_num(zombie_hp)}\n"
        f"⚔️ ATK زامبی: {format_num(zombie_atk)}\n"
        f"💰 جایزه: {format_num(reward)} سکه\n\n"
        f"❤️ HP تو: {format_num(session['hp'])}/{format_num(session['max_hp'])}\n"
    )

    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"zombie_attack_{user_id}")],
        [InlineKeyboardButton("💊 آیتم", callback_data=f"zombie_heal_{user_id}")],
        [InlineKeyboardButton("🏃 فرار", callback_data=f"zombie_flee_{user_id}")],
    ]

    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def zombie_attack(q, user_id):
    session = ZOMBIE_SESSIONS.get(user_id)
    if not session:
        await q.answer("❌ سشن پیدا نشد.", show_alert=True)
        return

    char = session["char"]
    atk = char[6]
    dmg = int(atk * random.uniform(0.9, 1.2))
    session["zombie_hp"] -= dmg

    text = f"⚔️ حمله! (-{format_num(dmg)} HP به زامبی)\n\n"

    if session["zombie_hp"] <= 0:
        # زامبی کشته شد
        reward = session["wave_reward"]
        add_coins(user_id, reward)
        session["total_reward"] += reward

        # ۴۰٪ HP برگرده
        heal = int(session["max_hp"] * 0.4)
        session["hp"] = min(session["max_hp"], session["hp"] + heal)

        text += (
            f"💀 زامبی کشته شد!\n"
            f"💰 +{format_num(reward)} سکه\n"
            f"💚 +{format_num(heal)} HP (۴۰٪)\n\n"
            f"❤️ HP تو: {format_num(session['hp'])}/{format_num(session['max_hp'])}\n"
            f"🌊 موج بعدی: {session['wave'] + 1}"
        )

        kb = [
            [InlineKeyboardButton("▶️ موج بعدی", callback_data=f"zombie_next_{user_id}")],
            [InlineKeyboardButton("🏃 فرار", callback_data=f"zombie_flee_{user_id}")],
        ]
        try:
            await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
        except Exception:
            await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    # زامبی حمله می‌کنه
    z_dmg = int(session["zombie_atk"] * random.uniform(0.9, 1.2))
    session["hp"] -= z_dmg

    if session["hp"] <= 0:
        text += (
            f"💥 زامبی حمله کرد! (-{format_num(z_dmg)} HP)\n\n"
            f"☠️ **مُردی!**\n"
            f"🌊 به موج {session['wave']} رسیدی\n"
            f"💰 کل جایزه: {format_num(session['total_reward'])}"
        )
        del ZOMBIE_SESSIONS[user_id]
        kb = [[InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")]]
        try:
            await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
        except Exception:
            await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    text += (
        f"🧟 HP زامبی: {format_num(session['zombie_hp'])}/{format_num(session['zombie_max_hp'])}\n"
        f"💥 زامبی حمله کرد! (-{format_num(z_dmg)} HP)\n"
        f"❤️ HP تو: {format_num(session['hp'])}/{format_num(session['max_hp'])}"
    )

    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"zombie_attack_{user_id}")],
        [InlineKeyboardButton("💊 آیتم", callback_data=f"zombie_heal_{user_id}")],
        [InlineKeyboardButton("🏃 فرار", callback_data=f"zombie_flee_{user_id}")],
    ]
    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def zombie_heal(q, user_id):
    session = ZOMBIE_SESSIONS.get(user_id)
    if not session:
        await q.answer("❌ سشن پیدا نشد.", show_alert=True)
        return

    # آیتم HP
    heal = int(session["max_hp"] * 0.3)
    session["hp"] = min(session["max_hp"], session["hp"] + heal)

    text = (
        f"💊 آیتم HP استفاده کردی!\n"
        f"💚 +{format_num(heal)} HP\n\n"
        f"❤️ HP تو: {format_num(session['hp'])}/{format_num(session['max_hp'])}\n"
        f"🧟 HP زامبی: {format_num(session['zombie_hp'])}"
    )
    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"zombie_attack_{user_id}")],
        [InlineKeyboardButton("🏃 فرار", callback_data=f"zombie_flee_{user_id}")],
    ]
    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def zombie_flee(q, user_id):
    session = ZOMBIE_SESSIONS.get(user_id)
    if not session:
        await q.answer("❌ سشن پیدا نشد.", show_alert=True)
        return
    wave = session["wave"]
    total = session["total_reward"]
    del ZOMBIE_SESSIONS[user_id]
    text = (
        f"🏃 فرار کردی!\n\n"
        f"🌊 به موج {wave} رسیدی\n"
        f"💰 کل جایزه: {format_num(total)} سکه"
    )
    kb = [[InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")]]
    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
# ============================================================
# 🗼 ENDLESS TOWER
# ============================================================
async def tower_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری. /start بزن.")
        return

    TOWER_SESSIONS[user_id] = {
        "floor": 0,
        "hp": char[5],
        "max_hp": char[5],
        "char": char,
        "total_reward": 0,
    }

    kb = [
        [InlineKeyboardButton("🗼 شروع طبقه ۱", callback_data=f"tower_start_{user_id}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
    ]
    text = (
        "🗼 **برج بی‌پایان**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "🎯 طبقه به طبقه بالا برو\n"
        "👹 هر طبقه: ۲ باس\n"
        "🌟 هر ۳ طبقه: باس کوچیک (+50K سکه)\n"
        "💰 هر طبقه: +100K سکه\n"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def tower_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "modes_back":
        kb = [
            [InlineKeyboardButton("🏰 قلعه", callback_data="modes_castle")],
            [InlineKeyboardButton("🧟 زامبی", callback_data="modes_zombie")],
            [InlineKeyboardButton("🗼 برج", callback_data="modes_tower")],
        ]
        await q.edit_message_text("🎮 مودها:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("tower_start_"):
        user_id = int(data.replace("tower_start_", ""))
        await tower_next_floor(q, user_id)
        return

    if data.startswith("tower_attack_"):
        user_id = int(data.replace("tower_attack_", ""))
        await tower_attack(q, user_id)
        return

    if data.startswith("tower_heal_"):
        user_id = int(data.replace("tower_heal_", ""))
        await tower_heal(q, user_id)
        return

    if data.startswith("tower_flee_"):
        user_id = int(data.replace("tower_flee_", ""))
        await tower_flee(q, user_id)
        return

    if data.startswith("tower_continue_"):
        user_id = int(data.replace("tower_continue_", ""))
        await tower_next_floor(q, user_id)
        return

    if data.startswith("tower_halfheal_"):
        user_id = int(data.replace("tower_halfheal_", ""))
        session = TOWER_SESSIONS.get(user_id)
        if session:
            heal = int(session["max_hp"] * 0.5)
            session["hp"] = min(session["max_hp"], session["hp"] + heal)
        await tower_next_floor(q, user_id)
        return


async def tower_next_floor(q, user_id):
    session = TOWER_SESSIONS.get(user_id)
    if not session:
        await q.answer("❌ سشن پیدا نشد.", show_alert=True)
        return

    session["floor"] += 1
    floor = session["floor"]

    is_mini_boss = (floor % 3 == 0)

    if is_mini_boss:
        enemy_hp = int(5000 * (1.3 ** (floor - 1)))
        enemy_atk = int(200 * (1.2 ** (floor - 1)))
        floor_reward = 50000
        label = "🌟 **باس کوچیک!**"
    else:
        enemy_hp = int(2000 * (1.2 ** (floor - 1)))
        enemy_atk = int(100 * (1.15 ** (floor - 1)))
        floor_reward = 100000
        label = "👹 **دشمن عادی**"

    session["enemy_hp"] = enemy_hp
    session["enemy_max_hp"] = enemy_hp
    session["enemy_atk"] = enemy_atk
    session["floor_reward"] = floor_reward
    session["is_mini_boss"] = is_mini_boss

    text = (
        f"{label}\n"
        f"🗼 **طبقه {floor}**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        f"👹 HP دشمن: {format_num(enemy_hp)}\n"
        f"⚔️ ATK دشمن: {format_num(enemy_atk)}\n"
        f"💰 جایزه: {format_num(floor_reward)} سکه\n\n"
        f"❤️ HP تو: {format_num(session['hp'])}/{format_num(session['max_hp'])}\n"
    )

    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"tower_attack_{user_id}")],
        [InlineKeyboardButton("💊 آیتم", callback_data=f"tower_heal_{user_id}")],
        [InlineKeyboardButton("🏃 فرار", callback_data=f"tower_flee_{user_id}")],
    ]

    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def tower_attack(q, user_id):
    session = TOWER_SESSIONS.get(user_id)
    if not session:
        await q.answer("❌ سشن پیدا نشد.", show_alert=True)
        return

    char = session["char"]
    atk = char[6]
    dmg = int(atk * random.uniform(0.9, 1.2))
    session["enemy_hp"] -= dmg

    text = f"⚔️ حمله! (-{format_num(dmg)} HP)\n\n"

    if session["enemy_hp"] <= 0:
        reward = session["floor_reward"]
        add_coins(user_id, reward)
        session["total_reward"] += reward

        if session["is_mini_boss"]:
            text += (
                f"🌟 **باس کوچیک کشته شد!**\n"
                f"💰 +{format_num(reward)} سکه\n\n"
                f"🎯 ادامه میدی یا ۵۰٪ HP برگردونی؟"
            )
            kb = [
                [InlineKeyboardButton("⚔️ ادامه میدم", callback_data=f"tower_continue_{user_id}")],
                [InlineKeyboardButton("💚 ۵۰٪ HP برگردون", callback_data=f"tower_halfheal_{user_id}")],
            ]
            try:
                await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
            except Exception:
                await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
            return
        else:
            heal = int(session["max_hp"] * 0.2)
            session["hp"] = min(session["max_hp"], session["hp"] + heal)
            text += (
                f"💀 دشمن کشته شد!\n"
                f"💰 +{format_num(reward)} سکه\n"
                f"💚 +{format_num(heal)} HP\n\n"
                f"❤️ HP تو: {format_num(session['hp'])}\n"
                f"🗼 طبقه بعدی: {session['floor'] + 1}"
            )
            kb = [
                [InlineKeyboardButton("▶️ طبقه بعدی", callback_data=f"tower_continue_{user_id}")],
                [InlineKeyboardButton("🏃 فرار", callback_data=f"tower_flee_{user_id}")],
            ]
            try:
                await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
            except Exception:
                await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
            return

    # دشمن حمله
    e_dmg = int(session["enemy_atk"] * random.uniform(0.9, 1.2))
    session["hp"] -= e_dmg

    if session["hp"] <= 0:
        text += (
            f"💥 دشمن حمله کرد! (-{format_num(e_dmg)})\n\n"
            f"☠️ **مُردی!**\n"
            f"🗼 به طبقه {session['floor']} رسیدی\n"
            f"💰 کل جایزه: {format_num(session['total_reward'])}"
        )
        del TOWER_SESSIONS[user_id]
        kb = [[InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")]]
        try:
            await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
        except Exception:
            await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    text += (
        f"👹 HP دشمن: {format_num(session['enemy_hp'])}/{format_num(session['enemy_max_hp'])}\n"
        f"💥 دشمن حمله کرد! (-{format_num(e_dmg)})\n"
        f"❤️ HP تو: {format_num(session['hp'])}/{format_num(session['max_hp'])}"
    )

    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"tower_attack_{user_id}")],
        [InlineKeyboardButton("💊 آیتم", callback_data=f"tower_heal_{user_id}")],
        [InlineKeyboardButton("🏃 فرار", callback_data=f"tower_flee_{user_id}")],
    ]
    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def tower_heal(q, user_id):
    session = TOWER_SESSIONS.get(user_id)
    if not session:
        await q.answer("❌ سشن پیدا نشد.", show_alert=True)
        return

    heal = int(session["max_hp"] * 0.3)
    session["hp"] = min(session["max_hp"], session["hp"] + heal)

    text = (
        f"💊 آیتم HP\n"
        f"💚 +{format_num(heal)} HP\n\n"
        f"❤️ HP تو: {format_num(session['hp'])}/{format_num(session['max_hp'])}\n"
        f"👹 HP دشمن: {format_num(session['enemy_hp'])}"
    )
    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"tower_attack_{user_id}")],
        [InlineKeyboardButton("🏃 فرار", callback_data=f"tower_flee_{user_id}")],
    ]
    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def tower_flee(q, user_id):
    session = TOWER_SESSIONS.get(user_id)
    if not session:
        await q.answer("❌ سشن پیدا نشد.", show_alert=True)
        return
    floor = session["floor"]
    total = session["total_reward"]
    del TOWER_SESSIONS[user_id]
    text = (
        f"🏃 فرار کردی!\n\n"
        f"🗼 به طبقه {floor} رسیدی\n"
        f"💰 کل جایزه: {format_num(total)} سکه"
    )
    kb = [[InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")]]
    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


# ============================================================
# 🎮 MAIN MODES MENU
# ============================================================
async def modes_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🏰 قلعه", callback_data="modes_castle")],
        [InlineKeyboardButton("🧟 زامبی", callback_data="modes_zombie")],
        [InlineKeyboardButton("🗼 برج", callback_data="modes_tower")],
    ]
    text = (
        "🎮 **مودهای جدید**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "🏰 قلعه — دفاع تیمی از قلعه\n"
        "🧟 زامبی — موج بی‌نهایت بقا\n"
        "🗼 برج — طبقه به طبقه بالا برو\n"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
