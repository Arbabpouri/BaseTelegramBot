# region imports

from telethon.events import NewMessage, CallbackQuery, StopPropagation
from telethon.custom import Message
from functions.step_functions import Parts, set_step, delete_step
from functions.filters_functions import (
    filter_admin_move,
    filter_set_entry_prize,
    filter_set_help,
    filter_set_rule,
    filter_set_start_menu,
    filter_set_message_to_support,
    filter_set_support_channel,
    filter_set_referral_bonus,
    filter_set_card_info,
)
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from settings.strings import (
    START_MENU,
    RULES,
    HELP,
    MESSAGE_TO_SUPPORT_TEXT,
    SELECT,
    ENTER_NUMBER,
    ENTER_TEXT,
    ENTER_URL,
    UPDATED,
    ERROR
)
from settings.client import client
from settings.database import SessionLocal, ConfigsModel
from settings.config import ENTRY_PRIZE, REFERRAL_BONUS, SUPPORT_CHANNEL_URL, CARD_INFO

# endregion


# region CallBackQuery Handlers

# CallbackQuery handler, show bots configs settings
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_CONFIGS, func=filter_admin_move))
async def config_settings_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        raise StopPropagation


# CallbackQuery handler, show bots configs text
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_TEXTS_SETTINGS, func=filter_admin_move))
async def config_text_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.CHANGE_TEXTS_SETTINGS)
        
    finally:
        raise StopPropagation


# CallbackQuery handler, show bots configs referral
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_REFERRAL_SETTINGS, func=filter_admin_move))
async def config_referral_panel(event: CallbackQuery.Event) -> None:
    
    try:
    
        await event.edit(SELECT, buttons=InlineButtons.CHANGE_REFERRAL_SETTINGS)
        
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for change entry prize
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_ENTERY_PRIZE, func=filter_admin_move))
async def change_entry_prize_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_ENTERY_PRIZE)
        await event.edit(ENTER_NUMBER, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    

# CallbackQuery handler, set step change referral bonus set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_REFERRAL_BONUS, func=filter_admin_move))
async def change_referral_bonus(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_REFERRAL_BONUS)
        await event.edit(ENTER_NUMBER, buttons=InlineButtons.CANCEL_ADMIN)
        
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for change rule set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_RULES_TEXT, func=filter_admin_move))
async def change_rule_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_RULES_TEXT)
        await event.edit(ENTER_TEXT, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    

# CallbackQuery handler, set step for change helps set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_HELP_TEXT, func=filter_admin_move))
async def change_help_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_HELP_TEXT)
        await event.edit(ENTER_TEXT, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation
    
    
# CallbackQuery handler, set step for change support channel set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_SUPPORT_CHANNEL, func=filter_admin_move))
async def change_support_channel_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_SUPPORT_CHANNEL)
        await event.edit(ENTER_URL, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for change start menu text set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_START_MENU_TEXT, func=filter_admin_move))
async def change_start_menu_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_START_MENU)
        await event.edit(ENTER_TEXT, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for change message to support text set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_MESSAGE_TO_SUPPORT_TEXT, func=filter_admin_move))
