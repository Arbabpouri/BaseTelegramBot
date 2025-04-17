from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from functions.database_functions import get_user
from functions.step_functions import Parts, set_step, delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from settings.strings import ENTER_USER_ID, SELECT
from . import client


# CallbackQuery handler, show user panel for ban, unban and more
@client.on(event=CallbackQuery(data=InlineButtonsData.USER_SETTING_PANEL))
async def user_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.USER_SETTING)
    
    finally:
        pass


# CallbackQuery handler, set step for add channels
@client.on(event=CallbackQuery(data=InlineButtonsData.BAN_USER))
async def ban_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.BAN_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL)
    
    finally:
        pass


# CallbackQuery handler, set step for add channels
@client.on(event=CallbackQuery(data=InlineButtonsData.UNBAN_USER))
async def unban_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.UNBAN_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL)
    
    finally:
        pass

    
# CallbackQuery handler, set step for add channels
@client.on(event=CallbackQuery(data=InlineButtonsData.SHOW_USER_INFO))
async def show_user_info_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SHOW_USER_INFO)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
    
