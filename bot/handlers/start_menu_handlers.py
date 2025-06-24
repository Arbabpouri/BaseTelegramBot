# region imports

from telethon.events import CallbackQuery, NewMessage, StopPropagation
from buttons.text_buttons import TextButtons, TextButtonsString
from buttons.url_buttons import UrlButtons
from functions.filters_functions import filter_user_move
from settings.strings import RULES, HELP, CONTACT_US, SELECT, referral_reply, referral_banner
from settings.config import REFERRAL_IMAGE_ADDRESS, SUPPORT_CHANNEL_URL
from settings.client import client
from settings.database import SessionLocal, UserModel

# endregion


# region NewMessage Handlers

# NewMessage handler, back to start menu panel
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.RULES})", func=filter_user_move))
async def rules(event: CallbackQuery.Event) -> None:
    
    try:
        
        await event.reply(RULES, buttons=TextButtons.START_MENU)
    
    finally:
        raise StopPropagation
    
    
# NewMessage handler, back to start menu panel
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.HELP})", func=filter_user_move))
async def help(event: CallbackQuery.Event) -> None:
    
    try:
        await event.reply(HELP, buttons=await UrlButtons.support_channel(SUPPORT_CHANNEL_URL))
    
    finally:
        raise StopPropagation
    

# NewMessage handler, back to start menu panel
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.CONTACT_US})", func=filter_user_move))
async def contact_us(event: CallbackQuery.Event) -> None:
    
    try:
        await event.reply(CONTACT_US, buttons=UrlButtons.CONTACT_US)
    
    finally:
        raise StopPropagation
    
    
# NewMessage handler, back to start menu panel
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.DEPOSIT_PANEL})", func=filter_user_move))
async def deposit(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.reply(SELECT, buttons=TextButtons.DEPOSIT_PLAN)
    
    finally:
        raise StopPropagation
    
    
# NewMessage handler, back to start menu panel
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.REFERRAL})", func=filter_user_move))
async def referral(event: CallbackQuery.Event) -> None:
    
    try:
    
        with SessionLocal() as session:
            user = session.query(UserModel).filter_by(user_id=event.sender_id).first()
            message = await client.send_file(entity=event.chat_id, file=REFERRAL_IMAGE_ADDRESS, caption=referral_banner(event.sender_id))
            await client.send_message(entity=event.chat_id, message=referral_reply(user), buttons=TextButtons.DEPOSIT_PLAN, reply_to=message)
    except Exception as e:
        print(e)

    finally:
        raise StopPropagation

# endregion
