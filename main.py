from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from config import *
from database import (init_db, get_user, add_coins, get_coins,
                      create_battle, get_battle, update_battle, end_battle,
                      get_abilities, get_items, use_item)
from characters import (create_character, get_user_characters,
                        get_active_character, set_active, buy_character)
from shop import buy_ability, buy_item, buy_buff, buy_slot, upgrade_character
from battle import (player_attack, player_defend, player_dodge,
                    player_ability, player_item, build_battle_message,
                    finish_battle)
from multi_battle import (init_multi_table, create_multi_battle, get_multi_battle,
                          update_multi_battle, end_multi_battle, player_action,
                          finish_multi_battle, build_battle_view)
from quests import (init_quests_table, reset_daily_quests,
                    update_quest_progress, get_user_quests, claim_quest, QUESTS)
from leaderboard import get_top_by_coins, get_top_by_level, get_top_by_rank
from images import IMAGES, SHOP_IMAGE
from admin import (is_admin, get_all_users, get_user_stats,
                   give_coins, take_coins, reset_user,
                   ban_user, unban_user, is_banned)
from gift import send_gift, get_gift_history, get_top_givers

PVP_SESSIONS = {}
TEAM_SESSIONS = {}
COOP_SESSIONS = {}

BATTLE_KB = [
    [InlineKeyboardButton("⚔️ حمله", callback_data="act_attack"),
     InlineKeyboardButton("🛡️ دفاع", callback_data="act_defend")],
    [InlineKeyboardButton("💨 جاخالی", callback_data="act_dodge"),
     InlineKeyboardButton("🔥 Ability", callback_data="act_ability")],
    [InlineKeyboardButton("🌀 گسترش قلمرو", callback_data="act_domain")],
    [InlineKeyboardButton("💊 آیتم", callback_data="act_item"),
     InlineKeyboardButton("🏳️ تسلیم", callback_data="act_surrender")],
]

COMMAND_DESCRIPTIONS = {
    "start": "شروع بازی و انتخاب کاراکتر",
    "profile": "پروفایل و آمار کاراکتر",
    "select": "انتخاب کاراکتر فعال",
    "coins": "موجودی سکه",
    "shop": "منوی شاپ (Ability, Item, Buff, Character)",
    "buy": "خرید Ability/Item/Buff — /buy <name>",
    "upgrade": "ارتقای Level کاراکتر",
    "battle": "باس‌فایت تکی (نوبتی)",
    "coop": "نبرد گروهی با یه رفیق (نوبتی)",
    "join": "پیوستن به Co-op — /join <session>",
    "startcoop": "شروع Co-op — /startcoop <session>",
    "pvp": "نبرد 1v1 با یه کاربر (نوبتی)",
    "joinpvp": "پیوستن به PvP — /joinpvp <session>",
    "team": "نبرد تیمی — /team <2-4>",
    "jointeam": "پیوستن به تیم — /jointeam <session> <1|2>",
    "startteam": "شروع نبرد تیمی — /startteam <session>",
    "quests": "کوئست‌های روزانه",
    "claim": "دریافت جایزه کوئست — /claim <key>",
    "leaderboard": "جدول برترین‌ها",
    "help": "همین پیام",
    "gift": "هدیه دادن Coin — /gift <amount> یا /gift <user_id> <amount>",
    "gifthistory": "تاریخچه هدیه‌های تو",
    "topgivers": "برترین هدیه‌دهنده‌ها",
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
            "🎮 به ONE PUNCH MEN RP خوش اومدی!\n\n"
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
        f"دستورات:\n"
        f"/profile — پروفایل\n"
        f"/shop — شاپ\n"
        f"/battle — باس‌فایت نوبتی\n"
        f"/quests — کوئست روزانه\n"
        f"/leaderboard — جدول\n"
        f"/help — راهنما"
    )


async def profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character. /start")
        return
    text = (
        f"Character: {char[2]} ({char[3]} Rank)\n"
        f"Level: {char[4]}\n"
        f"HP: {char[5]}\n"
        f"ATK: {char[6]}\n"
        f"DEF: {char[7]}\n"
        f"DODGE: {char[8]}%\n"
        f"Slots: {char[9]}\n"
        f"Coins: {get_coins(user_id)}"
    )
    await update.message.reply_text(text)


