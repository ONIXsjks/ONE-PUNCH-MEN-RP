from database import (get_guild_by_name, get_guild_by_id, get_user_guild,
                      create_guild, join_guild, leave_guild, get_guild_members,
                      donate_to_guild, add_guild_xp, upgrade_guild,
                      get_all_guilds, kick_guild_member, is_guild_leader,
                      can_upgrade_guild, get_guild_max_members,
                      get_guild_upgrade_req, get_guild_max_treasury,
                      search_guilds, get_top_guilds, get_coins, spend_coins,
                      get_username)


GUILD_CREATE_COST = 500000
GUILD_MIN_LEVEL = 20


def create_new_guild(user_id, name, char_level):
    """ساخت کلن جدید"""
    if len(name) < 3 or len(name) > 20:
        return "❌ اسم کلن باید بین ۳ تا ۲۰ حرف باشه!"

    if char_level < GUILD_MIN_LEVEL:
        return f"❌ برای ساخت کلن باید لول {GUILD_MIN_LEVEL} باشی!"

    existing = get_user_guild(user_id)
    if existing:
        return "❌ تو قبلاً توی یه کلنی!"

    if get_guild_by_name(name):
        return "❌ این اسم قبلاً گرفته شده!"

    coins = get_coins(user_id)
    if coins < GUILD_CREATE_COST:
        return f"❌ پول کافی نداری!\n💰 لازم: {GUILD_CREATE_COST:,}\n💵 داری: {coins:,}"

    spend_coins(user_id, GUILD_CREATE_COST)
    create_guild(name, user_id)
    return f"✅ کلن «{name}» ساخته شد!\n💰 هزینه: {GUILD_CREATE_COST:,}"


def join_existing_guild(user_id, name):
    """پیوستن به کلن"""
    existing = get_user_guild(user_id)
    if existing:
        return "❌ تو قبلاً توی یه کلنی!"

    guild = get_guild_by_name(name)
    if not guild:
        return "❌ کلن پیدا نشد!"

    guild_id = guild[0]
    level = guild[3]
    members_count = guild[6]
    max_members = get_guild_max_members(level)

    if members_count >= max_members:
        return f"❌ کلن پره!\n👥 {members_count}/{max_members}"

    join_guild(guild_id, user_id)
    return f"✅ به کلن «{name}» پیوستی!"


def leave_current_guild(user_id):
    """خروج از کلن"""
    existing = get_user_guild(user_id)
    if not existing:
        return "❌ تو توی هیچ کلنی نیستی!"

    if leave_guild(user_id):
        return f"✅ از کلن «{existing[1]}» خارج شدی!"
    return "❌ خطا در خروج"


def donate(user_id, amount):
    """دونیت به خزانه کلن"""
    existing = get_user_guild(user_id)
    if not existing:
        return "❌ تو توی کلنی نیستی!"

    if amount <= 0:
        return "❌ مقدار باید بیشتر از ۰ باشه!"

    coins = get_coins(user_id)
    if coins < amount:
        return f"❌ پول کافی نداری!\n💵 داری: {coins:,}"

    guild_id = existing[0]
    level = existing[3]
    treasury = existing[5]
    max_treasury = get_guild_max_treasury(level)

    if treasury + amount > max_treasury:
        return f"❌ خزانه پر می‌شه!\n💰 حداکثر: {max_treasury:,}\n💵 الان: {treasury:,}"

    spend_coins(user_id, amount)
    donate_to_guild(guild_id, amount)
    return f"✅ {amount:,} سکه به خزانه کلن اضافه شد!"


def try_upgrade_guild(user_id):
    """ارتقای کلن (فقط لیدر)"""
    existing = get_user_guild(user_id)
    if not existing:
        return "❌ تو توی کلنی نیستی!"

    guild_id = existing[0]
    if not is_guild_leader(guild_id, user_id):
        return "❌ فقط لیدر می‌تونه ارتقا بده!"

    can, msg = can_upgrade_guild(guild_id)
    if not can:
        return f"❌ {msg}"

    guild = get_guild_by_id(guild_id)
    level = guild[3]
    xp = guild[4]
    treasury = guild[5]
    req = get_guild_upgrade_req(level)
    xp_cost, coin_cost = req

    upgrade_guild(guild_id, level + 1, xp_cost, coin_cost)
    return f"🎉 کلن به سطح {level + 1} ارتقا یافت!\n💰 هزینه: {coin_cost:,}\n⚡ XP: {xp_cost:,}"


def kick_member(user_id, target_id):
    """اخراج عضو (فقط لیدر)"""
    existing = get_user_guild(user_id)
    if not existing:
        return "❌ تو توی کلنی نیستی!"

    guild_id = existing[0]
    if not is_guild_leader(guild_id, user_id):
        return "❌ فقط لیدر می‌تونه اخراج کنه!"

    if user_id == target_id:
        return "❌ نمی‌تونی خودت رو اخراج کنی!"

    members = get_guild_members(guild_id)
    target_exists = any(m[0] == target_id for m in members)
    if not target_exists:
        return "❌ این کاربر توی کلنت نیست!"

    kick_guild_member(guild_id, target_id)
    return f"✅ کاربر اخراج شد!"


def give_guild_xp(user_id, amount):
    """XP به کلن کاربر بده (وقتی می‌جنگه)"""
    existing = get_user_guild(user_id)
    if not existing:
        return
    guild_id = existing[0]
    add_guild_xp(guild_id, amount)


def format_guild(guild):
    """نمایش کلن به صورت متن خوشگل"""
    if not guild:
        return "❌ کلن پیدا نشد."

    gid = guild[0]
    name = guild[1]
    leader_id = guild[2]
    level = guild[3]
    xp = guild[4]
    treasury = guild[5]
    members_count = guild[6]

    max_members = get_guild_max_members(level)
    max_treasury = get_guild_max_treasury(level)
    upgrade_req = get_guild_upgrade_req(level)

    leader_name = get_username(leader_id)

    text = f"╔══════════════════════════╗\n"
    text += f"║      🏰 {name[:18].center(18)} ║\n"
    text += f"║      ⭐ سطح {level}         ║\n"
    text += f"╚══════════════════════════╝\n\n"
    text += f"👑 لیدر: {leader_name}\n"
    text += f"👥 اعضا: {members_count}/{max_members}\n"
    text += f"💰 خزانه: {treasury:,} / {max_treasury:,}\n"

    if upgrade_req:
        xp_needed, coin_needed = upgrade_req
        text += f"⚡ XP: {xp:,} / {xp_needed:,}\n"
        text += f"\n🔼 ارتقا بعدی:\n"
        text += f"├ 💰 {coin_needed:,} سکه\n"
        text += f"└ ⚡ {xp_needed:,} XP"
    else:
        text += f"⚡ XP: {xp:,}\n"
        text += f"\n🏆 کلن در حداکثر سطحه!"

    return text


def format_members(guild):
    """نمایش اعضای کلن"""
    if not guild:
        return "❌ کلن پیدا نشد."

    gid = guild[0]
    name = guild[1]
    leader_id = guild[2]

    members = get_guild_members(gid)
    text = f"╔══════════════════════════╗\n"
    text += f"║   👥 اعضای {name[:14].center(14)} ║\n"
    text += f"╚══════════════════════════╝\n\n"

    for uid, role in members:
        uname = get_username(uid)
        if role == "leader":
            text += f"👑 {uname} (لیدر)\n"
        else:
            text += f"👤 {uname}\n"

    return text