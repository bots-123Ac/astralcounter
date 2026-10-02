from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID

def owner_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.effective_user or update.effective_user.id != OWNER_ID:
            if update.message:
                await update.message.reply_text("❌ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ᴛʜᴇ ᴏᴡɴᴇʀ.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def group_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_chat.type not in ["group", "supergroup"]:
            if update.message:
                await update.message.reply_text("❌ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
