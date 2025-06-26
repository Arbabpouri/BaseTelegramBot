# region imports

from telethon.events import CallbackQuery, NewMessage, StopPropagation
from telethon.types import PeerUser, PeerChannel, User
from telethon.custom import Message 
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from buttons.text_buttons import TextButtons, TextButtonsString
from functions.step_functions import Parts, set_step, delete_step, get_user_step
from settings.client import client
from settings.config import FACTORS_CHANNEL_ID
from settings.strings import (
    ERROR,
    NUMBER_FOR_DEPOSIT_CARD,
    FACTOR_FOR_DEPOSIT_CARD,
    FACTOR_NOT_FOUND,
    factor_geted,
    send_factor_to_admin,
    factor_status_to_user,
)
from functions.filters_functions import (
    filter_user_move,
    filter_get_factor_for_deposit_card,
    filter_get_number_for_deposit_card,
    filter_acc_factor,
    filter_reject_factor,
)
from settings.database import UserModel, DepositModel, SessionLocal

# endregion

# region CallBackQuery Handlers


# CallBackQuery Handler, Acc Factor
@client.on(event=CallbackQuery(func=filter_acc_factor))
async def acc_factor(event: CallbackQuery.Event) -> None:
    
    try:
        factor_id = str(event.data.decode()).replace(InlineButtonsData.ACC_FACTOR.decode(), "")
        
        with SessionLocal() as session:
            factor = session.query(DepositModel).filter(DepositModel.factor_id == factor_id).first()
            
            if not factor:
                await event.answer(FACTOR_NOT_FOUND, alert=True)
                return
            
            factor.acc_or_reject_by_user_id = event.sender_id
            factor.status = True
            factor.user.balance += factor.amount
            session.commit()
            
            await event.edit(send_factor_to_admin(factor=factor))
            
            try:
                await client.send_message(entity=PeerUser(factor.user_id), message=factor_status_to_user(factor_id=factor_id, is_accept=factor.status))
            except: pass
    
    except Exception as e:
        print(e)
    
    finally:
        raise StopPropagation


# CallBackQuery Handler, Reject Factor
@client.on(event=CallbackQuery(func=filter_reject_factor))
async def reject_factor(event: CallbackQuery.Event) -> None:
    
    try:
        factor_id = str(event.data.decode()).replace(InlineButtonsData.REJECT_FACTOR.decode(), "")
        
        with SessionLocal() as session:
            factor = session.query(DepositModel).filter(DepositModel.factor_id == factor_id).first()
            
            if not factor:
                await event.answer(FACTOR_NOT_FOUND, alert=True)
                return
            
            factor.acc_or_reject_by_user_id = event.sender_id
            factor.status = False
            session.commit()
            
            await event.edit(send_factor_to_admin(factor=factor))
            
            try:
                await client.send_message(entity=PeerUser(factor.user_id), message=factor_status_to_user(factor_id=factor_id, is_accept=factor.status))
            except: pass
    
    except Exception as e:
        print(e)
    
    finally:
        raise StopPropagation


# endregion


# region NewMessage Handlers

# NewMessage Handler, deposit with card
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.DEPOSIT_WITH_CARD})", func=filter_user_move))
async def deposit_with_card(event: Message) -> None:
    
    try:
        
        set_step(event.sender_id, Parts.GET_NUMBER_FOR_DEPOSIT_CARD)
        await event.reply(NUMBER_FOR_DEPOSIT_CARD, buttons=TextButtons.CANCEL_USER)
        
    finally:
        raise StopPropagation


# NewMessage Handler, get number for deposit with card
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*\.?[0-9]*", func=filter_get_number_for_deposit_card))
async def get_number_for_deposit_with_card(event: Message) -> None:
    
    try:
        
        set_step(event.sender_id, Parts.GET_FACTOR_FOR_DEPOSIT_CARD, number_geted=float(event.message.message))
        await event.reply(FACTOR_FOR_DEPOSIT_CARD, buttons=TextButtons.CANCEL_USER)
        
    finally:
        raise StopPropagation


# NewMessage Handler, get number for deposit with card
@client.on(event=NewMessage(incoming=True, func=filter_get_factor_for_deposit_card))
async def get_factor_for_deposit_with_card(event: Message) -> None:
    
    try:
        
        user_step = get_user_step(event.sender_id)
        sender: User = await event.get_sender()
        
        with SessionLocal() as session:
            
            factor = DepositModel(
                username=sender.username,
                account_name=sender.first_name,
                user_id=event.sender_id, 
                amount=user_step.number_geted
            )
            session.add(factor)
            session.commit()
            
            await client.send_message(
                entity=PeerChannel(FACTORS_CHANNEL_ID), 
                message=send_factor_to_admin(factor=factor), 
                file=event.media,
                buttons=InlineButtons.acc_reject_factor(factor.factor_id)
            )
            
            await event.reply(factor_geted(factor_id=factor.factor_id), buttons=TextButtons.START_MENU)
            
    
    except Exception as e:
        print(e)
        await event.reply(ERROR, buttons=TextButtons.START_MENU)
        
    finally:
        delete_step(event.sender_id)
        raise StopPropagation


# endregion
