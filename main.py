from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
from images import IMAGES

PVP_SESSIONS = {}
TEAM_SESSIONS = {}
COOP_SESSIONS = {}

BATTLE_KB = [
    [InlineKeyboardButton("⚔️ حمله", callback_data="act_attack"),
     InlineKeyboardButton("🛡️ دفاع", callback_data="act_defend")],
    [InlineKeyboardButton("💨 جاخالی", callback_data="act_dodge"),
     InlineKeyboardButton("🔥 Ability", callback_data="act_ability")],
    [InlineKeyboardButton("💊 آیتم", callback_data="act_item"),
     InlineKeyboardButton("🏳️ تسلیم", callback_data="act_surrender")],
]


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id, user.username)
    reset_daily_quests(user.id)
    chars = get_user_characters(user.id)
    if not chars:
        create_character(user.id, "King", "C")
        chars = get_user_characters(user.id)
        set_active(user.id, chars[0][0])
        await update.message.reply_text(
            "Welcome to ONE PUNCH MEN RP!\n"
            "Starter: King (C Rank)\n"
            "Commands: /profile /shop /battle /coop /quests /leaderboard"
        )
    else:
        await update.message.reply_text("Welcome back! /help")


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
        [InlineKeyboardButton("Ability", callback_data="shop_ab")],
        [InlineKeyboardButton("Item", callback_data="shop_item")],
        [InlineKeyboardButton("Buff", callback_data="shop_buff")],
        [InlineKeyboardButton("Characters", callback_data="shop_char")],
    ]
    await update.message.reply_text("SHOP:", reply_markup=InlineKeyboardMarkup(kb))


async def shop_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == "shop_ab":
        text = "Abilities:\n\n"
        for name, info in ABILITIES.items():
            text += f"- {name} | {info['effect']} | {info['price']} coins\n"
        await q.message.reply_text(text)
    elif data == "shop_item":
        text = "Items:\n\n"
        for name, info in ITEMS.items():
            text += f"- {name} | {info['effect']} | {info['price']} coins\n"
        await q.message.reply_text(text)
    elif data == "shop_buff":
        text = "Buffs:\n\n"
        for name, info in BUFFS.items():
            text += f"- {name} | {info['effect']} | {info['price']} coins\n"
        await q.message.reply_text(text)
    elif data == "shop_char":
        text = "Characters:\n\n"
        for rank, chars in CHARACTERS.items():
            text += f"\n{rank} Rank ({CHAR_PRICES[rank]} coins):\n"
            for name, title in chars.items():
                text += f"  - {name} | {title}\n"
        text += "\nBuy: /buychar <name> <rank>"
        await q.message.reply_text(text)


async def buychar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /buychar <name> <rank>")
        return
    rank = ctx.args[-1].upper()
    char_name = " ".join(ctx.args[:-1])
    if rank not in CHARACTERS or char_name not in CHARACTERS[rank]:
        await update.message.reply_text("Invalid character or rank.")
        return
    msg = buy_character(update.effective_user.id, char_name, rank)
    await update.message.reply_text(msg)


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
            await q.message.reply_text("❌ Ability نداری.")
            return
        kb = [[InlineKeyboardButton(a, callback_data=f"ab_{a}")] for a in abilities]
        await q.message.reply_text("🔥 Ability انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
        return
    elif action == "item":
        items = get_items(user_id)
        if not items:
            await q.message.reply_text("❌ آیتم نداری.")
            return
        kb = [[InlineKeyboardButton(f"{n} (x{c})", callback_data=f"it_{n}")] for n, c in items]
        await q.message.reply_text("💊 آیتم انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
        return
    else:
        return

    if status == "won":
        reward = finish_battle(user_id, battle[2], True)
        end_battle(battle[0])
        await q.message.reply_text(f"{text}\n\n🏆 بردی!\n💰 +{reward} coin")
        return
    elif status == "lost":
        end_battle(battle[0])
        await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return

    update_battle(battle[0], php, bhp, 0, 0, 'active')
    new_battle = get_battle(user_id)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(new_battle, char)
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
        await q.message.reply_text(f"{text}\n\n🏆 بردی!\n💰 +{reward} coin")
        return
    elif status == "lost":
        end_battle(battle[0])
        await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return

    update_battle(battle[0], php, bhp, 0, 0, 'active')
    new_battle = get_battle(user_id)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(new_battle, char)
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
        await q.message.reply_text(f"{text}\n\n🏆 بردی!\n💰 +{reward} coin")
        return
    elif status == "lost":
        end_battle(battle[0])
        await q.message.reply_text(f"{text}\n\n💀 باختی!")
        return

    update_battle(battle[0], php, bhp, 0, 0, 'active')
    new_battle = get_battle(user_id)
    full_text = text + "\n\n━━━━━━━━━━━━━━━━\n\n" + build_battle_message(new_battle, char)
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
    session_id = f"coop_{host_id}_{boss_name}"
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
            text = f"🏆 نبرد تموم شد!\n\n{log}\n\n"
            for uid, amount in result["rewards"].items():
                text += f"👤 {uid}: +{amount} coin\n"
            await q.message.reply_text(text)
        else:
            await q.message.reply_text(f"🏆 نبرد تموم شد!\n\n{log}")
        return

    battle = get_multi_battle(session_id)
    if not battle:
        await q.message.reply_text(f"{log}\n\n❌ نبرد یافت نشد.")
        return
    view = build_battle_view(battle)
    kb = [
        [InlineKeyboardButton("⚔️ حمله", callback_data=f"mb_attack_{session_id}"),
         InlineKeyboardButton("🛡️ دفاع", callback_data=f"mb_defend_{session_id}")],
        [InlineKeyboardButton("💨 جاخالی", callback_data=f"mb_dodge_{session_id}")],
    ]
    await q.message.reply_text(f"{log}\n\n{view}", reply_markup=InlineKeyboardMarkup(kb))


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


# ============ HELP ============

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start\n/profile\n/shop\n/buy <name>\n/buychar <name> <rank>\n"
        "/select\n/upgrade\n/battle\n/coop\n/join <session>\n/startcoop <session>\n"
        "/pvp\n/joinpvp <session>\n/team <2-4>\n/jointeam <session> <1|2>\n"
        "/startteam <session>\n/quests\n/claim <key>\n/leaderboard\n/coins\n/help"
    )


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
    ]
    for cmd, fn in handlers:
        app.add_handler(CommandHandler(cmd, fn))

    callbacks = [
        ("^mb_", multi_action_callback),
        ("^act_", action_callback),
        ("^ab_", ability_use_callback),
        ("^it_", item_use_callback),
        ("^sel_", select_callback),
        ("^shop_", shop_callback),
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
