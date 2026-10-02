from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import start_keyboard, help_keyboard
from utils.constants import START_TEXT, HELP_MENU_TEXT
from utils.helpers import get_user_pfp
from services.user_service import get_or_create_user
from services.group_service import get_or_create_group
from config import OWNER_PFP, BOT_NAME, OWNER_NAME

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # Save user & group
    await get_or_create_user(user.id, user.username, user.first_name)
    if chat.type in ["group", "supergroup"]:
        await get_or_create_group(chat.id, chat.title, user.id)

    # ✅ Yahan clickable mention banaya ja raha hai
    user_mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'

    text = START_TEXT.format(
        user_mention=user_mention,   # <-- first_name ki jagah yeh pass karo
        bot_name=BOT_NAME,
        owner_name=OWNER_NAME,
    )

    # User PFP lo, agar nahi mili to owner PFP
    pfp = await get_user_pfp(context.bot, user.id, OWNER_PFP)

    try:
        await update.message.reply_photo(
            photo=pfp,
            caption=text,
            reply_markup=start_keyboard(),
            parse_mode="HTML",
        )
    except Exception:
        await update.message.reply_photo(
            photo=OWNER_PFP,
            caption=text,
            reply_markup=start_keyboard(),
            parse_mode="HTML",
        )


# Back button ke liye bhi same cheez karni hai
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help_menu":
        try:
            await query.edit_message_caption(
                caption=HELP_MENU_TEXT,
                reply_markup=help_keyboard(),
                parse_mode="HTML",
            )
        except Exception:
            await query.message.reply_text(
                HELP_MENU_TEXT,
                reply_markup=help_keyboard(),
                parse_mode="HTML",
            )
    elif query.data == "back_to_start":
        user = query.from_user
        # ✅ Yahan bhi clickable mention
        user_mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
        
        text = START_TEXT.format(
            user_mention=user_mention,
            bot_name=BOT_NAME,
            owner_name=OWNER_NAME,
        )
        await query.edit_message_caption(
            caption=text,
            reply_markup=start_keyboard(),
            parse_mode="HTML",
        )
