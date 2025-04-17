# reion imports

from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.types import Channel, PeerChannel
from functions.database_functions import add_channel, remove_channel, get_channels, get_channel
from functions.step_functions import Parts, set_step, delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from settings.strings import (
    SELECT, 
    ADD_CHANNEL, 
    ERROR, 
    DELETED,
    ADDED,
    CHANNEL_ALREADY_EXIST,
    BOT_NOT_ADMIN
)
from . import client

# endregion

# region CallBackQuery Handlers

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


# endregion


# region NewMessage Handlers


# NewMessage handler, get channels user id and add to db
@client.on(event=NewMessage(forwards=True, incoming=True))
async def new_channel(event: Message) -> None:
    
    try:
        
        channel = await event.forward.get_chat()
        if not isinstance(channel , Channel):
            await event.reply(ADD_CHANNEL)
            return
            
        if not channel.admin_rights:
            await event.reply(BOT_NOT_ADMIN, buttons=InlineButtons.CANCEL_ADMIN)
            return
        
        check_channel = get_channel(channel_id=channel.id)

        if not check_channel:
            channel_info = await client(GetFullChannelRequest(PeerChannel(int(check_channel.id))))
            add = add_channel(
                channel_id=channel.id,
                channel_name=channel.title,
                channel_url=channel_info.full_chat.exported_invite.link
            )
            
            if not add:
                await event.reply(ERROR, buttons=await InlineButtons.channels_panel())
                delete_step(user_id=event.sender_id)
            
            else:
                await event.reply(ADDED, buttons=await InlineButtons.channels_panel())
                delete_step(user_id=event.sender_id)
    
        else:
            await event.reply(CHANNEL_ALREADY_EXIST)
    
    except Exception as e:
        await event.reply(f"{ADD_CHANNEL}\n\n{ERROR} : \n{e}", buttons=InlineButtons.CANCEL_ADMIN)
                        
    finally:
        
        pass


# endregion
