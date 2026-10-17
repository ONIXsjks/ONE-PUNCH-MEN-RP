# ============================================================
# ARISE.PY — سیستم Arise (فقط برای Sung Jin-Woo)
# ============================================================

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import (get_user_shadows, get_shadows_count,
                      get_shadows_atk_bonus, add_shadow, get_shadow_slots)
from characters import get_active_character


# ============================================================
# CONFIG
# ============================================================
MAX_SHADOWS = 50          # حداکثر سایه‌ها
ATK_PER_SHADOW = 25       # ATK هر سایه
ARISE_CHAR = "Sung Jin-Woo"   # فقط این کاراکتر


# ============================================================
# HELPERS
# ============================================================
def is_arise_char(char_name):
    """آیا این کاراکتر Arise داره؟"""
    return char_name == ARISE_CHAR


def get_shadow_from_boss(boss_name):
    """اسم سایه رو از اسم باس می‌سازه"""
    # مثال: "Kaido" → "Shadow Kaido"
    return f"Shadow {boss_name}"


# ============================================================
# 🎯 ARISE — بعد از کشتن باس
# ============================================================
def try_arise(user_id, char_name, boss_name):
    """
    بعد از کشتن باس، سعی می‌کنه یه سایه بسازه.
    فقط برای Sung Jin-Woo کار می‌کنه.
    
    Returns:
        (success: bool, message: str)
    """
    # فقط Jin-Woo
    if char_name != ARISE_CHAR:
        return False, ""

    # چک تعداد سایه‌ها
    current_count = get_shadows_count(user_id, char_name)
    if current_count >= MAX_SHADOWS:
        return False, ""

    # ساخت سایه
    shadow_name = get_shadow_from_boss(boss_name)
    add_shadow(user_id, char_name, shadow_name)
    new_count = current_count + 1

    return True, (
        f"\n\n💀 **ARISE!**\n"
        f"🌟 سایه‌ی جدید: **{shadow_name}**\n"
        f"⚔️ +{ATK_PER_SHADOW} ATK دائمی\n"
        f"📊 مجموع سایه‌ها: {new_count}/{MAX_SHADOWS}"
    )


# ============================================================
# 📊 نمایش لیست سایه‌ها
# ============================================================
async def show_shadows(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """نمایش لیست سایه‌های کاربر"""
    user_id = update.effective_user.id
    char = get_active_character(user_id)

    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری. /start بزن.")
        return

    char_name = char[2]

    # چک کاراکتر
    if not is_arise_char(char_name):
        await update.message.reply_text("❌ این کاراکتر Arise نداره!")
        return

    # گرفتن سایه‌ها
    shadows = get_user_shadows(user_id, char_name)

    if not shadows:
        await update.message.reply_text(
            "💀 **سایه‌های تو**\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "📭 هنوز هیچ سایه‌ای نداری!\n\n"
            "🎯 برای ساختن سایه، باس بکش.\n"
            "💡 هر باس = +۱ سایه (+۲۵ ATK)"
        )
        return

    # ساخت پیام
    total_atk = get_shadows_atk_bonus(user_id, char_name)

    text = "💀 **سایه‌های تو**\n"
    text += "━━━━━━━━━━━━━━━━━━━\n\n"
    text += f"📊 تعداد: {len(shadows)}/{MAX_SHADOWS}\n"
    text += f"⚔️ مجموع ATK: +{total_atk}\n\n"
    text += "**لیست سایه‌ها:**\n"

    for i, (sname, atk_bonus) in enumerate(shadows[:20], 1):
        text += f"{i}. {sname} (+{atk_bonus})\n"

    if len(shadows) > 20:
        text += f"\n... و {len(shadows) - 20} سایه دیگه"

    kb = [[InlineKeyboardButton("🔙 بازگشت", callback_data="shadows_back")]]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


# ============================================================
# 🎯 Callback — دکمه Arise توی فایت
# ============================================================
async def arise_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """
    وقتی کاربر روی دکمه «💀 Arise» توی فایت می‌زنه.
    لیست سایه‌ها رو نشون می‌ده.
    """
    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id
    char = get_active_character(user_id)

    if not char:
        await q.answer("❌ کاراکتر فعال نداری.", show_alert=True)
        return

    char_name = char[2]

    # چک کاراکتر
    if not is_arise_char(char_name):
        await q.answer("❌ این کاراکتر Arise نداره!", show_alert=True)
        return

    # گرفتن سایه‌ها
    shadows = get_user_shadows(user_id, char_name)

    if not shadows:
        await q.answer("❌ هنوز سایه‌ای نداری!", show_alert=True)
        return

    # ساخت پیام
    total_atk = get_shadows_atk_bonus(user_id, char_name)

    text = "💀 **سایه‌های تو**\n"
    text += "━━━━━━━━━━━━━━━━━━━\n\n"
    text += f"📊 تعداد: {len(shadows)}/{MAX_SHADOWS}\n"
    text += f"⚔️ مجموع ATK: +{total_atk}\n\n"
    text += "**لیست سایه‌ها:**\n"

    for i, (sname, atk_bonus) in enumerate(shadows[:20], 1):
        text += f"{i}. {sname} (+{atk_bonus})\n"

    if len(shadows) > 20:
        text += f"\n... و {len(shadows) - 20} سایه دیگه"

    kb = [[InlineKeyboardButton("🔙 بازگشت", callback_data="act_back")]]

    try:
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        try:
            await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
        except Exception as e:
            print(f"arise_callback error: {e}")


# ============================================================
# 🎯 Callback — بازگشت از لیست سایه‌ها
# ============================================================
async def shadows_back_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """بازگشت از لیست سایه‌ها به پروفایل"""
    q = update.callback_query
    await q.answer()

    # پاک کردن پیام یا برگشت به پروفایل
    try:
        await q.message.delete()
    except Exception:
        pass

    await q.message.reply_text("🏠 برای دیدن پروفایل: /profile")