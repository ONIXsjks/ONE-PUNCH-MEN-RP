import sqlite3
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, BotCommand
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          CallbackQueryHandler, MessageHandler, filters)
from config import *
from database import (init_db, get_user, add_coins, get_coins, spend_coins,
                      create_battle, get_battle, update_battle, end_battle,
                      get_abilities, get_items, use_item, get_username,
                      get_user_guild, get_top_guilds,
                      get_world_progress, update_world_region, unlock_world_region,
                      increment_world_stat, add_world_treasure, get_world_treasures,
                      get_unlocked_regions, get_current_region,
                      get_char_image, get_custom_quest_db,
                      get_user_buffs, remove_user_buff,
                      reset_all_players, get_total_users_count,
                      remove_user_ability,
                      get_user_shadows, get_shadows_count,
                      get_shadows_atk_bonus, add_shadow)
from characters import (create_character, get_user_characters,
                        get_active_character, set_active, buy_character)
from shop import buy_ability, buy_item, buy_buff, buy_slot, upgrade_character
from guild import (create_new_guild, join_existing_guild, leave_current_guild,
                   donate, try_upgrade_guild, kick_member, give_guild_xp,
                   format_guild, format_members, GUILD_CREATE_COST, GUILD_MIN_LEVEL)
from battle import (player_attack, player_defend, player_dodge,
                    player_ability, player_item, build_battle_message,
                    finish_battle, player_ability_v2,
                    player_ability_shop, player_buff_shop, goku_transform, luffy_transform,
                    get_awaken_name)
from multi_battle import (init_multi_table, create_multi_battle, get_multi_battle,
                          update_multi_battle, end_multi_battle, player_action,
                          finish_multi_battle, build_battle_view, get_player,
                          next_turn)
from quests import (init_quests_table, reset_daily_quests,
                    update_quest_progress, get_user_quests, claim_quest, QUESTS)
from leaderboard import get_top_by_coins, get_top_by_level, get_top_by_rank
from images import IMAGES, SHOP_IMAGE
from admin import (is_admin, is_owner, has_permission, get_user_perms,
                   add_admin, remove_admin, list_admins,
                   get_all_users, get_user_stats, give_coins, take_coins,
                   reset_user, ban_user, unban_user, is_banned,
                   give_character, reset_character,
                   set_help, get_help, get_all_help,
                   set_char_image, get_char_image,
                   add_force_channel, remove_force_channel, get_force_channels,
                   set_custom_quest, get_custom_quest, get_all_custom_quests,
                   PERMISSIONS_LIST)
# ============ OLD ANIMES ============
from jjk_data import (CHARACTERS_JJK, BOSSES_JJK, FODDER_JJK, DOMAINS_JJK, ABILITIES_JJK)
from bleach_data import (CHARACTERS_BLEACH, CHAR_PRICES_BLEACH, BLEACH_ABILITIES_SHOP, BLEACH_BANKAI, BLEACH_BOSSES, BLEACH_FODDER, ABILITIES_BLEACH)
from opm_data import (CHARACTERS_OPM, ABILITIES_OPM, BOSSES_OPM)
from jjk_stats import JJK_STATS
from bleach_stats import BLEACH_STATS
from opm_stats import OPM_STATS

# ============ 7 ANIMES ============
from aot_data import (CHARACTERS_AOT, CHAR_PRICES_AOT, ABILITIES_AOT, AOT_BOSSES, AOT_FODDER)
from blackclover_data import (CHARACTERS_BLACKCLOVER, CHAR_PRICES_BLACKCLOVER, ABILITIES_BLACKCLOVER, BLACKCLOVER_BOSSES, BLACKCLOVER_FODDER)
from berserk_data import (CHARACTERS_BERSERK, CHAR_PRICES_BERSERK, ABILITIES_BERSERK, BERSERK_BOSSES, BERSERK_FODDER)
from demonslayer_data import (CHARACTERS_DEMONSLAYER, CHAR_PRICES_DEMONSLAYER, ABILITIES_DEMONSLAYER, DEMONSLAYER_BOSSES, DEMONSLAYER_FODDER)
from chainsawman_data import (CHARACTERS_CHAINSAWMAN, CHAR_PRICES_CHAINSAWMAN, ABILITIES_CHAINSAWMAN, CHAINSAWMAN_BOSSES, CHAINSAWMAN_FODDER)
from naruto_data import (CHARACTERS_NARUTO, CHAR_PRICES_NARUTO, ABILITIES_NARUTO, NARUTO_BOSSES, NARUTO_FODDER)
from sevendeadlysins_data import (CHARACTERS_SDS, CHAR_PRICES_SDS, ABILITIES_SDS, SDS_BOSSES, SDS_FODDER)

from aot_stats import AOT_STATS
from blackclover_stats import BLACKCLOVER_STATS
from berserk_stats import BERSERK_STATS
from demonslayer_stats import DEMONSLAYER_STATS
from chainsawman_stats import CHAINSAWMAN_STATS
from naruto_stats import NARUTO_STATS
from sevendeadlysins_stats import SDS_STATS

# ============ 8 ANIMES NEW ============
from onepiece_data import (CHARACTERS_ONEPIECE, CHAR_PRICES_ONEPIECE, ABILITIES_ONEPIECE, ONEPIECE_BOSSES, ONEPIECE_FODDER)
from dragonball_data import (CHARACTERS_DRAGONBALL, CHAR_PRICES_DRAGONBALL, ABILITIES_DRAGONBALL, DRAGONBALL_BOSSES, DRAGONBALL_FODDER)
from hxh_data import (CHARACTERS_HXH, CHAR_PRICES_HXH, ABILITIES_HXH, HXH_BOSSES, HXH_FODDER)
from sakamoto_data import (CHARACTERS_SAKAMOTO, CHAR_PRICES_SAKAMOTO, ABILITIES_SAKAMOTO, SAKAMOTO_BOSSES, SAKAMOTO_FODDER)
from sololeveling_data import (CHARACTERS_SOLOLEVELING, CHAR_PRICES_SOLOLEVELING, ABILITIES_SOLOLEVELING, SOLOLEVELING_BOSSES, SOLOLEVELING_FODDER)
from mushoku_data import (CHARACTERS_MUSHOKU, CHAR_PRICES_MUSHOKU, ABILITIES_MUSHOKU, MUSHOKU_BOSSES, MUSHOKU_FODDER)
from codegeass_data import (CHARACTERS_CODEGEASS, CHAR_PRICES_CODEGEASS, ABILITIES_CODEGEASS, CODEGEASS_BOSSES, CODEGEASS_FODDER)
from tokyoghoul_data import (CHARACTERS_TOKYOGHOUL, CHAR_PRICES_TOKYOGHOUL, ABILITIES_TOKYOGHOUL, TOKYOGHOUL_BOSSES, TOKYOGHOUL_FODDER)

from onepiece_stats import ONEPIECE_STATS
from dragonball_stats import DRAGONBALL_STATS
from hxh_stats import HXH_STATS
from sakamoto_stats import SAKAMOTO_STATS
from sololeveling_stats import SOLOLEVELING_STATS
from mushoku_stats import MUSHOKU_STATS
from codegeass_stats import CODEGEASS_STATS
from tokyoghoul_stats import TOKYOGHOUL_STATS

from world import (REGIONS, TREASURES, get_region, get_region_name, random_explore_event, random_treasure, random_reward, can_unlock_region, get_player_region_view, get_region_view, format_treasure, format_world_progress, format_treasures_list)
from anime_registry import (ANIME_REGISTRY, get_anime, get_anime_list, get_characters_by_anime, get_char_price_by_anime, find_char_anime, get_anime_bosses, get_anime_shop_abilities)
from modes import (modes_cmd, castle_cmd, castle_callback, zombie_cmd, zombie_callback, tower_cmd, tower_callback)
from arise import (try_arise, show_shadows, arise_callback, shadows_back_callback, MAX_SHADOWS, ATK_PER_SHADOW)
from gift import send_gift, get_gift_history, get_top_givers

PVP_SESSIONS = {}
TEAM_SESSIONS = {}
COOP_SESSIONS = {}
def get_all_stats(char_name, rank):
    for stats_dict in [JJK_STATS, BLEACH_STATS, OPM_STATS, AOT_STATS, BLACKCLOVER_STATS, BERSERK_STATS,
                       DEMONSLAYER_STATS, CHAINSAWMAN_STATS, NARUTO_STATS, SDS_STATS, ONEPIECE_STATS,
                       DRAGONBALL_STATS, HXH_STATS, SAKAMOTO_STATS, SOLOLEVELING_STATS, MUSHOKU_STATS,
                       CODEGEASS_STATS, TOKYOGHOUL_STATS]:
        if char_name in stats_dict:
            return stats_dict[char_name]
    return RANK_STATS.get(rank, RANK_STATS["C"])

def get_char_price(char_name, rank):
    stats = get_all_stats(char_name, rank)
    if "price" in stats:
        return stats["price"]
    return CHAR_PRICES.get(rank, 8000)

def get_character_abilities(char_name):
    for data in [ABILITIES_JJK, ABILITIES_BLEACH, ABILITIES_OPM, ABILITIES_AOT, ABILITIES_BLACKCLOVER,
                 ABILITIES_BERSERK, ABILITIES_DEMONSLAYER, ABILITIES_CHAINSAWMAN, ABILITIES_NARUTO,
                 ABILITIES_SDS, ABILITIES_ONEPIECE, ABILITIES_DRAGONBALL, ABILITIES_HXH, ABILITIES_SAKAMOTO,
                 ABILITIES_SOLOLEVELING, ABILITIES_MUSHOKU, ABILITIES_CODEGEASS, ABILITIES_TOKYOGHOUL]:
        if char_name in data:
            return data[char_name]
    return None

def get_character_domain_bankai(char_name):
    return char_name in DOMAINS_JJK, char_name in BLEACH_BANKAI

def get_battle_kb(char_name=None, user_id=None, battle=None):
    kb = []
    if char_name:
        if battle:
            domain_active = battle.get("domain_active", 0) == 1
            bankai_used = battle.get("bankai_used", 0) >= 1
            geass_used = battle.get("geass_used", 0) >= 1
            awakening_active = domain_active or bankai_used or geass_used
            
            if awakening_active:
                if battle.get("awaken_blue_used", 0) == 0:
                    kb.append([InlineKeyboardButton(f"🔵 {get_awaken_name(char_name, 'blue')} (۳۰)", callback_data="act_awaken_blue")])
                if battle.get("awaken_red_used", 0) == 0:
                    kb.append([InlineKeyboardButton(f"🔴 {get_awaken_name(char_name, 'red')} (۳۵)", callback_data="act_awaken_red")])
                if battle.get("awaken_purple_used", 0) == 0:
                    kb.append([InlineKeyboardButton(f"🟣 {get_awaken_name(char_name, 'purple')} (۴۰)", callback_data="act_awaken_purple")])
            else:
                abs_data = get_character_abilities(char_name)
                if abs_data:
                    ab1 = abs_data.get("ability_1", {}).get("name", "Ability 1")
                    ab2 = abs_data.get("ability_2", {}).get("name", "Ability 2")
                    ab3 = abs_data.get("ability_3", {}).get("name", "Ultimate")
                    kb.append([InlineKeyboardButton(f"🔵 {ab1}", callback_data="act_ability_1")])
                    kb.append([InlineKeyboardButton(f"🔴 {ab2}", callback_data="act_ability_2")])
                    kb.append([InlineKeyboardButton(f"🟣 {ab3} (۱ بار)", callback_data="act_ability_3")])
    
    kb.append([InlineKeyboardButton("⚔️ حمله", callback_data="act_attack"), InlineKeyboardButton("🛡️ دفاع", callback_data="act_defend")])
    kb.append([InlineKeyboardButton("💨 جاخالی", callback_data="act_dodge"), InlineKeyboardButton("💊 آیتم", callback_data="act_item")])
    kb.append([InlineKeyboardButton("🔥 Ability", callback_data="act_shop_ability"), InlineKeyboardButton("✨ باف", callback_data="act_shop_buff")])
    
    if char_name and battle:
        has_domain, has_bankai = get_character_domain_bankai(char_name)
        if has_domain and battle.get("domain_used", 0) == 0: 
            kb.append([InlineKeyboardButton("🌀 گسترش قلمرو", callback_data="act_domain")])
        if has_bankai and battle.get("bankai_used", 0) == 0: 
            kb.append([InlineKeyboardButton("⚔️ Bankai", callback_data="act_bankai")])
        if char_name == "Sung Jin-Woo": 
            kb.append([InlineKeyboardButton("💀 Arise", callback_data="act_arise")])
        if char_name == "Son Goku": 
            kb.append([InlineKeyboardButton("🐉 فرم بعدی (Transform)", callback_data="act_goku_form")])
        if char_name == "Monkey D. Luffy": 
            kb.append([InlineKeyboardButton("🏴‍☠️ فرم بعدی (Gear)", callback_data="act_luffy_form")])
        if char_name in ABILITIES_CODEGEASS and battle.get("geass_used", 0) == 0: 
            kb.append([InlineKeyboardButton("👁️ گیاس دوم", callback_data="act_ultimate_geass")])
        
        if not has_domain and not has_bankai and char_name not in ABILITIES_CODEGEASS and not awakening_active:
            kb.append([InlineKeyboardButton("🔥 اویکن (Awakening)", callback_data="act_awakening")])

    kb.append([InlineKeyboardButton("🏳️ تسلیم", callback_data="act_surrender")])
    return kb

