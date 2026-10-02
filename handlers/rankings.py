from telegram import Update
from telegram.ext import ContextTypes
from services.message_service import get_top_users, get_group_top_users
from utils.decorators import group_only

async def rankings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ ᴜsᴇ ᴛʜɪs ɪɴ ᴀ ɢʀᴏᴜᴘ.")
        return

    top = await get_group_top_users(chat.id, 10)
    if not top:
        await update.message.reply_text("📭 ɴᴏ ᴀᴄᴛɪᴠɪᴛʏ ʏᴇᴛ.")
        return

    text = "🏆 <b>ɢʀᴏᴜᴘ ᴛᴏᴘ ᴜsᴇʀs</b>\n\n"
    for i, m in enumerate(top, 1):
        text += f"{i}. <code>{m.user_id}</code> — <b>{m.messages_in_group}</b> ᴍsɢs\n"
    await update.message.reply_text(text, parse_mode="HTML")

async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = await get_top_users(10)
    if not top:
        await update.message.reply_text("📭 ɴᴏ ᴅᴀᴛᴀ ʏᴇᴛ.")
        return

    text = "🌍 <b>ɢʟᴏʙᴀʟ ᴛᴏᴘ ᴜsᴇʀs</b>\n\n"
    for i, u in enumerate(top, 1):
        name = u.first_name or u.username or str(u.user_id)
        text += f"{i}. {name} — <b>{u.total_messages}</b> ᴍsɢs\n"
    await update.message.reply_text(text, parse_mode="HTML")
