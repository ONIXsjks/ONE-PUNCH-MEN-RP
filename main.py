from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from config import *
from database import init_db, get_user, add_coins, get_coins
from characters import (create_character, get_user_characters,
                        get_active_character, set_active, buy_character)
from shop import buy_ability, buy_item, buy_buff, buy_slot, upgrade_character
from battle import fight_boss
from coop import coop_fight_boss
from pvp import pvp_fight
from team_battle import team_fight
from quests import (init_quests_table, reset_daily_quests,
                    update_quest_progress, get_user_quests, claim_quest, QUESTS)
from leaderboard import get_top_by_coins, get_top_by_level, get_top_by_rank
from images import IMAGES

# Active sessions
PVP_SESSIONS = {}
TEAM_SESSIONS = {}
COOP_SESSIONS = {}

# ============ START ============
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
            "Starter character: King (C Rank)\n"
            "Farm bosses, earn coins, buy better characters!\n"
            "Commands: /profile /shop /battle /coop /quests /leaderboard"
        )
    else:
        await update.message.reply_text("Welcome back! /help")

# ============ PROFILE ============
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

# ============ COINS ============
async def coins(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    c = get_coins(update.effective_user.id)
    await update.message.reply_text(f"Coins: {c}")

# ============ SHOP ============
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

# ============ BUY CHARACTER ============
async def buychar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /buychar <name> <rank>\nEx: /buychar Genos A")
        return
    rank = ctx.args[-1].upper()
    char_name = " ".join(ctx.args[:-1])
    if rank not in CHARACTERS or char_name not in CHARACTERS[rank]:
        await update.message.reply_text("Invalid character or rank.")
        return
    msg = buy_character(update.effective_user.id, char_name, rank)
    await update.message.reply_text(msg)

# ============ SELECT CHARACTER ============
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

# ============ BUY ============
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

# ============ UPGRADE ============
async def upgrade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    msg = upgrade_character(user_id, char[0])
    update_quest_progress(user_id, "level_up_1")
    await update.message.reply_text(msg)

# ============ SOLO BATTLE ============
async def battle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    kb = [[InlineKeyboardButton(name, callback_data=f"solo_{name}")] for name in BOSSES]
    await update.message.reply_text("Solo Battle - Choose boss:", reply_markup=InlineKeyboardMarkup(kb))

async def solo_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    boss_name = q.data.replace("solo_", "")
    user_id = q.from_user.id
    char = get_active_character(user_id)
    if not char:
        await q.message.reply_text("No active character.")
        return
    win, log, reward, images = fight_boss(user_id, char, boss_name)
    for img in images[:3]:
        try:
            await q.message.reply_photo(photo=img)
        except Exception:
            pass
    if win:
        await q.message.reply_text(f"WIN!\n\n{log}\n\n+{reward} coins")
    else:
        await q.message.reply_text(f"LOSE!\n\n{log}")

# ============ COOP ============
async def coop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("No active character.")
        return
    kb = [[InlineKeyboardButton(name, callback_data=f"coopboss_{name}")] for name in BOSSES]
    await update.message.reply_text("Co-op Battle - Host chooses boss:", reply_markup=InlineKeyboardMarkup(kb))

async def coop_boss_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    boss_name = q.data.replace("coopboss_", "")
    host_id = q.from_user.id
    session_id = f"{host_id}_{boss_name}"
    COOP_SESSIONS[session_id] = {"host": host_id, "boss": boss_name, "players": [host_id]}
    await q.message.reply_text(
        f"Co-op session created for {boss_name}\n"
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
    await update.message.reply_text(f"Joined!")

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
    win, log, reward, images = coop_fight_boss(p1_id, char1, p2_id, char2, s["boss"])
    for img in images[:3]:
        try:
            await update.message.reply_photo(photo=img)
        except Exception:
            pass
    if win:
        await update.message.reply_text(f"CO-OP WIN!\n\n{log}\n\n+{reward} coins each")
    else:
        await update.message.reply_text(f"CO-OP LOSE!\n\n{log}")
    del COOP_SESSIONS[session_id]

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
        f"PvP session created!\nSession ID: {session_id}\n"
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
    winner, log, reward = pvp_fight(s["host"], char_host, user_id, char)
    if winner == 1:
        text = f"Host wins!\n\n{log}\n\n+{reward} coins"
    elif winner == 2:
        text = f"Opponent wins!\n\n{log}\n\n+{reward} coins"
    else:
        text = f"Draw!\n\n{log}\n\n+{reward} coins"
    await update.message.reply_text(text)
    del PVP_SESSIONS[session_id]

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
        f"Team Battle ({size}v{size}) created!\nSession: {session_id}\n"
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
        await update.message.reply_text(
            f"Need {s['size']} each.\nT1: {len(s['team1'])} | T2: {len(s['team2'])}"
        )
        return
    winner, log, reward = team_fight(s["team1"], s["team2"])
    if winner == 1:
        text = f"Team 1 wins!\n\n{log}\n\n+{reward} coins each"
    elif winner == 2:
        text = f"Team 2 wins!\n\n{log}\n\n+{reward} coins each"
    else:
        text = f"Draw!\n\n{log}\n\n+{reward} coins each"
    await update.message.reply_text(text)
    del TEAM_SESSIONS[session_id]

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
        "/start - Start\n"
        "/profile - Your profile\n"
        "/shop - Shop\n"
        "/buy <name> - Buy ability/item/buff\n"
        "/buychar <name> <rank> - Buy character\n"
        "/select - Choose active character\n"
        "/upgrade - Level up\n"
        "/battle - Solo boss\n"
        "/coop - Create co-op\n"
        "/join <session> - Join co-op\n"
        "/startcoop <session> - Start co-op\n"
        "/pvp - Create PvP\n"
        "/joinpvp <session> - Join PvP\n"
        "/team <2-4> - Create team battle\n"
        "/jointeam <session> <1|2> - Join team\n"
        "/startteam <session> - Start team\n"
        "/quests - Daily quests\n"
        "/claim <key> - Claim quest\n"
        "/leaderboard - Top players\n"
        "/coins - Balance"
    )

# ============ MAIN ============
def main():
    init_db()
    init_quests_table()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("buychar", buychar))
    app.add_handler(CommandHandler("select", select))
    app.add_handler(CommandHandler("upgrade", upgrade))
    app.add_handler(CommandHandler("battle", battle))
    app.add_handler(CommandHandler("coop", coop))
    app.add_handler(CommandHandler("join", join_coop))
    app.add_handler(CommandHandler("startcoop", start_coop))
    app.add_handler(CommandHand
