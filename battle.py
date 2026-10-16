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
    text += "💰 /give /take\n"
    text += "👤 /userinfo /allusers /resetuser /ban /unban\n"
    text += "🎭 /givechar /resetchar\n"
    if is_owner(user_id):
        text += "\n👑 /addadmin /removeadmin /listadmins\n"
        text += "📜 /sethelp /viewhelp\n"
        text += "🖼️ عکس + کپشن /setcharimage <name>\n"
        text += "📢 /addchannel /removechannel /listchannels\n"
        text += "🎯 /setquest /viewquests\n"
        text += "\n👑 /ownerpanel\n"
    await update.message.reply_text(text)


async def give_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_coins"):
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
    await update.message.reply_text(f"✅ {amount:,} coin به {target_id} دادی.")


async def take_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not has_permission(update.effective_user.id, "manage_coins"):
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
    text = f"👤 کاربر: {user[0] or 'Unknown'}\n🆔 ID: {target_id}\n💰 Coins: {user[1]:,}\n\n🦸 کاراکترها:\n"
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
    try:
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
        target = int(ctx.args[1])
        reward = int(ctx.args[2])
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
    text = "🎯 کوئست‌ها:\n\n"
    for key, desc, target, reward in quests:
        text += f"🔹 {key}: {target} — {reward:,}\n"
    await update.message.reply_text(text)
