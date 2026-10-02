from telegram import Update
from telegram.ext import ContextTypes
from utils.constants import HELP_TEXTS
from keyboards.inline import back_keyboard

async def help_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data in HELP_TEXTS:
        await query.edit_message_caption(
            caption=HELP_TEXTS[data],
            reply_markup=back_keyboard(),
            parse_mode="HTML",
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 <b>ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs</b>\n\n"
        "<code>/start</code> — sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n"
        "<code>/help</code> — sʜᴏᴡ ᴛʜɪs ʜᴇʟᴘ\n"
        "<code>/stats</code> — ʏᴏᴜʀ ᴘᴇʀsᴏɴᴀʟ sᴛᴀᴛs\n"
        "<code>/rankings</code> — ɢʀᴏᴜᴘ ᴛᴏᴘ ᴜsᴇʀs\n"
        "<code>/top</code> — ɢʟᴏʙᴀʟ ᴛᴏᴘ ᴜsᴇʀs\n"
        "<code>/profile</code> — ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ\n"
        "<code>/mygifts</code> — ʏᴏᴜʀ ɢɪғᴛs\n"
        "<code>/ping</code> — ʙᴏᴛ ʟᴀᴛᴇɴᴄʏ\n"
        "<code>/groupstats</code> — ɢʀᴏᴜᴘ sᴛᴀᴛs"
    )
    await update.message.reply_text(text, parse_mode="HTML")
