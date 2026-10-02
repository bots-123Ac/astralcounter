from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select

from utils.decorators import owner_only
from database.db import async_session
from database.models import User, Group
from services.user_service import get_user
from services.message_service import (
    get_user_groups_with_counts,
    get_today_message_count,
)
from keyboards.inline import profile_keyboard


# ─────────────────────────────────────────────────────────
#  /broadcast
# ─────────────────────────────────────────────────────────
@owner_only
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "ᴜsᴀɢᴇ: /broadcast &lt;ᴍᴇssᴀɢᴇ&gt;", parse_mode="HTML"
        )
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


# ─────────────────────────────────────────────────────────
#  /ping
# ─────────────────────────────────────────────────────────
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 ᴘᴏɴɢ! ʙᴏᴛ ɪs ᴀʟɪᴠᴇ.")


# ─────────────────────────────────────────────────────────
#  /profile  +  prof_* callbacks
# ─────────────────────────────────────────────────────────
TIMEFRAME_LABELS = {
    "all": "📊 ᴀʟʟ ᴛɪᴍᴇ",
    "monthly": "📅 ᴍᴏɴᴛʜʟʏ (30 ᴅ)",
    "weekly": "📆 ᴡᴇᴇᴋʟʏ (7 ᴅ)",
    "today": "⏰ ᴛᴏᴅᴀʏ (24ʜ)",
}


async def _build_profile_text(user_obj, db_user, timeframe="all", bot=None):
    lines = [
        "👤 <b>ᴘʀᴏғɪʟᴇ</b>",
        "",
        f"ɴᴀᴍᴇ: {user_obj.first_name or 'ᴜsᴇʀ'}",
        f"ᴜsᴇʀɴᴀᴍᴇ: @{user_obj.username}" if user_obj.username else "ᴜsᴇʀɴᴀᴍᴇ: —",
        f"ɪᴅ: <code>{user_obj.id}</code>",
        f"💬 ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs: <b>{db_user.total_messages}</b>",
        f"🏆 ʟᴇᴠᴇʟ: <b>{db_user.level}</b>",
        "",
        f"— {TIMEFRAME_LABELS[timeframe]} ɢʀᴏᴜᴘ sᴛᴀᴛs —",
        "",
    ]

    groups = await get_user_groups_with_counts(
        user_obj.id, timeframe=timeframe, limit=20, bot=bot
    )
    if not groups:
        lines.append("📭 ɴᴏ ᴀᴄᴛɪᴠɪᴛʏ ʏᴇᴛ.")
    else:
        for g in groups:
            title = g["title"] or "ɢʀᴏᴜᴘ"
            link = g["link"]
            count = g["count"]
            # Group name clickable
            lines.append(
                f'• <a href="{link}">{title}</a> — <b>{count}</b> ᴍsɢs'
            )

    return "\n".join(lines)


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await get_user(user.id)
    if not db_user:
        await update.message.reply_text("❌ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ. /start ᴋᴀʀᴇɪɴ.")
        return

    text = await _build_profile_text(user, db_user, "all", bot=context.bot)
    await update.message.reply_text(
        text,
        reply_markup=profile_keyboard("all"),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


async def profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    if not data.startswith("prof_"):
        return

    timeframe = data.replace("prof_", "")
    if timeframe not in TIMEFRAME_LABELS:
        timeframe = "all"

    user = query.from_user
    db_user = await get_user(user.id)
    if not db_user:
        await query.edit_message_text("❌ ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.")
        return

    text = await _build_profile_text(user, db_user, timeframe, bot=context.bot)
    try:
        await query.edit_message_text(
            text,
            reply_markup=profile_keyboard(timeframe),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    except Exception:
        pass


# ─────────────────────────────────────────────────────────
#  /mygifts
# ─────────────────────────────────────────────────────────
async def mygifts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await get_user(user.id)
    gifts = db_user.gifts if db_user else 0
    await update.message.reply_text(
        f"🎁 <b>ʏᴏᴜʀ ɢɪғᴛs</b>\n\nᴛᴏᴛᴀʟ: <b>{gifts}</b>",
        parse_mode="HTML",
    )


# ─────────────────────────────────────────────────────────
#  /groupstats
# ─────────────────────────────────────────────────────────
async def groupstats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ ɢʀᴏᴜᴘ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ.")
        return

    async with async_session() as session:
        result = await session.execute(
            select(Group).where(Group.group_id == chat.id)
        )
        group = result.scalar_one_or_none()

    if not group:
        await update.message.reply_text("📭 ɴᴏ ᴅᴀᴛᴀ ʏᴇᴛ.")
        return

    today_count = await get_today_message_count(chat.id)

    text = (
        f"📊 <b>ɢʀᴏᴜᴘ sᴛᴀᴛs</b>\n\n"
        f"ᴛɪᴛʟᴇ: {group.title}\n"
        f"🆔 ɪᴅ: <code>{group.group_id}</code>\n"
        f"💬 ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs: <b>{group.total_messages}</b>\n"
        f"⏰ ᴛᴏᴅᴀʏ: <b>{today_count}</b>"
    )
    await update.message.reply_text(text, parse_mode="HTML")
