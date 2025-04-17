from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from functions.database_functions import add_channel, remove_channel, get_channels
from functions.step_functions import Parts, set_step, delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from settings.strings import ENTER_USER_ID, SELECT, ADD_CHANNEL, ERROR, DELETED
from . import client


# CallbackQuery handler, show bots channels settings
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANNEL_PANEL))
async def channels_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=await InlineButtons.channels_panel())
    
    finally:
        pass


# CallbackQuery handler, set step for add channels
@client.on(event=CallbackQuery(data=InlineButtonsData.ADD_CHANNEL))
async def add_channel_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.ADD_CHANNEL)
        await event.edit(ADD_CHANNEL, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
    
    
# CallBack handler, get channels user id and check in db? and remove from db
@client.on(event=CallbackQuery(pattern=f"^b{InlineButtonsData.DELETE_CHANNEL}"))
async def delete_channel(event: Message) -> None:
    
    try:
        
        channel_id = int(str(event.data.decode()).replace(InlineButtonsData.DELETE_CHANNEL, ''))
        if await remove_channel(channel_id=channel_id):
            await event.edit(DELETED, buttons=await InlineButtons.channels_panel())
        else:
            await event.edit(ERROR, buttons=await InlineButtons.channels_panel())
        
    finally:
        pass


# NewMessage handler, get channels user id and add to db
@client.on(event=NewMessage())
async def new_channel(event: Message) -> None:
    pass
