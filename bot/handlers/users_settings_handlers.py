# region imports

from telethon.events import NewMessage, CallbackQuery, StopPropagation
from telethon.custom import Message
from telethon.types import PeerUser
from functions.step_functions import Parts, set_step, delete_step, get_user_step
from functions.filters_functions import set_filter
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from settings.strings import (
    ENTER_USER_ID,
    SELECT, 
    UPDATED,
    USER_NOT_EXIST,
    ERROR,
    NOT_SEND,
    SENDED,
    SEND_AMOUNT,
    increase_user_balance,
    reduce_user_balance,
    user_info as user_info_str, 
)
from settings.client import client
from settings.database import SessionLocal, UserModel

# endregion


# region CallbackQuery Handlers

# CallbackQuery handler, show user panel for ban, unban and more
@client.on(event=CallbackQuery(data=InlineButtonsData.USER_SETTING_PANEL, func=lambda e: set_filter(e, is_admin=True)))
async def user_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.USER_SETTING)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for ban user
@client.on(event=CallbackQuery(data=InlineButtonsData.BAN_USER, func=lambda e: set_filter(e, is_admin=True)))
async def ban_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.BAN_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for unban user
@client.on(event=CallbackQuery(data=InlineButtonsData.UNBAN_USER, func=lambda e: set_filter(e, is_admin=True)))
async def unban_user_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.UNBAN_USER)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation

    
# CallbackQuery handler, set step for show user info
@client.on(event=CallbackQuery(data=InlineButtonsData.SHOW_USER_INFO, func=lambda e: set_filter(e, is_admin=True)))
async def show_user_info_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.SHOW_USER_INFO)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for increase user balance
@client.on(event=CallbackQuery(data=InlineButtonsData.INCREASE_USER_BALANCE, func=lambda e: set_filter(e, is_admin=True)))
async def increase_user_balance_set_step(event: CallbackQuery.Event) -> None:
    
    try:
        
        set_step(event.sender_id, Parts.GET_USER_FOR_INCREASE_BALANCE)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for add reduce user balance
@client.on(event=CallbackQuery(data=InlineButtonsData.REDUCE_USER_BALANCE, func=lambda e: set_filter(e, is_admin=True)))
async def reduce_user_balance_set_step(event: CallbackQuery.Event) -> None:
    
    try:
        
        set_step(event.sender_id, Parts.GET_USER_FOR_REDUCE_BALANCE)
        await event.edit(ENTER_USER_ID, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# endregion


# region NewMessage Handlers

# NewMessage handler, Ban user
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*$", func=lambda e: set_filter(e, is_admin=True, user_step=Parts.BAN_USER)))
async def ban_user_from_bot(event: Message) -> None:
    
    try:
    
        user = int(event.message.message)
        
        with SessionLocal() as session:
            user = session.query(UserModel).filter_by(user_id=user).first()
            
            if user:
                user.is_ban = True
                session.commit()
                await event.reply(UPDATED, buttons=InlineButtons.USER_SETTING)
                delete_step(user_id=event.sender_id)
            
            else:
                await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
        
    finally:
        raise StopPropagation


# NewMessage handler, UnBan user
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*$", func=lambda e: set_filter(e, is_admin=True, user_step=Parts.UNBAN_USER)))
async def unban_user_from_bot(event: Message) -> None:
    
    try:
    
        user = int(event.message.message)
        
        with SessionLocal() as session:
            user = session.query(UserModel).filter_by(user_id=user).first()
            
            if user:
                user.is_ban = False
                session.commit()
                await event.reply(UPDATED, buttons=InlineButtons.USER_SETTING)
                delete_step(user_id=event.sender_id)
            
            else:
                await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
        
    finally:
        raise StopPropagation
    
    
# NewMessage handler, show user info
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*$", func=lambda e: set_filter(e, is_admin=True, user_step=Parts.SHOW_USER_INFO)))
async def get_user_info(event: Message) -> None:
    
    try:
    
        user = int(event.message.message)
        
        with SessionLocal() as session:
            user = session.query(UserModel).filter_by(user_id=user).first()
            
            if user:
                await event.reply(await user_info_str(user), buttons=InlineButtons.USER_SETTING)
                delete_step(user_id=event.sender_id)
            
            else:
                await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
        
    finally:
        raise StopPropagation


# NewMessage handler, get user for increase/redice user balance
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*$", func=lambda e: set_filter(e, is_admin=True, user_step=[Parts.INCREASE_USER_BALANCE, Parts.REDUCE_USER_BALANCE])))
async def get_user_for_work(event: Message) -> None:
    try:
        
        user_id = int(event.message.message)
        
        with SessionLocal() as session:
            
            user = session.query(UserModel).filter_by(user_id=user_id).first()
            
            if user:
                
                user_step = get_user_step(event.sender_id)
                
                set_step(
                    user_id=event.sender_id,
                    step=Parts.INCREASE_USER_BALANCE if user_step.step == Parts.GET_USER_FOR_INCREASE_BALANCE else Parts.REDUCE_USER_BALANCE,
                    user_geted=user_id,
                )
                
                await event.reply(SEND_AMOUNT, buttons=InlineButtons.CANCEL_ADMIN)
            
            else:
                await event.reply(USER_NOT_EXIST, buttons=InlineButtons.CANCEL_ADMIN)
    
    except Exception as e:
        await event.reply(ERROR, buttons=InlineButtons.ADMIN_PANEL)
        delete_step(event.sender_id)
    
    finally:
        raise StopPropagation


# NewMessage handler, show increase user balance
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*\.?[0-9]*$", func=lambda e: set_filter(e, is_admin=True, user_step=Parts.INCREASE_USER_BALANCE)))
async def increase_user_balance_get_value(event: Message) -> None:
    
    try:
    
        value = float(event.message.message)
        
        with SessionLocal() as session:
            
            user_step = get_user_step(event.sender_id)
            user = session.query(UserModel).filter_by(user_id=user_step.user_geted).first()
            user.balance += value
            session.commit()
            
            await event.reply(UPDATED, buttons=InlineButtons.USER_SETTING)
            
            try:
                await client.send_message(PeerUser(user_step.user_geted), message=increase_user_balance(value=value))
                await event.reply(SENDED)
            except: 
                await event.reply(NOT_SEND)
            
    except Exception as e:
        await event.reply(ERROR, buttons=InlineButtons.ADMIN_PANEL)
    
    finally:
        delete_step(event.sender_id)
        raise StopPropagation


# NewMessage handler, show reduce user balance
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*\.?[0-9]*$", func=lambda e: set_filter(e, is_admin=True, user_step=Parts.REDUCE_USER_BALANCE)))
async def reduce_user_balance_get_value(event: Message) -> None:
    
    try:
    
        value = float(event.message.message)
        
        with SessionLocal() as session:
            
            user_step = get_user_step(event.sender_id)
            user = session.query(UserModel).filter_by(user_id=user_step.user_geted).first()
            user.balance -= value
            session.commit()
            
            await event.reply(UPDATED, buttons=InlineButtons.USER_SETTING)
            
            try:
                await client.send_message(PeerUser(user_step.user_geted), message=reduce_user_balance(value=value))
                await event.reply(SENDED)
            except: 
                await event.reply(NOT_SEND)
            
    except Exception as e:
        await event.reply(ERROR, buttons=InlineButtons.ADMIN_PANEL)
    
    finally:
        delete_step(event.sender_id)
        raise StopPropagation


# endregion
