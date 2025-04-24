# region imports

from telethon.events import NewMessage, CallbackQuery, StopPropagation
from telethon.custom import Message
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.types import Channel, PeerChannel
from functions.step_functions import Parts, set_step, delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from settings.strings import (
    SELECT, 
    ADD_CHANNEL, 
    ERROR, 
    DELETED,
    ADDED,
    CHANNEL_ALREADY_EXIST,
    BOT_NOT_ADMIN
)
from functions.filters_functions import filter_admin_move, filter_add_channel, filter_delete_channel
from settings.client import client
from settings.database import SessionLocal, ChannelModel

# endregion


# region CallBackQuery Handlers

# CallbackQuery handler, show bots channels settings
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANNEL_PANEL, func=filter_admin_move))
async def channels_panel(event: CallbackQuery.Event) -> None:
    
    try:
        with SessionLocal() as session:
            channels = session.query(ChannelModel).all()
            await event.edit(SELECT, buttons=await InlineButtons.channels_panel(channels=channels))
    
    except Exception as e:
        print(e)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for add channels
@client.on(event=CallbackQuery(data=InlineButtonsData.ADD_CHANNEL, func=filter_admin_move))
async def add_channel_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.ADD_CHANNEL)
        await event.edit(ADD_CHANNEL, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    
    
# CallBack handler, get channels user id and check in db? and remove from db
@client.on(event=CallbackQuery(func=filter_delete_channel))
async def delete_channel(event: CallbackQuery.Event) -> None:
    
    try:        
        channel_id = int(str(event.data.decode()).replace(InlineButtonsData.DELETE_CHANNEL.decode(), ''))
        with SessionLocal() as session:
            channel = session.query(ChannelModel).filter_by(channel_id=channel_id).first()
            channels = session.query(ChannelModel).all()
            if channel:
                session.delete(channel)
                session.commit()
                await event.edit(DELETED, buttons=await InlineButtons.channels_panel(channels=channels))
            else:
                
                await event.edit(ERROR, buttons=await InlineButtons.channels_panel(channels=channels))
    
    except Exception as e:
        print(e)
        
    finally:
        raise StopPropagation


# endregion


# region NewMessage Handlers


# NewMessage handler, get channels user id and add to db
@client.on(event=NewMessage(forwards=True, incoming=True, func=filter_add_channel))
async def new_channel(event: Message) -> None:
    
    try:
        
        channel = await event.forward.get_chat()
        if not isinstance(channel , Channel):
            await event.reply(ADD_CHANNEL)
            return
            
        if not channel.admin_rights:
            await event.reply(BOT_NOT_ADMIN, buttons=InlineButtons.CANCEL_ADMIN)
            return
        
        
        with SessionLocal() as session:
            check_channel = session.query(ChannelModel).filter_by(channel_id=channel.id).first()

            if not check_channel:
                
                channel_info = await client(GetFullChannelRequest(PeerChannel(int(channel.id))))
                channel_add = ChannelModel(
                    channel_id=channel.id,
                    channel_name=channel.title,
                    channel_url=channel_info.full_chat.exported_invite.link
                )
            
                session.add(channel_add)
                session.commit()
                
                delete_step(user_id=event.sender_id)
                channels = session.query(ChannelModel).all()
                await event.reply(ADDED, buttons=await InlineButtons.channels_panel(channels=channels))
    
            else:
                await event.reply(CHANNEL_ALREADY_EXIST)
    
    except Exception as e:
        await event.reply(f"{ADD_CHANNEL}\n\n{ERROR} : \n{e}", buttons=InlineButtons.CANCEL_ADMIN)
                        
    finally:
        
        raise StopPropagation


# endregion
