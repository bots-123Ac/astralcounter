from telegram import Update
from telegram.ext import ContextTypes

from services.user_service import increment_user_messages, get_or_create_user
from services.group_service import (
    increment_group_messages,
    update_group_member,
    get_or_create_group,
)
from services.message_service import (
    log_message,
    get_today_message_count,
    maybe_send_milestone,
)

# Telegram's anonymous admin bot id
ANONYMOUS_ADMIN_ID = 1087968824


async def track_group_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    # ── Basic checks ─────────────────────────────────────────
    if not message or not chat:
        return
    if chat.type not in ["group", "supergroup"]:
        return

    # ── Anonymous admin / channel post → skip ───────────────
    if message.sender_chat is not None:
        return
    if not user:
        return
    if user.id == ANONYMOUS_ADMIN_ID:
        return
    if user.is_bot:
        return

    # ── Commands ko skip karo ────────────────────────────────
    text = message.text or message.caption or ""
    if text.startswith("/"):
        return

    if message.entities:
        for ent in message.entities:
            if ent.type == "bot_command" and ent.offset == 0:
                return
    if message.caption_entities:
        for ent in message.caption_entities:
            if ent.type == "bot_command" and ent.offset == 0:
                return

    user_id = user.id
    group_id = chat.id

    # ── Save user + group (title bhi update karo har baar) ───
    await get_or_create_user(user_id, user.username, user.first_name)
    await get_or_create_group(group_id, chat.title, user_id)

    # ── Counters ─────────────────────────────────────────────
    await increment_user_messages(user_id)
    await increment_group_messages(group_id)
    await update_group_member(group_id, user_id)
    await log_message(user_id, group_id)

    # ── Milestone check ──────────────────────────────────────
    try:
        today_count = await get_today_message_count(group_id)
        await maybe_send_milestone(context.bot, group_id, today_count)
    except Exception:
        pass
