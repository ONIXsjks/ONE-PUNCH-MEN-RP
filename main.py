from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, BotCommand
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          CallbackQueryHandler, MessageHandler, filters)
from config import *
from database import (init_db, get_user, add_coins, get_coins,
                      create_battle, get_battle, update_battle, end_battle,
                      get_abilities, get_items, use_item, get_username,
                      get_user_guild, get_top_guilds)
from characters import (create_character, get_user_characters,
                        get_active_character, set_active, buy_character)
from shop import buy_ability, buy_item, buy_buff, buy_slot, upgrade_character
from guild import (create_new_guild, join_existing_guild, leave_current_guild,
                   donate, try_upgrade_guild, kick_member, give_guild_xp,
                   format_guild, format_members, GUILD_CREATE_COST, GUILD_MIN_LEVEL)
from battle import (player_attack, player_defend, player_dodge,
                    player_ability, player_item, build_battle_message,
                    finish_battle)
from multi_battle import (init_multi_table, create_multi_battle, get_multi_battle,
                          update_multi_battle, end_multi_battle, player_action,
                          finish_multi_battle, build_battle_view, get_player)
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
from gift import send_gift, get_gift_history, get_top_givers
from jjk_data import (CHARACTERS_JJK, BOSSES_JJK, FODDER_JJK,
                      DOMAINS_JJK, ABILITIES_JJK)
from bleach_data import (CHARACTERS_BLEACH, CHAR_PRICES_BLEACH,
                         BLEACH_ABILITIES_SHOP, BLEACH_BANKAI,
                         BLEACH_BOSSES, BLEACH_FODDER)
from opm_data import (CHARACTERS_OPM, ABILITIES_OPM, BOSSES_OPM)
from jjk_stats import JJK_STATS
from bleach_stats import BLEACH_STATS
from opm_stats import OPM_STATS


PVP_SESSIONS = {}
TEAM_SESSIONS = {}
COOP_SESSIONS = {}


def get_all_stats(char_name, rank):
    for stats_dict in [JJK_STATS, BLEACH_STATS, OPM_STATS]:
        if char_name in stats_dict:
            return stats_dict[char_name]
    return RANK_STATS.get(rank, RANK_STATS["C"])


def get_char_price(char_name, rank):
    stats = get_all_stats(char_name, rank)
    if "price" in stats:
        return stats["price"]
    return CHAR_PRICES.get(rank, 8000)


BATTLE_KB = [
    [InlineKeyboardButton("⚔️ حمله", callback_data="act_attack"),
     InlineKeyboardButton("🛡️ دفاع", callback_data="act_defend")],
    [InlineKeyboardButton("💨 جاخالی", callback_data="act_dodge"),
     InlineKeyboardButton("🔥 Ability", callback_data="act_ability")],
    [InlineKeyboardButton("🌀 گسترش قلمرو", callback_data="act_domain")],
    [InlineKeyboardButton("⚔️ Bankai", callback_data="act_bankai")],
    [InlineKeyboardButton("💊 آیتم", callback_data="act_item"),
     InlineKeyboardButton("🏳️ تسلیم", callback_data="act_surrender")],
]


def get_multi_kb(session_id):
    return [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"mb_attack_{session_id}"),
         InlineKeyboardButton("🛡️ دفاع", callback_data=f"mb_defend_{session_id}")],
        [InlineKeyboardButton("💨 جاخالی", callback_data=f"mb_dodge_{session_id}")],
        [InlineKeyboardButton("🌀 گسترش قلمرو", callback_data=f"mb_domain_{session_id}")],
        [InlineKeyboardButton("🔥 Ability", callback_data=f"mb_ability_{session_id}"),
         InlineKeyboardButton("🔥 باف", callback_data=f"mb_buff_{session_id}")],
        [InlineKeyboardButton("⚔️ Bankai", callback_data=f"mb_bankai_{session_id}")],
    ]


COMMAND_DESCRIPTIONS = {
    "start": "شروع بازی", "profile": "پروفایل", "coins": "موجودی سکه",
    "shop": "شاپ", "upgrade": "ارتقای لول", "battle": "باس‌فایت تکی",
    "pvp": "نبرد 1v1", "team": "نبرد تیمی", "coop": "نبرد گروهی",
    "quests": "کوئست روزانه", "leaderboard": "لیدربورد", "guild": "کلن",
    "gift": "هدیه دادن", "jjk": "جوجوتسو", "opm": "One-Punch Man", "help": "راهنما",
}
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id, user.username)
    reset_daily_quests(user.id)
    chars = get_user_characters(user.id)
    if not chars:
        kb = []
        for c_name, c_title in CHARACTERS["C"].items():
            kb.append([InlineKeyboardButton(
                f"{c_name} — {c_title}",
                callback_data=f"first_{c_name}"
            )])
        await update.message.reply_text(
            "🎮 به BANG BANG RP خوش اومدی!\n\n"
            "یه کاراکتر رایگان انتخاب کن (C Rank):",
            reply_markup=InlineKeyboardMarkup(kb)
        )
    else:
        await update.message.reply_text("Welcome back! /help")


async def first_char_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    char_name = q.data.replace("first_", "")
    user_id = q.from_user.id

    existing = get_user_characters(user_id)
    if existing:
        await q.message.reply_text("❌ تو قبلاً یه کاراکتر انتخاب کردی!")
        return

    if char_name not in CHARACTERS["C"]:
        await q.message.reply_text("❌ کاراکتر نامعتبر.")
        return

    create_character(user_id, char_name, "C")
    chars = get_user_characters(user_id)
    set_active(user_id, chars[0][0])

    await q.message.reply_text(
        f"✅ کاراکتر {char_name} (C Rank) انتخاب شد!\n\n"
        f"/profile\n/shop\n/battle\n/help"
    )


