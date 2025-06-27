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
        raise StopPropagation


# CallbackQuery handler, set step for send message to all users in db
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_TO_USERS, func=filter_admin_move))
async def send_to_users_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SEND_TO_USERS)
        await event.edit(ENTER_MESSAGE, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation

    
# CallbackQuery handler, set step for send message to one user
@client.on(event=CallbackQuery(data=InlineButtonsData.SEND_TO_USER, func=filter_admin_move))
async def send_to_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SEND_TO_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for forward message to one user
@client.on(event=CallbackQuery(data=InlineButtonsData.FORWARD_TO_USER, func=filter_admin_move))
async def forward_to_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.FORWARD_TO_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    

# CallbackQuery handler, set step for forward message to one users
@client.on(event=CallbackQuery(data=InlineButtonsData.FORWARD_TO_USERS, func=filter_admin_move))
async def forward_to_users_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.FORWARD_TO_USERS)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    


# endregion


# region NewMessage Handlers

# NewMessage handler, set step for send message to all users in db
@client.on(event=NewMessage(incoming=True, func=filter_get_message_send_users))
async def get_message_send_to_users(event: Message) -> None:
    
    try:
    
        func = client.send_message if get_user_step(event.sender_id) == Parts.SEND_TO_USERS else client.forward_messages
        delete_step(user_id=event.sender_id)
        await client.send_message(event.sender_id, SENDING, buttons=InlineButtons.SEND_PANEL)
        
        success = 0
        
        with SessionLocal() as session:
            
            users = session.query(UserModel).all()
        
            for user in users:
                try:
                    await func(PeerUser(user.user_id), event.message)
                    success += 1
                    await asyncio.sleep(0.05)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds + 2)
                except Exception as e:
                    continue
        
        await event.reply(message_sended(success_num=success))
        
    finally:
        raise StopPropagation


@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*$", func=filter_get_user_send))
async def get_user_send_to_user(event: Message) -> None:
    
    try:
    
        user_id = int(event.message.message)
        user_step = get_user_step(event.sender_id)
        
        with SessionLocal() as session:
            user = session.query(UserModel).filter_by(user_id=user_id).first()
            if user:
                set_step(
                    user_id=event.sender_id, 
                    step=Parts.GET_MESSAGE_SEND_TO_USER if user_step.step == Parts.GET_MESSAGE_SEND_TO_USER else Parts.GET_MESSAGE_FORWARD_TO_USER,
                    user_geted=user_id
                )
                await event.reply(ENTER_MESSAGE, buttons=InlineButtons.CANCEL_ADMIN)
            
            else:
                await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
    
    except Exception as e:
        print(e)
    
    finally:
        raise StopPropagation
    

@client.on(event=NewMessage(incoming=True, func=filter_get_message_send_user))
async def get_message_send_to_user(event: Message) -> None:
    
    try:
    
        try:

            user_step = get_user_step(event.sender_id)
            
            if user_step.step == Parts.GET_MESSAGE_SEND_TO_USER:
            
                await client.send_message(PeerUser(user_id=user_step.user_geted), message=event.message)
            
            else: 
                await client.forward_messages(PeerUser(user_id=user_step.user_geted), messages=event.message)
                
            await event.reply(message_sended(1), buttons=InlineButtons.SEND_PANEL)

        except Exception as e:
            print(e)
            await event.reply(NOT_SEND, buttons=InlineButtons.SEND_PANEL)

        finally:
            delete_step(user_id=event.sender_id)

    finally:
        raise StopPropagation  
    
# endregion