def get_multi_kb(session_id, char_name=None, current_turn=None, user_id=None):
    kb = []
    if char_name:
        abs_data = get_character_abilities(char_name)
        if abs_data:
            ab1 = abs_data.get("ability_1", {}).get("name", "Ability 1")
            ab2 = abs_data.get("ability_2", {}).get("name", "Ability 2")
            ab3 = abs_data.get("ability_3", {}).get("name", "Ultimate")
            kb.append([InlineKeyboardButton(f"🔵 {ab1}", callback_data=f"mb_ab1_{session_id}")])
            kb.append([InlineKeyboardButton(f"🔴 {ab2}", callback_data=f"mb_ab2_{session_id}")])
            kb.append([InlineKeyboardButton(f"🟣 {ab3} (۱ بار)", callback_data=f"mb_ab3_{session_id}")])
    kb.append([InlineKeyboardButton("⚔️ حمله", callback_data=f"mb_attack_{session_id}"), InlineKeyboardButton("🛡️ دفاع", callback_data=f"mb_defend_{session_id}")])
    kb.append([InlineKeyboardButton("💨 جاخالی", callback_data=f"mb_dodge_{session_id}"), InlineKeyboardButton("💊 آیتم", callback_data=f"mb_item_{session_id}")])
    if char_name:
        has_domain, has_bankai = get_character_domain_bankai(char_name)
        if has_domain: kb.append([InlineKeyboardButton("🌀 Domain", callback_data=f"mb_domain_{session_id}")])
        if has_bankai: kb.append([InlineKeyboardButton("⚔️ Bankai", callback_data=f"mb_bankai_{session_id}")])
        if char_name == "Sung Jin-Woo": kb.append([InlineKeyboardButton("💀 Arise", callback_data=f"mb_arise_{session_id}")])
    kb.append([InlineKeyboardButton("🏳️ تسلیم", callback_data=f"mb_surrender_{session_id}")])
    return kb

def save_menu_owner(ctx, menu_name, user_id):
    ctx.user_data[f"owner_{menu_name}"] = user_id

