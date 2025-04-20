# region imports

from telethon.events import NewMessage, CallbackQuery, StopPropagation
from telethon.custom import Message
from telethon.types import PeerUser
from telethon.errors import FloodWaitError
import asyncio
from functions.step_functions import Parts, set_step, delete_step, get_user_step
from functions.filters_functions import (
    filter_admin_move,
    filter_get_message_send_user,
    filter_get_message_send_users,
    filter_get_user_send
    
)
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from settings.strings import ENTER_USER_ID, SELECT, ENTER_MESSAGE, SENDING, message_sended, USER_NOT_EXIST, NOT_SEND
from settings.client import client
from settings.database import SessionLocal, UserModel

# endregion


# region CallbackQuery Handlers

# CallbackQuery handler, show send message panel
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_PANEL, func=filter_admin_move))
async def send_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.SEND_PANEL)
    
    finally:
        pass


# CallbackQuery handler, set step for send message to all users in db
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_TO_USERS, func=filter_admin_move))
async def send_to_users_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SEND_TO_USERS)
        await event.edit(ENTER_MESSAGE, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        pass
    
    
# CallbackQuery handler, set step for send message to one user
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_TO_USER, func=filter_admin_move))
async def send_to_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SEND_TO_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        pass

# endregion


# region NewMessage Handlers

# NewMessage handler, set step for send message to all users in db
@client.on(event=NewMessage(incoming=True, func=filter_get_message_send_users))
async def get_message_send_to_users(event: Message) -> None:
    
    try:
    
        delete_step(user_id=event.sender_id)
        await client.send_message(event.sender_id, SENDING, buttons=InlineButtons.SEND_PANEL)
        
        success = 0
        
        with SessionLocal() as session:
            
            users = session.query(UserModel).all()
        
            for user in users:
                try:
                    await client.send_message(PeerUser(user.user_id), message=event.message)
                    success += 1
                    await asyncio.sleep(0.1)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds + 2)
                except Exception as e:
                    continue
        
        await event.reply(message_sended(success_num=success))
        
    finally:
        raise StopPropagation


@client.on(event=NewMessage(pattern=r"[0-9]*", incoming=True, func=filter_get_user_send))
async def get_user_send_to_user(event: Message) -> None:
    
    try:
    
        user = int(event.message.message)
        
        with SessionLocal() as session:
            user = session.query(UserModel).filter_by(user_id=user).first()
            if user:
                set_step(user_id=event.sender_id, step=Parts.GET_MESSAGE_SEND_TO_USER)
                await event.reply(ENTER_MESSAGE, buttons=InlineButtons.CANCEL_ADMIN)
            
            else:
                await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    

@client.on(event=NewMessage(incoming=True, func=filter_get_message_send_user))
async def get_message_send_to_user(event: Message) -> None:
    
    try:
    
        try:
            user_step = get_user_step(event.sender_id)
            await client.send_message(PeerUser(user_id=user_step.user_geted), message=event.message)
            await event.reply(message_sended(1))
        except:
            await event.reply(NOT_SEND)
        finally:
            delete_step(user_id=event.sender_id)

    finally:
        raise StopPropagation  
    
# endregion
