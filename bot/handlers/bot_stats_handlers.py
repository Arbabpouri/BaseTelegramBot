# region imports

from telethon.events import CallbackQuery, NewMessage, StopPropagation
from buttons.inline_buttons import InlineButtonsData
from buttons.text_buttons import TextButtons, TextButtonsString
from settings.strings import bot_stats, my_account
from functions.filters_functions import filter_user_move, filter_admin_move
from settings.client import client
from settings.database import SessionLocal, UserModel, ChannelModel

# endregion


# region CallbackQuery Handlers

# CallbackQuery handler, show bot stats
@client.on(event=CallbackQuery(data=InlineButtonsData.BOT_STATS, func=filter_admin_move))
async def bot_status(event: CallbackQuery.Event) -> None:
    
    try:
        
        with SessionLocal() as session:
            users_num = session.query(UserModel).count()
            channels_num = session.query(ChannelModel).count()
            
            await event.answer(bot_stats(users=users_num, channels=channels_num))
        
    finally:
        raise StopPropagation

# endregion


# region NewMessage Handlers

# NewMessage handler, show user stats
@client.on(event=NewMessage(incoming=True, pattern=TextButtonsString.MY_ACCOUNT, func=filter_user_move))
async def user_account_info(event: CallbackQuery.Event) -> None:
    
    try:
        
        with SessionLocal() as session:
            user = session.query(UserModel).filter_by(user_id=event.sender_id).first()
            await event.reply(my_account(user=user), buttons=TextButtons.START_MENU, parse_mode='html')
        
    finally:
        raise StopPropagation

# endregion