async def coins(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    c = get_coins(update.effective_user.id)
    await update.message.reply_text(f"Coins: {c}")


async def shop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🛡️ Ability", callback_data="shop_ab")],
        [InlineKeyboardButton("💊 آیتم", callback_data="shop_item")],
        [InlineKeyboardButton("🔥 باف", callback_data="shop_buff")],
        [InlineKeyboardButton("🦸 کاراکترها", callback_data="shop_char")],
    ]
    try:
        await update.message.reply_photo(
            photo=SHOP_IMAGE,
            caption="🏪 شاپ:\nیه دسته انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(kb)
        )
    except Exception:
        await update.message.reply_text(
            "🏪 شاپ:\nیه دسته انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(kb)
        )


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
                    photo=SHOP_IMAGE,
                    caption=caption,
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
            price = info["price"]
            kb.append([InlineKeyboardButton(
                f"{fa} — {price} 💰",
                callback_data=f"buyab_{name}"
            )])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🛡️ Ability ها:\nیه Ability انتخاب کن:", kb)

    elif data == "shop_item":
        kb = []
        for name, info in ITEMS.items():
            fa = ITEM_FA.get(name, name)
            price = info["price"]
            kb.append([InlineKeyboardButton(
                f"{fa} — {price} 💰",
                callback_data=f"buyit_{name}"
            )])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "💊 آیتم‌ها:\nیه آیتم انتخاب کن:", kb)

    elif data == "shop_buff":
        kb = []
        for name, info in BUFFS.items():
            fa = BUFF_FA.get(name, name)
            price = info["price"]
            kb.append([InlineKeyboardButton(
                f"{fa} — {price} 💰",
                callback_data=f"buybf_{name}"
            )])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🔥 باف‌ها:\nیه باف انتخاب کن:", kb)

    elif data == "shop_char":
        kb = []
        for rank, chars in CHARACTERS.items():
            kb.append([InlineKeyboardButton(
                f"📦 {rank} Rank — {CHAR_PRICES[rank]} 💰",
                callback_data=f"shchrank_{rank}"
            )])
        kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_main")])
        await edit_shop_msg(q, "🦸 کاراکترها:\nیه رنک انتخاب کن:", kb)

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
        await q.answer("❌ کاراکتر فعال نداری. /start", show_alert=True)
        return
    result = buy_ability(user_id, char[2], ability_name)
    fa = ABILITY_FA.get(ability_name, ability_name)
    await q.answer(f"{fa}\n{result}", show_alert=True)


async def buy_item_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    item_name = q.data.replace("buyit_", "")
    user_id = q.from_user.id
    result = buy_item(user_id, item_name)
    fa = ITEM_FA.get(item_name, item_name)
    await q.answer(f"{fa}\n{result}", show_alert=True)


