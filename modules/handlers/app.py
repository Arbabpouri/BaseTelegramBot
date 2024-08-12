from telethon import TelegramClient
from config import BotConfig

client = TelegramClient(
    session=BotConfig.SESSION_NAME,
    api_id=BotConfig.API_ID,
    api_hash=BotConfig.API_HASH
).start(bot_token=BotConfig.BOT_TOKEN)
