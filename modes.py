# ============================================================
# MODES.PY — Castle Defense + Zombie Survival + Endless Tower
# ============================================================

import random
import time
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import (add_coins, get_coins, get_username, get_user_buffs, 
                      create_battle, get_battle, end_battle, DB_NAME)
from characters import get_active_character
from battle import build_battle_message, get_boss_data


# ============================================================
# HELPERS
# ============================================================
def format_num(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def get_survival_boss_hp(wave):
    """محاسبه HP باس بر اساس موج (۱۰,۰۰۰ تا ۱,۰۰۰,۰۰۰)"""
    base_hp = 10000
    growth = 1.047  # ضریب رشد ۴.۷ درصدی
    return min(1000000, int(base_hp * (growth ** (wave - 1))))


def get_survival_wave(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT survival_wave FROM characters WHERE user_id=? AND is_active=1", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 1


def update_survival_wave(user_id, wave):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE characters SET survival_wave = ? WHERE user_id=? AND is_active=1", (user_id, wave))
    conn.commit()
    conn.close()


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
        wave = get_survival_wave(user_id)
        hp = get_survival_boss_hp(wave)
        kb = [
            [InlineKeyboardButton("⚔️ شروع نبرد", callback_data=f"castle_start_{wave}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
        ]
        text = (
            "🏰 **دفاع از قلعه**\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌊 موج فعلی: {wave}/100\n"
            f"👹 HP دشمن: {format_num(hp)}\n\n"
            "🎯 با هر برد، موج بالاتر میره!\n"
            "💀 اگه ببازی، از موج ۱ شروع می‌کنی."
        )
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("castle_start_"):
        wave = int(data.replace("castle_start_", ""))
        hp = get_survival_boss_hp(wave)
        boss_name = "Castle Survival"
        
        existing = get_battle(user_id)
        if existing: end_battle(existing["id"])
        
        create_battle(user_id, boss_name, char[5], hp)
        battle_data = get_battle(user_id)
        text = f"🏰 **قلعه - موج {wave}**\n\n" + build_battle_message(battle_data, char)
        
        # 🆕 استفاده از دکمه‌های نبرد (از main.py)
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
        wave = get_survival_wave(user_id)
        hp = get_survival_boss_hp(wave)
        kb = [
            [InlineKeyboardButton("⚔️ شروع نبرد", callback_data=f"zombie_start_{wave}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
        ]
        text = (
            "🧟 **بقای زامبی**\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌊 موج فعلی: {wave}/100\n"
            f"🧟 HP زامبی: {format_num(hp)}\n\n"
            "🎯 با هر برد، موج بالاتر میره!\n"
            "💀 اگه ببازی، از موج ۱ شروع می‌کنی."
        )
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("zombie_start_"):
        wave = int(data.replace("zombie_start_", ""))
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
        wave = get_survival_wave(user_id)
        hp = get_survival_boss_hp(wave)
        kb = [
            [InlineKeyboardButton("⚔️ شروع نبرد", callback_data=f"tower_start_{wave}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="modes_back")],
        ]
        text = (
            "🗼 **برج بی‌پایان**\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"🌊 طبقه فعلی: {wave}/100\n"
            f"👹 HP دشمن: {format_num(hp)}\n\n"
            "🎯 با هر برد، طبقه بالاتر میره!\n"
            "💀 اگه ببازی، از طبقه ۱ شروع می‌کنی."
        )
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("tower_start_"):
        wave = int(data.replace("tower_start_", ""))
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