async def buy_buff_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    buff_name = q.data.replace("buybf_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.answer("❌ کاراکتر فعال نداری.", show_alert=True)
        return
    result = buy_buff(user_id, char[2], buff_name)
    fa = BUFF_FA.get(buff_name, buff_name)
    await q.answer(f"{fa}\n{result}", show_alert=True)


async def shop_char_rank_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    rank = q.data.replace("shchrank_", "")
    kb = []
    for name, title in CHARACTERS[rank].items():
        price = CHAR_PRICES[rank]
        kb.append([InlineKeyboardButton(
            f"{name} ({title}) — {price} 💰",
            callback_data=f"buych_{name}_{rank}"
        )])
    kb.append([InlineKeyboardButton("🔙 بازگشت", callback_data="shop_char")])
    await edit_shop_msg(q, f"🦸 {rank} Rank — کاراکتر انتخاب کن:", kb)


async def buy_char_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data.replace("buych_", "")
    parts = data.rsplit("_", 1)
    char_name = parts[0]
    rank = parts[1]
    user_id = q.from_user.id
    result = buy_character(user_id, char_name, rank)
    await q.answer(f"{char_name} ({rank})\n{result}", show_alert=True)


async def buychar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("از /shop استفاده کن!")


async def select(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chars = get_user_characters(user_id)
    if not chars:
        await update.message.reply_text("No characters.")
        return
    kb = [[InlineKeyboardButton(f"{c[2]} ({c[3]}) Lv{c[4]}", callback_data=f"sel_{c[0]}")]
          for c in chars]
    await update.message.reply_text("Select active:", reply_markup=InlineKeyboardMarkup(kb))


async def select_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    char_id = int(q.data.replace("sel_", ""))
    set_active(q.from_user.id, char_id)
    await q.message.reply_text("Character selected!")


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
        await update.message.reply_text("No active character.")
        return
    msg = upgrade_character(user_id, char[0])
    update_quest_progress(user_id, "level_up_1")
    await update.message.reply_text(msg)
  

# ============ BOSS BATTLE (TURN-BASED) ============

async def battle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    kb = [[InlineKeyboardButton(name, callback_data=f"solo_{name}")] for name in BOSSES]
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
        end_battle(existing[0])

    boss = BOSSES[boss_name]
    create_battle(user_id, boss_name, char[5], boss["hp"])

    battle_data = get_battle(user_id)
    text = build_battle_message(battle_data, char)

    if boss_name == "Saitama Phase 1":
        try:
            await q.message.reply_photo(photo=IMAGES["saitama_normal"])
        except Exception:
            pass
    elif boss_name.startswith("Goku"):
        try:
            await q.message.reply_photo(photo=IMAGES["goku_normal"])
        except Exception:
            pass

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
        end_battle(battle[0])
        try:
            await q.edit_message_text("🏳️ تسلیم شدی!")
        except Exception:
            await q.message.reply_text("🏳️ تسلیم شدی!")
        return

    if action == "attack":
        status, text, php, bhp = player_attack(battle, char)
    elif action == "defend":
        status, text, php, bhp = player_defend(battle, char)
    elif action == "dodge":
        status, text, php, bhp = player_dodge(battle, char)
    elif action == "ability":
        abilities = get_abilities(user_id, char[2])
        if not abilities:
            await q.answer("❌ Ability نداری.", show_alert=True)
            return
        kb = []
        for a in abilities:
            fa = ABILITY_FA.get(a, a)
            kb.append([InlineKeyboardButton(fa, callback_data=f"ab_{a}")])
        await q.message.reply_text("🔥 Ability انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
        return
    elif action == "item":
        items = get_items(user_id)
        if not items:
            await q.answer("❌ آیتم نداری.", show_alert=True)
            return
        kb = []
        for n, c in items:
            fa = ITEM_FA.get(n, n)
            kb.append([InlineKeyboardButton(f"{fa} (x{c})", callback_data=f"it_{n}")])
        await q.message.reply_text("💊 آیتم انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
        return 
elif action == "domain":
    from domain_system import has_domain, can_use_domain
    if not has_domain(char[2]):
        await q.answer("❌ این کاراکتر گسترش قلمرو نداره!", show_alert=True)
        return

    allowed, msg = can_use_domain(battle, char[2])
    if not allowed:
        await q.answer(msg, show_alert=True)
        return

    status, text, php, bhp = player_ability(battle, char, "DOMAIN")

    if status == "won":
        reward = finish_battle(user_id, battle[2], True)
        end_battle(battle[0])
        try:
            await q.edit_message_text(f"{text}\n\n🏆 بردی!\n💰 +{reward} coin")
        except Exception:
            await q.message.reply_text(f"{text}\n\n🏆 بردی!\n💰 +{reward} coin")
        return
    elif status == "lost":
        end_battle(battle[0])
        try:
            await q.edit_message_text(f"{text}\n\n💀 باختی!")
        except Exception:
            await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return

    update_battle(battle[0], php, bhp, 0, 0, 'active')
    new_battle = get_battle(user_id)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(new_battle, char)
    await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))
    return

    else:
        return

    if status == "won":
        reward = finish_battle(user_id, battle[2], True)
        end_battle(battle[0])
        msg = f"{text}\n\n🏆 بردی!\n💰 +{reward} coin"
        try:
            await q.edit_message_text(msg)
        except Exception:
            await q.message.reply_text(msg)
        return
    elif status == "lost":
        end_battle(battle[0])
        msg = f"{text}\n\n💀 باختی!"
        try:
            await q.edit_message_text(msg)
        except Exception:
            await q.message.reply_text(msg)
        return

    update_battle(battle[0], php, bhp, 0, 0, 'active')
    new_battle = get_battle(user_id)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(new_battle, char)

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

    status, text, php, bhp = player_ability(battle, char, ability_name)

    if status == "won":
        reward = finish_battle(user_id, battle[2], True)
        end_battle(battle[0])
        msg = f"{text}\n\n🏆 بردی!\n💰 +{reward} coin"
        try:
            await q.edit_message_text(msg)
        except Exception:
            await q.message.reply_text(msg)
        return
    elif status == "lost":
        end_battle(battle[0])
        msg = f"{text}\n\n💀 باختی!"
        try:
            await q.edit_message_text(msg)
        except Exception:
            await q.message.reply_text(msg)
        return

    update_battle(battle[0], php, bhp, 0, 0, 'active')
    new_battle = get_battle(user_id)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(new_battle, char)

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

    status, text, php, bhp = player_item(battle, char, item_name)

    if status == "won":
        reward = finish_battle(user_id, battle[2], True)
        end_battle(battle[0])
        msg = f"{text}\n\n🏆 بردی!\n💰 +{reward} coin"
        try:
            await q.edit_message_text(msg)
        except Exception:
            await q.message.reply_text(msg)
        return
    elif status == "lost":
        end_battle(battle[0])
        msg = f"{text}\n\n💀 باختی!"
        try:
            await q.edit_message_text(msg)
        except Exception:
            await q.message.reply_text(msg)
        return

    update_battle(battle[0], php, bhp, 0, 0, 'active')
    new_battle = get_battle(user_id)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(new_battle, char)

    if len(full_text) > 3500:
        full_text = full_text[:3500] + "..."

    try:
        await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))
    except Exception:
        await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(BATTLE_KB))


