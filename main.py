import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from config import BOT_TOKEN
from database.db import init_db
from handlers.start import start_command, help_callback
from handlers.help import help_category_callback, help_command
from handlers.stats import stats_command
from handlers.bot_stats import bot_stats_command
from handlers.group_activity import track_group_activity
from handlers.rankings import rankings_command, top_command, rankings_callback
from handlers.admin import (
    broadcast_command,
    ping_command,
    profile_command,
    mygifts_command,
    groupstats_command,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def post_init(app):
    await init_db()
    logger.info("Database initialized.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    # ── Commands ─────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("rankings", rankings_command))
    app.add_handler(CommandHandler("top", top_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("mygifts", mygifts_command))
    app.add_handler(CommandHandler("ping", ping_command))
    app.add_handler(CommandHandler("groupstats", groupstats_command))

    # ── Owner-only commands ──────────────────────────────────
    app.add_handler(CommandHandler("botstats", bot_stats_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))

    # ── Callback queries ─────────────────────────────────────
    app.add_handler(CallbackQueryHandler(
        help_callback, pattern="^(help_menu|back_to_start)$"
    ))
    app.add_handler(CallbackQueryHandler(
        help_category_callback, pattern="^cmd_"
    ))
    app.add_handler(CallbackQueryHandler(
        rankings_callback, pattern="^rank_"
    ))

    # ── Group activity tracker (must be last) ────────────────
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, track_group_activity
    ))

    logger.info("Bot starting...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
