from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from functions.database_functions import add_channel, remove_channel, get_channels
from functions.step_functions import Parts, set_step, delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from settings.strings import ENTER_USER_ID, SELECT, ENTER_MESSAGE
from settings.client import client


# CallbackQuery handler, show send message panel
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_PANEL))
async def join(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.back_to(BackToEnum.ADMIN_PANEL))
    
    finally:
        pass

# CallbackQuery handler, show send message panel
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_PANEL))
async def send_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.back_to(BackToEnum.ADMIN_PANEL))
    
    finally:
        pass


