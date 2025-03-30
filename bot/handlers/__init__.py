from telethon import TelegramClient
from settings import BotConfig


client = TelegramClient(
    session=BotConfig.SESSION_NAME,
    api_id=BotConfig.API_ID,
    api_hash=BotConfig.API_HASH
).start(bot_token=BotConfig.BOT_TOKEN)


from .admin_settings_handlers import *
from .send_message_settings import *
from .channels_settings import *
