from telethon.events import NewMessage, CallbackQuery
from telethon.custom import Message
from functions.database_functions import get_config, update_configs
from functions.step_functions import Parts, set_step, delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData, BackToEnum
from settings.strings import SELECT, ENTER_NUMBER, ENTER_TEXT, ENTER_URL
from . import client


# CallbackQuery handler, show bots configs settings
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_CONFIGS))
async def config_settings_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.back_to(BackToEnum.ADMIN_SETTING))
        
    finally:
        pass


# CallbackQuery handler, set step for change entry prize
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_ENTERY_PRIZE))
async def change_entry_prize_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_ENTERY_PRIZE)
        await event.edit(ENTER_NUMBER, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
    

# CallbackQuery handler, set step change referral bonus set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_REFERRAL_BONUS))
async def remove_config_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_REFERRAL_BONUS)
        await event.edit(ENTER_NUMBER, buttons=InlineButtons.CANCEL)
        
    finally:
        pass


# CallbackQuery handler, set step for change rule set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_RULES_TEXT))
async def change_rule_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_RULES_TEXT)
        await event.edit(ENTER_TEXT, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
    

# CallbackQuery handler, set step for change helps set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_HELP_TEXT))
async def change_rule_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_HELP_TEXT)
        await event.edit(ENTER_TEXT, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
    
    
# CallbackQuery handler, set step for change support channel set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_SUPPORT_CHANNEL))
async def change_rule_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_SUPPORT_CHANNEL)
        await event.edit(ENTER_URL, buttons=InlineButtons.CANCEL)
    
    finally:
        pass
    

