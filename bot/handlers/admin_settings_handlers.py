# region imports

from telethon.events import NewMessage, CallbackQuery, StopPropagation
from telethon.custom import Message
from functions.database_functions import add_admin, remove_admin, get_admins
from functions.step_functions import Parts, set_step, delete_step
from functions.filters_functions import filter_admin_move, filter_add_admin, filter_del_admin
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from buttons.commands import Commands
from settings.strings import (
    show_admins as string_show_admins, 
    ENTER_USER_ID, 
    SELECT, 
    ADMIN_PANEL,
    USER_NOT_EXIST,
    ADDED
)
from settings.client import client

# endregion


# region CallBackQuery Handlers

# CallbackQuery handler, show bots admins settings
@client.on(event=CallbackQuery(data=InlineButtonsData.ADMIN_SETTING_PANEL, func=filter_admin_move))
async def admin_settings_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.back_to(BackToEnum.ADMIN_PANEL))
        
    finally:
        raise StopPropagation


# CallbackQuery handler, show bots admins
@client.on(event=CallbackQuery(data=InlineButtonsData.SHOW_ADMINS, func=filter_admin_move))
async def show_admins(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(string_show_admins(admins=await get_admins()), buttons=InlineButtons.back_to(BackToEnum.ADMIN_SETTING))
        
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for add admin
@client.on(event=CallbackQuery(data=InlineButtonsData.ADD_ADMIN, func=filter_admin_move))
async def add_admin_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.ADD_ADMIN)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    

# CallbackQuery handler, set step for remove admin
@client.on(event=CallbackQuery(data=InlineButtonsData.DELETE_ADMIN, func=filter_admin_move))
async def remove_admin_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.DELETE_ADMIN)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
        
    finally:
        raise StopPropagation


# endregion


# region NewMessage Handlers


# NewMessage handler, open panel admin
@client.on(event=NewMessage(incoming=True, pattern=Commands.ADMIN, func=filter_admin_move))
async def open_admin_panel(event: Message) -> None:
    try:
        
        await event.reply(ADMIN_PANEL, buttons=InlineButtons.ADMIN_PANEL)
        
    finally:
        raise StopPropagation


# NewMessage handler, get admin user id and add to db
@client.on(event=NewMessage(incoming=True, pattern=r"[0-9]*", func=filter_add_admin))
async def new_admin(event: Message) -> None:
    
    try:
        
        user = int(event.message.message)
        add = add_admin(user_id=user)
        if not add:
            await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
            return None
        delete_step(user_id=event.sender_id)
        await event.reply(ADDED, buttons=InlineButtons.ADMIN_SETTING)
    
    finally:
        
        raise StopPropagation


# NewMessage handler, get admin user id and check in db? and remove from db
@client.on(event=NewMessage(incoming=True, pattern=r"[0-9]*", func=filter_del_admin))
async def delete_admin(event: Message) -> None:
    try:
        user = int(event.message.message)
        add = remove_admin(user_id=user)
        if not add:
            await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
            return None
        
        delete_step(user_id=event.sender_id)
        await event.reply(ADDED, buttons=InlineButtons.ADMIN_SETTING)
    
    finally:
        raise StopPropagation

# endregion