async def profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری. /start بزن.")
        return

    user = get_user(user_id)
    username = user[1] if user and user[1] else "ناشناس"

    char_name = char[2]
    rank = char[3]
    level = char[4]
    hp = char[5]
    atk = char[6]
    dfn = char[7]
    dodge = char[8]
    slots = char[9]

    has_domain = "✅" if char_name in DOMAINS_JJK else "❌"
    domain_name = ""
    if char_name in DOMAINS_JJK:
        domain_name = f" - {DOMAINS_JJK[char_name]['name']}"
    has_bankai = "✅" if char_name in BLEACH_BANKAI else "❌"
    bankai_name = ""
    if char_name in BLEACH_BANKAI:
        bankai_name = f" - {BLEACH_BANKAI[char_name]['name']}"

    text = (
        f"╔══════════════════════════╗\n"
        f"║      👤 @{username[:14].center(14)} ║\n"
        f"╚══════════════════════════╝\n\n"
        f"╭───── 🎭 کاراکتر فعال ─────╮\n"
        f"│ 🦸 {char_name[:18].ljust(18)} │\n"
        f"│ ⭐ Rank: {rank.ljust(14)} │\n"
        f"│ 📊 Level: {str(level).ljust(13)} │\n"
        f"╰────────────────────────────╯\n\n"
        f"⚔️ آمار کاراکتر:\n"
        f"├ ❤️ HP: {hp:,}\n"
        f"├ ⚔️ ATK: {atk:,}\n"
        f"├ 🛡️ DEF: {dfn:,}\n"
        f"├ 💨 DODGE: {dodge}%\n"
        f"└ 🎰 Slots: {slots}\n\n"
        f"🔥 قابلیت‌ها:\n"
        f"├ 🌀 Domain: {has_domain}{domain_name}\n"
        f"└ ⚔️ Bankai: {has_bankai}{bankai_name}\n\n"
        f"💰 سکه: {get_coins(user_id):,}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    kb = [
        [InlineKeyboardButton("🎭 تغییر کاراکتر", callback_data="prof_select"),
         InlineKeyboardButton("📜 کوئست‌ها", callback_data="prof_quests")],
        [InlineKeyboardButton("🏆 لیدربورد", callback_data="prof_lb"),
         InlineKeyboardButton("🎁 هدیه", callback_data="prof_gift")],
        [InlineKeyboardButton("⚔️ نبرد سریع", callback_data="prof_battle"),
         InlineKeyboardButton("🏰 کلن", callback_data="prof_guild")],
    ]

    img = get_char_image(char_name)
    if img:
        try:
            await update.message.reply_photo(photo=img, caption=text, reply_markup=InlineKeyboardMarkup(kb))
            return
        except Exception:
            pass
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def profile_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "prof_select":
        user_id = q.from_user.id
        chars = get_user_characters(user_id)
        if not chars:
            await q.message.reply_text("❌ کاراکتری نداری.")
            return
        kb = [[InlineKeyboardButton(f"{c[2]} ({c[3]}) Lv{c[4]}", callback_data=f"sel_{c[0]}")] for c in chars]
        await q.message.reply_text("🎭 انتخاب کاراکتر فعال:", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "prof_quests":
        await q.message.reply_text("📜 برای دیدن کوئست‌ها: /quests")

    elif data == "prof_lb":
        kb = [
            [InlineKeyboardButton("Top by Coins", callback_data="lb_coins")],
            [InlineKeyboardButton("Top by Level", callback_data="lb_level")],
            [InlineKeyboardButton("Top by Rank", callback_data="lb_rank")],
        ]
        await q.message.reply_text("🏆 لیدربورد:", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "prof_gift":
        await q.message.reply_text(
            "🎁 برای هدیه دادن:\n\n"
            "روش ۱: روی پیام کسی ریپلای کن و بنویس:\n"
            "  /gift 500\n\n"
            "روش ۲: با آیدی:\n"
            "  /gift 123456789 500"
        )

    elif data == "prof_battle":
        await q.message.reply_text("⚔️ برای نبرد: /battle")

    elif data == "prof_guild":
        guild = get_user_guild(q.from_user.id)
        if not guild:
            await q.message.reply_text(
                f"🏰 تو توی هیچ کلنی نیستی!\n\n📝 ساخت: /guild_create <name>\n💰 هزینه: {GUILD_CREATE_COST:,}"
            )
            return
        text = format_guild(guild)
        kb = [
            [InlineKeyboardButton("👥 اعضا", callback_data="guild_members"),
             InlineKeyboardButton("💰 دونیت", callback_data="guild_donate_info")],
            [InlineKeyboardButton("🔼 ارتقا", callback_data="guild_upgrade"),
             InlineKeyboardButton("🚪 خروج", callback_data="guild_leave")],
            [InlineKeyboardButton("🏆 رتبه‌بندی", callback_data="guild_top")],
        ]
        await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def coins(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    c = get_coins(update.effective_user.id)
    await update.message.reply_text(f"Coins: {c:,}")
async def shop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🛡️ Ability", callback_data="shop_ab")],
        [InlineKeyboardButton("💊 آیتم", callback_data="shop_item")],
        [InlineKeyboardButton("🔥 باف", callback_data="shop_buff")],
        [InlineKeyboardButton("🦸 کاراکترها", callback_data="shop_char")],
    ]
    try:
        await update.message.reply_photo(
            photo=SHOP_IMAGE, caption="🏪 شاپ:\nیه دسته انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(kb)
        )
    except Exception:
        await update.message.reply_text("🏪 شاپ:\nیه دسته انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))


async def edit_shop_msg(q, caption, keyboard):
    try:
        await q.edit_message_media(
            media=InputMediaPhoto(media=SHOP_IMAGE, caption=caption),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception:
        try:
            await q.edit_message_caption(caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
            try:
                await q.edit_message_text(caption, reply_markup=InlineKeyboardMarkup(keyboard))
            except Exception:
                await q.message.reply_photo(
                    photo=SHOP_IMAGE, caption=caption,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )


async def shop_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "shop_ab":
        kb = []
        for name, info in ABILITIES.items():
            fa = ABILITY_FA.get(name, name)
            kb.append([InlineKeyboardButton(f"{fa} — {info['price']:,} 💰", callback_data=f"buyab_{name}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🛡️ Ability ها:", kb)

    elif data == "shop_item":
        kb = []
        for name, info in ITEMS.items():
            fa = ITEM_FA.get(name, name)
            kb.append([InlineKeyboardButton(f"{fa} — {info['price']:,} 💰", callback_data=f"buyit_{name}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "💊 آیتم‌ها:", kb)

    elif data == "shop_buff":
        kb = []
        for name, info in BUFFS.items():
            fa = BUFF_FA.get(name, name)
            kb.append([InlineKeyboardButton(f"{fa} — {info['price']:,} 💰", callback_data=f"buybf_{name}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🔥 باف‌ها:", kb)

    elif data == "shop_char":
        kb = []
        for rank, chars in CHARACTERS.items():
            kb.append([InlineKeyboardButton(f"📦 {rank} Rank", callback_data=f"shchrank_{rank}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🦸 کاراکترها:", kb)

    elif data == "shop_main":
        kb = [
            [InlineKeyboardButton("🛡️ Ability", callback_data="shop_ab")],
            [InlineKeyboardButton("💊 آیتم", callback_data="shop_item")],
            [InlineKeyboardButton("🔥 باف", callback_data="shop_buff")],
            [InlineKeyboardButton("🦸 کاراکترها", callback_data="shop_char")],
        ]
        await edit_shop_msg(q, "🏪 شاپ:\nیه دسته انتخاب کن:", kb)


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


async def shop_char_rank_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rank = q.data.replace("shchrank_", "")
    kb = []
    for name, title in CHARACTERS[rank].items():
        price = get_char_price(name, rank)
        kb.append([InlineKeyboardButton(f"{name} ({title}) — {price:,} 💰", callback_data=f"buych_{name}_{rank}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_char")])
    await edit_shop_msg(q, f"🦸 {rank} Rank:", kb)


async def buy_char_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data.replace("buych_", "")
    parts = data.rsplit("_", 1)
    char_name = parts[0]
    rank = parts[1]
    result = buy_character(q.from_user.id, char_name, rank)
    if "Not enough" in str(result) or "کافی" in str(result):
        await q.message.reply_text(f"❌ {char_name}\n💰 پولت کمه!")
    else:
        await q.message.reply_text(f"✅ {char_name} ({rank})\n🎉 خریدی!")


async def buychar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("از /shop استفاده کن!")


async def select(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chars = get_user_characters(user_id)
    if not chars:
        await update.message.reply_text("No characters.")
        return
    kb = [[InlineKeyboardButton(f"{c[2]} ({c[3]}) Lv{c[4]}", callback_data=f"sel_{c[0]}")] for c in chars]
    await update.message.reply_text("Select active:", reply_markup=InlineKeyboardMarkup(kb))


async def select_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    char_id = int(q.data.replace("sel_", ""))
    set_active(q.from_user.id, char_id)
    await q.message.reply_text("✅ کاراکتر فعال عوض شد!")


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
async def guild_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    guild = get_user_guild(user_id)
    if not guild:
        await update.message.reply_text(
            "🏰 تو توی هیچ کلنی نیستی!\n\n"
            "📝 ساخت: /guild_create <name>\n🔍 پیوستن: /guild_join <name>\n"
            "📋 لیست: /guild_list\n\n"
            f"💰 هزینه: {GUILD_CREATE_COST:,} سکه\n⭐ حداقل لول: {GUILD_MIN_LEVEL}"
        )
        return
    text = format_guild(guild)
    kb = [
        [InlineKeyboardButton("👥 اعضا", callback_data="guild_members"),
         InlineKeyboardButton("💰 دونیت", callback_data="guild_donate_info")],
        [InlineKeyboardButton("🔼 ارتقا", callback_data="guild_upgrade"),
         InlineKeyboardButton("🚪 خروج", callback_data="guild_leave")],
        [InlineKeyboardButton("🏆 رتبه‌بندی", callback_data="guild_top")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def guild_create(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not ctx.args:
        await update.message.reply_text("❌ Usage: /guild_create <name>")
        return
    name = " ".join(ctx.args)
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری!")
        return
    msg = create_new_guild(user_id, name, char[4])
    await update.message.reply_text(msg)


async def guild_join(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("❌ Usage: /guild_join <name>")
        return
    msg = join_existing_guild(update.effective_user.id, " ".join(ctx.args))
    await update.message.reply_text(msg)


async def guild_leave(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = leave_current_guild(update.effective_user.id)
    await update.message.reply_text(msg)


async def guild_donate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("❌ Usage: /guild_donate <amount>")
        return
    try:
        amount = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ عدد معتبر بده!")
        return
    msg = donate(update.effective_user.id, amount)
    await update.message.reply_text(msg)


async def guild_upgrade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = try_upgrade_guild(update.effective_user.id)
    await update.message.reply_text(msg)


async def guild_members_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    guild = get_user_guild(update.effective_user.id)
    if not guild:
        await update.message.reply_text("❌ تو توی کلنی نیستی!")
        return
    await update.message.reply_text(format_members(guild))


async def guild_kick(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("❌ Usage: /guild_kick <user_id>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده!")
        return
    msg = kick_member(update.effective_user.id, target_id)
    await update.message.reply_text(msg)


async def guild_list(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    guilds = get_top_guilds(10)
    if not guilds:
        await update.message.reply_text("📭 هنوز هیچ کلنی ساخته نشده!")
        return
    text = "🏰 کلن‌های برتر:\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, g in enumerate(guilds, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {g[1]} — سطح {g[3]} | 👥 {g[6]}\n"
    await update.message.reply_text(text)


async def guild_leaderboard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    guilds = get_top_guilds(10)
    if not guilds:
        await update.message.reply_text("📭 هنوز هیچ کلنی ساخته نشده!")
        return
    text = "🏆 برترین کلن‌ها:\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, g in enumerate(guilds, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {g[1]}\n   ⭐ سطح {g[3]} | ⚡ {g[4]:,} XP | 💰 {g[5]:,}\n\n"
    await update.message.reply_text(text)


async def guild_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    user_id = q.from_user.id

    if data == "guild_members":
        guild = get_user_guild(user_id)
        if not guild:
            await q.message.reply_text("❌ تو توی کلنی نیستی!")
            return
        await q.message.reply_text(format_members(guild))

    elif data == "guild_donate_info":
        await q.message.reply_text(
            "💰 دونیت به خزانه کلن\n\n"
            "دستور: /guild_donate <amount>\nمثال: /guild_donate 50000\n\n"
            "🎁 هر ۵۰,۰۰۰ سکه = ۵ XP به کلن"
        )

    elif data == "guild_upgrade":
        await q.message.reply_text(try_upgrade_guild(user_id))

    elif data == "guild_leave":
        await q.message.reply_text(leave_current_guild(user_id))

    elif data == "guild_top":
        guilds = get_top_guilds(10)
        if not guilds:
            await q.message.reply_text("📭 هنوز هیچ کلنی ساخته نشده!")
            return
        text = "🏆 برترین کلن‌ها:\n━━━━━━━━━━━━━━━━━━━\n\n"
        for i, g in enumerate(guilds, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {g[1]} — سطح {g[3]} | 👥 {g[6]}\n"
        await q.message.reply_text(text)
async def battle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    kb = []
    for name in BOSSES:
        kb.append([InlineKeyboardButton(name, callback_data=f"solo_{name}")])
    for name, data in BOSSES_JJK.items():
        kb.append([InlineKeyboardButton(f"👹 {data.get('display_name', name)}", callback_data=f"solo_{name}")])
    for name, data in BLEACH_BOSSES.items():
        kb.append([InlineKeyboardButton(f"⚔️ {data.get('display_name', name)}", callback_data=f"solo_{name}")])
    for name, data in BOSSES_OPM.items():
        kb.append([InlineKeyboardButton(f"💪 {data.get('display_name', name)}", callback_data=f"solo_{name}")])
    await update.message.reply_text("⚔️ باس انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))


async def solo_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    boss_name = q.data.replace("solo_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.message.reply_text("No active character.")
        return
    existing = get_battle(user_id)
    if existing:
        end_battle(existing["id"])

    if boss_name in BLEACH_BOSSES:
        create_battle(user_id, boss_name, char[5], BLEACH_BOSSES[boss_name]["hp"])
    elif boss_name in BLEACH_FODDER:
        create_battle(user_id, boss_name, char[5], BLEACH_FODDER[boss_name]["hp"])
    elif boss_name in BOSSES_JJK:
        create_battle(user_id, boss_name, char[5], BOSSES_JJK[boss_name]["hp"])
    elif boss_name in FODDER_JJK:
        create_battle(user_id, boss_name, char[5], FODDER_JJK[boss_name]["hp"])
    elif boss_name in BOSSES_OPM:
        create_battle(user_id, boss_name, char[5], BOSSES_OPM[boss_name]["hp"])
    elif boss_name in BOSSES:
        create_battle(user_id, boss_name, char[5], BOSSES[boss_name]["hp"])
    else:
        await q.message.reply_text("❌ باس پیدا نشد.")
        return
    battle_data = get_battle(user_id)
    text = build_battle_message(battle_data, char)
    await q.message.reply_text(text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))


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
        try:
            await q.edit_message_text("🏳️ تسلیم شدی!")
        except Exception:
            await q.message.reply_text("🏳️ تسلیم شدی!")
        return
    if action == "attack":
        status, text, battle = player_attack(battle, char)
    elif action == "defend":
        status, text, battle = player_defend(battle, char)
    elif action == "dodge":
        status, text, battle = player_dodge(battle, char)
    elif action == "ability":
        abilities = get_abilities(user_id, char[2])
        if not abilities:
            await q.answer("❌ Ability نداری.", show_alert=True)
            return
        kb = [[InlineKeyboardButton(ABILITY_FA.get(a, a), callback_data=f"ab_{a}")] for a in abilities]
        await q.message.reply_text("🔥 Ability انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
        return
    elif action == "item":
        items = get_items(user_id)
        if not items:
            await q.answer("❌ آیتم نداری.", show_alert=True)
            return
        kb = [[InlineKeyboardButton(f"{ITEM_FA.get(n, n)} (x{c})", callback_data=f"it_{n}")] for n, c in items]
        await q.message.reply_text("💊 آیتم انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
        return
    elif action == "domain":
        if char[2] not in DOMAINS_JJK:
            await q.answer("❌ این کاراکتر Domain نداره!", show_alert=True)
            return
        status, text, battle = player_ability(battle, char, "DOMAIN")
    elif action == "bankai":
        if char[2] not in BLEACH_BANKAI:
            await q.answer("❌ این کاراکتر Bankai نداره!", show_alert=True)
            return
        status, text, battle = player_ability(battle, char, "BANKAI")
    else:
        return

    if status == "won":
        reward = finish_battle(user_id, battle["boss_name"], True)
        end_battle(battle["id"])
        try:
            await q.edit_message_text(f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin")
        except Exception:
            await q.message.reply_text(f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin")
        return
    elif status == "lost":
        end_battle(battle["id"])
        try:
            await q.edit_message_text(f"{text}\n\n💀 باختی!")
        except Exception:
            await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return
    update_battle(battle)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
    if len(full_text) > 3500:
        full_text = full_text[:3500] + "..."
    try:
        await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))
    except Exception:
        await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))


async def ability_use_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ability_name = q.data.replace("ab_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    battle = get_battle(user_id)
    if not battle:
        return
    status, text, battle = player_ability(battle, char, ability_name)
    if status == "won":
        reward = finish_battle(user_id, battle["boss_name"], True)
        end_battle(battle["id"])
        try:
            await q.edit_message_text(f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin")
        except Exception:
            await q.message.reply_text(f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin")
        return
    elif status == "lost":
        end_battle(battle["id"])
        try:
            await q.edit_message_text(f"{text}\n\n💀 باختی!")
        except Exception:
            await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return
    update_battle(battle)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
    if len(full_text) > 3500:
        full_text = full_text[:3500] + "..."
    try:
        await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))
    except Exception:
        await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))


async def item_use_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    item_name = q.data.replace("it_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    battle = get_battle(user_id)
    if not battle:
        return
    if not use_item(user_id, item_name):
        await q.message.reply_text("❌ آیتم نداری.")
        return
    status, text, battle = player_item(battle, char, item_name)
    if status == "won":
        reward = finish_battle(user_id, battle["boss_name"], True)
        end_battle(battle["id"])
        try:
            await q.edit_message_text(f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin")
        except Exception:
            await q.message.reply_text(f"{text}\n\n🏆 بردی!\n💰 +{reward:,} coin")
        return
    elif status == "lost":
        end_battle(battle["id"])
        try:
            await q.edit_message_text(f"{text}\n\n💀 باختی!")
        except Exception:
            await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return
    update_battle(battle)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(battle, char)
    if len(full_text) > 3500:
        full_text = full_text[:3500] + "..."
    try:
        await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))
    except Exception:
        await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))
async def coop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    kb = []
    for name in BOSSES:
        kb.append([InlineKeyboardButton(name, callback_data=f"coopboss_{name}")])
    for name, data in BOSSES_JJK.items():
        kb.append([InlineKeyboardButton(f"👹 {data.get('display_name', name)}", callback_data=f"coopboss_{name}")])
    for name, data in BLEACH_BOSSES.items():
        kb.append([InlineKeyboardButton(f"⚔️ {data.get('display_name', name)}", callback_data=f"coopboss_{name}")])
    for name, data in BOSSES_OPM.items():
        kb.append([InlineKeyboardButton(f"💪 {data.get('display_name', name)}", callback_data=f"coopboss_{name}")])
    await update.message.reply_text("👥 Co-op - Host chooses boss:", reply_markup=InlineKeyboardMarkup(kb))


async def coop_boss_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    boss_name = q.data.replace("coopboss_", "")
    host_id = q.from_user.id
    safe_boss = boss_name.replace(" ", "_").replace("+", "plus")
    session_id = f"coop_{host_id}_{safe_boss}"
    COOP_SESSIONS[session_id] = {"host": host_id, "boss": boss_name, "players": [host_id]}
    await q.message.reply_text(
        f"👥 Co-op: {boss_name}\nSession: {session_id}\n"
        f"Others: /join {session_id}\nHost: /startcoop {session_id}"
    )


async def join_coop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /join <session_id>")
        return
    session_id = ctx.args[0]
    if session_id not in COOP_SESSIONS:
        await update.message.reply_text("Session not found.")
        return
    user_id = update.effective_user.id
    if not get_active_character(user_id):
        await update.message.reply_text("Need active character.")
        return
    s = COOP_SESSIONS[session_id]
    if user_id in s["players"]:
        await update.message.reply_text("Already joined!")
        return
    if len(s["players"]) >= 2:
        await update.message.reply_text("Session full.")
        return
    s["players"].append(user_id)
    await update.message.reply_text("✅ Joined!")


async def start_coop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /startcoop <session_id>")
        return
    session_id = ctx.args[0]
    if session_id not in COOP_SESSIONS:
        await update.message.reply_text("Session not found.")
        return
    s = COOP_SESSIONS[session_id]
    if update.effective_user.id != s["host"]:
        await update.message.reply_text("Only host can start.")
        return
    if len(s["players"]) < 2:
        await update.message.reply_text("Need 2 players.")
        return
    p1_id, p2_id = s["players"][0], s["players"][1]
    char1 = get_active_character(p1_id)
    char2 = get_active_character(p2_id)
    boss_hp = 5000
    if s["boss"] in BLEACH_BOSSES:
        boss_hp = BLEACH_BOSSES[s["boss"]]["hp"]
    elif s["boss"] in BOSSES_JJK:
        boss_hp = BOSSES_JJK[s["boss"]]["hp"]
    elif s["boss"] in BOSSES_OPM:
        boss_hp = BOSSES_OPM[s["boss"]]["hp"]
    elif s["boss"] in BOSSES:
        boss_hp = BOSSES[s["boss"]]["hp"]
    team1 = [
        {"uid": p1_id, "name": char1[2], "display": get_username(p1_id),
         "hp": char1[5], "max_hp": char1[5], "atk": char1[6], "def": char1[7],
         "dodge": char1[8], "defending": 0, "dodged_next": 0},
        {"uid": p2_id, "name": char2[2], "display": get_username(p2_id),
         "hp": char2[5], "max_hp": char2[5], "atk": char2[6], "def": char2[7],
         "dodge": char2[8], "defending": 0, "dodged_next": 0},
    ]
    create_multi_battle(session_id=session_id, battle_type="coop",
                        host_id=s["host"], players=[p1_id, p2_id],
                        team1=team1, team2=[], boss_name=s["boss"], boss_hp=boss_hp)
    battle = get_multi_battle(session_id)
    await update.message.reply_text(build_battle_view(battle), reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))


async def pvp(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not get_active_character(user_id):
        await update.message.reply_text("No active character.")
        return
    session_id = f"pvp_{user_id}"
    PVP_SESSIONS[session_id] = {"host": user_id, "opponent": None}
    await update.message.reply_text(
        f"⚔️ PvP session: {session_id}\nOpponent: /joinpvp {session_id}"
    )


async def join_pvp(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /joinpvp <session_id>")
        return
    session_id = ctx.args[0]
    if session_id not in PVP_SESSIONS:
        await update.message.reply_text("Not found.")
        return
    s = PVP_SESSIONS[session_id]
    user_id = update.effective_user.id
    if user_id == s["host"]:
        await update.message.reply_text("Can't fight yourself.")
        return
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    char_host = get_active_character(s["host"])
    team1 = [{"uid": s["host"], "name": char_host[2], "display": get_username(s["host"]),
              "hp": char_host[5], "max_hp": char_host[5], "atk": char_host[6],
              "def": char_host[7], "dodge": char_host[8], "defending": 0, "dodged_next": 0}]
    team2 = [{"uid": user_id, "name": char[2], "display": get_username(user_id),
              "hp": char[5], "max_hp": char[5], "atk": char[6], "def": char[7],
              "dodge": char[8], "defending": 0, "dodged_next": 0}]
    create_multi_battle(session_id=session_id, battle_type="pvp", host_id=s["host"],
                        players=[s["host"], user_id], team1=team1, team2=team2)
    battle = get_multi_battle(session_id)
    await update.message.reply_text(build_battle_view(battle), reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))


async def team(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /team <size 2-4>")
        return
    try:
        size = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("Size must be number.")
        return
    if size < 2 or size > 4:
        await update.message.reply_text("Size must be 2-4.")
        return
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    session_id = f"team_{user_id}_{size}"
    TEAM_SESSIONS[session_id] = {"host": user_id, "size": size,
                                 "team1": [(user_id, char)], "team2": []}
    await update.message.reply_text(
        f"👥 Team Battle ({size}v{size})\nSession: {session_id}\n"
        f"T1: /jointeam {session_id} 1\nT2: /jointeam {session_id} 2\nStart: /startteam {session_id}"
    )


async def join_team(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /jointeam <session_id> <1|2>")
        return
    session_id = ctx.args[0]
    try:
        team_num = int(ctx.args[1])
    except ValueError:
        await update.message.reply_text("Team must be 1 or 2.")
        return
    if session_id not in TEAM_SESSIONS:
        await update.message.reply_text("Not found.")
        return
    s = TEAM_SESSIONS[session_id]
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    all_players = [p[0] for p in s["team1"]] + [p[0] for p in s["team2"]]
    if user_id in all_players:
        await update.message.reply_text("Already joined.")
        return
    if team_num == 1:
        if len(s["team1"]) >= s["size"]:
            await update.message.reply_text("Team 1 full.")
            return
        s["team1"].append((user_id, char))
        await update.message.reply_text(f"Joined T1 ({len(s['team1'])}/{s['size']})")
    elif team_num == 2:
        if len(s["team2"]) >= s["size"]:
            await update.message.reply_text("Team 2 full.")
            return
        s["team2"].append((user_id, char))
        await update.message.reply_text(f"Joined T2 ({len(s['team2'])}/{s['size']})")


async def start_team(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /startteam <session_id>")
        return
    session_id = ctx.args[0]
    if session_id not in TEAM_SESSIONS:
        await update.message.reply_text("Not found.")
        return
    s = TEAM_SESSIONS[session_id]
    if update.effective_user.id != s["host"]:
        await update.message.reply_text("Only host can start.")
        return
    if len(s["team1"]) != s["size"] or len(s["team2"]) != s["size"]:
        await update.message.reply_text(f"Need {s['size']} each.")
        return
    team1 = [{"uid": u, "name": c[2], "display": get_username(u),
              "hp": c[5], "max_hp": c[5], "atk": c[6], "def": c[7], "dodge": c[8],
              "defending": 0, "dodged_next": 0} for u, c in s["team1"]]
    team2 = [{"uid": u, "name": c[2], "display": get_username(u),
              "hp": c[5], "max_hp": c[5], "atk": c[6], "def": c[7], "dodge": c[8],
              "defending": 0, "dodged_next": 0} for u, c in s["team2"]]
    all_ids = [p["uid"] for p in team1 + team2]
    create_multi_battle(session_id=session_id, battle_type="team", host_id=s["host"],
                        players=all_ids, team1=team1, team2=team2)
    battle = get_multi_battle(session_id)
    await update.message.reply_text(build_battle_view(battle), reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))


async def multi_action_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    parts = data.split("_", 2)
    action = parts[1]
    session_id = parts[2]
    user_id = q.from_user.id
    status, log = player_action(session_id, user_id, action)
    if status is None:
        await q.answer(log, show_alert=True)
        return
    if status in ("won", "team1_won", "team2_won", "draw"):
        result = finish_multi_battle(session_id)
        if result:
            if status == "won":
                text = "🏆 بردی!\n\n"
            elif status == "team1_won":
                text = "🏆 Team 1 برنده شد!\n\n"
            elif status == "team2_won":
                text = "🏆 Team 2 برنده شد!\n\n"
            else:
                text = "🤝 مساوی!\n\n"
            text += f"{log}\n\n💰 جوایز:\n"
            for uid, amount in result["rewards"].items():
                text += f"👤 {get_username(uid)}: +{amount:,} coin\n"
            try:
                await q.edit_message_text(text)
            except Exception:
                await q.message.reply_text(text)
        return
    battle = get_multi_battle(session_id)
    if not battle:
        return
    view = build_battle_view(battle)
    log_lines = log.split("\n")
    if len(log_lines) > 5:
        log = "\n".join(log_lines[-5:])
    full_text = f"{log}\n\n{view}"
    if len(full_text) > 3500:
        full_text = full_text[:3500] + "..."
    kb = get_multi_kb(session_id)
    try:
        await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(kb))


async def multi_domain_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    session_id = q.data.replace("mb_domain_", "")
    status, log = player_action(session_id, q.from_user.id, "domain")
    if status is None:
        await q.answer(log, show_alert=True)
        return
    battle = get_multi_battle(session_id)
    if not battle:
        return
    view = build_battle_view(battle)
    try:
        await q.edit_message_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))
    except Exception:
        await q.message.reply_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))


async def multi_bankai_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    session_id = q.data.replace("mb_bankai_", "")
    status, log = player_action(session_id, q.from_user.id, "bankai")
    if status is None:
        await q.answer(log, show_alert=True)
        return
    battle = get_multi_battle(session_id)
    if not battle:
        return
    view = build_battle_view(battle)
    try:
        await q.edit_message_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))
    except Exception:
        await q.message.reply_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))


async def multi_ability_menu_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    session_id = q.data.replace("mb_ability_", "")
    user_id = q.from_user.id
    battle = get_multi_battle(session_id)
    if not battle:
        return
    player, team = get_player(battle, user_id)
    if not player:
        return
    char_name = player["name"]
    kb = []
    jjk_abs = ABILITIES_JJK.get(char_name, {})
    for key in ["ability_1", "ability_2"]:
        if key in jjk_abs:
            ab_name = jjk_abs[key]["name"]
            kb.append([InlineKeyboardButton(ab_name, callback_data=f"mb_abuse_{ab_name}_{session_id}")])
    for ab_name in ABILITIES:
        fa = ABILITY_FA.get(ab_name, ab_name)
        kb.append([InlineKeyboardButton(fa, callback_data=f"mb_abuse_{ab_name}_{session_id}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data=f"mb_back_{session_id}")])
    await q.message.reply_text("🔥 Ability انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))


async def multi_ability_use_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data.replace("mb_abuse_", "")
    parts = data.rsplit("_", 1)
    ability_name = parts[0]
    session_id = parts[1]
    status, log = player_action(session_id, q.from_user.id, "ability", extra=ability_name)
    if status is None:
        await q.answer(log, show_alert=True)
        return
    battle = get_multi_battle(session_id)
    if not battle:
        return
    view = build_battle_view(battle)
    try:
        await q.edit_message_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))
    except Exception:
        await q.message.reply_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))


async def multi_buff_menu_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    session_id = q.data.replace("mb_buff_", "")
    kb = []
    for buff_name in BUFFS:
        fa = BUFF_FA.get(buff_name, buff_name)
        kb.append([InlineKeyboardButton(fa, callback_data=f"mb_buffuse_{buff_name}_{session_id}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data=f"mb_back_{session_id}")])
    await q.message.reply_text("🔥 باف انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))


async def multi_buff_use_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data.replace("mb_buffuse_", "")
    parts = data.rsplit("_", 1)
    buff_name = parts[0]
    session_id = parts[1]
    status, log = player_action(session_id, q.from_user.id, "buff", extra=buff_name)
    if status is None:
        await q.answer(log, show_alert=True)
        return
    battle = get_multi_battle(session_id)
    if not battle:
        return
    view = build_battle_view(battle)
    try:
        await q.edit_message_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))
    except Exception:
        await q.message.reply_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))


async def multi_back_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    session_id = q.data.replace("mb_back_", "")
    battle = get_multi_battle(session_id)
    if not battle:
        await q.answer("نبرد نیست!", show_alert=True)
        return
    view = build_battle_view(battle)
    try:
        await q.edit_message_text(view, reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))
    except Exception:
        await q.message.reply_text(view, reply_markup=InlineKeyboardMarkup(get_multi_kb(session_id)))
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
    text += "\nClaim: /claim <quest_key>"
    await update.message.reply_text(text)


async def claim(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /claim <quest_key>")
        return
    key = ctx.args[0]
    if key not in QUESTS:
        await update.message.reply_text("Invalid quest key.")
        return
    msg = claim_quest(update.effective_user.id, key)
    await update.message.reply_text(msg)


async def leaderboard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("Top by Coins", callback_data="lb_coins")],
        [InlineKeyboardButton("Top by Level", callback_data="lb_level")],
        [InlineKeyboardButton("Top by Rank", callback_data="lb_rank")],
    ]
    await update.message.reply_text("Leaderboard:", reply_markup=InlineKeyboardMarkup(kb))


async def leaderboard_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == "lb_coins":
        rows = get_top_by_coins(10)
        text = "Top 10 by Coins:\n\n"
        for i, (name, coins) in enumerate(rows, 1):
            text += f"{i}. {name or 'Unknown'} - {coins:,}\n"
        await q.message.reply_text(text)
    elif data == "lb_level":
        rows = get_top_by_level(10)
        text = "Top 10 by Level:\n\n"
        for i, (name, char, rank, level) in enumerate(rows, 1):
            text += f"{i}. {name or 'Unknown'} - {char} ({rank}) Lv{level}\n"
        await q.message.reply_text(text)
    elif data == "lb_rank":
        rows = get_top_by_rank(10)
        text = "Top 10 by Rank:\n\n"
        for i, (name, char, rank) in enumerate(rows, 1):
            text += f"{i}. {name or 'Unknown'} - {char} ({rank})\n"
        await q.message.reply_text(text)


async def admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ تو ادمین نیستی!")
        return
    text = "👑 پنل ادمین\n━━━━━━━━━━━━━━━━━━━\n\n"
    if is_owner(user_id):
        text += "🔑 مالک اصلی\n\n"
    text += "💰 /give /take\n👤 /userinfo /allusers /resetuser /ban /unban\n"
    text += "🎭 /givechar /resetchar\n"
    if is_owner(user_id):
        text += "\n👑 /addadmin /removeadmin /listadmins\n"
        text += "📜 /sethelp /viewhelp\n"
        text += "🖼️ عکس + کپشن /setcharimage <name>\n"
        text += "📢 /addchannel /removechannel /listchannels\n"
        text += "🎯 /setquest /viewquests\n"
    await update.message.reply_text(text)


async def give_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_coins"):
        return
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /give <user_id> <amount>")
        return
    try:
        target_id = int(ctx.args[0]); amount = int(ctx.args[1])
    except ValueError:
        await update.message.reply_text("❌ اعداد معتبر بده.")
        return
    give_coins(target_id, amount)
    await update.message.reply_text(f"✅ {amount:,} coin به {target_id} دادی.")


async def take_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_coins"):
        return
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /take <user_id> <amount>")
        return
    try:
        target_id = int(ctx.args[0]); amount = int(ctx.args[1])
    except ValueError:
        await update.message.reply_text("❌ اعداد معتبر بده.")
        return
    if take_coins(target_id, amount):
        await update.message.reply_text(f"✅ {amount:,} coin از {target_id} گرفتی.")
    else:
        await update.message.reply_text("❌ کاربر Coin کافی نداره.")


async def userinfo_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /userinfo <user_id>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    user, chars = get_user_stats(target_id)
    if not user:
        await update.message.reply_text("❌ کاربر پیدا نشد.")
        return
    text = f"👤 {user[0] or 'Unknown'}\n🆔 {target_id}\n💰 {user[1]:,}\n\n🦸 کاراکترها:\n"
    if not chars:
        text += "  ❌ هیچ کاراکتری نداره\n"
    else:
        for c in chars:
            text += f"  • {c[0]} ({c[1]}) Lv{c[2]}\n"
    await update.message.reply_text(text)


async def allusers_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    rows = get_all_users()
    text = f"📋 کل کاربران: {len(rows)}\n\n"
    for i, (uid, name, coins) in enumerate(rows[:30], 1):
        text += f"{i}. {name or 'Unknown'} ({uid}) — {coins:,}\n"
    if len(rows) > 30:
        text += f"\n... و {len(rows) - 30} نفر دیگه"
    await update.message.reply_text(text)


async def resetuser_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_chars"):
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /resetuser <user_id>")
        return
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    reset_user(target_id)
    await update.message.reply_text(f"♻️ کاربر {target_id} ریست شد.")


async def ban_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "ban_users"):
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /ban <user_id>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    ban_user(target_id)
    await update.message.reply_text(f"🚫 کاربر {target_id} بن شد.")


async def unban_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "ban_users"):
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /unban <user_id>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    unban_user(target_id)
    await update.message.reply_text(f"✅ کاربر {target_id} آنبن شد.")


async def gift(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        target_id = target.id
        target_name = target.first_name
        if not ctx.args:
            await update.message.reply_text("❌ مقدار رو بنویس: /gift <amount>")
            return
        try:
            amount = int(ctx.args[0])
        except ValueError:
            await update.message.reply_text("❌ مقدار معتبر بده.")
            return
        msg = send_gift(user_id, target_id, amount)
        await update.message.reply_text(f"🎁 به {target_name}:\n{msg}")
        return
    if len(ctx.args) >= 2:
        try:
            target_id = int(ctx.args[0]); amount = int(ctx.args[1])
        except ValueError:
            await update.message.reply_text("❌ اعداد معتبر بده.")
            return
        msg = send_gift(user_id, target_id, amount)
        await update.message.reply_text(msg)
        return
    await update.message.reply_text("🎁 /gift 500 یا ریپلای + /gift 500")


async def gift_history(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    rows = get_gift_history(user_id, 10)
    if not rows:
        await update.message.reply_text("📭 هیچ هدیه‌ای نداری.")
        return
    text = "🎁 تاریخچه:\n\n"
    for from_id, to_id, amount, date in rows:
        if from_id == user_id:
            text += f"📤 تو → {to_id}: {amount:,}\n"
        else:
            text += f"📥 {from_id} → تو: {amount:,}\n"
    await update.message.reply_text(text)


async def top_givers(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    rows = get_top_givers(10)
    if not rows:
        await update.message.reply_text("📭 هنوز کسی هدیه نداده.")
        return
    text = "🏆 برترین هدیه‌دهنده‌ها:\n\n"
    for i, (uid, total) in enumerate(rows, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {uid} — {total:,}\n"
    await update.message.reply_text(text)
async def addadmin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ فقط مالک!")
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /addadmin <user_id>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    add_admin(target_id, "all", update.effective_user.id)
    await update.message.reply_text(f"✅ {target_id} ادمین شد!")


async def removeadmin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ فقط مالک!")
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /removeadmin <user_id>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    ok, msg = remove_admin(target_id)
    await update.message.reply_text(msg)


async def listadmins_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        return
    admins = list_admins()
    text = "👑 ادمین‌ها:\n\n"
    for uid, role, perms in admins:
        text += f"👤 {uid} — {role} | {perms}\n"
    if not admins:
        text = "📭 هیچ ادمینی اضافه نشده."
    await update.message.reply_text(text)


async def givechar_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_chars"):
        return
    if len(ctx.args) < 3:
        await update.message.reply_text("Usage: /givechar <user_id> <char_name> <rank>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    rank = ctx.args[-1]
    char_name = " ".join(ctx.args[1:-1])
    if rank not in CHARACTERS or char_name not in CHARACTERS[rank]:
        await update.message.reply_text("❌ کاراکتر پیدا نشد.")
        return
    stats = get_all_stats(char_name, rank)
    ok, msg = give_character(target_id, char_name, rank,
                             stats.get("hp", 400), stats.get("atk", 60),
                             stats.get("def", 20), stats.get("dodge", 10))
    await update.message.reply_text(msg)


async def resetchar_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_chars"):
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /resetchar <user_id>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    ok, msg = reset_character(target_id)
    await update.message.reply_text(msg)


async def sethelp_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_help"):
        return
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /sethelp <key> <text>")
        return
    key = ctx.args[0]
    text = " ".join(ctx.args[1:])
    ok, msg = set_help(key, text)
    await update.message.reply_text(msg)


async def viewhelp_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    helps = get_all_help()
    if not helps:
        await update.message.reply_text("📭 هیچ Help ذخیره نشده.")
        return
    text = "📜 Help:\n\n"
    for key, val in helps:
        text += f"🔹 {key}: {val[:50]}\n"
    await update.message.reply_text(text)


async def setcharimage_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_images"):
        return
    if not update.message.photo:
        await update.message.reply_text(
            "❌ عکس بفرست + کپشن:\n/setcharimage <اسم کاراکتر>"
        )
        return
    caption = update.message.caption or ""
    text_part = caption.replace("/setcharimage", "").strip()
    if not text_part:
        await update.message.reply_text("❌ اسم کاراکتر رو توی کپشن بنویس!")
        return
    char_name = text_part
    file_id = update.message.photo[-1].file_id
    found = False
    for rank in CHARACTERS:
        if char_name in CHARACTERS[rank]:
            found = True
            break
    if not found:
        await update.message.reply_text(f"❌ کاراکتر «{char_name}» پیدا نشد!")
        return
    ok, msg = set_char_image(char_name, file_id)
    await update.message.reply_text(msg)


async def addchannel_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_channels"):
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /addchannel <channel_id>")
        return
    ok, msg = add_force_channel(ctx.args[0], ctx.args[0])
    await update.message.reply_text(msg)


async def removechannel_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_channels"):
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /removechannel <channel_id>")
        return
    ok, msg = remove_force_channel(ctx.args[0])
    await update.message.reply_text(msg)


async def listchannels_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    channels = get_force_channels()
    if not channels:
        await update.message.reply_text("📭 هیچ کانالی اضافه نشده.")
        return
    text = "📢 کانال‌ها:\n\n"
    for ch_id, ch_name in channels:
        text += f"🔹 {ch_name} ({ch_id})\n"
    await update.message.reply_text(text)


async def setquest_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_quests"):
        return
    if len(ctx.args) < 3:
        await update.message.reply_text("Usage: /setquest <key> <target> <reward>")
        return
    key = ctx.args[0]
    try:
        target = int(ctx.args[1]); reward = int(ctx.args[2])
    except ValueError:
        await update.message.reply_text("❌ اعداد معتبر بده.")
        return
    ok, msg = set_custom_quest(key, f"کوئست {key}", target, reward)
    await update.message.reply_text(msg)


async def viewquests_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    quests = get_all_custom_quests()
    if not quests:
        await update.message.reply_text("📭 هیچ کوئست سفارشی ذخیره نشده.")
        return
    text = "🎯 کوئست‌های سفارشی:\n\n"
    for key, desc, target, reward in quests:
        text += f"🔹 {key}: {target} — {reward:,}\n"
    await update.message.reply_text(text)
async def jjk_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🛒 کاراکترها", callback_data="jjk_chars")],
        [InlineKeyboardButton("🐾 نوچه‌ها (فارم)", callback_data="jjk_fodder")],
        [InlineKeyboardButton("👹 باس‌های ویژه", callback_data="jjk_bosses")],
    ]
    await update.message.reply_text("🌀 جوجوتسو کایسن\n━━━━━━━━━━━━━━━━━━━\n\nیه بخش انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))


async def jjk_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == "jjk_chars":
        kb = []
        for rank in ["S", "A", "B", "C"]:
            if rank in CHARACTERS_JJK:
                kb.append([InlineKeyboardButton(f"📦 {rank} Rank", callback_data=f"jjkrank_{rank}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="jjk_back")])
        await q.edit_message_text("🛒 کاراکترها:", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "jjk_fodder":
        kb = []
        for fname, fdata in FODDER_JJK.items():
            kb.append([InlineKeyboardButton(f"{fdata['display_name']} (HP {fdata['hp']:,}) — {fdata['reward']:,} 💰", callback_data=f"jjkfodder_{fname}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="jjk_back")])
        await q.edit_message_text("🐾 نوچه‌ها:", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "jjk_bosses":
        kb = []
        for bname, bdata in BOSSES_JJK.items():
            kb.append([InlineKeyboardButton(f"{bdata['display_name']} (HP {bdata['hp']:,})", callback_data=f"jjkboss_{bname}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="jjk_back")])
        await q.edit_message_text("👹 باس‌ها:", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "jjk_back":
        kb = [
            [InlineKeyboardButton("🛒 کاراکترها", callback_data="jjk_chars")],
            [InlineKeyboardButton("🐾 نوچه‌ها (فارم)", callback_data="jjk_fodder")],
            [InlineKeyboardButton("👹 باس‌های ویژه", callback_data="jjk_bosses")],
        ]
        await q.edit_message_text("🌀 جوجوتسو\nیه بخش انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))


async def jjk_rank_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rank = q.data.replace("jjkrank_", "")
    kb = []
    for name, title in CHARACTERS_JJK.get(rank, {}).items():
        price = get_char_price(name, rank)
        kb.append([InlineKeyboardButton(f"{name} — {price:,} 💰", callback_data=f"jjkbuy_{name}_{rank}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="jjk_chars")])
    await q.edit_message_text(f"🦸 {rank} Rank:", reply_markup=InlineKeyboardMarkup(kb))


async def jjk_buy_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data.replace("jjkbuy_", "")
    parts = data.rsplit("_", 1)
    result = buy_character(q.from_user.id, parts[0], parts[1])
    if "Not enough" in str(result) or "کافی" in str(result):
        await q.message.reply_text(f"❌ {parts[0]}\n💰 پولت کمه!")
    else:
        await q.message.reply_text(f"✅ {parts[0]} ({parts[1]})\n🎉 خریدی!")


async def jjk_fodder_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    fodder_name = q.data.replace("jjkfodder_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.answer("❌ کاراکتر فعال نداری.", show_alert=True)
        return
    fdata = FODDER_JJK.get(fodder_name)
    if not fdata:
        return
    existing = get_battle(user_id)
    if existing:
        end_battle(existing["id"])
    create_battle(user_id, fodder_name, char[5], fdata["hp"])
    battle_data = get_battle(user_id)
    await q.message.reply_text(build_battle_message(battle_data, char), reply_markup=InlineKeyboardMarkup(BATTLE_KB))


async def jjk_boss_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    boss_name = q.data.replace("jjkboss_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.answer("❌ کاراکتر فعال نداری.", show_alert=True)
        return
    bdata = BOSSES_JJK.get(boss_name)
    if not bdata:
        return
    existing = get_battle(user_id)
    if existing:
        end_battle(existing["id"])
    create_battle(user_id, boss_name, char[5], bdata["hp"])
    battle_data = get_battle(user_id)
    await q.message.reply_text(build_battle_message(battle_data, char), reply_markup=InlineKeyboardMarkup(BATTLE_KB))


async def opm_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🛒 کاراکترها", callback_data="opm_chars")],
        [InlineKeyboardButton("👹 باس‌ها", callback_data="opm_bosses")],
    ]
    await update.message.reply_text("💪 One-Punch Man\n━━━━━━━━━━━━━━━━━━━\n\nیه بخش انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))


async def opm_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == "opm_chars":
        kb = []
        for rank in ["S", "A", "B", "C"]:
            if rank in CHARACTERS_OPM:
                kb.append([InlineKeyboardButton(f"📦 {rank} Rank", callback_data=f"opmrank_{rank}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="opm_back")])
        await q.edit_message_text("🛒 کاراکترها:", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "opm_bosses":
        kb = []
        for bname, bdata in BOSSES_OPM.items():
            kb.append([InlineKeyboardButton(f"{bdata['display_name']} (HP {bdata['hp']:,})", callback_data=f"opmboss_{bname}")])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="opm_back")])
        await q.edit_message_text("👹 باس‌ها:", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "opm_back":
        kb = [
            [InlineKeyboardButton("🛒 کاراکترها", callback_data="opm_chars")],
            [InlineKeyboardButton("👹 باس‌ها", callback_data="opm_bosses")],
        ]
        await q.edit_message_text("💪 One-Punch Man\nیه بخش انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))


async def opm_rank_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rank = q.data.replace("opmrank_", "")
    kb = []
    for name, title in CHARACTERS_OPM.get(rank, {}).items():
        price = get_char_price(name, rank)
        kb.append([InlineKeyboardButton(f"{name} — {price:,} 💰", callback_data=f"opmbuy_{name}_{rank}")])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="opm_chars")])
    await q.edit_message_text(f"🦸 {rank} Rank:", reply_markup=InlineKeyboardMarkup(kb))


async def opm_buy_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data.replace("opmbuy_", "")
    parts = data.rsplit("_", 1)
    result = buy_character(q.from_user.id, parts[0], parts[1])
    if "Not enough" in str(result) or "کافی" in str(result):
        await q.message.reply_text(f"❌ {parts[0]}\n💰 پولت کمه!")
    else:
        await q.message.reply_text(f"✅ {parts[0]} ({parts[1]})\n🎉 خریدی!")


async def opm_boss_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    boss_name = q.data.replace("opmboss_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.answer("❌ کاراکتر فعال نداری.", show_alert=True)
        return
    bdata = BOSSES_OPM.get(boss_name)
    if not bdata:
        return
    existing = get_battle(user_id)
    if existing:
        end_battle(existing["id"])
    create_battle(user_id, boss_name, char[5], bdata["hp"])
    battle_data = get_battle(user_id)
    await q.message.reply_text(build_battle_message(battle_data, char), reply_markup=InlineKeyboardMarkup(BATTLE_KB))


async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    custom = get_help("general")
    text = "🎮 BANG BANG RP — راهنما\n━━━━━━━━━━━━━━━━━━━\n\n"
    if custom:
        text += f"{custom}\n\n"
    text += "👤 /profile /select /coins\n"
    text += "🏪 /shop /upgrade\n"
    text += "⚔️ /battle /pvp /team /coop\n"
    text += "🏰 /guild\n"
    text += "📜 /quests /leaderboard\n"
    text += "🎁 /gift\n"
    text += "🌀 /jjk\n"
    text += "💪 /opm\n"
    text += "❓ /help\n"
    await update.message.reply_text(text)


async def post_init(app):
    await app.bot.set_my_commands([
        BotCommand("start", "شروع بازی"),
        BotCommand("profile", "پروفایل"),
        BotCommand("coins", "موجودی سکه"),
        BotCommand("shop", "شاپ"),
        BotCommand("upgrade", "ارتقای لول"),
        BotCommand("battle", "باس‌فایت تکی"),
        BotCommand("pvp", "نبرد 1v1"),
        BotCommand("team", "نبرد تیمی"),
        BotCommand("coop", "نبرد گروهی"),
        BotCommand("quests", "کوئست روزانه"),
        BotCommand("leaderboard", "لیدربورد"),
        BotCommand("guild", "کلن"),
        BotCommand("gift", "هدیه دادن"),
        BotCommand("jjk", "جوجوتسو"),
        BotCommand("opm", "One-Punch Man"),
        BotCommand("help", "راهنما"),
    ])


def main():
    init_db()
    init_quests_table()
    init_multi_table()
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    handlers = [
        ("start", start), ("profile", profile), ("shop", shop), ("buy", buy),
        ("buychar", buychar), ("select", select), ("upgrade", upgrade),
        ("battle", battle), ("coop", coop), ("join", join_coop),
        ("startcoop", start_coop), ("pvp", pvp), ("joinpvp", join_pvp),
        ("team", team), ("jointeam", join_team), ("startteam", start_team),
        ("quests", quests_cmd), ("claim", claim), ("leaderboard", leaderboard),
        ("coins", coins), ("help", help_cmd), ("gift", gift),
        ("gifthistory", gift_history), ("topgivers", top_givers),
        ("admin", admin), ("give", give_cmd), ("take", take_cmd),
        ("userinfo", userinfo_cmd), ("allusers", allusers_cmd),
        ("resetuser", resetuser_cmd), ("ban", ban_cmd), ("unban", unban_cmd),
        ("jjk", jjk_menu), ("opm", opm_menu),
        ("guild", guild_cmd), ("guild_create", guild_create),
        ("guild_join", guild_join), ("guild_leave", guild_leave),
        ("guild_donate", guild_donate), ("guild_upgrade", guild_upgrade),
        ("guild_members", guild_members_cmd), ("guild_kick", guild_kick),
        ("guild_list", guild_list), ("guild_leaderboard", guild_leaderboard),
        ("addadmin", addadmin_cmd), ("removeadmin", removeadmin_cmd),
        ("listadmins", listadmins_cmd), ("givechar", givechar_cmd),
        ("resetchar", resetchar_cmd), ("sethelp", sethelp_cmd),
        ("viewhelp", viewhelp_cmd), ("setcharimage", setcharimage_cmd),
        ("addchannel", addchannel_cmd), ("removechannel", removechannel_cmd),
        ("listchannels", listchannels_cmd), ("setquest", setquest_cmd),
        ("viewquests", viewquests_cmd),
    ]
    for cmd, fn in handlers:
        app.add_handler(CommandHandler(cmd, fn))

    # 👇 این خط برای عکس + کپشن مهمه
    app.add_handler(MessageHandler(
        filters.PHOTO & filters.CaptionRegex(r'^/setcharimage'),
        setcharimage_cmd
    ))

    callbacks = [
        ("^first_", first_char_callback), ("^prof_", profile_callback),
        ("^guild_", guild_callback), ("^mb_domain_", multi_domain_callback),
        ("^mb_bankai_", multi_bankai_callback), ("^mb_ability_", multi_ability_menu_callback),
        ("^mb_abuse_", multi_ability_use_callback), ("^mb_buffuse_", multi_buff_use_callback),
        ("^mb_buff_", multi_buff_menu_callback), ("^mb_back_", multi_back_callback),
        ("^mb_", multi_action_callback), ("^act_", action_callback),
        ("^ab_", ability_use_callback), ("^it_", item_use_callback),
        ("^sel_", select_callback), ("^shop_", shop_callback),
        ("^buyab_", buy_ability_callback), ("^buyit_", buy_item_callback),
        ("^buybf_", buy_buff_callback), ("^shchrank_", shop_char_rank_callback),
        ("^buych_", buy_char_callback), ("^solo_", solo_callback),
        ("^coopboss_", coop_boss_callback), ("^lb_", leaderboard_callback),
        ("^jjkrank_", jjk_rank_callback), ("^jjkbuy_", jjk_buy_callback),
        ("^jjkfodder_", jjk_fodder_callback), ("^jjkboss_", jjk_boss_callback),
        ("^jjk_", jjk_callback), ("^opmrank_", opm_rank_callback),
        ("^opmbuy_", opm_buy_callback), ("^opmboss_", opm_boss_callback),
        ("^opm_", opm_callback),
    ]
    for pattern, fn in callbacks:
        app.add_handler(CallbackQueryHandler(fn, pattern=pattern))

    print("Bot Started")
    app.run_polling()


if __name__ == "__main__":
    main()
