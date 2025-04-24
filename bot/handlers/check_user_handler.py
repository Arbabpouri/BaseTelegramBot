from telethon.events import NewMessage, CallbackQuery, StopPropagation
from telethon.custom import Message
from buttons.inline_buttons import InlineButtonsData
from buttons.text_buttons import TextButtons
from buttons.commands import Commands
from settings.strings import START_MENU
from settings.client import client
from functions.check_user import check_user


# CallbackQuery handler, show send message panel
@client.on(event=CallbackQuery())
async def check_user_inline(event: CallbackQuery.Event) -> None:
    
    try:

        invited_by = None
        data = str(event.data.decode())

        if data.startswith(str(InlineButtonsData.JOINED_IN_CHANNEL.decode())):
            
            await event.delete()
            invited_by = data.split("_")[-1]
            invited_by = int(invited_by) if invited_by.isnumeric() else None
        
        if not await check_user(event.sender_id, invited_by):
            raise StopPropagation
        
        if data.startswith(str(InlineButtonsData.JOINED_IN_CHANNEL.decode())):
            await event.respond(START_MENU, buttons=TextButtons.START_MENU)
            raise StopPropagation()
    
    except Exception as e:
        print(e)
            

# NewMessage handler, show send message panel
@client.on(event=NewMessage(pattern=r".*", incoming=True))
async def check_user_text(event: Message) -> None:
    
    try:
    

        invited_by = None
        text = str(event.message.message)
        if text.startswith(f"{Commands.START} "):
            
            await event.delete()
            invited_by = text.split(" ")[-1]
            invited_by = int(invited_by) if invited_by else None
    
        if not await check_user(event.sender_id, invited_by):
            raise StopPropagation
        
        if text.startswith(Commands.START):
            await event.respond(START_MENU, buttons=TextButtons.START_MENU)
            raise StopPropagation()
            
    finally:
        pass
