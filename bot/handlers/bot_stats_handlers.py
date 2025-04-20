# region imports

from telethon.events import CallbackQuery, NewMessage, StopPropagation
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from buttons.text_buttons import TextButtons, TextButtonsString
from settings.strings import bot_stats, my_account
from functions.database_functions import get_users, get_channels, get_user
from functions.filters_functions import filter_user_move, filter_admin_move
from settings.client import client

# endregion


# region CallbackQuery Handlers

# CallbackQuery handler, show bot stats
@client.on(event=CallbackQuery(data=InlineButtonsData.BOT_STATS, func=filter_admin_move))
async def bot_status(event: CallbackQuery.Event) -> None:
    
    try:
        users_num = len(await get_users())
        channels_num = len(await get_channels())
        await event.edit(bot_stats(users=users_num, channels=channels_num), buttons=InlineButtons.back_to(BackToEnum.ADMIN_SETTING))
        
    finally:
        raise StopPropagation

# endregion


# region NewMessage Handlers

# NewMessage handler, show user stats
@client.on(event=NewMessage(pattern=TextButtonsString.MY_ACCOUNT, func=filter_user_move))
async def user_account_info(event: CallbackQuery.Event) -> None:
    
    try:
        
        user = await get_user(event.sender_id)
        await event.reply(my_account(user=user), buttons=TextButtons.START_MENU)
        
    finally:
        raise StopPropagation

# endregion
