from telegram import ReplyKeyboardMarkup

def main_reply_keyboard():
    keyboard = [
        ["📊 sᴛᴀᴛs", "🏆 ʀᴀɴᴋɪɴɢs"],
        ["🎁 ᴍʏ ɢɪғᴛs", "👤 ᴘʀᴏғɪʟᴇ"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
