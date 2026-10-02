from telegram import Update
from telegram.ext import ContextTypes
from services.user_service import increment_user_messages, get_or_create_user
from services.group_service import increment_group_messages, update_group_member
from services.message_service import log_message


async def track_group_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Track ALL message types in groups (text, sticker, gif, photo, video, voice, etc.)
    EXCEPT commands (messages starting with '/').
    """
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    # ── Basic checks ─────────────────────────────────────────
    if not message or not user or not chat:
        return
    if chat.type not in ["group", "supergroup"]:
        return
    if user.is_bot:
        return

    # ── Command skip (koi bhi message jo '/' se start ho) ────
    # Yeh text, caption dono check karta hai
    text = message.text or message.caption or ""
    if text.startswith("/"):
        return

    # ── Bot commands ko skip karo (jaise /start@botname) ─────
    if message.entities:
        for ent in message.entities:
            if ent.type == "bot_command" and ent.offset == 0:
                return

    user_id = user.id
    group_id = chat.id

    # ── Ensure user exists in DB ─────────────────────────────
    await get_or_create_user(user_id, user.username, user.first_name)

    # ── Update all counters ──────────────────────────────────
    await increment_user_messages(user_id)
    await increment_group_messages(group_id)
    await update_group_member(group_id, user_id)
    await log_message(user_id, group_id)
