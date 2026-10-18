# ============================================================
# MODES.PY — Castle Defense + Zombie Survival + Endless Tower
# ============================================================

import random
import time
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import (add_coins, get_coins, get_username, DB_NAME,
                      create_battle, get_battle, end_battle, spend_coins)
from characters import get_active_character
from battle import build_battle_message, finish_battle


# ============================================================
# HELPERS
# ============================================================
def format_num(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def get_survival_boss_hp(wave):
    base_hp = 10000
    growth = 1.047
    return min(1000000, int(base_hp * (growth ** (wave - 1))))


def get_mode_wave(user_id, mode):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    col = f"{mode}_wave"
    c.execute(f"SELECT {col} FROM characters WHERE user_id=? AND is_active=1", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 1


def set_mode_wave(user_id, mode, wave):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    col = f"{mode}_wave"
    c.execute(f"UPDATE characters SET {col}=? WHERE user_id=? AND is_active=1", (wave, user_id))
    conn.commit()
    conn.close()


def get_entry_cost(mode):
    return 10000


def get_reward_by_wave(wave):
    if wave <= 10:
        return 20000
    elif wave <= 20:
        return 40000
    elif wave <= 30:
        return 60000
    elif wave <= 40:
        return 80000
    elif wave <= 50:
        return 90000
    elif wave <= 60:
        return 110000
    elif wave <= 70:
        return 250000
    elif wave <= 80:
        return 350000
    elif wave <= 90:
        return 500000
    else:
        return 1000000


# ============================================================
# 🏰 CASTLE
# ============================================================
async def castle_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await modes_cmd(update, ctx)


async def castle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.answer("❌ کاراکتر فعال نداری. /start بزن.", show_alert=True)
        return

    if data == "modes_castle":
        wave = get_mode_wave(user_id, "castle")
        hp = get_survival_boss_hp(wave)
        cost = get_entry_cost("castle")
        reward = get_reward_by_wave(wave)
        kb = [
            [InlineKeyboardButton(f"⚔️ شروع نبرد (ورودی: {format_num(cost)} سکه)", callback_data=f"castle_start_{wave}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
        ]
        text = (
            "🏰 **دفاع از قلعه**\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌊 موج فعلی: {wave}/100\n"
            f"👹 HP دشمن: {format_num(hp)}\n"
            f"🎁 جایزه این موج: {format_num(reward)} سکه\n"
            f"💰 هزینه ورود: {format_num(cost)} سکه\n\n"
            "🎯 با هر برد، موج بالاتر میره!\n"
            "💀 اگه ببازی، از موج ۱ شروع می‌کنی."
        )
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("castle_start_"):
        wave = int(data.replace("castle_start_", ""))
        cost = get_entry_cost("castle")
        if not spend_coins(user_id, cost):
            await q.answer(f"❌ پولت کمه! نیاز: {format_num(cost)}", show_alert=True)
            return
        
        hp = get_survival_boss_hp(wave)
        boss_name = "Castle Survival"
        
        existing = get_battle(user_id)
        if existing: end_battle(existing["id"])
        
        create_battle(user_id, boss_name, char[5], hp)
        battle_data = get_battle(user_id)
        text = f"🏰 **قلعه - موج {wave}**\n\n" + build_battle_message(battle_data, char)
        
        from main import get_battle_kb
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id)))
        return


# ============================================================
# 🧟 ZOMBIE
# ============================================================
async def zombie_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await modes_cmd(update, ctx)


async def zombie_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.answer("❌ کاراکتر فعال نداری. /start بزن.", show_alert=True)
        return

    if data == "modes_zombie":
        wave = get_mode_wave(user_id, "zombie")
        hp = get_survival_boss_hp(wave)
        cost = get_entry_cost("zombie")
        reward = get_reward_by_wave(wave)
        kb = [
            [InlineKeyboardButton(f"⚔️ شروع نبرد (ورودی: {format_num(cost)} سکه)", callback_data=f"zombie_start_{wave}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
        ]
        text = (
            "🧟 **بقای زامبی**\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌊 موج فعلی: {wave}/100\n"
            f"🧟 HP زامبی: {format_num(hp)}\n"
            f"🎁 جایزه این موج: {format_num(reward)} سکه\n"
            f"💰 هزینه ورود: {format_num(cost)} سکه\n\n"
            "🎯 با هر برد، موج بالاتر میره!\n"
            "💀 اگه ببازی، از موج ۱ شروع می‌کنی."
        )
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("zombie_start_"):
        wave = int(data.replace("zombie_start_", ""))
        cost = get_entry_cost("zombie")
        if not spend_coins(user_id, cost):
            await q.answer(f"❌ پولت کمه! نیاز: {format_num(cost)}", show_alert=True)
            return
        
        hp = get_survival_boss_hp(wave)
        boss_name = "Zombie Survival"
        
        existing = get_battle(user_id)
        if existing: end_battle(existing["id"])
        
        create_battle(user_id, boss_name, char[5], hp)
        battle_data = get_battle(user_id)
        text = f"🧟 **زامبی - موج {wave}**\n\n" + build_battle_message(battle_data, char)
        
        from main import get_battle_kb
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id)))
        return


# ============================================================
# 🗼 TOWER
# ============================================================
async def tower_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await modes_cmd(update, ctx)


async def tower_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.answer("❌ کاراکتر فعال نداری. /start بزن.", show_alert=True)
        return

    if data == "modes_tower":
        wave = get_mode_wave(user_id, "tower")
        hp = get_survival_boss_hp(wave)
        cost = get_entry_cost("tower")
        reward = get_reward_by_wave(wave)
        kb = [
            [InlineKeyboardButton(f"⚔️ شروع نبرد (ورودی: {format_num(cost)} سکه)", callback_data=f"tower_start_{wave}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
        ]
        text = (
            "🗼 **برج بی‌پایان**\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌊 طبقه فعلی: {wave}/100\n"
            f"👹 HP دشمن: {format_num(hp)}\n"
            f"🎁 جایزه این طبقه: {format_num(reward)} سکه\n"
            f"💰 هزینه ورود: {format_num(cost)} سکه\n\n"
            "🎯 با هر برد، طبقه بالاتر میره!\n"
            "💀 اگه ببازی، از طبقه ۱ شروع می‌کنی."
        )
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("tower_start_"):
        wave = int(data.replace("tower_start_", ""))
        cost = get_entry_cost("tower")
        if not spend_coins(user_id, cost):
            await q.answer(f"❌ پولت کمه! نیاز: {format_num(cost)}", show_alert=True)
            return
        
        hp = get_survival_boss_hp(wave)
        boss_name = "Tower Survival"
        
        existing = get_battle(user_id)
        if existing: end_battle(existing["id"])
        
        create_battle(user_id, boss_name, char[5], hp)
        battle_data = get_battle(user_id)
        text = f"🗼 **برج - طبقه {wave}**\n\n" + build_battle_message(battle_data, char)
        
        from main import get_battle_kb
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id)))
        return


# ============================================================
# 🎮 MAIN MENU
# ============================================================
async def modes_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🏰 قلعه", callback_data="modes_castle")],
        [InlineKeyboardButton("🧟 زامبی", callback_data="modes_zombie")],
        [InlineKeyboardButton("🗼 برج", callback_data="modes_tower")],
    ]
    await update.message.reply_text("🎮 **مودهای بقا (Survival):**", reply_markup=InlineKeyboardMarkup(kb))


async def join_castle_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    pass