async def check_menu_owner(q, ctx, menu_name):
    if ctx.user_data.get(f"owner_{menu_name}") != q.from_user.id:
        await q.answer("❌ این منو برای شما نیست! لطفاً خودتان دستور مربوطه را بزنید.", show_alert=True)
        return False
    return True
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id, user.username)
    reset_daily_quests(user.id)
    chars = get_user_characters(user.id)
    if not chars:
        kb = []
        for c_name, c_title in CHARACTERS["C"].items():
            kb.append([InlineKeyboardButton(f"{c_name} — {c_title}", callback_data=f"first_{c_name}")])
        await update.message.reply_text("🎮 به BANG BANG RP خوش اومدی!\n\nیه کاراکتر رایگان انتخاب کن (C Rank):", reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text("Welcome back! /help")

async def first_char_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    char_name = q.data.replace("first_", "")
    user_id = q.from_user.id
    if get_user_characters(user_id):
        await q.message.reply_text("❌ تو قبلاً یه کاراکتر انتخاب کردی!")
        return
    if char_name not in CHARACTERS["C"]:
        await q.message.reply_text("❌ کاراکتر نامعتبر.")
        return
    create_character(user_id, char_name, "C")
    chars = get_user_characters(user_id)
    set_active(user_id, chars[0][0])
    await q.message.reply_text(f"✅ کاراکتر {char_name} (C Rank) انتخاب شد!\n\n/profile\n/shop\n/battle\n/help")

async def profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری. /start بزن.")
        return
    user = get_user(user_id)
    username = user[1] if user and user[1] else "ناشناس"
    char_name, rank, level, hp, atk, dfn, dodge, slots = char[2], char[3], char[4], char[5], char[6], char[7], char[8], char[9]
    has_domain, has_bankai = get_character_domain_bankai(char_name)
    domain_name = f" - {DOMAINS_JJK[char_name]['name']}" if has_domain else ""
    bankai_name = f" - {BLEACH_BANKAI[char_name]['name']}" if has_bankai else ""
    
    abs_data = get_character_abilities(char_name)
    abs_text = f"🔵 {abs_data.get('ability_1', {}).get('name', '—')}\n🔴 {abs_data.get('ability_2', {}).get('name', '—')}\n🟣 {abs_data.get('ability_3', {}).get('name', '—')} (۱ بار)\n" if abs_data else "❌ Ability تعریف نشده\n"
    
    arise_text = ""
    if char_name == "Sung Jin-Woo":
        arise_text = f"\n💀 **Arise:** {get_shadows_count(user_id, char_name)}/{MAX_SHADOWS} (+{get_shadows_atk_bonus(user_id, char_name)} ATK)\n"
    
    energy_text = ""
    try:
        conn = sqlite3.connect(DB_NAME); c = conn.cursor()
        c.execute("SELECT naruto_chakra, max_naruto_chakra, dragonball_ki, max_dragonball_ki, sololeveling_mana, max_sololeveling_mana, hxh_nen, max_hxh_nen, mushoku_mana, max_mushoku_mana, tokyoghoul_rc, max_tokyoghoul_rc, sds_magic, max_sds_magic, sakamoto_stamina, max_sakamoto_stamina, aot_titan, max_aot_titan, blackclover_mana, max_blackclover_mana, berserk_bloodlust, max_berserk_bloodlust, demonslayer_breath, max_demonslayer_breath, chainsawman_blood, max_chainsawman_blood, opm_power, max_opm_power FROM characters WHERE user_id=? AND is_active=1", (user_id,)); row = c.fetchone(); conn.close()
        if row:
            if char_name in ABILITIES_NARUTO: energy_text += f"\n🍥 **چاکرا:** {row[0]}/{row[1]}"
            elif char_name in ABILITIES_DRAGONBALL: energy_text += f"\n🐉 **کی:** {row[2]}/{row[3]}"
            elif char_name in ABILITIES_SOLOLEVELING: energy_text += f"\n🗡️ **مانا:** {row[4]}/{row[5]}"
            elif char_name in ABILITIES_HXH: energy_text += f"\n🎯 **نن:** {row[6]}/{row[7]}"
            elif char_name in ABILITIES_MUSHOKU: energy_text += f"\n🌀 **مانا:** {row[8]}/{row[9]}"
            elif char_name in ABILITIES_TOKYOGHOUL: energy_text += f"\n👁️ **RC:** {row[10]}/{row[11]}"
            elif char_name in ABILITIES_SDS: energy_text += f"\n⚔️ **جادو:** {row[12]}/{row[13]}"
            elif char_name in ABILITIES_SAKAMOTO: energy_text += f"\n🍡 **استقامت:** {row[14]}/{row[15]}"
            elif char_name in ABILITIES_AOT: energy_text += f"\n⚡ **قدرت تایتان:** {row[16]}/{row[17]}"
            elif char_name in ABILITIES_BLACKCLOVER: energy_text += f"\n🍀 **مانا:** {row[18]}/{row[19]}"
            elif char_name in ABILITIES_BERSERK: energy_text += f"\n🩸 **خون‌آشامی:** {row[20]}/{row[21]}"
            elif char_name in ABILITIES_DEMONSLAYER: energy_text += f"\n🌸 **نفس:** {row[22]}/{row[23]}"
            elif char_name in ABILITIES_CHAINSAWMAN: energy_text += f"\n🪚 **خون:** {row[24]}/{row[25]}"
            elif char_name in ABILITIES_OPM: energy_text += f"\n💪 **قدرت مطلق:** {row[26]}/{row[27]}"
    except Exception: pass
    
    text = (
        f"╔══════════════════════════╗\n║      👤 @{username[:14].center(14)} ║\n╚══════════════════════════╝\n\n"
        f"╭───── 🎭 کاراکتر فعال ─────╮\n│ 🦸 {char_name[:18].ljust(18)} │\n│ ⭐ Rank: {rank.ljust(14)} │\n│ 📊 Level: {str(level).ljust(13)} │\n╰────────────────────────────╯\n\n"
        f"⚔️ آمار کاراکتر:\n├ ❤️ HP: {hp:,}\n├ ⚔️ ATK: {atk:,}\n├ 🛡️ DEF: {dfn:,}\n├ 💨 DODGE: {dodge}%\n└ 🎰 Slots: {slots}\n\n"
        f"🔥 Ability ها:\n{abs_text}\n"
        f"🌀 Domain: {'✅' if has_domain else '❌'}{domain_name}\n⚔️ Bankai: {'✅' if has_bankai else '❌'}{bankai_name}\n"
        f"{arise_text}{energy_text}\n💰 سکه: {get_coins(user_id):,}\n━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    kb = [
        [InlineKeyboardButton("🎭 تغییر کاراکتر", callback_data="prof_select"), InlineKeyboardButton("📜 کوئست‌ها", callback_data="prof_quests")],
        [InlineKeyboardButton("🏆 لیدربورد", callback_data="prof_lb"), InlineKeyboardButton("🎁 هدیه", callback_data="prof_gift")],
        [InlineKeyboardButton("⚔️ نبرد سریع", callback_data="prof_battle"), InlineKeyboardButton("🏰 کلن", callback_data="prof_guild")],
        [InlineKeyboardButton("🗺️ دنیای آزاد", callback_data="prof_world")],
    ]
    
    img = get_char_image(char_name)
    if img:
        try:
            await update.message.reply_photo(photo=img, caption=text, reply_markup=InlineKeyboardMarkup(kb))
            return
        except Exception: pass
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
async def smart_upgrade(update, ctx, energy_col, max_col, energy_name, abilities_dict):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char or char[2] not in abilities_dict:
        return await update.message.reply_text(f"❌ این کاراکتر {energy_name} نداره!")
    amount = 10
    if ctx.args:
        try: amount = int(ctx.args[0])
        except ValueError: return await update.message.reply_text("❌ عدد معتبر بده!")
    if amount <= 0: return await update.message.reply_text("❌ عدد باید مثبت باشه!")
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute(f"SELECT {energy_col}, {max_col} FROM characters WHERE user_id=? AND is_active=1", (user_id,))
    row = c.fetchone()
    if not row: conn.close(); return
    current_energy, current_max = row[0], row[1]
    if current_max >= 500:
        conn.close()
        return await update.message.reply_text(f"❌ {energy_name} به حداکثر (۵۰۰) رسیده!")
    from config import get_energy_upgrade_cost
    total_cost = 0; temp_level = current_max
    for i in range(amount):
        if temp_level >= 500: break
        total_cost += get_energy_upgrade_cost(temp_level)
        temp_level += 10
    if get_coins(user_id) < total_cost:
        conn.close()
        return await update.message.reply_text(f"❌ پول کافی نداری!\n💰 هزینه: {total_cost:,}\n💵 موجودی: {get_coins(user_id):,}")
    if not spend_coins(user_id, total_cost):
        conn.close(); return await update.message.reply_text("❌ خطا در پرداخت!")
    new_max = min(500, current_max + (amount * 10))
    diff = new_max - current_max
    c.execute(f"UPDATE characters SET {max_col} = {max_col} + ?, {energy_col} = {energy_col} + ? WHERE user_id=? AND is_active=1", (diff, diff, user_id))
    conn.commit(); conn.close()
    await update.message.reply_text(f"✅ {energy_name} +{diff} (حداکثر جدید: {new_max})\n💰 هزینه: {total_cost:,}")

async def upgrade_ce(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "cursed_energy", "max_cursed_energy", "انرژی نفرینی", ABILITIES_JJK)
async def upgrade_rei(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "reiatsu", "max_reiatsu", "ریستو", ABILITIES_BLEACH)
async def upgrade_geass(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "geass_power", "max_geass_power", "گیاس", ABILITIES_CODEGEASS)
async def upgrade_haki(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "haki", "max_haki", "هاکی", ABILITIES_ONEPIECE)
async def upgrade_chakra(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "naruto_chakra", "max_naruto_chakra", "چاکرا", ABILITIES_NARUTO)
async def upgrade_ki(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "dragonball_ki", "max_dragonball_ki", "کی", ABILITIES_DRAGONBALL)
async def upgrade_mana(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "sololeveling_mana", "max_sololeveling_mana", "مانا", ABILITIES_SOLOLEVELING)
async def upgrade_nen(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "hxh_nen", "max_hxh_nen", "نن", ABILITIES_HXH)
async def upgrade_mushoku_mana(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "mushoku_mana", "max_mushoku_mana", "مانا", ABILITIES_MUSHOKU)
async def upgrade_rc(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "tokyoghoul_rc", "max_tokyoghoul_rc", "RC", ABILITIES_TOKYOGHOUL)
async def upgrade_magic(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "sds_magic", "max_sds_magic", "جادو", ABILITIES_SDS)
async def upgrade_stamina(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "sakamoto_stamina", "max_sakamoto_stamina", "استقامت", ABILITIES_SAKAMOTO)
async def upgrade_titan(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "aot_titan", "max_aot_titan", "قدرت تایتان", ABILITIES_AOT)
async def upgrade_bcmana(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "blackclover_mana", "max_blackclover_mana", "مانا", ABILITIES_BLACKCLOVER)
async def upgrade_bloodlust(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "berserk_bloodlust", "max_berserk_bloodlust", "خون‌آشامی", ABILITIES_BERSERK)
async def upgrade_breath(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "demonslayer_breath", "max_demonslayer_breath", "نفس", ABILITIES_DEMONSLAYER)
async def upgrade_blood(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "chainsawman_blood", "max_chainsawman_blood", "خون", ABILITIES_CHAINSAWMAN)
async def upgrade_opm(update: Update, ctx: ContextTypes.DEFAULT_TYPE): await smart_upgrade(update, ctx, "opm_power", "max_opm_power", "قدرت مطلق", ABILITIES_OPM)
async def profile_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    user_id = q.from_user.id
    if data == "prof_select":
        chars = get_user_characters(user_id)
        if not chars:
            await q.message.reply_text("❌ کاراکتری نداری.")
            return
        kb = [[InlineKeyboardButton(f"{c[2]} ({c[3]}) Lv{c[4]}", callback_data=f"sel_{c[0]}")] for c in chars]
        await q.message.reply_text("🎭 انتخاب کاراکتر فعال:", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "prof_quests":
        await q.message.reply_text("📜 برای دیدن کوئست‌ها: /quests")
    elif data == "prof_lb":
        await q.message.reply_text("🏆 لیدربورد:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Top by Coins", callback_data="lb_coins")], [InlineKeyboardButton("Top by Level", callback_data="lb_level")], [InlineKeyboardButton("Top by Rank", callback_data="lb_rank")]]))
    elif data == "prof_gift":
        await q.message.reply_text("🎁 برای هدیه دادن:\n\nروش ۱: روی پیام کسی ریپلای کن و بنویس:\n  /gift 500\n\nروش ۲: با آیدی:\n  /gift 123456789 500")
    elif data == "prof_battle":
        await q.message.reply_text("⚔️ برای نبرد: /battle")
    elif data == "prof_guild":
        guild = get_user_guild(user_id)
        if not guild:
            await q.message.reply_text(f"🏰 تو توی هیچ کلنی نیستی!\n\n📝 ساخت: /guild_create <name>\n💰 هزینه: {GUILD_CREATE_COST:,}")
            return
        await q.message.reply_text(format_guild(guild), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👥 اعضا", callback_data="guild_members"), InlineKeyboardButton("💰 دونیت", callback_data="guild_donate_info")], [InlineKeyboardButton("🔼 ارتقا", callback_data="guild_upgrade"), InlineKeyboardButton("🚪 خروج", callback_data="guild_leave")], [InlineKeyboardButton("🏆 رتبه‌بندی", callback_data="guild_top")]]))
    elif data == "prof_world":
        await q.message.reply_text(get_player_region_view(user_id), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌲 جنگل", callback_data="world_forest")], [InlineKeyboardButton("🏜️ بیابان", callback_data="world_desert")], [InlineKeyboardButton("🏔️ کوه", callback_data="world_mountain")], [InlineKeyboardButton("🌋 آتشفشان", callback_data="world_volcano")], [InlineKeyboardButton("🏰 سیاه‌چال", callback_data="world_dungeon")], [InlineKeyboardButton("📊 پیشرفت", callback_data="world_progress"), InlineKeyboardButton("🏆 گنج‌ها", callback_data="world_treasures")]]))

async def coins(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Coins: {get_coins(update.effective_user.id):,}")

async def select(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chars = get_user_characters(update.effective_user.id)
    if not chars:
        await update.message.reply_text("No characters.")
        return
    kb = [[InlineKeyboardButton(f"{c[2]} ({c[3]}) Lv{c[4]}", callback_data=f"sel_{c[0]}")] for c in chars]
    await update.message.reply_text("Select active:", reply_markup=InlineKeyboardMarkup(kb))

async def select_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    set_active(q.from_user.id, int(q.data.replace("sel_", "")))
    await q.message.reply_text("✅ کاراکتر فعال عوض شد!")

async def shop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    save_menu_owner(ctx, "shop", update.effective_user.id)
    kb = [[InlineKeyboardButton("🛡️ Ability", callback_data="shop_ab")], [InlineKeyboardButton("💊 آیتم", callback_data="shop_item")], [InlineKeyboardButton("🔥 باف", callback_data="shop_buff")], [InlineKeyboardButton("🦸 کاراکترها", callback_data="shop_char")]]
    try:
        await update.message.reply_photo(photo=SHOP_IMAGE, caption="🏪 شاپ:\nیه دسته انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await update.message.reply_text("🏪 شاپ:\nیه دسته انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))

async def edit_shop_msg(q, caption, keyboard):
    try:
        await q.edit_message_media(media=InputMediaPhoto(media=SHOP_IMAGE, caption=caption), reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception:
        try:
            await q.edit_message_caption(caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
            try:
                await q.edit_message_text(caption, reply_markup=InlineKeyboardMarkup(keyboard))
            except Exception:
                await q.message.reply_photo(photo=SHOP_IMAGE, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
async def shop_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "shop"): return
    data = q.data
    if data == "shop_ab":
        kb = [[InlineKeyboardButton(f"{ABILITY_FA.get(n, n)} — {i['price']:,} 💰", callback_data=f"buyab_{n}")] for n, i in ABILITIES.items()]
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🛡️ Ability ها:", kb)
    elif data == "shop_item":
        kb = [[InlineKeyboardButton(f"{ITEM_FA.get(n, n)} — {i['price']:,} 💰", callback_data=f"buyit_{n}")] for n, i in ITEMS.items()]
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "💊 آیتم‌ها:", kb)
    elif data == "shop_buff":
        kb = [[InlineKeyboardButton(f"{BUFF_FA.get(n, n)} — {i['price']:,} 💰", callback_data=f"buybf_{n}")] for n, i in BUFFS.items()]
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🔥 باف‌ها:", kb)
    elif data == "shop_char":
        kb = [[InlineKeyboardButton(f"{emoji} {name_fa}", callback_data=f"shchanime_{anime_key}")] for anime_key, emoji, name, name_fa in get_anime_list()]
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🦸 انیمه انتخاب کن:", kb)
    elif data == "shop_main":
        kb = [[InlineKeyboardButton("🛡️ Ability", callback_data="shop_ab")], [InlineKeyboardButton("💊 آیتم", callback_data="shop_item")], [InlineKeyboardButton("🔥 باف", callback_data="shop_buff")], [InlineKeyboardButton("🦸 کاراکترها", callback_data="shop_char")]]
        await edit_shop_msg(q, "🏪 شاپ:\nیه دسته انتخاب کن:", kb)

async def shop_anime_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "shop"): return
    anime_key = q.data.replace("shchanime_", "")
    anime = get_anime(anime_key)
    if not anime:
        await q.answer("❌ انیمه پیدا نشد.", show_alert=True)
        return
    kb = [[InlineKeyboardButton(f"📦 {rank} Rank — {len(anime['characters'][rank])} کاراکتر", callback_data=f"shchrank_{anime_key}_{rank}")] for rank in anime["characters"].keys()]
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_char")])
    await edit_shop_msg(q, f"{anime['emoji']} {anime['name_fa']} — رنک انتخاب کن:", kb)

async def shop_char_rank_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "shop"): return
    raw = q.data.replace("shchrank_", "")
    parts = raw.rsplit("_", 1)
    if len(parts) != 2:
        await q.answer("❌ خطا در اطلاعات.", show_alert=True)
        return
    anime_key, rank = parts[0], parts[1]
    anime = get_anime(anime_key)
    if not anime:
        await q.answer("❌ انیمه پیدا نشد.", show_alert=True)
        return
    chars = anime["characters"].get(rank, {})
    if not chars:
        await q.answer("❌ کاراکتری توی این رنک نیست.", show_alert=True)
        return
    kb = [[InlineKeyboardButton(f"🎭 {name} — {get_char_price(name, rank):,} 💰", callback_data=f"buych_{anime_key}_{rank}_{name.replace(' ', '§')}")] for name, title in chars.items()]
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data=f"shchanime_{anime_key}")])
    await edit_shop_msg(q, f"{anime['emoji']} {anime['name_fa']} — {rank} Rank:", kb)

async def buy_char_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    parts = q.data.replace("buych_", "").split("_", 2)
    if len(parts) < 3:
        await q.answer("❌ خطا در اطلاعات.", show_alert=True)
        return
    anime_key, rank, char_name = parts[0], parts[1], parts[2].replace("§", " ")
    anime = get_anime(anime_key)
    if not anime:
        await q.answer("❌ انیمه پیدا نشد.", show_alert=True)
        return
    result = buy_character(q.from_user.id, char_name, rank)
    if "Not enough" in str(result) or "کافی" in str(result):
        await q.answer("💰 پولت کمه!", show_alert=True)
        await q.message.reply_text(f"❌ {char_name} ({rank})\n💰 پولت کافی نیست!")
    else:
        await q.answer("✅ خریداری شد!")
        await q.message.reply_text(f"✅ {anime['emoji']} {char_name} ({rank})\n🎉 خریدی!")

