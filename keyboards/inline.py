from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import GROUP_LINK, CHANNEL_LINK, SUPPORT_LINK, OWNER_ID, BOT_USERNAME


# ─────────────────────────────────────────────────────────
#  START MENU
# ─────────────────────────────────────────────────────────
def start_keyboard():
    keyboard = [
        [InlineKeyboardButton(
            "➕ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕",
            url=f"https://t.me/{BOT_USERNAME.lstrip('@')}?startgroup=true"
        )],
        [InlineKeyboardButton("📖 ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs 📖", callback_data="help_menu")],
        [InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", url=f"tg://user?id={OWNER_ID}")],
        [
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url=CHANNEL_LINK),
            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_LINK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ─────────────────────────────────────────────────────────
#  HELP MENU
# ─────────────────────────────────────────────────────────
def help_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔴 sᴛᴀᴛs", callback_data="cmd_stats"),
            InlineKeyboardButton("🟢 ʀᴀɴᴋɪɴɢs", callback_data="cmd_rankings"),
            InlineKeyboardButton("🔵 ᴘʀᴏғɪʟᴇ", callback_data="cmd_profile"),
        ],
        [
            InlineKeyboardButton("🟡 ɢɪғᴛs", callback_data="cmd_gifts"),
            InlineKeyboardButton("🟠 ᴛᴏᴘ", callback_data="cmd_top"),
            InlineKeyboardButton("🟣 ᴘɪɴɢ", callback_data="cmd_ping"),
        ],
        [
            InlineKeyboardButton("⚫ ɢʀᴏᴜᴘ sᴛᴀᴛs", callback_data="cmd_groupstats"),
            InlineKeyboardButton("⚪ ʜᴇʟᴘ", callback_data="cmd_help"),
        ],
        [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="back_to_start")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_keyboard():
    keyboard = [
        [InlineKeyboardButton("◀️ ʙᴀᴄᴋ ᴛᴏ ʜᴇʟᴘ", callback_data="help_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ─────────────────────────────────────────────────────────
#  RANKINGS — Timeframe buttons
# ─────────────────────────────────────────────────────────
def rankings_keyboard(current="all"):
    """Timeframe buttons for /rankings (marks the active one)."""
    def mark(tf):
        return "✅ " if tf == current else ""

    keyboard = [
        [InlineKeyboardButton(
            f"{mark('all')}📊 ᴀʟʟ ᴛɪᴍᴇ",
            callback_data="rank_all"
        )],
        [
            InlineKeyboardButton(
                f"{mark('monthly')}📅 ᴍᴏɴᴛʜʟʏ",
                callback_data="rank_monthly"
            ),
            InlineKeyboardButton(
                f"{mark('weekly')}📆 ᴡᴇᴇᴋʟʏ",
                callback_data="rank_weekly"
            ),
        ],
        [InlineKeyboardButton(
            f"{mark('today')}⏰ ᴛᴏᴅᴀʏ (24ʜ)",
            callback_data="rank_today"
        )],
    ]
    return InlineKeyboardMarkup(keyboard)


# ─────────────────────────────────────────────────────────
#  PROFILE — Timeframe buttons
# ─────────────────────────────────────────────────────────
def profile_keyboard(current="all"):
    """Timeframe buttons for /profile (marks active)."""
    def mark(tf):
        return "✅ " if tf == current else ""

    keyboard = [
        [
            InlineKeyboardButton(f"{mark('all')}📊 ᴀʟʟ ᴛɪᴍᴇ", callback_data="prof_all"),
            InlineKeyboardButton(f"{mark('monthly')}📅 ᴍᴏɴᴛʜʟʏ", callback_data="prof_monthly"),
        ],
        [
            InlineKeyboardButton(f"{mark('weekly')}📆 ᴡᴇᴇᴋʟʏ", callback_data="prof_weekly"),
            InlineKeyboardButton(f"{mark('today')}⏰ ᴛᴏᴅᴀʏ", callback_data="prof_today"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