def player_ability(battle, char, ability_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    char_name = char[2]
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    # ========== DOMAIN (×۸ + فریز) ==========
    if ability_name == "DOMAIN":
        if battle.get("domain_used", 0) >= 1:
            return "active", "❌ Domain فقط ۱ بار در نبرد!", battle
        domain = DOMAINS.get(char_name) or DOMAINS_JJK.get(char_name)
        if not domain:
            return "active", "❌ این کاراکتر Domain نداره!", battle
        battle["domain_used"] = 1
        battle["domain_active"] = 1
        battle["domain_turns"] = domain.get("duration", 2)
        battle["domain_name"] = domain["name"]
        effects = domain.get("effects", {})
        battle["domain_atk_boost"] = effects.get("atk_boost", 0)

        dmg = int(char[6] * 8)
        bhp = max(0, bhp - dmg)
        text = box_title(f"🌀 {domain['name'][:20]}", 26)
        text += f"\n\n💥 {format_num(dmg)} آسیب (×۸)"

        if "freeze" in effects:
            battle["boss_frozen"] = effects["freeze"]
            text += f"\n❄️ باس فریز شد! ({effects['freeze']} نوبت)"
        if "atk_boost" in effects:
            text += f"\n⚔️ ATK +{effects['atk_boost']}٪"
        if "heal" in effects:
            heal = int(pmax * effects["heal"] / 100)
            php = min(pmax, php + heal)
            text += f"\n💚 +{format_num(heal)} HP"

        text += f"\n\n👹 {boss['display_name']}"
        text += f"\n{hp_bar(bhp, bmax)}"

        if bhp <= 0:
            battle["php"] = php; battle["bhp"] = bhp
            return "won", text, battle

        php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

        battle = apply_bankai_round(battle)
        php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
        if bt:
            text += f"\n{bt}"

        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0:
            return "won", text, battle
        if php <= 0:
            return "lost", text, battle
        return "active", text, battle

    # ========== BANKAI (×۶) ==========
    if ability_name == "BANKAI":
        if battle.get("bankai_used", 0) >= 1:
            return "active", "❌ Bankai فقط ۱ بار در نبرد!", battle
        bankai = BANKAI.get(char_name) or BLEACH_BANKAI.get(char_name)
        if not bankai:
            return "active", "❌ این کاراکتر Bankai نداره!", battle
        battle["bankai_used"] = 1
        battle["bankai_data"] = bankai
        battle["bankai_atk_current"] = 0
        battle["bankai_dodge_current"] = 0
        battle["bankai_heal_current"] = 0
        battle["bankai_bleed_current"] = 0
        battle["bankai_enemy_debuff_current"] = 0
        battle["bankai_self_dmg_current"] = 0

        dmg = int(char[6] * 6)
        bhp = max(0, bhp - dmg)
        text = box_title(f"⚔️ {bankai['name'][:20]}", 26)
        text += f"\n\n💥 {format_num(dmg)} آسیب (×۶)"
        text += f"\n\n👹 {boss['display_name']}"
        text += f"\n{hp_bar(bhp, bmax)}"

        if bhp <= 0:
            battle["php"] = php; battle["bhp"] = bhp
            return "won", text, battle

        php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

        battle = apply_bankai_round(battle)
        php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
        if bt:
            text += f"\n{bt}"

        battle["php"] = php; battle["bhp"] = bhp
        if bhp <= 0:
            return "won", text, battle
        if php <= 0:
            return "lost", text, battle
        return "active", text, battle

    # ========== ABILITY های ۳گانه ==========
    abilities = ABILITIES_3.get(char_name, {})
    if not abilities:
        return "active", "❌ Ability پیدا نشد.", battle

    found_key = None
    found_ab = None
    for key in ["ability_1", "ability_2", "ability_3"]:
        if key in abilities and abilities[key]["name"] == ability_name:
            found_key = key
            found_ab = abilities[key]
            break

    if not found_ab:
        return "active", "❌ Ability پیدا نشد.", battle

    # 🟣 Ultimate فقط ۱ بار
    if found_key == "ability_3":
        if battle.get("spam_state") == "purple_used":
            return "active", f"🟣 {ability_name} فقط ۱ بار در کل نبرد!", battle

    mult = found_ab.get("mult", 3)
    dmg = int(char[6] * mult)
    bhp = max(0, bhp - dmg)

    if found_key == "ability_3":
        text = box_title(f"🟣 {ability_name[:20]}!", 26)
        battle["spam_state"] = "purple_used"
    elif found_key == "ability_1":
        text = box_simple(f"🔵 {ability_name[:18]}!")
    else:
        text = box_simple(f"🔴 {ability_name[:18]}!")

    text += f"\n\n💥 {format_num(dmg)} آسیب ({mult}x)"
    text += f"\n\n👹 {boss['display_name']}"
    text += f"\n{hp_bar(bhp, bmax)}"

    if bhp <= 0:
        battle["php"] = php; battle["bhp"] = bhp
        return "won", text, battle

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_ability_v2(battle, char, action):
    """Alias برای player_ability با action"""
    char_name = char[2]
    if action == "domain":
        return player_ability(battle, char, "DOMAIN")
    if action == "bankai":
        return player_ability(battle, char, "BANKAI")
    abilities = ABILITIES_3.get(char_name, {})
    if action in abilities:
        ab_name = abilities[action]["name"]
        return player_ability(battle, char, ab_name)
    return "active", "❌ Ability نامعتبر.", battle


# ============ SHOP ABILITY (خریداری‌شده از شاپ) ============

def player_ability_shop(battle, char, ability_name):
    """استفاده از Ability خریداری‌شده از شاپ"""
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    info = ABILITIES.get(ability_name)
    if not info:
        return "active", "❌ Ability پیدا نشد.", battle

    eff = info.get("effect", "")
    text = box_simple(f"🔥 {ability_name}!")

    if "x2" in eff:
        dmg = int(char[6] * 2)
    elif "x3.5" in eff:
        dmg = int(char[6] * 3.5)
    elif "x3" in eff:
        dmg = int(char[6] * 3)
    elif "x4" in eff:
        dmg = int(char[6] * 4)
    elif "x5" in eff:
        dmg = int(char[6] * 5)
    elif "x6" in eff:
        dmg = int(char[6] * 6)
    else:
        dmg = int(char[6] * 2)

    bhp = max(0, bhp - dmg)
    text += f"\n\n💥 {format_num(dmg)} آسیب"
    text += f"\n\n👹 {boss['display_name']}"
    text += f"\n{hp_bar(bhp, bmax)}"

    if bhp <= 0:
        battle["php"] = php; battle["bhp"] = bhp
        return "won", text, battle

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


# ============ SHOP BUFF (خریداری‌شده از شاپ) ============

def player_buff_shop(battle, char, buff_name):
    """استفاده از باف خریداری‌شده از شاپ"""
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    info = BUFFS.get(buff_name)
    if not info:
        return "active", "❌ باف پیدا نشد.", battle

    eff = info.get("effect", "")
    text = box_simple(f"✨ {buff_name}!")

    if "Max HP" in eff:
        heal = 500
        php = min(pmax, php + heal)
        text += f"\n\n💚 +{format_num(heal)} HP"
    elif "ATK" in eff and "150" in eff:
        battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 15
        text += "\n\n⚔️ ATK +۱۵٪"
    elif "DEF" in eff:
        text += "\n\n🛡️ DEF +۸۰"
    elif "DODGE" in eff:
        text += "\n\n💨 دوج +۱۰٪"
    elif "all +20" in eff:
        battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 20
        text += "\n\n🔥 همه +۲۰٪"
    elif "all +50" in eff:
        battle["domain_atk_boost"] = battle.get("domain_atk_boost", 0) + 50
        text += "\n\n🔥 همه +۵۰٪"

    text += f"\n\n👤 {hp_bar(php, pmax)}"

    php, bhp, text = boss_turn(battle, boss, php, pmax, bhp, bmax, text)

    battle = apply_bankai_round(battle)
    php, bhp, bt = apply_bankai_effects(battle, php, pmax, bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = php; battle["bhp"] = bhp
    if bhp <= 0:
        return "won", text, battle
    if php <= 0:
        return "lost", text, battle
    return "active", text, battle


def player_item(battle, char, item_name):
    boss = get_boss_data(battle["boss_name"])
    if not boss:
        return "active", "❌ باس پیدا نشد.", battle
    info = ITEMS.get(item_name)
    if not info:
        return "active", "❌ آیتم نداری.", battle
    php = battle["php"]; bhp = battle["bhp"]
    pmax = battle["pmax"]; bmax = battle["bmax"]

    text = box_simple(f"💊 {item_name}!")
    new_php = php
    new_bhp = bhp
    if item_name == "Health Potion":
        new_php = min(pmax, php + 500)
        text += "\n\n💚 HP +۵۰۰"
    elif item_name == "Mega Potion":
        new_php = min(pmax, php + 1500)
        text += "\n\n💚 HP +۱,۵۰۰"
    elif item_name == "Damage Boost":
        dmg, _ = roll_damage(char[6] * 2)
        new_bhp = max(0, bhp - dmg)
        text += f"\n\n💥 ATK x2 → {format_num(dmg)}"
    elif item_name == "Bomb":
        new_bhp = max(0, bhp - 500)
        text += "\n\n💥 ۵۰۰ آسیب"
    else:
        text += f"\n\n{info.get('effect_fa', info.get('effect', ''))}"

    if new_bhp <= 0:
        battle["php"] = new_php; battle["bhp"] = new_bhp
        return "won", text, battle

    new_php, new_bhp, text = boss_turn(battle, boss, new_php, pmax, new_bhp, bmax, text)

    battle = apply_bankai_round(battle)
    new_php, new_bhp, bt = apply_bankai_effects(battle, new_php, pmax, new_bhp, bmax)
    if bt:
        text += f"\n{bt}"

    battle["php"] = new_php; battle["bhp"] = new_bhp
    if new_bhp <= 0:
        return "won", text, battle
    if new_php <= 0:
        return "lost", text, battle
    return "active", text, battle


def build_battle_message(battle, char):
    boss = get_boss_data(battle["boss_name"])
    boss_atk = boss["atk"] if boss else 0
    boss_display = boss["display_name"] if boss else battle["boss_name"]

    text = f"╔══════════════════════════╗\n"
    text += f"║  👹 {boss_display[:20].center(20)} ║\n"
    text += f"╚══════════════════════════╝\n\n"
    text += f"{hp_bar(battle['bhp'], battle['bmax'])}\n"
    text += f"⚔️ ATK: {format_num(boss_atk)}\n"

    text += f"\n╭───── 👤 {char[2][:16]} ─────╮\n"
    text += f"│ ⭐ {char[3]} Rank{' ' * (14 - len(char[3]))}│\n"
    text += f"│ {hp_bar(battle['php'], battle['pmax'])} │\n"
    text += f"│ ⚔️ ATK: {format_num(char[6])}{' ' * (13 - len(format_num(char[6])))}│\n"
    text += f"│ 🛡️ DEF: {format_num(char[7])}{' ' * (13 - len(format_num(char[7])))}│\n"
    text += f"│ 💨 DODGE: {char[8]}%{' ' * (10 - len(str(char[8])))}│\n"
    text += f"╰{'─' * 25}╯"

    if battle.get("domain_active", 0) == 1:
        text += f"\n\n🌀 قلمرو: {battle.get('domain_name', '')} ({battle.get('domain_turns', 0)} راند)"
    if battle.get("bankai_used", 0) >= 1:
        bankai = battle.get("bankai_data", {})
        text += f"\n⚔️ Bankai: {bankai.get('name', '')}"

    if battle.get("boss_frozen", 0) > 0:
        text += f"\n❄️ باس فریز است ({battle['boss_frozen']} نوبت)"

    text += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n🎯 نوبت توئه!"
    return text


def finish_battle(uid, boss_name, won):
    if won:
        boss = get_boss_data(boss_name)
        reward = boss["reward"] if boss else 5000
        add_coins(uid, reward)
        update_quest_progress(uid, "win_3_bosses")
        update_quest_progress(uid, "win_5_bosses")
        if boss_name == "Saitama Phase 1":
            update_quest_progress(uid, "kill_saitama")
        if boss_name.startswith("Goku"):
            update_quest_progress(uid, "kill_goku")

        try:
            from guild import give_guild_xp
            xp_amount = 5
            if boss:
                boss_hp = boss.get("hp", 0)
                if boss_hp >= 40000:
                    xp_amount = 20
                elif boss_hp >= 20000:
                    xp_amount = 10
                elif boss_hp >= 5000:
                    xp_amount = 5
                else:
                    xp_amount = 2
            give_guild_xp(uid, xp_amount)
        except Exception:
            pass

        return reward
    return 0