# region imports

from telethon.events import CallbackQuery, NewMessage, StopPropagation
from telethon.custom import Message
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from buttons.text_buttons import TextButtons, TextButtonsString
from buttons.url_buttons import UrlButtons
from functions.filters_functions import filter_user_move
from settings.strings import CONTACT_US, SELECT, referral_reply, referral_banner, StringsVariableChangable
from settings.config import REFERRAL_IMAGE_ADDRESS, ConfigVariableChangable
from settings.client import client
from settings.database import SessionLocal, UserModel

# endregion


# region CallBackQuery Handlers

# CallBackQuery Handler, send support username
@client.on(event=CallbackQuery(data=InlineButtonsData.MESSAGE_TO_SUPPORT_CONFIRM_RULES, func=filter_user_move))
async def send_support_username(event: CallbackQuery.Event) -> None:
    
    try:
        
        await event.edit(CONTACT_US, buttons=UrlButtons.CONTACT_US)
    
    finally:
        raise StopPropagation


# endregion

# region NewMessage Handlers

# NewMessage handler, send rules
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.RULES})", func=filter_user_move))
async def rules(event: Message) -> None:
    
    try:
        
        await event.reply(StringsVariableChangable.RULES, buttons=TextButtons.START_MENU)
    
    finally:
        raise StopPropagation
    
    
# NewMessage handler, send help text
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.HELP})", func=filter_user_move))
async def help(event: Message) -> None:
    
    try:
        await event.reply(StringsVariableChangable.HELP, buttons=await UrlButtons.support_channel(ConfigVariableChangable.SUPPORT_CHANNEL_URL))
    
    finally:
        raise StopPropagation
    

# NewMessage handler, send support 
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.CONTACT_US})", func=filter_user_move))
async def contact_us(event: Message) -> None:
    
    try:
        await event.reply(StringsVariableChangable.MESSAGE_TO_SUPPORT_TEXT, buttons=InlineButtons.MESSAGE_TO_SUPPORT)
    
    finally:
        raise StopPropagation
    
    
# NewMessage handler, send deposit panel
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.DEPOSIT_PANEL})", func=filter_user_move))
async def deposit(event: Message) -> None:
    
    try:
    
        await event.reply(SELECT, buttons=TextButtons.DEPOSIT_PLAN)
    
    finally:
        raise StopPropagation
    
    
# NewMessage handler, send referral banner
@client.on(event=NewMessage(incoming=True, pattern=fr"({TextButtonsString.REFERRAL})", func=filter_user_move))
async def referral(event: Message) -> None:
    
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
