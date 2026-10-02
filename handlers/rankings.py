from telegram import Update
from telegram.ext import ContextTypes
from services.message_service import get_top_users, get_group_top_users
from keyboards.inline import rankings_keyboard


TIMEFRAME_LABELS = {
    "all": "🏆 <b>ᴀʟʟ ᴛɪᴍᴇ ᴛᴏᴘ ᴜsᴇʀs</b>",
    "monthly": "📅 <b>ᴍᴏɴᴛʜʟʏ ᴛᴏᴘ ᴜsᴇʀs</b> <i>(30 ᴅᴀʏs)</i>",
    "weekly": "📆 <b>ᴡᴇᴇᴋʟʏ ᴛᴏᴘ ᴜsᴇʀs</b> <i>(7 ᴅᴀʏs)</i>",
    "today": "⏰ <b>ᴛᴏᴅᴀʏ's ᴛᴏᴘ ᴜsᴇʀs</b> <i>(ʟᴀsᴛ 24ʜ)</i>",
}


async def _build_group_rankings_text(group_id: int, timeframe: str) -> str:
    top = await get_group_top_users(group_id, limit=10, timeframe=timeframe)
    header = TIMEFRAME_LABELS.get(timeframe, TIMEFRAME_LABELS["all"])

    if not top:
        return f"{header}\n\n📭 ɴᴏ ᴀᴄᴛɪᴠɪᴛʏ ʏᴇᴛ."

    text = f"{header}\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for i, entry in enumerate(top, 1):
        rank = medals[i - 1] if i <= 3 else f"<b>{i}.</b>"
        text += (
            f"{rank} "
            f'<a href="tg://user?id={entry["user_id"]}">{entry["name"]}</a> '
            f"— <b>{entry['messages']}</b> ᴍsɢs\n"
        )
    return text


async def rankings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ ᴜsᴇ ᴛʜɪs ɪɴ ᴀ ɢʀᴏᴜᴘ.")
        return

    text = await _build_group_rankings_text(chat.id, "all")
    await update.message.reply_text(
        text,
        reply_markup=rankings_keyboard("all"),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


async def rankings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles rank_all / rank_monthly / rank_weekly / rank_today buttons."""
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    if not data.startswith("rank_"):
        return

    timeframe = data.replace("rank_", "")
    if timeframe not in TIMEFRAME_LABELS:
        timeframe = "all"

    text = await _build_group_rankings_text(query.message.chat_id, timeframe)

    try:
        await query.edit_message_text(
            text,
            reply_markup=rankings_keyboard(timeframe),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    except Exception:
        # Agar same text dobara click hua to Telegram error deta hai — ignore
        pass


async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Global top users across all groups."""
    top = await get_top_users(10)
    if not top:
        await update.message.reply_text("📭 ɴᴏ ᴅᴀᴛᴀ ʏᴇᴛ.")
        return

    text = "🌍 <b>ɢʟᴏʙᴀʟ ᴛᴏᴘ ᴜsᴇʀs</b>\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for i, u in enumerate(top, 1):
        rank = medals[i - 1] if i <= 3 else f"<b>{i}.</b>"
        name = u.first_name or u.username or f"ᴜsᴇʀ {u.user_id}"
        text += (
            f"{rank} "
            f'<a href="tg://user?id={u.user_id}">{name}</a> '
            f"— <b>{u.total_messages}</b> ᴍsɢs\n"
        )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