# ============ CO-OP ============

async def coop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    kb = [[InlineKeyboardButton(name, callback_data=f"coopboss_{name}")] for name in BOSSES]
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
        f"👥 Co-op session for {boss_name}\n"
        f"Session ID: {session_id}\n"
        f"Others: /join {session_id}\n"
        f"Host: /startcoop {session_id} when ready."
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
    char = get_active_character(user_id)
    if not char:
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
    boss = BOSSES[s["boss"]]

    team1 = [
        {"uid": p1_id, "name": char1[2], "hp": char1[5], "max_hp": char1[5],
         "atk": char1[6], "def": char1[7], "dodge": char1[8],
         "defending": 0, "dodged_next": 0},
        {"uid": p2_id, "name": char2[2], "hp": char2[5], "max_hp": char2[5],
         "atk": char2[6], "def": char2[7], "dodge": char2[8],
         "defending": 0, "dodged_next": 0},
    ]

    create_multi_battle(
        session_id=session_id,
        battle_type="coop",
        host_id=s["host"],
        players=[p1_id, p2_id],
        team1=team1,
        team2=[],
        boss_name=s["boss"],
        boss_hp=boss["hp"]
    )

    battle = get_multi_battle(session_id)
    view = build_battle_view(battle)
    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"mb_attack_{session_id}"),
         InlineKeyboardButton("🛡️ دفاع", callback_data=f"mb_defend_{session_id}")],
        [InlineKeyboardButton("💨 جاخالی", callback_data=f"mb_dodge_{session_id}")],
    [InlineKeyboardButton("🌀 گسترش قلمرو", callback_data=f"mb_domain_{session_id}")],
  ]
    await update.message.reply_text(view, reply_markup=InlineKeyboardMarkup(kb))
  

# ============ PVP ============

