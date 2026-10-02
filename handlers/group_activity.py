from telegram import Update
from telegram.ext import ContextTypes
from services.user_service import increment_user_messages, get_or_create_user
from services.group_service import increment_group_messages, update_group_member
from services.message_service import log_message

async def track_group_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    if update.effective_chat.type not in ["group", "supergroup"]:
        return
    if update.effective_user.is_bot:
        return

    user_id = update.effective_user.id
    group_id = update.effective_chat.id

    # Ensure user exists
    await get_or_create_user(
        user_id,
        update.effective_user.username,
        update.effective_user.first_name,
    )

    await increment_user_messages(user_id)
    await increment_group_messages(group_id)
    await update_group_member(group_id, user_id)
    await log_message(user_id, group_id)