async def buy_ability_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ability_name = q.data.replace("buyab_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.message.reply_text("❌ کاراکتر فعال نداری.")
        return
    result = buy_ability(user_id, char[2], ability_name)
    fa = ABILITY_FA.get(ability_name, ability_name)
    if "Not enough" in str(result) or "کافی" in str(result):
        await q.message.reply_text(f"❌ {fa}\n💰 پولت کمه!")
    elif "Already" in str(result) or "قبلاً" in str(result):
        await q.message.reply_text(f"⚠️ {fa}\nقبلاً خریدیش!")
    else:
        await q.message.reply_text(f"✅ {fa}\n🎉 خریدی!")

async def buy_item_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    item_name = q.data.replace("buyit_", "")
    result = buy_item(q.from_user.id, item_name)
    fa = ITEM_FA.get(item_name, item_name)
    if "Not enough" in str(result) or "کافی" in str(result):
        await q.message.reply_text(f"❌ {fa}\n💰 پولت کمه!")
    else:
        await q.message.reply_text(f"✅ {fa}\n🎉 خریدی!")

async def buy_buff_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    buff_name = q.data.replace("buybf_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.message.reply_text("❌ کاراکتر فعال نداری.")
        return
    result = buy_buff(user_id, char[2], buff_name)
    fa = BUFF_FA.get(buff_name, buff_name)
    if "Not enough" in str(result) or "کافی" in str(result):
        await q.message.reply_text(f"❌ {fa}\n💰 پولت کمه!")
    else:
        await q.message.reply_text(f"✅ {fa}\n🎉 خریدی!")
async def buychar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("از /shop استفاده کن!")

async def buy(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /buy <name>")
        return
    name = " ".join(ctx.args)
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    if name in ABILITIES:
        msg = buy_ability(user_id, char[2], name)
        update_quest_progress(user_id, "buy_1_ability")
    elif name in ITEMS:
        msg = buy_item(user_id, name)
    elif name in BUFFS:
        msg = buy_buff(user_id, char[2], name)
    else:
        msg = "Not found."
    await update.message.reply_text(msg)

async def upgrade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری.")
        return
    target_level = None
    if ctx.args:
        try:
            target_level = int(ctx.args[0])
        except ValueError:
            await update.message.reply_text("❌ عدد معتبر بده! مثال: /upgrade 15")
            return
    msg = upgrade_character(user_id, char[0], target_level)
    update_quest_progress(user_id, "level_up_1")
    await update.message.reply_text(msg)

async def battle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not get_active_character(user_id):
        await update.message.reply_text("No active character.")
        return
    save_menu_owner(ctx, "battle", user_id)
    kb = [
        [InlineKeyboardButton("🌀 Jujutsu Kaisen", callback_data="bosses_jjk")], [InlineKeyboardButton("⚔️ Bleach", callback_data="bosses_bleach")],
        [InlineKeyboardButton("💪 One Punch Man", callback_data="bosses_opm")], [InlineKeyboardButton("🗡️ Attack on Titan", callback_data="bosses_aot")],
        [InlineKeyboardButton("🍀 Black Clover", callback_data="bosses_bc")], [InlineKeyboardButton("🩸 Berserk", callback_data="bosses_berserk")],
        [InlineKeyboardButton("🌸 Demon Slayer", callback_data="bosses_ds")], [InlineKeyboardButton("🪚 Chainsaw Man", callback_data="bosses_csm")],
        [InlineKeyboardButton("🍥 Naruto", callback_data="bosses_naruto")], [InlineKeyboardButton("⚔️ Seven Deadly Sins", callback_data="bosses_sds")],
        [InlineKeyboardButton("🏴‍☠️ One Piece", callback_data="bosses_op")], [InlineKeyboardButton("🐉 Dragon Ball", callback_data="bosses_db")],
        [InlineKeyboardButton("🎯 Hunter x Hunter", callback_data="bosses_hxh")], [InlineKeyboardButton("🍡 Sakamoto Days", callback_data="bosses_sakamoto")],
        [InlineKeyboardButton("🗡️ Solo Leveling", callback_data="bosses_solo")], [InlineKeyboardButton("🌀 Mushoku Tensei", callback_data="bosses_mushoku")],
        [InlineKeyboardButton("♟️ Code Geass", callback_data="bosses_cg")], [InlineKeyboardButton("👁️ Tokyo Ghoul", callback_data="bosses_tg")],
    ]
    await update.message.reply_text("⚔️ **انیمه‌ی مورد نظر رو انتخاب کن:**", reply_markup=InlineKeyboardMarkup(kb))

async def bosses_anime_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "battle"): return
    data = q.data.replace("bosses_", "")
    kb = []
    if data == "jjk":
        for name, d in BOSSES_JJK.items(): kb.append([InlineKeyboardButton(f"👹 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in FODDER_JJK.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "bleach":
        for name, d in BLEACH_BOSSES.items(): kb.append([InlineKeyboardButton(f"⚔️ {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in BLEACH_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "opm":
        for name, d in BOSSES_OPM.items(): kb.append([InlineKeyboardButton(f"💪 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "aot":
        for name, d in AOT_BOSSES.items(): kb.append([InlineKeyboardButton(f"🗡️ {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in AOT_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "bc":
        for name, d in BLACKCLOVER_BOSSES.items(): kb.append([InlineKeyboardButton(f"🍀 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in BLACKCLOVER_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "berserk":
        for name, d in BERSERK_BOSSES.items(): kb.append([InlineKeyboardButton(f"🩸 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in BERSERK_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "ds":
        for name, d in DEMONSLAYER_BOSSES.items(): kb.append([InlineKeyboardButton(f"🌸 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in DEMONSLAYER_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "csm":
        for name, d in CHAINSAWMAN_BOSSES.items(): kb.append([InlineKeyboardButton(f"🪚 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in CHAINSAWMAN_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "naruto":
        for name, d in NARUTO_BOSSES.items(): kb.append([InlineKeyboardButton(f"🍥 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in NARUTO_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "sds":
        for name, d in SDS_BOSSES.items(): kb.append([InlineKeyboardButton(f"⚔️ {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in SDS_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "op":
        for name, d in ONEPIECE_BOSSES.items(): kb.append([InlineKeyboardButton(f"🏴‍☠️ {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in ONEPIECE_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "db":
        for name, d in DRAGONBALL_BOSSES.items(): kb.append([InlineKeyboardButton(f"🐉 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in DRAGONBALL_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "hxh":
        for name, d in HXH_BOSSES.items(): kb.append([InlineKeyboardButton(f"🎯 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in HXH_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "sakamoto":
        for name, d in SAKAMOTO_BOSSES.items(): kb.append([InlineKeyboardButton(f"🍡 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in SAKAMOTO_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "solo":
        for name, d in SOLOLEVELING_BOSSES.items(): kb.append([InlineKeyboardButton(f"🗡️ {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in SOLOLEVELING_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "mushoku":
        for name, d in MUSHOKU_BOSSES.items(): kb.append([InlineKeyboardButton(f"🌀 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in MUSHOKU_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "cg":
        for name, d in CODEGEASS_BOSSES.items(): kb.append([InlineKeyboardButton(f"♟️ {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in CODEGEASS_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    elif data == "tg":
        for name, d in TOKYOGHOUL_BOSSES.items(): kb.append([InlineKeyboardButton(f"👁️ {d.get('display_name', name)}", callback_data=f"solo_{name}")])
        for name, d in TOKYOGHOUL_FODDER.items(): kb.append([InlineKeyboardButton(f"🌱 {d.get('display_name', name)}", callback_data=f"solo_{name}")])
    
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="battle_back")])
    await q.edit_message_text(f"⚔️ **لیست باس‌ها:**", reply_markup=InlineKeyboardMarkup(kb))
async def battle_back_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "battle"): return
    kb = [
        [InlineKeyboardButton("🌀 Jujutsu Kaisen", callback_data="bosses_jjk")], [InlineKeyboardButton("⚔️ Bleach", callback_data="bosses_bleach")],
        [InlineKeyboardButton("💪 One Punch Man", callback_data="bosses_opm")], [InlineKeyboardButton("🗡️ Attack on Titan", callback_data="bosses_aot")],
        [InlineKeyboardButton("🍀 Black Clover", callback_data="bosses_bc")], [InlineKeyboardButton("🩸 Berserk", callback_data="bosses_berserk")],
        [InlineKeyboardButton("🌸 Demon Slayer", callback_data="bosses_ds")], [InlineKeyboardButton("🪚 Chainsaw Man", callback_data="bosses_csm")],
        [InlineKeyboardButton("🍥 Naruto", callback_data="bosses_naruto")], [InlineKeyboardButton("⚔️ Seven Deadly Sins", callback_data="bosses_sds")],
        [InlineKeyboardButton("🏴‍☠️ One Piece", callback_data="bosses_op")], [InlineKeyboardButton("🐉 Dragon Ball", callback_data="bosses_db")],
        [InlineKeyboardButton("🎯 Hunter x Hunter", callback_data="bosses_hxh")], [InlineKeyboardButton("🍡 Sakamoto Days", callback_data="bosses_sakamoto")],
        [InlineKeyboardButton("🗡️ Solo Leveling", callback_data="bosses_solo")], [InlineKeyboardButton("🌀 Mushoku Tensei", callback_data="bosses_mushoku")],
        [InlineKeyboardButton("♟️ Code Geass", callback_data="bosses_cg")], [InlineKeyboardButton("👁️ Tokyo Ghoul", callback_data="bosses_tg")],
    ]
    await q.edit_message_text("⚔️ **انیمه‌ی مورد نظر رو انتخاب کن:**", reply_markup=InlineKeyboardMarkup(kb))

async def solo_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "battle"): return
    boss_name = q.data.replace("solo_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.message.reply_text("No active character.")
        return
    existing = get_battle(user_id)
    if existing: end_battle(existing["id"])
    boss_hp = 5000
    all_bosses = [BLEACH_BOSSES, BLEACH_FODDER, BOSSES_JJK, FODDER_JJK, BOSSES_OPM, BOSSES, AOT_BOSSES, AOT_FODDER, BLACKCLOVER_BOSSES, BLACKCLOVER_FODDER, BERSERK_BOSSES, BERSERK_FODDER, DEMONSLAYER_BOSSES, DEMONSLAYER_FODDER, CHAINSAWMAN_BOSSES, CHAINSAWMAN_FODDER, NARUTO_BOSSES, NARUTO_FODDER, SDS_BOSSES, SDS_FODDER, ONEPIECE_BOSSES, ONEPIECE_FODDER, DRAGONBALL_BOSSES, DRAGONBALL_FODDER, HXH_BOSSES, HXH_FODDER, SAKAMOTO_BOSSES, SAKAMOTO_FODDER, SOLOLEVELING_BOSSES, SOLOLEVELING_FODDER, MUSHOKU_BOSSES, MUSHOKU_FODDER, CODEGEASS_BOSSES, CODEGEASS_FODDER, TOKYOGHOUL_BOSSES, TOKYOGHOUL_FODDER]
    for bosses_dict in all_bosses:
        if boss_name in bosses_dict:
            boss_hp = bosses_dict[boss_name]["hp"]
            break
    else:
        await q.message.reply_text("❌ باس پیدا نشد.")
        return
    create_battle(user_id, boss_name, char[5], boss_hp)
    battle_data = get_battle(user_id)
    await q.message.reply_text(build_battle_message(battle_data, char), reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle_data)))
async def action_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    action = q.data.replace("act_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    battle = get_battle(user_id)
    if not battle:
        await q.message.reply_text("❌ نبرد فعالی نداری. /battle بزن.")
        return
    
    if action == "surrender":
        end_battle(battle["id"])
        try: await q.edit_message_text("🏳️ تسلیم شدی!")
        except Exception: await q.message.reply_text("🏳️ تسلیم شدی!")
        return

    # 🆕 منطق اویکن
    if action == "awakening":
        if battle.get("domain_active", 0) == 1 or battle.get("bankai_used", 0) == 1 or battle.get("geass_used", 0) == 1:
            await q.answer("❌ در حال حاضر در حالت اویکن هستی!", show_alert=True)
            return
        battle["domain_active"] = 1
        battle["domain_turns"] = 3
        battle["domain_name"] = "Awakening"
        update_battle(battle)
        text = box_title("🔥 اویکن فعال شد!", 26)
        text += "\n\n۳ تا Ability جدید باز شد (هر کدوم ۱ بار)"
        full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
        try: await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
        except Exception: await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
        return

    if action in ("awaken_blue", "awaken_red", "awaken_purple"):
        if action == "awaken_blue":
            if battle.get("awaken_blue_used", 0) == 1:
                await q.answer("❌ این Ability رو قبلاً استفاده کردی!", show_alert=True)
                return
            mult, cost, color = 5, 30, "blue"
            battle["awaken_blue_used"] = 1
        elif action == "awaken_red":
            if battle.get("awaken_red_used", 0) == 1:
                await q.answer("❌ این Ability رو قبلاً استفاده کردی!", show_alert=True)
                return
            mult, cost, color = 5, 35, "red"
            battle["awaken_red_used"] = 1
        else:
            if battle.get("awaken_purple_used", 0) == 1:
                await q.answer("❌ این Ability رو قبلاً استفاده کردی!", show_alert=True)
                return
            mult, cost, color = 6, 40, "purple"
            battle["awaken_purple_used"] = 1

        # 🆕 ذخیره وضعیت مصرف اویکن در دیتابیس
        conn = sqlite3.connect(DB_NAME); c = conn.cursor()
        c.execute(f"UPDATE active_battles SET awaken_{color}_used = 1 WHERE id = ?", (battle["id"],))
        conn.commit(); conn.close()

        ability_name = get_awaken_name(char[2], color)

        # کم کردن انرژی
        conn = sqlite3.connect(DB_NAME); c = conn.cursor()
        energy_col = "cursed_energy"
        if char[2] in BLEACH_BANKAI or char[2] in ABILITIES_BLEACH: energy_col = "reiatsu"
        elif char[2] in ABILITIES_CODEGEASS: energy_col = "geass_power"
        elif char[2] in ABILITIES_ONEPIECE: energy_col = "haki"
        elif char[2] in ABILITIES_NARUTO: energy_col = "naruto_chakra"
        elif char[2] in ABILITIES_DRAGONBALL: energy_col = "dragonball_ki"
        elif char[2] in ABILITIES_SOLOLEVELING: energy_col = "sololeveling_mana"
        elif char[2] in ABILITIES_HXH: energy_col = "hxh_nen"
        elif char[2] in ABILITIES_MUSHOKU: energy_col = "mushoku_mana"
        elif char[2] in ABILITIES_TOKYOGHOUL: energy_col = "tokyoghoul_rc"
        elif char[2] in ABILITIES_SDS: energy_col = "sds_magic"
        elif char[2] in ABILITIES_SAKAMOTO: energy_col = "sakamoto_stamina"
        elif char[2] in ABILITIES_AOT: energy_col = "aot_titan"
        elif char[2] in ABILITIES_BLACKCLOVER: energy_col = "blackclover_mana"
        elif char[2] in ABILITIES_BERSERK: energy_col = "berserk_bloodlust"
        elif char[2] in ABILITIES_DEMONSLAYER: energy_col = "demonslayer_breath"
        elif char[2] in ABILITIES_CHAINSAWMAN: energy_col = "chainsawman_blood"
        elif char[2] in ABILITIES_OPM: energy_col = "opm_power"

        c.execute(f"SELECT {energy_col} FROM characters WHERE user_id=? AND is_active=1", (user_id,))
        row = c.fetchone()
        energy = row[0] if row else 0
        if energy < cost:
            conn.close()
            await q.answer(f"❌ انرژی کافی نداری! (نیاز: {cost})", show_alert=True)
            return
        c.execute(f"UPDATE characters SET {energy_col} = {energy_col} - ? WHERE user_id=? AND is_active=1", (cost, user_id))
        conn.commit(); conn.close()

        # اعمال دمیج
        dmg = int(char[6] * mult)
        battle["bhp"] = max(0, battle["bhp"] - dmg)
        text = box_title(f"🔥 {ability_name}!", 26)
        text += f"\n\n💥 {format_num(dmg)} آسیب ({mult}x)\n⚡ انرژی مصرفی: {cost}"
        text += f"\n\n👹 باس: {hp_bar(battle['bhp'], battle['bmax'])}"
        
        if battle["bhp"] <= 0:
            reward = finish_battle(user_id, battle["boss_name"], True)
            end_battle(battle["id"])
            final_text = f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin"
            try: await q.edit_message_text(final_text)
            except Exception: await q.message.reply_text(final_text)
            return
            
        # نوبت باس
        from battle import boss_turn, get_boss_data
        boss = get_boss_data(battle["boss_name"])
        php, bhp, text = boss_turn(battle, boss, battle["php"], battle["pmax"], battle["bhp"], battle["bmax"], text)
        battle["php"] = php; battle["bhp"] = bhp
        update_battle(battle)
        full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
        try: await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
        except Exception: await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
        return

    # بقیه دکمه‌ها
    if action in ("ability_1", "ability_2", "ability_3"):
        status, text, battle = player_ability_v2(battle, char, action)
    elif action == "attack":
        status, text, battle = player_attack(battle, char)
    elif action == "defend":
        status, text, battle = player_defend(battle, char)
    elif action == "dodge":
        status, text, battle = player_dodge(battle, char)
    elif action == "goku_form":
        if char[2] != "Son Goku":
            await q.answer("❌ فقط گوکو می‌تونه تغییر فرم بده!", show_alert=True)
            return
        status, text, battle = goku_transform(battle, char)
    elif action == "luffy_form":
        if char[2] != "Monkey D. Luffy":
            await q.answer("❌ فقط لوفی می‌تونه تغییر فرم بده!", show_alert=True)
            return
        status, text, battle = luffy_transform(battle, char)
    elif action == "ultimate_geass":
        if char[2] not in ABILITIES_CODEGEASS:
            await q.answer("❌ این کاراکتر گیاس دوم نداره!", show_alert=True)
            return
        status, text, battle = player_ability_v2(battle, char, "ultimate_geass")
    elif action == "item":
        items = get_items(user_id)
        if not items:
            await q.answer("❌ آیتم نداری.", show_alert=True)
            return
        kb = [[InlineKeyboardButton(f"{ITEM_FA.get(n, n)} (x{c})", callback_data=f"it_{n}")] for n, c in items]
        await q.message.reply_text("💊 آیتم انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
        return
    elif action == "shop_ability":
        abilities = get_abilities(user_id, char[2])
        if not abilities:
            await q.answer("❌ Ability خریداری‌شده نداری.", show_alert=True)
            return
        kb = [[InlineKeyboardButton(ABILITY_FA.get(a, a), callback_data=f"shopab_{a}")] for a in abilities]
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="act_back")])
        await q.message.reply_text("🔥 Ability خریداری‌شده:", reply_markup=InlineKeyboardMarkup(kb))
        return
    elif action == "shop_buff":
        buffs = get_user_buffs(user_id, char[2])
        if not buffs:
            await q.answer("❌ باف خریداری‌شده نداری.", show_alert=True)
            return
        kb = [[InlineKeyboardButton(BUFF_FA.get(b, b), callback_data=f"shopbf_{b}")] for b in buffs]
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="act_back")])
        await q.message.reply_text("✨ باف خریداری‌شده:", reply_markup=InlineKeyboardMarkup(kb))
        return
    elif action == "back":
        text = build_battle_message(battle, char)
        try: await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
        except Exception: await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
        return
    elif action == "domain":
        if char[2] not in DOMAINS_JJK:
            await q.answer("❌ این کاراکتر Domain نداره!", show_alert=True)
            return
        status, text, battle = player_ability_v2(battle, char, "domain")
    elif action == "bankai":
        if char[2] not in BLEACH_BANKAI:
            await q.answer("❌ این کاراکتر Bankai نداره!", show_alert=True)
            return
        status, text, battle = player_ability_v2(battle, char, "bankai")
    elif action == "arise":
        if char[2] != "Sung Jin-Woo":
            await q.answer("❌ این کاراکتر Arise نداره!", show_alert=True)
            return
        shadows = get_user_shadows(user_id, char[2])
        if not shadows:
            await q.answer("❌ هیچ سایه‌ای نداری! اول باس بکش.", show_alert=True)
            return
        shadows_text = "💀 **سایه‌های تو:**\n\n"
        for i, (sname, atk_bonus) in enumerate(shadows, 1):
            shadows_text += f"{i}. {sname} (+{atk_bonus} ATK)\n"
        shadows_text += f"\n⚔️ مجموع ATK: +{sum(s[1] for s in shadows)}"
        try: await q.edit_message_text(shadows_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="act_back")]]))
        except Exception: await q.message.reply_text(shadows_text)
        return
    else:
        return
    
    if status == "won":
        reward = finish_battle(user_id, battle["boss_name"], True)
        arise_text = ""
        try:
            success, msg = try_arise(user_id, char[2], battle["boss_name"])
            if success: arise_text = msg
        except Exception: pass
        end_battle(battle["id"])
        final_text = f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin{arise_text}"
        try: await q.edit_message_text(final_text)
        except Exception: await q.message.reply_text(final_text)
        return
    elif status == "lost":
        end_battle(battle["id"])
        try: await q.edit_message_text(f"{text}\n\n💀 باختی!")
        except Exception: await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return
    
    if char[2] == "Son Goku":
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE active_battles SET goku_form = ? WHERE id = ?", (battle.get("goku_form", 0), battle["id"]))
        conn.commit()
        conn.close()
    elif char[2] == "Monkey D. Luffy":
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE active_battles SET luffy_form = ? WHERE id = ?", (battle.get("luffy_form", 0), battle["id"]))
        conn.commit()
        conn.close()
        
    update_battle(battle)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
    if len(full_text) > 3500: full_text = full_text[:3500] + "..."
    try: await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
    except Exception: await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
async def item_use_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    item_name = q.data.replace("it_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    battle = get_battle(user_id)
    if not battle or not use_item(user_id, item_name): return
    status, text, battle = player_item(battle, char, item_name)
    if status == "won":
        reward = finish_battle(user_id, battle["boss_name"], True)
        arise_text = ""
        try:
            success, msg = try_arise(user_id, char[2], battle["boss_name"])
            if success: arise_text = msg
        except Exception: pass
        end_battle(battle["id"])
        final_text = f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin{arise_text}"
        try: await q.edit_message_text(final_text)
        except Exception: await q.message.reply_text(final_text)
        return
    elif status == "lost":
        end_battle(battle["id"])
        try: await q.edit_message_text(f"{text}\n\n💀 باختی!")
        except Exception: await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return
    update_battle(battle)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
    if len(full_text) > 3500: full_text = full_text[:3500] + "..."
    try: await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
    except Exception: await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))

async def shop_ability_use_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ability_name = q.data.replace("shopab_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    battle = get_battle(user_id)
    if not battle: return
    status, text, battle = player_ability_shop(battle, char, ability_name)
    try: remove_user_ability(user_id, char[2], ability_name)
    except Exception: pass
    if status == "won":
        reward = finish_battle(user_id, battle["boss_name"], True)
        arise_text = ""
        try:
            success, msg = try_arise(user_id, char[2], battle["boss_name"])
            if success: arise_text = msg
        except Exception: pass
        end_battle(battle["id"])
        final_text = f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin{arise_text}"
        try: await q.edit_message_text(final_text)
        except Exception: await q.message.reply_text(final_text)
        return
    elif status == "lost":
        end_battle(battle["id"])
        try: await q.edit_message_text(f"{text}\n\n💀 باختی!")
        except Exception: await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return
    update_battle(battle)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
    if len(full_text) > 3500: full_text = full_text[:3500] + "..."
    try: await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
    except Exception: await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))

async def shop_buff_use_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    buff_name = q.data.replace("shopbf_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    battle = get_battle(user_id)
    if not battle: return
    status, text, battle = player_buff_shop(battle, char, buff_name)
    remove_user_buff(user_id, char[2], buff_name)
    if status == "won":
        reward = finish_battle(user_id, battle["boss_name"], True)
        arise_text = ""
        try:
            success, msg = try_arise(user_id, char[2], battle["boss_name"])
            if success: arise_text = msg
        except Exception: pass
        end_battle(battle["id"])
        final_text = f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin{arise_text}"
        try: await q.edit_message_text(final_text)
        except Exception: await q.message.reply_text(final_text)
        return
    elif status == "lost":
        end_battle(battle["id"])
        try: await q.edit_message_text(f"{text}\n\n💀 باختی!")
        except Exception: await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return
    update_battle(battle)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
    if len(full_text) > 3500: full_text = full_text[:3500] + "..."
    try: await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
    except Exception: await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, battle)))
async def world_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not get_active_character(user_id):
        await update.message.reply_text("❌ کاراکتر فعال نداری. /start بزن.")
        return
    save_menu_owner(ctx, "world", user_id)
    text = get_player_region_view(user_id)
    kb = [[InlineKeyboardButton("🌲 جنگل", callback_data="world_forest")], [InlineKeyboardButton("🏜️ بیابان", callback_data="world_desert")], [InlineKeyboardButton("🏔️ کوه", callback_data="world_mountain")], [InlineKeyboardButton("🌋 آتشفشان", callback_data="world_volcano")], [InlineKeyboardButton("🏰 سیاه‌چال", callback_data="world_dungeon")], [InlineKeyboardButton("📊 پیشرفت", callback_data="world_progress"), InlineKeyboardButton("🏆 گنج‌ها", callback_data="world_treasures")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def world_region_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "world"): return
    region_key = q.data.replace("world_", "")
    user_id = q.from_user.id
    if region_key not in get_unlocked_regions(user_id):
        can, msg = can_unlock_region(user_id, region_key)
        if not can:
            await q.answer(msg, show_alert=True)
            return
        unlock_world_region(user_id, region_key)
    update_world_region(user_id, region_key)
    await q.edit_message_text(get_region_view(user_id, region_key), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚶 گشتن", callback_data=f"explore_{region_key}")], [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")]]))

async def world_explore_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "world"): return
    region_key = q.data.replace("explore_", "")
    user_id = q.from_user.id
    region = get_region(region_key)
    if not region:
        await q.answer("❌ منطقه پیدا نشد.", show_alert=True)
        return
    event = random_explore_event()
    increment_world_stat(user_id, "explores")

    if event == "enemy":
        enemy_name = random.choice(region["enemies"])
        char = get_active_character(user_id)
        existing = get_battle(user_id)
        if existing: end_battle(existing["id"])
        enemy_hp = 20000 if region_key == "forest" else (50000 if region_key == "desert" else (120000 if region_key == "mountain" else (250000 if region_key == "volcano" else 500000)))
        create_battle(user_id, enemy_name, char[5], enemy_hp)
        text = f"👹 یه دشمن ظاهر شد!\n\n{enemy_name}\n\n" + build_battle_message(get_battle(user_id), char)
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, get_battle(user_id))))
    elif event == "treasure":
        t_key, t_data = random_treasure()
        if t_data:
            if t_data["type"] == "coins":
                amount = t_data["value"] // 2
                add_coins(user_id, amount)
                reward_text = f"💰 +{amount:,} سکه"
            elif t_data["type"] == "item":
                item_names = ["Health Potion", "Mega Potion", "Damage Boost", "Bomb"]
                chosen_item = random.choice(item_names)
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("SELECT id, quantity FROM items WHERE user_id=? AND item_name=?", (user_id, chosen_item))
                row = c.fetchone()
                if row: c.execute("UPDATE items SET quantity = quantity + 1 WHERE id=?", (row[0],))
                else: c.execute("INSERT INTO items (user_id, item_name, quantity) VALUES (?,?,1)", (user_id, chosen_item))
                conn.commit()
                conn.close()
                reward_text = f"🎁 آیتم: {chosen_item}"
            else:
                reward_text = f"✨ {t_data['effect']}"
            add_world_treasure(user_id, t_data["name"])
            increment_world_stat(user_id, "treasures")
            text = f"🎁 یه صندوق پیدا کردی!\n\n{format_treasure(t_key, t_data)}\n\n🎉 جایزه: {reward_text}"
        else:
            text = "🎁 صندوق خالی بود..."
        kb = [[InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")], [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    elif event == "mine":
        amount = random_reward(region_key) // 4
        add_coins(user_id, amount)
        text = f"💎 یه معدن پیدا کردی!\n\n💰 +{amount:,} سکه"
        kb = [[InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")], [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    elif event == "gate":
        all_regions = list(REGIONS.keys())
        current_idx = all_regions.index(region_key) if region_key in all_regions else 0
        if current_idx + 1 < len(all_regions):
            next_region = all_regions[current_idx + 1]
            unlocked_new = unlock_world_region(user_id, next_region)
            text = f"🚪 دروازه باز شد!\n\n🎉 منطقه جدید باز شد: {get_region_name(next_region)}" if unlocked_new else f"🚪 دروازه به {get_region_name(next_region)}"
        else:
            text = "🚪 دروازه به جایی نمی‌ره..."
        kb = [[InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")], [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    elif event == "riddle":
        reward = random.choice([500, 2000, 5000, 10000])
        add_coins(user_id, reward)
        text = f"❓ یه معما حل کردی!\n\n💰 +{reward:,} سکه"
        kb = [[InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")], [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    elif event == "rare_boss":
        boss_name = region["boss"]
        char = get_active_character(user_id)
        existing = get_battle(user_id)
        if existing: end_battle(existing["id"])
        boss_hp = 50000 if region_key == "forest" else (120000 if region_key == "desert" else (300000 if region_key == "mountain" else (600000 if region_key == "volcano" else 150000)))
        create_battle(user_id, boss_name, char[5], boss_hp)
        text = f"🌟 یه باس کمیاب ظاهر شد!\n\n👑 {boss_name}\n\n" + build_battle_message(get_battle(user_id), char)
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(get_battle_kb(char[2], user_id, get_battle(user_id))))
    elif event == "trap":
        loss = random_reward(region_key) // 4
        coins = get_coins(user_id)
        if coins >= loss:
            add_coins(user_id, -loss)
            text = f"💀 توی تله افتادی!\n\n💸 -{loss:,} سکه"
        else:
            text = "💀 توی تله افتادی! ولی پولی نداشتی..."
        kb = [[InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")], [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def world_progress_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "world"): return
    await q.edit_message_text(format_world_progress(q.from_user.id), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏆 گنج‌ها", callback_data="world_treasures")], [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")]]))

async def world_treasures_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "world"): return
    await q.edit_message_text(format_treasures_list(q.from_user.id), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊 پیشرفت", callback_data="world_progress")], [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")]]))

async def world_back_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "world"): return
    kb = [[InlineKeyboardButton("🌲 جنگل", callback_data="world_forest")], [InlineKeyboardButton("🏜️ بیابان", callback_data="world_desert")], [InlineKeyboardButton("🏔️ کوه", callback_data="world_mountain")], [InlineKeyboardButton("🌋 آتشفشان", callback_data="world_volcano")], [InlineKeyboardButton("🏰 سیاه‌چال", callback_data="world_dungeon")], [InlineKeyboardButton("📊 پیشرفت", callback_data="world_progress"), InlineKeyboardButton("🏆 گنج‌ها", callback_data="world_treasures")]]
    await q.edit_message_text(get_player_region_view(q.from_user.id), reply_markup=InlineKeyboardMarkup(kb))
async def quests_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    reset_daily_quests(user_id)
    user_quests = get_user_quests(user_id)
    if not user_quests:
        await update.message.reply_text("No quests today.")
        return
    text = "Daily Quests:\n\n"
    for key, prog, completed, claimed in user_quests:
        q = QUESTS[key]
        status = "CLAIMED" if claimed else ("READY" if completed else f"{prog}/{q['target']}")
        text += f"- {q['desc']} [{status}] (+{q['reward']})\n"
    await update.message.reply_text(text)

async def claim(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /claim <quest_key>")
        return
    key = ctx.args[0]
    if key not in QUESTS:
        await update.message.reply_text("Invalid quest key.")
        return
    await update.message.reply_text(claim_quest(update.effective_user.id, key))

async def leaderboard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    save_menu_owner(ctx, "lb", update.effective_user.id)
    kb = [[InlineKeyboardButton("Top by Coins", callback_data="lb_coins")], [InlineKeyboardButton("Top by Level", callback_data="lb_level")], [InlineKeyboardButton("Top by Rank", callback_data="lb_rank")]]
    await update.message.reply_text("Leaderboard:", reply_markup=InlineKeyboardMarkup(kb))

async def leaderboard_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "lb"): return
    if q.data == "lb_coins":
        text = "Top 10 by Coins:\n\n" + "".join([f"{i}. {name or 'Unknown'} - {coins:,}\n" for i, (name, coins) in enumerate(get_top_by_coins(10), 1)])
        await q.message.reply_text(text)
    elif q.data == "lb_level":
        text = "Top 10 by Level:\n\n" + "".join([f"{i}. {name or 'Unknown'} - {char} ({rank}) Lv{level}\n" for i, (name, char, rank, level) in enumerate(get_top_by_level(10), 1)])
        await q.message.reply_text(text)
    elif q.data == "lb_rank":
        text = "Top 10 by Rank:\n\n" + "".join([f"{i}. {name or 'Unknown'} - {char} ({rank})\n" for i, (name, char, rank) in enumerate(get_top_by_rank(10), 1)])
        await q.message.reply_text(text)

async def guild_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    save_menu_owner(ctx, "guild", update.effective_user.id)
    guild = get_user_guild(update.effective_user.id)
    if not guild:
        await update.message.reply_text(f"🏰 تو توی هیچ کلنی نیستی!\n\n📝 ساخت: /guild_create <name>\n🔍 پیوستن: /guild_join <name>\n📋 لیست: /guild_list\n\n💰 هزینه: {GUILD_CREATE_COST:,} سکه\n⭐ حداقل لول: {GUILD_MIN_LEVEL}")
        return
    kb = [[InlineKeyboardButton("👥 اعضا", callback_data="guild_members"), InlineKeyboardButton("💰 دونیت", callback_data="guild_donate_info")], [InlineKeyboardButton("🔼 ارتقا", callback_data="guild_upgrade"), InlineKeyboardButton("🚪 خروج", callback_data="guild_leave")], [InlineKeyboardButton("🏆 رتبه‌بندی", callback_data="guild_top")]]
    await update.message.reply_text(format_guild(guild), reply_markup=InlineKeyboardMarkup(kb))

async def guild_create(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args: return await update.message.reply_text("❌ Usage: /guild_create <name>")
    char = get_active_character(update.effective_user.id)
    if not char: return await update.message.reply_text("❌ کاراکتر فعال نداری!")
    await update.message.reply_text(create_new_guild(update.effective_user.id, " ".join(ctx.args), char[4]))

async def guild_join(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args: return await update.message.reply_text("❌ Usage: /guild_join <name>")
    await update.message.reply_text(join_existing_guild(update.effective_user.id, " ".join(ctx.args)))

async def guild_leave(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(leave_current_guild(update.effective_user.id))

async def guild_donate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args: return await update.message.reply_text("❌ Usage: /guild_donate <amount>")
    try: amount = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ عدد معتبر بده!")
    await update.message.reply_text(donate(update.effective_user.id, amount))

async def guild_upgrade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(try_upgrade_guild(update.effective_user.id))

async def guild_members_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    guild = get_user_guild(update.effective_user.id)
    if not guild: return await update.message.reply_text("❌ تو توی کلنی نیستی!")
    await update.message.reply_text(format_members(guild))

async def guild_kick(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args: return await update.message.reply_text("❌ Usage: /guild_kick <user_id>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده!")
    await update.message.reply_text(kick_member(update.effective_user.id, target_id))

async def guild_list(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    guilds = get_top_guilds(10)
    if not guilds: return await update.message.reply_text("📭 هنوز هیچ کلنی ساخته نشده!")
    text = "🏰 کلن‌های برتر:\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, g in enumerate(guilds, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {g[1]} — سطح {g[3]} | 👥 {g[6]}\n"
    await update.message.reply_text(text)

async def guild_leaderboard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    guilds = get_top_guilds(10)
    if not guilds: return await update.message.reply_text("📭 هنوز هیچ کلنی ساخته نشده!")
    text = "🏆 برترین کلن‌ها:\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, g in enumerate(guilds, 1):
        text += f"{i}. {g[1]}\n   ⭐ سطح {g[3]} | ⚡ {g[4]:,} XP | 💰 {g[5]:,}\n\n"
    await update.message.reply_text(text)

async def guild_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not await check_menu_owner(q, ctx, "guild"): return
    data = q.data
    user_id = q.from_user.id
    if data == "guild_members":
        guild = get_user_guild(user_id)
        await q.message.reply_text(format_members(guild) if guild else "❌ تو توی کلنی نیستی!")
    elif data == "guild_donate_info":
        await q.message.reply_text("💰 دونیت به خزانه کلن\n\nدستور: /guild_donate <amount>\nمثال: /guild_donate 50000\n\n🎁 هر ۵۰,۰۰۰ سکه = ۵ XP به کلن")
    elif data == "guild_upgrade":
        await q.message.reply_text(try_upgrade_guild(user_id))
    elif data == "guild_leave":
        await q.message.reply_text(leave_current_guild(user_id))
    elif data == "guild_top":
        guilds = get_top_guilds(10)
        if not guilds: return await q.message.reply_text("📭 هنوز هیچ کلنی ساخته نشده!")
        text = "🏆 برترین کلن‌ها:\n━━━━━━━━━━━━━━━━━━━\n\n"
        for i, g in enumerate(guilds, 1):
            text += f"{i}. {g[1]} — سطح {g[3]} | 👥 {g[6]}\n"
        await q.message.reply_text(text)
async def pvp(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not get_active_character(user_id): return await update.message.reply_text("No active character.")
    session_id = f"pvp_{user_id}"
    PVP_SESSIONS[session_id] = {"host": user_id, "opponent": None}
    await update.message.reply_text(f"⚔️ PvP session: {session_id}\nOpponent: /joinpvp {session_id}")

async def join_pvp(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args: return await update.message.reply_text("Usage: /joinpvp <session_id>")
    session_id = ctx.args[0]
    if session_id not in PVP_SESSIONS: return await update.message.reply_text("Not found.")
    s = PVP_SESSIONS[session_id]
    user_id = update.effective_user.id
    if user_id == s["host"]: return await update.message.reply_text("Can't fight yourself.")
    char = get_active_character(user_id)
    if not char: return await update.message.reply_text("No active character.")
    char_host = get_active_character(s["host"])
    team1 = [{"uid": s["host"], "name": char_host[2], "display": get_username(s["host"]), "hp": char_host[5], "max_hp": char_host[5], "atk": char_host[6], "def": char_host[7], "dodge": char_host[8], "defending": 0, "dodged_next": 0}]
    team2 = [{"uid": user_id, "name": char[2], "display": get_username(user_id), "hp": char[5], "max_hp": char[5], "atk": char[6], "def": char[7], "dodge": char[8], "defending": 0, "dodged_next": 0}]
    create_multi_battle(session_id=session_id, battle_type="pvp", host_id=s["host"], players=[s["host"], user_id], team1=team1, team2=team2)
    battle = get_multi_battle(session_id)
    next_player, _ = get_player(battle, battle["current_turn"])
    next_char = next_player["name"] if next_player else char_host[2]
    await update.message.reply_text(build_battle_view(battle), reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id, next_char, battle["current_turn"], battle["current_turn"])))

async def coop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not get_active_character(update.effective_user.id): return await update.message.reply_text("No active character.")
    kb = [[InlineKeyboardButton("🌀 JJK Bosses", callback_data="coop_jjk")], [InlineKeyboardButton("🏴‍☠️ One Piece Bosses", callback_data="coop_op")], [InlineKeyboardButton("🗡️ Solo Leveling Bosses", callback_data="coop_solo")]]
    await update.message.reply_text("👥 Co-op - Host chooses boss:", reply_markup=InlineKeyboardMarkup(kb))

async def coop_boss_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    boss_name = q.data.replace("coopboss_", "")
    session_id = f"coop_{q.from_user.id}_{boss_name.replace(' ', '_')}"
    COOP_SESSIONS[session_id] = {"host": q.from_user.id, "boss": boss_name, "players": [q.from_user.id]}
    await q.message.reply_text(f"👥 Co-op: {boss_name}\nSession: {session_id}\nOthers: /join {session_id}\nHost: /startcoop {session_id}")

async def join_coop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args: return await update.message.reply_text("Usage: /join <session_id>")
    session_id = ctx.args[0]
    if session_id not in COOP_SESSIONS: return await update.message.reply_text("Session not found.")
    user_id = update.effective_user.id
    if not get_active_character(user_id): return await update.message.reply_text("Need active character.")
    s = COOP_SESSIONS[session_id]
    if user_id in s["players"]: return await update.message.reply_text("Already joined!")
    if len(s["players"]) >= 2: return await update.message.reply_text("Session full.")
    s["players"].append(user_id)
    await update.message.reply_text("✅ Joined!")

async def start_coop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args: return await update.message.reply_text("Usage: /startcoop <session_id>")
    session_id = ctx.args[0]
    if session_id not in COOP_SESSIONS: return await update.message.reply_text("Session not found.")
    s = COOP_SESSIONS[session_id]
    if update.effective_user.id != s["host"]: return await update.message.reply_text("Only host can start.")
    if len(s["players"]) < 2: return await update.message.reply_text("Need 2 players.")
    p1_id, p2_id = s["players"][0], s["players"][1]
    char1, char2 = get_active_character(p1_id), get_active_character(p2_id)
    boss_hp = 5000
    if s["boss"] in BLEACH_BOSSES: boss_hp = BLEACH_BOSSES[s["boss"]]["hp"]
    elif s["boss"] in BOSSES_JJK: boss_hp = BOSSES_JJK[s["boss"]]["hp"]
    team1 = [{"uid": p1_id, "name": char1[2], "display": get_username(p1_id), "hp": char1[5], "max_hp": char1[5], "atk": char1[6], "def": char1[7], "dodge": char1[8], "defending": 0, "dodged_next": 0}, {"uid": p2_id, "name": char2[2], "display": get_username(p2_id), "hp": char2[5], "max_hp": char2[5], "atk": char2[6], "def": char2[7], "dodge": char2[8], "defending": 0, "dodged_next": 0}]
    create_multi_battle(session_id=session_id, battle_type="coop", host_id=s["host"], players=[p1_id, p2_id], team1=team1, team2=[], boss_name=s["boss"], boss_hp=boss_hp)
    battle = get_multi_battle(session_id)
    await update.message.reply_text(build_battle_view(battle), reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id, char1[2], battle["current_turn"], p1_id)))

async def multi_action_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    session_id = q.data.split("_", 2)[2]
    action = q.data.split("_")[1]
    user_id = q.from_user.id
    battle = get_multi_battle(session_id)
    if not battle or str(battle["current_turn"]) != str(user_id):
        await q.answer("⏳ نوبت تو نیست یا نبرد فعال نیست!", show_alert=True)
        return
    await q.answer()
    action_map = {"ab1": "ability_1", "ab2": "ability_2", "ab3": "ability_3"}
    status, log = player_action(session_id, user_id, action_map.get(action, action))
    if status is None: return await q.answer(log, show_alert=True)
    if status in ("won", "team1_won", "team2_won", "draw"):
        result = finish_multi_battle(session_id)
        if result:
            text = "🏆 بردی!\n\n" + log + "\n\n💰 جوایز:\n" + "".join([f"👤 {get_username(uid)}: +{amount:,} coin\n" for uid, amount in result["rewards"].items()])
            return await q.edit_message_text(text)
        return
    battle = get_multi_battle(session_id)
    view = build_battle_view(battle)
    next_player, _ = get_player(battle, battle["current_turn"])
    kb = get_multi_kb(session_id, next_player["name"] if next_player else None, battle["current_turn"], battle["current_turn"])
    await q.edit_message_text(f"{log}\n\n{view}"[:3500], reply_markup=InlineKeyboardMarkup(kb))

async def setcharimage_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ تو ادمین نیستی!")
        return
    caption = update.message.caption
    if not caption or len(caption.split()) < 2:
        await update.message.reply_text("Usage: عکس رو با کپشن /setcharimage <char_name> بفرست")
        return
    char_name = " ".join(caption.split()[1:])
    photo_file_id = update.message.photo[-1].file_id
    from database import set_char_image_db
    set_char_image_db(char_name, photo_file_id)
    await update.message.reply_text(f"✅ عکس برای {char_name} با موفقیت ثبت شد!")

async def send_gift(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id
    if not ctx.args:
        await update.message.reply_text("Usage: /gift <amount> (روی پیام طرف ریپلای کن) یا /gift <user_id> <amount>")
        return
    target_id = None
    amount = 0
    if update.message.reply_to_message:
        target_id = update.message.reply_to_message.from_user.id
        try: amount = int(ctx.args[0])
        except ValueError: return await update.message.reply_text("❌ مبلغ باید عدد باشه.")
    elif len(ctx.args) >= 2:
        try: target_id = int(ctx.args[0]); amount = int(ctx.args[1])
        except ValueError: return await update.message.reply_text("❌ آیدی یا مبلغ نامعتبره.")
    else:
        return await update.message.reply_text("❌ باید روی پیام کسی ریپلای کنی یا آیدی بفرستی.")
    if target_id == sender_id: return await update.message.reply_text("❌ نمیتونی به خودت هدیه بدی!")
    if amount <= 0: return await update.message.reply_text("❌ مبلغ باید بیشتر از صفر باشه!")
    from database import spend_coins, add_coins
    if get_coins(sender_id) < amount:
        return await update.message.reply_text(f"❌ سکه کافی نداری! موجودی تو: {get_coins(sender_id):,}")
    if spend_coins(sender_id, amount):
        add_coins(target_id, amount)
        await update.message.reply_text(f"🎁 **هدیه ارسال شد!**\nاز: {get_username(sender_id)}\nبه: {get_username(target_id)}\n💰 مبلغ: {amount:,} سکه")
async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 **راهنمای ربات**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "🎮 /start - شروع بازی\n"
        "👤 /profile - پروفایل\n"
        "💰 /coins - موجودی سکه\n"
        "🏪 /shop - فروشگاه\n"
        "⚔️ /battle - نبرد با باس\n"
        "🏰 /guild - کلن\n"
        "📜 /quests - کوئست روزانه\n"
        "🗺️ /world - دنیای آزاد\n"
        "🏆 /leaderboard - لیدربورد\n"
        "🎁 /gift - هدیه دادن\n\n"
        "🔮 **دستورات ارتقای انرژی:**\n"
        "/upgradece - انرژی نفرینی (JJK)\n"
        "/upgraderei - ریستو (Bleach)\n"
        "/upgradegeass - گیاس (Code Geass)\n"
        "/upgradehaki - هاکی (One Piece)\n"
        "/upgradechakra - چاکرا (Naruto)\n"
        "/upgradeki - کی (Dragon Ball)\n"
        "/upgrademana - مانا (Solo Leveling)\n"
        "/upgradenen - نن (Hunter x Hunter)\n"
        "/upgrademushoku - مانا (Mushoku)\n"
        "/upgraderc - RC (Tokyo Ghoul)\n"
        "/upgrademagic - جادو (SDS)\n"
        "/upgradestamina - استقامت (Sakamoto)\n"
        "/upgradetitan - قدرت تایتان (AOT)\n"
        "/upgradebcmana - مانا (Black Clover)\n"
        "/upgradebloodlust - خون‌آشامی (Berserk)\n"
        "/upgradebreath - نفس (Demon Slayer)\n"
        "/upgradeblood - خون (Chainsaw Man)\n"
        "/upgradeopm - قدرت مطلق (OPM)\n\n"
        "🔧 /admin - پنل ادمین"
    )
    await update.message.reply_text(text)

async def admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ تو ادمین نیستی!")
        return
    text = "👑 پنل ادمین\n━━━━━━━━━━━━━━━━━━━\n\n"
    if is_owner(user_id):
        text += "🔑 مالک اصلی\n\n"
    text += "💰 /give /take\n"
    text += "👤 /userinfo /allusers /resetuser /ban /unban\n"
    text += "🎭 /givechar /resetchar\n"
    if is_owner(user_id):
        text += "\n👑 /addadmin /removeadmin /listadmins\n"
        text += "📜 /sethelp /viewhelp\n"
        text += "🖼️ عکس + کپشن /setcharimage <name>\n"
        text += "📢 /addchannel /removechannel /listchannels\n"
        text += "\n👑 /ownerpanel\n"
    await update.message.reply_text(text)

async def give_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_coins"): return
    if len(ctx.args) < 2: return await update.message.reply_text("Usage: /give <user_id> <amount>")
    try: target_id = int(ctx.args[0]); amount = int(ctx.args[1])
    except ValueError: return await update.message.reply_text("❌ اعداد معتبر بده.")
    give_coins(target_id, amount)
    await update.message.reply_text(f"✅ {amount:,} coin به {target_id} دادی.")

async def take_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_coins"): return
    if len(ctx.args) < 2: return await update.message.reply_text("Usage: /take <user_id> <amount>")
    try: target_id = int(ctx.args[0]); amount = int(ctx.args[1])
    except ValueError: return await update.message.reply_text("❌ اعداد معتبر بده.")
    if take_coins(target_id, amount):
        await update.message.reply_text(f"✅ {amount:,} coin از {target_id} گرفتی.")
    else:
        await update.message.reply_text("❌ کاربر Coin کافی نداره.")

async def userinfo_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not ctx.args: return await update.message.reply_text("Usage: /userinfo <user_id>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده.")
    user, chars = get_user_stats(target_id)
    if not user: return await update.message.reply_text("❌ کاربر پیدا نشد.")
    text = f"👤 کاربر: {user[0] or 'Unknown'}\n🆔 ID: {target_id}\n💰 Coins: {user[1]:,}\n\n🦸 کاراکترها:\n"
    if not chars: text += "  ❌ هیچ کاراکتری نداره\n"
    else:
        for c in chars: text += f"  • {c[0]} ({c[1]}) Lv{c[2]}\n"
    await update.message.reply_text(text)

async def allusers_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    rows = get_all_users()
    text = f"📋 کل کاربران: {len(rows)}\n\n"
    for i, (uid, name, coins) in enumerate(rows[:30], 1):
        text += f"{i}. {name or 'Unknown'} ({uid}) — {coins:,}\n"
    if len(rows) > 30: text += f"\n... و {len(rows) - 30} نفر دیگه"
    await update.message.reply_text(text)

async def resetuser_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_chars"): return
    if not ctx.args: return await update.message.reply_text("Usage: /resetuser <user_id>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده.")
    reset_user(target_id)
    await update.message.reply_text(f"♻️ کاربر {target_id} ریست شد.")

async def ban_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "ban_users"): return
    if not ctx.args: return await update.message.reply_text("Usage: /ban <user_id>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده.")
    ban_user(target_id)
    await update.message.reply_text(f"🚫 کاربر {target_id} بن شد.")

async def unban_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "ban_users"): return
    if not ctx.args: return await update.message.reply_text("Usage: /unban <user_id>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده.")
    unban_user(target_id)
    await update.message.reply_text(f"✅ کاربر {target_id} آنبن شد.")

async def addadmin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return await update.message.reply_text("❌ فقط مالک!")
    if not ctx.args: return await update.message.reply_text("Usage: /addadmin <user_id>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده.")
    add_admin(target_id, "all", update.effective_user.id)
    await update.message.reply_text(f"✅ {target_id} ادمین شد!")

async def removeadmin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return await update.message.reply_text("❌ فقط مالک!")
    if not ctx.args: return await update.message.reply_text("Usage: /removeadmin <user_id>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده.")
    ok, msg = remove_admin(target_id)
    await update.message.reply_text(msg)

async def listadmins_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    admins = list_admins()
    text = "👑 ادمین‌ها:\n\n"
    for uid, role, perms in admins:
        text += f"👤 {uid} — {role} | {perms}\n"
    if not admins: text = "📭 هیچ ادمینی اضافه نشده."
    await update.message.reply_text(text)

async def givechar_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_chars"): return
    if len(ctx.args) < 3: return await update.message.reply_text("Usage: /givechar <user_id> <char_name> <rank>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده.")
    rank = ctx.args[-1]
    char_name = " ".join(ctx.args[1:-1])
    if rank not in CHARACTERS or char_name not in CHARACTERS[rank]:
        return await update.message.reply_text("❌ کاراکتر پیدا نشد.")
    stats = get_all_stats(char_name, rank)
    ok, msg = give_character(target_id, char_name, rank, stats.get("hp", 400), stats.get("atk", 60), stats.get("def", 20), stats.get("dodge", 10))
    await update.message.reply_text(msg)

async def resetchar_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_chars"): return
    if not ctx.args: return await update.message.reply_text("Usage: /resetchar <user_id>")
    try: target_id = int(ctx.args[0])
    except ValueError: return await update.message.reply_text("❌ آیدی معتبر بده.")
    ok, msg = reset_character(target_id)
    await update.message.reply_text(msg)

async def owner_panel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return await update.message.reply_text("❌ فقط مالک!")
    text = "👑 **پنل مالک**\n━━━━━━━━━━━━━━━━━━━\n\n"
    text += "👥 /allusers - لیست همه کاربران\n"
    text += "🔄 /resetall - ریست کل پلیرها\n"
    await update.message.reply_text(text)

async def resetall_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return await update.message.reply_text("❌ فقط مالک!")
    total = reset_all_players()
    await update.message.reply_text(f"♻️ همه پلیرها ریست شدن! ({total} کاربر)")

async def post_init(app):
    commands_list = [
        BotCommand("start", "شروع بازی"), BotCommand("profile", "پروفایل"),
        BotCommand("coins", "موجودی سکه"), BotCommand("shop", "شاپ"),
        BotCommand("upgrade", "ارتقای لول"), BotCommand("battle", "باس‌فایت تکی"),
        BotCommand("pvp", "نبرد 1v1"), BotCommand("coop", "نبرد گروهی"),
        BotCommand("world", "دنیای آزاد"), BotCommand("quests", "کوئست روزانه"),
        BotCommand("leaderboard", "لیدربورد"), BotCommand("guild", "کلن"),
        BotCommand("gift", "هدیه دادن"), BotCommand("modes", "مودها"),
        BotCommand("upgradece", "انرژی نفرینی (JJK)"), BotCommand("upgraderei", "ریستو (Bleach)"),
        BotCommand("upgradegeass", "گیاس (Code Geass)"), BotCommand("upgradehaki", "هاکی (One Piece)"),
        BotCommand("upgradechakra", "چاکرا (Naruto)"), BotCommand("upgradeki", "کی (Dragon Ball)"),
        BotCommand("upgrademana", "مانا (Solo)"), BotCommand("upgradenen", "نن (Hunter)"),
        BotCommand("upgrademushoku", "مانا (Mushoku)"), BotCommand("upgraderc", "RC (Tokyo Ghoul)"),
        BotCommand("upgrademagic", "جادو (SDS)"), BotCommand("upgradestamina", "استقامت (Sakamoto)"),
        BotCommand("upgradetitan", "قدرت تایتان (AOT)"), BotCommand("upgradebcmana", "مانا (Black Clover)"),
        BotCommand("upgradebloodlust", "خون‌آشامی (Berserk)"), BotCommand("upgradebreath", "نفس (Demon Slayer)"),
        BotCommand("upgradeblood", "خون (Chainsaw Man)"), BotCommand("upgradeopm", "قدرت مطلق (OPM)"),
        BotCommand("help", "راهنما"),
    ]
    await app.bot.set_my_commands(commands_list)

def main():
    init_db()
    init_multi_table()
    try:
        init_quests_table()
    except Exception:
        pass

    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # ============ COMMANDS ============
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("coins", coins))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("select", select))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("buychar", buychar))
    app.add_handler(CommandHandler("upgrade", upgrade))
    app.add_handler(CommandHandler("battle", battle))
    app.add_handler(CommandHandler("pvp", pvp))
    app.add_handler(CommandHandler("joinpvp", join_pvp))
    app.add_handler(CommandHandler("coop", coop))
    app.add_handler(CommandHandler("join", join_coop))
    app.add_handler(CommandHandler("startcoop", start_coop))
    app.add_handler(CommandHandler("guild", guild_cmd))
    app.add_handler(CommandHandler("guild_create", guild_create))
    app.add_handler(CommandHandler("guild_join", guild_join))
    app.add_handler(CommandHandler("guild_leave", guild_leave))
    app.add_handler(CommandHandler("guild_donate", guild_donate))
    app.add_handler(CommandHandler("guild_upgrade", guild_upgrade))
    app.add_handler(CommandHandler("guild_members", guild_members_cmd))
    app.add_handler(CommandHandler("guild_kick", guild_kick))
    app.add_handler(CommandHandler("guild_list", guild_list))
    app.add_handler(CommandHandler("guild_leaderboard", guild_leaderboard))
    app.add_handler(CommandHandler("world", world_cmd))
    app.add_handler(CommandHandler("quests", quests_cmd))
    app.add_handler(CommandHandler("claim", claim))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("gift", send_gift))
    app.add_handler(CommandHandler("help", help_cmd))

    # 🆕 MODES Commands
    app.add_handler(CommandHandler("modes", modes_cmd))
    app.add_handler(CommandHandler("castle", castle_cmd))
    app.add_handler(CommandHandler("zombie", zombie_cmd))
    app.add_handler(CommandHandler("tower", tower_cmd))

    # 🆕 Energy Upgrade Commands
    app.add_handler(CommandHandler("upgradece", upgrade_ce))
    app.add_handler(CommandHandler("upgraderei", upgrade_rei))
    app.add_handler(CommandHandler("upgradegeass", upgrade_geass))
    app.add_handler(CommandHandler("upgradehaki", upgrade_haki))
    app.add_handler(CommandHandler("upgradechakra", upgrade_chakra))
    app.add_handler(CommandHandler("upgradeki", upgrade_ki))
    app.add_handler(CommandHandler("upgrademana", upgrade_mana))
    app.add_handler(CommandHandler("upgradenen", upgrade_nen))
    app.add_handler(CommandHandler("upgrademushoku", upgrade_mushoku_mana))
    app.add_handler(CommandHandler("upgraderc", upgrade_rc))
    app.add_handler(CommandHandler("upgrademagic", upgrade_magic))
    app.add_handler(CommandHandler("upgradestamina", upgrade_stamina))
    app.add_handler(CommandHandler("upgradetitan", upgrade_titan))
    app.add_handler(CommandHandler("upgradebcmana", upgrade_bcmana))
    app.add_handler(CommandHandler("upgradebloodlust", upgrade_bloodlust))
    app.add_handler(CommandHandler("upgradebreath", upgrade_breath))
    app.add_handler(CommandHandler("upgradeblood", upgrade_blood))
    app.add_handler(CommandHandler("upgradeopm", upgrade_opm))

    # 🆕 Admin & Owner Commands
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("give", give_cmd))
    app.add_handler(CommandHandler("take", take_cmd))
    app.add_handler(CommandHandler("userinfo", userinfo_cmd))
    app.add_handler(CommandHandler("allusers", allusers_cmd))
    app.add_handler(CommandHandler("resetuser", resetuser_cmd))
    app.add_handler(CommandHandler("ban", ban_cmd))
    app.add_handler(CommandHandler("unban", unban_cmd))
    app.add_handler(CommandHandler("addadmin", addadmin_cmd))
    app.add_handler(CommandHandler("removeadmin", removeadmin_cmd))
    app.add_handler(CommandHandler("listadmins", listadmins_cmd))
    app.add_handler(CommandHandler("givechar", givechar_cmd))
    app.add_handler(CommandHandler("resetchar", resetchar_cmd))
    app.add_handler(CommandHandler("ownerpanel", owner_panel))
    app.add_handler(CommandHandler("resetall", resetall_cmd))

    # ============ MESSAGE HANDLERS ============
    app.add_handler(MessageHandler(filters.PHOTO & filters.CaptionRegex(r'^/setcharimage'), setcharimage_cmd))

    # ============ CALLBACK HANDLERS ============
    app.add_handler(CallbackQueryHandler(first_char_callback, pattern="^first_"))
    app.add_handler(CallbackQueryHandler(profile_callback, pattern="^prof_"))
    app.add_handler(CallbackQueryHandler(select_callback, pattern="^sel_"))
    app.add_handler(CallbackQueryHandler(shop_callback, pattern="^shop_"))
    app.add_handler(CallbackQueryHandler(shop_anime_callback, pattern="^shchanime_"))
    app.add_handler(CallbackQueryHandler(shop_char_rank_callback, pattern="^shchrank_"))
    app.add_handler(CallbackQueryHandler(buy_char_callback, pattern="^buych_"))
    app.add_handler(CallbackQueryHandler(buy_ability_callback, pattern="^buyab_"))
    app.add_handler(CallbackQueryHandler(buy_item_callback, pattern="^buyit_"))
    app.add_handler(CallbackQueryHandler(buy_buff_callback, pattern="^buybf_"))
    
    # Battle
    app.add_handler(CallbackQueryHandler(solo_callback, pattern="^solo_"))
    app.add_handler(CallbackQueryHandler(bosses_anime_callback, pattern="^bosses_"))
    app.add_handler(CallbackQueryHandler(battle_back_callback, pattern="^battle_back$"))
    app.add_handler(CallbackQueryHandler(action_callback, pattern="^act_"))
    app.add_handler(CallbackQueryHandler(item_use_callback, pattern="^it_"))
    app.add_handler(CallbackQueryHandler(shop_ability_use_callback, pattern="^shopab_"))
    app.add_handler(CallbackQueryHandler(shop_buff_use_callback, pattern="^shopbf_"))
    
    # Coop & Multi
    app.add_handler(CallbackQueryHandler(coop_boss_callback, pattern="^coopboss_"))
    app.add_handler(CallbackQueryHandler(multi_action_callback, pattern="^mb_(attack|defend|dodge|ab1|ab2|ab3)_"))
    
    # World
    app.add_handler(CallbackQueryHandler(world_region_callback, pattern="^world_(forest|desert|mountain|volcano|dungeon)$"))
    app.add_handler(CallbackQueryHandler(world_explore_callback, pattern="^explore_"))
    app.add_handler(CallbackQueryHandler(world_progress_callback, pattern="^world_progress$"))
    app.add_handler(CallbackQueryHandler(world_treasures_callback, pattern="^world_treasures$"))
    app.add_handler(CallbackQueryHandler(world_back_callback, pattern="^world_back$"))
    
    # Guild & Leaderboard
    app.add_handler(CallbackQueryHandler(guild_callback, pattern="^guild_"))
    app.add_handler(CallbackQueryHandler(leaderboard_callback, pattern="^lb_"))

    # Modes
    app.add_handler(CallbackQueryHandler(castle_callback, pattern="^modes_castle$"))
    app.add_handler(CallbackQueryHandler(zombie_callback, pattern="^modes_zombie$"))
    app.add_handler(CallbackQueryHandler(tower_callback, pattern="^modes_tower$"))
    app.add_handler(CallbackQueryHandler(castle_callback, pattern="^castle_start_"))
    app.add_handler(CallbackQueryHandler(zombie_callback, pattern="^zombie_start_"))
    app.add_handler(CallbackQueryHandler(tower_callback, pattern="^tower_start_"))
    app.add_handler(CallbackQueryHandler(castle_callback, pattern="^modes_back$"))

    # Arise
    app.add_handler(CallbackQueryHandler(arise_callback, pattern="^arise_show$"))
    app.add_handler(CallbackQueryHandler(shadows_back_callback, pattern="^shadows_back$"))

    print("🤖 Bot Started!")
    app.run_polling()

if __name__ == "__main__":
    main()