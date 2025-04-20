from telethon import TelegramClient
from settings.config import API_HASH, API_ID, SESSION_NAME, BOT_TOKEN


client = TelegramClient(
    session=SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH
).start(bot_token=BOT_TOKEN)