async def pvp(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    session_id = f"pvp_{user_id}"
    PVP_SESSIONS[session_id] = {"host": user_id, "opponent": None}
    await update.message.reply_text(
        f"⚔️ PvP session created!\nSession ID: {session_id}\n"
        f"Opponent: /joinpvp {session_id}"
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

    team1 = [{"uid": s["host"], "name": char_host[2], "hp": char_host[5],
              "max_hp": char_host[5], "atk": char_host[6], "def": char_host[7],
              "dodge": char_host[8], "defending": 0, "dodged_next": 0}]
    team2 = [{"uid": user_id, "name": char[2], "hp": char[5], "max_hp": char[5],
              "atk": char[6], "def": char[7], "dodge": char[8],
              "defending": 0, "dodged_next": 0}]

    create_multi_battle(
        session_id=session_id,
        battle_type="pvp",
        host_id=s["host"],
        players=[s["host"], user_id],
        team1=team1,
        team2=team2
    )

    battle = get_multi_battle(session_id)
    view = build_battle_view(battle)
    kb = [
    [InlineKeyboardButton("⚔️ حمله", callback_data=f"mb_attack_{session_id}"),
     InlineKeyboardButton("🛡️ دفاع", callback_data=f"mb_defend_{session_id}")],
    [InlineKeyboardButton("💨 جاخالی", callback_data=f"mb_dodge_{session_id}")],
    [InlineKeyboardButton("🌀 گسترش قلمرو", callback_data=f"mb_domain_{session_id}")],
]    
  await update.message.reply_text(view, reply_markup=InlineKeyboardMarkup(kb))


# ============ TEAM BATTLE ============

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
    TEAM_SESSIONS[session_id] = {
        "host": user_id, "size": size,
        "team1": [(user_id, char)], "team2": []
    }
    await update.message.reply_text(
        f"👥 Team Battle ({size}v{size})!\nSession: {session_id}\n"
        f"Join T1: /jointeam {session_id} 1\n"
        f"Join T2: /jointeam {session_id} 2\n"
        f"Start: /startteam {session_id}"
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
        await update.message.reply_text(f"Joined Team 1 ({len(s['team1'])}/{s['size']})")
    elif team_num == 2:
        if len(s["team2"]) >= s["size"]:
            await update.message.reply_text("Team 2 full.")
            return
        s["team2"].append((user_id, char))
        await update.message.reply_text(f"Joined Team 2 ({len(s['team2'])}/{s['size']})")


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

    team1 = [{"uid": u, "name": c[2], "hp": c[5], "max_hp": c[5],
              "atk": c[6], "def": c[7], "dodge": c[8],
              "defending": 0, "dodged_next": 0} for u, c in s["team1"]]
    team2 = [{"uid": u, "name": c[2], "hp": c[5], "max_hp": c[5],
              "atk": c[6], "def": c[7], "dodge": c[8],
              "defending": 0, "dodged_next": 0} for u, c in s["team2"]]

    all_ids = [p["uid"] for p in team1 + team2]

    create_multi_battle(
        session_id=session_id,
        battle_type="team",
        host_id=s["host"],
        players=all_ids,
        team1=team1,
        team2=team2
    )

    battle = get_multi_battle(session_id)
    view = build_battle_view(battle)
    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"mb_attack_{session_id}"),
         InlineKeyboardButton("🛡️ دفاع", callback_data=f"mb_defend_{session_id}")],
            [InlineKeyboardButton("💨 جاخالی", callback_data=f"mb_dodge_{session_id}")],
    [InlineKeyboardButton("🌀 گسترش قلمرو", callback_data=f"mb_domain_{session_id}")],
]
    await update.message.reply_text(view, reply_markup=InlineKeyboardMarkup(kb))


