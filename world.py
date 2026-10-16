async def world_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    char = get_active_character(user_id)
    if not char:
        await update.message.reply_text("❌ کاراکتر فعال نداری. /start بزن.")
        return
    text = get_player_region_view(user_id)
    kb = [
        [InlineKeyboardButton("🌲 جنگل", callback_data="world_forest")],
        [InlineKeyboardButton("🏜️ بیابان", callback_data="world_desert")],
        [InlineKeyboardButton("🏔️ کوه", callback_data="world_mountain")],
        [InlineKeyboardButton("🌋 آتشفشان", callback_data="world_volcano")],
        [InlineKeyboardButton("🏰 سیاه‌چال", callback_data="world_dungeon")],
        [InlineKeyboardButton("📊 پیشرفت", callback_data="world_progress"),
         InlineKeyboardButton("🏆 گنج‌ها", callback_data="world_treasures")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def world_region_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    region_key = q.data.replace("world_", "")
    user_id = q.from_user.id
    unlocked = get_unlocked_regions(user_id)
    if region_key not in unlocked:
        can, msg = can_unlock_region(user_id, region_key)
        if not can:
            await q.answer(msg, show_alert=True)
            return
        unlock_world_region(user_id, region_key)
    update_world_region(user_id, region_key)
    text = get_region_view(user_id, region_key)
    kb = [
        [InlineKeyboardButton("🚶 گشتن", callback_data=f"explore_{region_key}")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")],
    ]
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
async def world_explore_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
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
        if existing:
            end_battle(existing["id"])
        enemy_hp = 10000
        if region_key == "forest":
            enemy_hp = 10000
        elif region_key == "desert":
            enemy_hp = 30000
        elif region_key == "mountain":
            enemy_hp = 80000
        elif region_key == "volcano":
            enemy_hp = 200000
        elif region_key == "dungeon":
            enemy_hp = 500000
        create_battle(user_id, enemy_name, char[5], enemy_hp)
        battle_data = get_battle(user_id)
        text = f"👹 یه دشمن ظاهر شد!\n\n{enemy_name}\n\n" + build_battle_message(battle_data, char)
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(
            get_battle_kb(char[2], user_id)
        ))

    elif event == "treasure":
        t_key, t_data = random_treasure()
        if t_data:
            if t_data["type"] == "coins":
                amount = t_data["value"] // 2
                add_coins(user_id, amount)
                reward_text = f"💰 +{amount:,} سکه"
            elif t_data["type"] == "item":
                try:
                    item_names = ["Health Potion", "Mega Potion", "Damage Boost", "Bomb"]
                    chosen_item = random.choice(item_names)
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("SELECT id, quantity FROM items WHERE user_id=? AND item_name=?",
                              (user_id, chosen_item))
                    row = c.fetchone()
                    if row:
                        c.execute("UPDATE items SET quantity = quantity + 1 WHERE id=?", (row[0],))
                    else:
                        c.execute("INSERT INTO items (user_id, item_name, quantity) VALUES (?,?,1)",
                                  (user_id, chosen_item))
                    conn.commit()
                    conn.close()
                    reward_text = f"🎁 آیتم: {chosen_item}"
                except Exception as e:
                    reward_text = f"❌ خطا در دادن آیتم: {e}"
            else:
                reward_text = f"✨ {t_data['effect']}"
            add_world_treasure(user_id, t_data["name"])
            increment_world_stat(user_id, "treasures")
            text = f"🎁 یه صندوق پیدا کردی!\n\n{format_treasure(t_key, t_data)}\n\n🎉 جایزه: {reward_text}"
        else:
            text = "🎁 صندوق خالی بود..."
        kb = [
            [InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")],
        ]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

    elif event == "mine":
        amount = random_reward(region_key) // 4
        add_coins(user_id, amount)
        text = f"💎 یه معدن پیدا کردی!\n\n💰 +{amount:,} سکه"
        kb = [
            [InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")],
        ]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

    elif event == "gate":
        all_regions = list(REGIONS.keys())
        current_idx = all_regions.index(region_key) if region_key in all_regions else 0
        if current_idx + 1 < len(all_regions):
            next_region = all_regions[current_idx + 1]
            unlocked_new = unlock_world_region(user_id, next_region)
            if unlocked_new:
                text = f"🚪 دروازه باز شد!\n\n🎉 منطقه جدید باز شد: {get_region_name(next_region)}"
            else:
                text = f"🚪 دروازه به {get_region_name(next_region)}"
        else:
            text = "🚪 دروازه به جایی نمی‌ره..."
        kb = [
            [InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")],
        ]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

    elif event == "riddle":
        riddle_rewards = [500, 2000, 5000, 10000]
        reward = random.choice(riddle_rewards)
        add_coins(user_id, reward)
        text = f"❓ یه معما حل کردی!\n\n💰 +{reward:,} سکه"
        kb = [
            [InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")],
        ]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    elif event == "rare_boss":
        boss_name = region["boss"]
        char = get_active_character(user_id)
        existing = get_battle(user_id)
        if existing:
            end_battle(existing["id"])
        boss_hp = 50000
        if region_key == "forest":
            boss_hp = 50000
        elif region_key == "desert":
            boss_hp = 120000
        elif region_key == "mountain":
            boss_hp = 300000
        elif region_key == "volcano":
            boss_hp = 600000
        elif region_key == "dungeon":
            boss_hp = 1500000
        create_battle(user_id, boss_name, char[5], boss_hp)
        battle_data = get_battle(user_id)
        text = f"🌟 یه باس کمیاب ظاهر شد!\n\n👑 {boss_name}\n\n" + build_battle_message(battle_data, char)
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(
            get_battle_kb(char[2], user_id)
        ))

    elif event == "trap":
        loss = random_reward(region_key) // 4
        coins = get_coins(user_id)
        if coins >= loss:
            add_coins(user_id, -loss)
            text = f"💀 توی تله افتادی!\n\n💸 -{loss:,} سکه"
        else:
            text = "💀 توی تله افتادی! ولی پولی نداشتی..."
        kb = [
            [InlineKeyboardButton("🚶 گشتن دوباره", callback_data=f"explore_{region_key}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")],
        ]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def world_progress_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = format_world_progress(q.from_user.id)
    kb = [
        [InlineKeyboardButton("🏆 گنج‌ها", callback_data="world_treasures")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")],
    ]
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def world_treasures_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = format_treasures_list(q.from_user.id)
    kb = [
        [InlineKeyboardButton("📊 پیشرفت", callback_data="world_progress")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="world_back")],
    ]
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def world_back_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = get_player_region_view(q.from_user.id)
    kb = [
        [InlineKeyboardButton("🌲 جنگل", callback_data="world_forest")],
        [InlineKeyboardButton("🏜️ بیابان", callback_data="world_desert")],
        [InlineKeyboardButton("🏔️ کوه", callback_data="world_mountain")],
        [InlineKeyboardButton("🌋 آتشفشان", callback_data="world_volcano")],
        [InlineKeyboardButton("🏰 سیاه‌چال", callback_data="world_dungeon")],
        [InlineKeyboardButton("📊 پیشرفت", callback_data="world_progress"),
         InlineKeyboardButton("🏆 گنج‌ها", callback_data="world_treasures")],
    ]
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))