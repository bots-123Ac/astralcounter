from telegram import Bot

async def get_user_pfp(bot: Bot, user_id: int, fallback: str) -> str:
    """User ki PFP le, agar nahi mili to fallback URL de."""
    try:
        photos = await bot.get_user_profile_photos(user_id, limit=1)
        if photos and photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            return file_id
    except Exception:
        pass
    return fallback