async def change_message_to_support_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_MESSAGE_TO_SUPPORT)
        await event.edit(ENTER_TEXT, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation


# CallbackQuery handler, set step for change card info text set step
@client.on(event=CallbackQuery(data=InlineButtonsData.CHANGE_CARD_INFO, func=filter_admin_move))
async def change_card_info_set_step(event: CallbackQuery.Event) -> None:
    
    try:
    
        set_step(user_id=event.sender_id, step=Parts.CHANGE_CARD_INFO)
        await event.edit(ENTER_TEXT, buttons=InlineButtons.CANCEL_ADMIN)
    
    finally:
        raise StopPropagation



# endregion


# region NewMessageHandlers

# NewMessage handler, change rule
@client.on(event=NewMessage(incoming=True, pattern=".*", func=filter_set_rule))
async def set_rule(event: Message) -> None:
    
    try:
        global RULES
        text = str(event.message.message)
        with SessionLocal() as session:
            config = session.query(ConfigsModel).first()
            config.rules_text = text
            RULES = text
            session.commit()
            
        await event.reply(UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
        
    except:
        await event.reply(ERROR, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        
        delete_step(user_id=event.sender_id)
        raise StopPropagation
    
    
# NewMessage handler, change help
@client.on(event=NewMessage(incoming=True, pattern=".*", func=filter_set_help))
async def set_help(event: Message) -> None:
    
    try:
        global HELP
        text = str(event.message.message)
        with SessionLocal() as session:
            config = session.query(ConfigsModel).first()
            config.help_text = text
            HELP = text
            session.commit()
            
        await event.reply(UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
        
    except:
        await event.reply(ERROR, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        
        delete_step(user_id=event.sender_id)
        raise StopPropagation
    

# NewMessage handler, change start menu text
@client.on(event=NewMessage(incoming=True, pattern=".*", func=filter_set_start_menu))
async def set_start_menu(event: Message) -> None:
    
    try:
        global START_MENU
        text = str(event.message.message)
        with SessionLocal() as session:
            config = session.query(ConfigsModel).first()
            config.start_menu_text = text
            START_MENU = text
            session.commit()
            
        await event.reply(UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
        
    except:
        await event.reply(ERROR, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        
        delete_step(user_id=event.sender_id)
        raise StopPropagation
   

# NewMessage handler, change message to support text
@client.on(event=NewMessage(incoming=True, pattern=".*", func=filter_set_message_to_support))
async def set_message_to_support(event: Message) -> None:
    
    try:
        global MESSAGE_TO_SUPPORT_TEXT
        text = str(event.message.message)
        with SessionLocal() as session:
            config = session.query(ConfigsModel).first()
            config.message_to_support_text = text
            MESSAGE_TO_SUPPORT_TEXT = text
            session.commit()
            
        await event.reply(UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
        
    except:
        await event.reply(ERROR, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        
        delete_step(user_id=event.sender_id)
        raise StopPropagation


# NewMessage handler, change card info text
@client.on(event=NewMessage(incoming=True, pattern=".*", func=filter_set_card_info))
async def set_card_info(event: Message) -> None:
    
    try:
        global CARD_INFO
        text = str(event.message.message)
        with SessionLocal() as session:
            config = session.query(ConfigsModel).first()
            config.card_info = text
            CARD_INFO = text
            session.commit()
            
        await event.reply(UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
        
    except:
        await event.reply(ERROR, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        
        delete_step(user_id=event.sender_id)
        raise StopPropagation


# NewMessage handler, change support channel
@client.on(event=NewMessage(incoming=True, pattern=r"^(?:https://telegram\.me/|https://t\.me/|t\.me/|telegram\.me/|@)[A-Za-z0-9_+]+", func=filter_set_support_channel))
async def set_support_channel(event: Message) -> None:
    
    try:
        global SUPPORT_CHANNEL_URL
        text = str(event.message.message)
        with SessionLocal() as session:
            config = session.query(ConfigsModel).first()
            config.support_channel_url = text
            SUPPORT_CHANNEL_URL = text
            session.commit()
        await event.reply(UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
        
    except:
        await event.reply(ERROR, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        
        delete_step(user_id=event.sender_id)
        raise StopPropagation
    
    
# NewMessage handler, change referral bonus
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*$", func=filter_set_referral_bonus))
async def set_referral_bonus(event: Message) -> None:
    
    try:
        global REFERRAL_BONUS
        num = int(event.message.message)
        with SessionLocal() as session:
            config = session.query(ConfigsModel).first()
            config.referral_bonus = num
            REFERRAL_BONUS = num
            session.commit()
            
        await event.reply(UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
        
    except:
        await event.reply(ERROR, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        
        delete_step(user_id=event.sender_id)
        raise StopPropagation
    
    
# NewMessage handler, change entry prize
@client.on(event=NewMessage(incoming=True, pattern=r"^[0-9]*$", func=filter_set_entry_prize))
async def set_entry_prize(event: Message) -> None:
    
    try:
        global ENTRY_PRIZE
        num = int(event.message.message)
        with SessionLocal() as session:
            config = session.query(ConfigsModel).first()
            config.entry_prize = num
            ENTRY_PRIZE = num
            session.commit()
            
        await event.reply(UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
    
    except:
        await event.reply(ERROR, buttons=InlineButtons.CONFIGS_PANEL)
        
    finally:
        
        delete_step(user_id=event.sender_id)
        raise StopPropagation

# endregion
