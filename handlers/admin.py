from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import owner_only
from database.db import async_session
from database.models import User
from sqlalchemy import select

@owner_only
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /broadcast &lt;ᴍᴇssᴀɢᴇ&gt;", parse_mode="HTML")
        return
    message = " ".join(context.args)

    async with async_session() as session:
        result = await session.execute(select(User.user_id))
        user_ids = [row[0] for row in result.all()]

    sent = 0
    failed = 0
    for uid in user_ids:
        try:
            await context.bot.send_message(uid, message)
            sent += 1
        except Exception:
            failed += 1

    await update.message.reply_text(
        f"📢 ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏɴᴇ\n✅ sᴇɴᴛ: {sent}\n❌ ғᴀɪʟᴇᴅ: {failed}"
    )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 ᴘᴏɴɢ! ʙᴏᴛ ɪs ᴀʟɪᴠᴇ.")

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    from services.user_service import get_user
    db_user = await get_user(user.id)
    if not db_user:
        await update.message.reply_text("❌ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ. /start ᴋᴀʀᴇɪɴ.")
        return
    text = (
        f"👤 <b>ᴘʀᴏғɪʟᴇ</b>\n\n"
        f"ɴᴀᴍᴇ: {user.first_name}\n"
        f"ᴜsᴇʀɴᴀᴍᴇ: @{user.username or 'N/A'}\n"
        f"ɪᴅ: <code>{user.id}</code>\n"
        f"💬 ᴍᴇssᴀɢᴇs: <b>{db_user.total_messages}</b>\n"
        f"🏆 ʟᴇᴠᴇʟ: <b>{db_user.level}</b>"
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def mygifts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    from services.user_service import get_user
    db_user = await get_user(user.id)
    gifts = db_user.gifts if db_user else 0
    await update.message.reply_text(
        f"🎁 <b>ʏᴏᴜʀ ɢɪғᴛs</b>\n\nᴛᴏᴛᴀʟ: <b>{gifts}</b>",
        parse_mode="HTML",
    )

async def groupstats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ ɢʀᴏᴜᴘ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ.")
        return

    from database.db import async_session
    from database.models import Group
    from sqlalchemy import select
    async with async_session() as session:
        result = await session.execute(select(Group).where(Group.group_id == chat.id))
        group = result.scalar_one_or_none()

    if not group:
        await update.message.reply_text("📭 ɴᴏ ᴅᴀᴛᴀ ʏᴇᴛ.")
        return

    text = (
        f"📊 <b>ɢʀᴏᴜᴘ sᴛᴀᴛs</b>\n\n"
        f"ᴛɪᴛʟᴇ: {group.title}\n"
        f"🆔 ɪᴅ: <code>{group.group_id}</code>\n"
        f"💬 ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs: <b>{group.total_messages}</b>"
    )
    await update.message.reply_text(text, parse_mode="HTML")
