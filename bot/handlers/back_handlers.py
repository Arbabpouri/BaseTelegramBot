# region imports

from telethon.events import CallbackQuery, NewMessage
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from buttons.text_buttons import TextButtons, TextButtonsString
from settings.strings import BACKED
from functions.filters_functions import filter_admin_move
from . import client

# endregion


# region CallBackQuery Handlers

# CallbackQuery handler, back to admin panel
@client.on(event=CallbackQuery(data=InlineButtonsData.BACK_TO_ADMIN, func=filter_admin_move))
async def back_to_admin_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(BACKED, buttons=InlineButtons.ADMIN_PANEL)
    
    finally:
        pass
    
    

# CallbackQuery handler, back to admin settings
@client.on(event=CallbackQuery(data=InlineButtonsData.BACK_TO_ADMIN, func=filter_admin_move))
async def back_to_admin_setting(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(BACKED, buttons=InlineButtons.ADMIN_SETTING)
    
    finally:
        pass
    

# endregion


# region NewMessage Handlers

# NewMessage handler, back to start menu panel
@client.on(event=NewMessage(pattern=TextButtonsString.BACK_TO_START))
async def back_to_start_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.reply(BACKED, buttons=TextButtons.START_MENU)
    
    finally:
        pass
    
# endregion
