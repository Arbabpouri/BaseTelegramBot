# region imports

from telethon.events import CallbackQuery, StopPropagation
from functions.step_functions import delete_step
from buttons.inline_buttons import InlineButtons, InlineButtonsData
from buttons.text_buttons import TextButtons
from settings.strings import CANCELED, ERROR
from . import client

# endregion


# region CallBackQuery Handlers

# CallbackQuery handler, cancel and delete step
@client.on(event=CallbackQuery(data=InlineButtonsData.CANCEL_USER))
async def cancel_user_inline(event: CallbackQuery.Event) -> None:
    
    try:

        await event.reply(CANCELED, buttons=TextButtons.START_MENU)
    
    except:
        await event.reply(ERROR, buttons=TextButtons.START_MENU)
    
    finally:
        delete_step(event.sender_id)
        raise StopPropagation
    
    
# CallbackQuery handler, cancel and delete step
@client.on(event=CallbackQuery(data=InlineButtonsData.CANCEL_ADMIN))
async def cancel_admin_inline(event: CallbackQuery.Event) -> None:
    
    try:
        await event.edit(CANCELED, buttons=InlineButtons.ADMIN_PANEL)
    
    except:
        await event.edit(ERROR, buttons=InlineButtons.ADMIN_PANEL)
    
    finally:
        delete_step(event.sender_id)
        raise StopPropagation


# endregion
