import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "7790607144"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///astral_counter.db")

# Bot branding
BOT_NAME = "˹𝐀𝐬𝐭𝐫𝐚𝐥 ꭙ 𝐂𝐨𝐮𝐧𝐭𝐞𝐫˼"
BOT_USERNAME = "@astralXcounterBot"
OWNER_NAME = "⏤͟͞ 𝐂𝐑𝐀𝐙𝐘 𝐁𝐎𝐘 ᭄࿐"
OWNER_PFP = "https://files.catbox.moe/424au6.jpg"
GROUP_LINK = "https://t.me/+-j8FiVjAUXExMmM1"
CHANNEL_LINK = "https://t.me/Astral_study_chest"
