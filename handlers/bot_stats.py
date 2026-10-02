from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import owner_only
from services.message_service import get_bot_stats

@owner_only
async def bot_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = await get_bot_stats()
    text = (
        f"📊 <b>ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs</b>\n\n"
        f"👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs: <b>{stats['users']}</b>\n"
        f"👥 ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs: <b>{stats['groups']}</b>\n"
        f"💬 ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs: <b>{stats['messages']}</b>\n"
    )
    await update.message.reply_text(text, parse_mode="HTML")