# ============ MULTI ACTION HANDLER ============

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
            text = "🏆 نبرد تموم شد!\n\n"
            for uid, amount in result["rewards"].items():
                text += f"👤 {uid}: +{amount} coin\n"
            try:
                await q.edit_message_text(text)
            except Exception:
                await q.message.reply_text(text)
        else:
            try:
                await q.edit_message_text("🏆 نبرد تموم شد!")
            except Exception:
                await q.message.reply_text("🏆 نبرد تموم شد!")
        return

    battle = get_multi_battle(session_id)
    if not battle:
        try:
            await q.edit_message_text("❌ نبرد یافت نشد.")
        except Exception:
            await q.message.reply_text("❌ نبرد یافت نشد.")
        return

    view = build_battle_view(battle)

    log_lines = log.split("\n")
    if len(log_lines) > 5:
        log = "\n".join(log_lines[-5:])

    full_text = f"{log}\n\n{view}"
    if len(full_text) > 3500:
        full_text = full_text[:3500] + "..."

    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"mb_attack_{session_id}"),
         InlineKeyboardButton("🛡️ دفاع", callback_data=f"mb_defend_{session_id}")],
            [InlineKeyboardButton("💨 جاخالی", callback_data=f"mb_dodge_{session_id}")],
    [InlineKeyboardButton("🌀 گسترش قلمرو", callback_data=f"mb_domain_{session_id}")],
    ]
  
    try:
        await q.edit_message_text(full_text, reply_markup=InlineKeyboardMarkup(kb))
    except Exception:
        await q.message.reply_text(full_text, reply_markup=InlineKeyboardMarkup(kb))


# ============ QUESTS ============

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


# ============ LEADERBOARD ============

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
            text += f"{i}. {name or 'Unknown'} - {coins} coins\n"
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
      

# ============ ADMIN ============

async def admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ تو ادمین نیستی!")
        return

    text = (
        "👑 پنل ادمین\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "💰 مدیریت سکه:\n"
        "  /give <user_id> <amount> — سکه بده\n"
        "  /take <user_id> <amount> — سکه بگیر\n\n"
        "👤 مدیریت کاربران:\n"
        "  /userinfo <user_id> — آمار کاربر\n"
        "  /allusers — لیست کاربران\n"
        "  /resetuser <user_id> — ریست کاربر\n"
        "  /ban <user_id> — بن\n"
        "  /unban <user_id> — آنبن\n"
    )
    await update.message.reply_text(text)


async def give_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /give <user_id> <amount>")
        return
    try:
        target_id = int(ctx.args[0])
        amount = int(ctx.args[1])
    except ValueError:
        await update.message.reply_text("❌ اعداد معتبر بده.")
        return
    give_coins(target_id, amount)
    await update.message.reply_text(f"✅ {amount} coin به {target_id} دادی.")


async def take_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /take <user_id> <amount>")
        return
    try:
        target_id = int(ctx.args[0])
        amount = int(ctx.args[1])
    except ValueError:
        await update.message.reply_text("❌ اعداد معتبر بده.")
        return
    if take_coins(target_id, amount):
        await update.message.reply_text(f"✅ {amount} coin از {target_id} گرفتی.")
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
    text = f"👤 کاربر: {user[0] or 'Unknown'}\n"
    text += f"🆔 ID: {target_id}\n"
    text += f"💰 Coins: {user[1]}\n\n"
    text += "🦸 کاراکترها:\n"
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
        text += f"{i}. {name or 'Unknown'} ({uid}) — {coins} 💰\n"
    if len(rows) > 30:
        text += f"\n... و {len(rows) - 30} نفر دیگه"
    await update.message.reply_text(text)


async def resetuser_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /resetuser <user_id>")
        return
    try:
        target_id = int(ctx.args[0])
    except ValueError:
        await update.message.reply_text("❌ آیدی معتبر بده.")
        return
    reset_user(target_id)
    await update.message.reply_text(f"♻️ کاربر {target_id} ریست شد.")


async def ban_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
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
    if not is_admin(update.effective_user.id):
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


# ============ GIFT ============

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
            target_id = int(ctx.args[0])
            amount = int(ctx.args[1])
        except ValueError:
            await update.message.reply_text("❌ اعداد معتبر بده.")
            return
        msg = send_gift(user_id, target_id, amount)
        await update.message.reply_text(msg)
        return

    await update.message.reply_text(
        "🎁 چطوری هدیه بدم:\n\n"
        "روش ۱: روی پیام کاربر ریپلای کن و بنویس:\n"
        "  /gift 500\n\n"
        "روش ۲: با آیدی عددی:\n"
        "  /gift 123456789 500"
    )


