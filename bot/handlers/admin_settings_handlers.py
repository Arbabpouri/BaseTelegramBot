from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from . import client


# CallbackQuery handler, show bots admins
@client.on(event=CallbackQuery())
async def show_admins(event: CallbackQuery.Event) -> None:
    pass


# CallbackQuery handler, set step for add admin
@client.on(event=CallbackQuery())
async def add_admin_set_step(event: CallbackQuery.Event) -> None:
    pass


# CallbackQuery handler, set step for remove admin
@client.on(event=CallbackQuery())
async def remove_admin_set_step(event: CallbackQuery.Event) -> None:
    pass


# NewMessage handler, get admin user id and add to db
@client.on(event=NewMessage())
async def add_admin(event: Message) -> None:
    pass


# NewMessage handler, get admin user id and check in db? and remove from db
@client.on(event=NewMessage())
async def remove_admin(event: Message) -> None:
    pass

