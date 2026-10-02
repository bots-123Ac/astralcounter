from telegram import Update
from telegram.ext import ContextTypes
from services.user_service import get_user

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await get_user(user.id)

    if not db_user:
        await update.message.reply_text("❌ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ. ᴘʟᴇᴀsᴇ /start ғɪʀsᴛ.")
        return

    text = (
        f"📊 <b>ʏᴏᴜʀ sᴛᴀᴛs</b>\n\n"
        f"👤 ɴᴀᴍᴇ: {user.first_name}\n"
        f"🆔 ɪᴅ: <code>{user.id}</code>\n"
        f"💬 ᴍᴇssᴀɢᴇs: <b>{db_user.total_messages}</b>\n"
        f"🏆 ʟᴇᴠᴇʟ: <b>{db_user.level}</b>\n"
        f"🎁 ɢɪғᴛs: <b>{db_user.gifts}</b>\n"
    )
    await update.message.reply_text(text, parse_mode="HTML")
