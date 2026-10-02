from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import start_keyboard, help_keyboard
from utils.constants import START_TEXT
from services.user_service import get_or_create_user
from services.group_service import get_or_create_group
from config import OWNER_PFP

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # User & Group save
    await get_or_create_user(user.id, user.username, user.first_name)
    if chat.type in ["group", "supergroup"]:
        await get_or_create_group(chat.id, chat.title, user.id)

    text = START_TEXT.format(
        first_name=user.first_name or "User",
        bot_name="˹𝐀𝐬𝐭𝐫𝐚𝐥 ꭙ 𝐂𝐨𝐮ɴᴛᴇʀ˼",
        owner_name="⏤͟͞ 𝐂𝐑𝐀𝐙𝐘 𝐁𝐎𝐘 ᭄࿐"
    )

    await update.message.reply_photo(
        photo=OWNER_PFP,
        caption=text,
        reply_markup=start_keyboard(),
        parse_mode="HTML"
    )

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help_menu":
        await query.edit_message_caption(
            caption="❖ ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴘ\n"
                    "ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ\n\n"
                    "ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /",
            reply_markup=help_keyboard(),
            parse_mode="HTML"
        )
    elif query.data == "back_to_start":
        user = query.from_user
        text = START_TEXT.format(
            first_name=user.first_name or "User",
            bot_name="˹𝐀𝐬𝐭𝐫𝐚𝐥 ꭙ 𝐂ᴏᴜɴᴛᴇʀ˼",
            owner_name="⏤͟͞ 𝐂𝐑𝐀𝐙𝐘 𝐁𝐎𝐘 ᭄࿐"
        )
        await query.edit_message_caption(
            caption=text,
            reply_markup=start_keyboard(),
            parse_mode="HTML"
        )