async def gift_history(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    rows = get_gift_history(user_id, 10)
    if not rows:
        await update.message.reply_text("📭 هیچ هدیه‌ای نداری.")
        return

    text = "🎁 تاریخچه هدیه‌ها:\n\n"
    for from_id, to_id, amount, date in rows:
        if from_id == user_id:
            text += f"📤 تو → {to_id}: {amount} 💰\n"
        else:
            text += f"📥 {from_id} → تو: {amount} 💰\n"
    await update.message.reply_text(text)


async def top_givers(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    rows = get_top_givers(10)
    if not rows:
        await update.message.reply_text("📭 هنوز کسی هدیه نداده.")
        return

    text = "🏆 برترین هدیه‌دهنده‌ها:\n\n"
    for i, (uid, total) in enumerate(rows, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {uid} — {total} 💰\n"
    await update.message.reply_text(text)
  

# ============ HELP ============

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = "🎮 ONE PUNCH MEN RP — راهنما\n"
    text += "━━━━━━━━━━━━━━━━━━━\n\n"

    categories = {
    "👤 حساب کاربری": ["start", "profile", "select", "coins"],
    "🏪 شاپ و خرید": ["shop", "buy", "upgrade"],
    "⚔️ نبرد": ["battle", "coop", "join", "startcoop",
                "pvp", "joinpvp", "team", "jointeam", "startteam"],
    "📜 کوئست و رتبه": ["quests", "claim", "leaderboard"],
    "🎁 هدیه": ["gift", "gifthistory", "topgivers"],
    "❓ راهنما": ["help"],
}

    for cat_name, cmds in categories.items():
        text += f"{cat_name}:\n"
        for c in cmds:
            desc = COMMAND_DESCRIPTIONS.get(c, "—")
            text += f"  /{c} — {desc}\n"
        text += "\n"

    text += "━━━━━━━━━━━━━━━━━━━\n"
    text += "💡 برای شروع: /start"
    await update.message.reply_text(text)


# ============ MAIN ============

def main():
    init_db()
    init_quests_table()
    init_multi_table()
    app = Application.builder().token(BOT_TOKEN).build()

    handlers = [
        ("start", start),
        ("profile", profile),
        ("shop", shop),
        ("buy", buy),
        ("buychar", buychar),
        ("select", select),
        ("upgrade", upgrade),
        ("battle", battle),
        ("coop", coop),
        ("join", join_coop),
        ("startcoop", start_coop),
        ("pvp", pvp),
        ("joinpvp", join_pvp),
        ("team", team),
        ("jointeam", join_team),
        ("startteam", start_team),
        ("quests", quests_cmd),
        ("claim", claim),
        ("leaderboard", leaderboard),
        ("coins", coins),
        ("help", help_cmd),
        ("gift", gift),
        ("gifthistory", gift_history),
        ("topgivers", top_givers),
        ("admin", admin),
        ("give", give_cmd),
        ("take", take_cmd),
        ("userinfo", userinfo_cmd),
        ("allusers", allusers_cmd),
        ("resetuser", resetuser_cmd),
        ("ban", ban_cmd),
        ("unban", unban_cmd),
    ]
    for cmd, fn in handlers:
        app.add_handler(CommandHandler(cmd, fn))

    callbacks = [
        ("^first_", first_char_callback),
        ("^mb_", multi_action_callback),
        ("^act_", action_callback),
        ("^ab_", ability_use_callback),
        ("^it_", item_use_callback),
        ("^sel_", select_callback),
        ("^shop_", shop_callback),
        ("^buyab_", buy_ability_callback),
        ("^buyit_", buy_item_callback),
        ("^buybf_", buy_buff_callback),
        ("^shchrank_", shop_char_rank_callback),
        ("^buych_", buy_char_callback),
        ("^solo_", solo_callback),
        ("^coopboss_", coop_boss_callback),
        ("^lb_", leaderboard_callback),
    ]
    for pattern, fn in callbacks:
        app.add_handler(CallbackQueryHandler(fn, pattern=pattern))

    print("Bot Started")
    app.run_polling()


if __name__ == "__main__":
    main()
