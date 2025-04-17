from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from functions.database_functions import add_admin, remove_admin, user_is_admin, get_admins
from functions.step_functions import Parts, set_step, delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from buttons.commands import Commands
from buttons.text_buttons import TextButtonsString, TextButtons
from settings.strings import show_admins as string_show_admins, ENTER_USER_ID, SELECT, ADMIN_PANEL
from . import client


# region CallBackQuery Handlers

# CallbackQuery handler, show bots admins settings
@client.on(event=CallbackQuery(data=InlineButtonsData.ADMIN_SETTING_PANEL))
async def admin_settings_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.back_to(BackToEnum.ADMIN_PANEL))
        
    finally:
        pass


# CallbackQuery handler, show bots admins
@client.on(event=CallbackQuery(data=InlineButtonsData.SHOW_ADMINS))
async def show_admins(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(string_show_admins(admins=await get_admins()), buttons=InlineButtons.back_to(BackToEnum.ADMIN_SETTING))
        
    finally:
        pass


# CallbackQuery handler, set step for add admin
@client.on(event=CallbackQuery(data=InlineButtonsData.ADD_ADMIN))
async def add_admin_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.ADD_ADMIN)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
    

# CallbackQuery handler, set step for remove admin
@client.on(event=CallbackQuery(data=InlineButtonsData.DELETE_ADMIN))
async def remove_admin_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.DELETE_ADMIN)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL)
        
    finally:
        pass


# endregion


# region NewMessage Handlers

# NewMessage handler, open panel admin
@client.on(event=NewMessage(incoming=True, pattern=Commands.ADMIN))
async def open_admin_panel(event: Message) -> None:
    try:
        
        await event.reply(ADMIN_PANEL, buttons=InlineButtons.ADMIN_PANEL)
        
    finally:
        pass


# NewMessage handler, get admin user id and add to db
@client.on(event=NewMessage(incoming=True))
async def new_admin(event: Message) -> None:
    pass


# NewMessage handler, get admin user id and check in db? and remove from db
@client.on(event=NewMessage(incoming=True))
async def remove_admin(event: Message) -> None:
    pass


# endregion