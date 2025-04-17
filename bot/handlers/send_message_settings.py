from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from functions.database_functions import add_channel, remove_channel, get_channels
from functions.step_functions import Parts, set_step, delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from settings.strings import ENTER_USER_ID, SELECT, ENTER_MESSAGE
from . import client


# CallbackQuery handler, show send message panel
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_PANEL))
async def send_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.back_to(BackToEnum.ADMIN_PANEL))
    
    finally:
        pass


# CallbackQuery handler, set step for send message to all users in db
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_TO_USERS))
async def send_to_users_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SEND_TO_USERS)
        await event.edit(ENTER_MESSAGE, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
    
    
# CallbackQuery handler, set step for send message to one user
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_TO_USER))
async def send_to_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SEND_TO_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
