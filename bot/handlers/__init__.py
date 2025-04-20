from telethon import TelegramClient
from settings.config import API_HASH, API_ID, SESSION_NAME, BOT_TOKEN


client = TelegramClient(
    session=SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH
).start(bot_token=BOT_TOKEN)


from .admin_settings_handlers import *
from .back_handlers import *
from .bot_settings_handlers import *
from .bot_stats_handlers import *
from .cancel_handlers import *
from .channels_settings import *
from .check_user_handler import *
from .send_message_settings import *
from .start_menu_handlers import *
from .users_settings_handlers import *
