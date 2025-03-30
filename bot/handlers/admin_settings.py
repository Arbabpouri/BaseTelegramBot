from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from . import client


# CallbackQuery handler, show bots admins

async def show_admins(event: Message) -> None:
    pass


# CallbackQuery handler, set step for add admin

async def add_admin_set_step(event: Message) -> None:
    pass


# CallbackQuery handler, set step for remove admin

async def remove_admin_set_step(event: Message) -> None:
    pass

