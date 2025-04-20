# region imports

from telethon.events import NewMessage, CallbackQuery, StopPropagation
from telethon.custom import Message
from functions.database_functions import get_user, ban_user, unban_user
from functions.step_functions import Parts, set_step, delete_step
from functions.filters_functions import filter_admin_move, filter_ban_user, filter_unban_user, filter_user_info
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from settings.strings import ENTER_USER_ID, SELECT, UPDATED, USER_NOT_EXIST, user_info as user_info_str
from . import client

# endregion


# region CallbackQuery Handlers

# CallbackQuery handler, show user panel for ban, unban and more
@client.on(event=CallbackQuery(data=InlineButtonsData.USER_SETTING_PANEL, func=filter_admin_move))
async def user_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.USER_SETTING)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for add channels
@client.on(event=CallbackQuery(data=InlineButtonsData.BAN_USER, func=filter_admin_move))
async def ban_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.BAN_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for add channels
@client.on(event=CallbackQuery(data=InlineButtonsData.UNBAN_USER, func=filter_admin_move))
async def unban_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.UNBAN_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation

    
# CallbackQuery handler, set step for add channels
@client.on(event=CallbackQuery(data=InlineButtonsData.SHOW_USER_INFO, func=filter_admin_move))
async def show_user_info_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SHOW_USER_INFO)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    
# endregion


# region NewMessage Handlers

# NewMessage handler, Ban user
@client.on(event=NewMessage(pattern="[0-9]*", func=filter_ban_user))
async def ban_user_from_bot(event: Message) -> None:
    
    try:
    
        user = int(event.message.message)
        if await ban_user(user_id=user):
            await event.reply(UPDATED, buttons=InlineButtons.USER_SETTING)
            delete_step(user_id=event.sender_id)
            
        else:
            await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
        
    finally:
        raise StopPropagation


# NewMessage handler, UnBan user
@client.on(event=NewMessage(pattern="[0-9]*", func=filter_unban_user))
async def unban_user_from_bot(event: Message) -> None:
    
    try:
    
        user = int(event.message.message)
        if await unban_user(user_id=user):
            await event.reply(UPDATED, buttons=InlineButtons.USER_SETTING)
            delete_step(user_id=event.sender_id)
            
        else:
            await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
        
    finally:
        raise StopPropagation
    
    
# NewMessage handler, show user info
@client.on(event=NewMessage(pattern="[0-9]*", func=filter_user_info))
async def get_user_info(event: Message) -> None:
    
    try:
    
        user = int(event.message.message)
        
        if user_info := await get_user(user_id=user):
            await event.reply(await user_info(user_info), buttons=InlineButtons.USER_SETTING)
            delete_step(event.sender_id)
        
        else:
            await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation



# endregion