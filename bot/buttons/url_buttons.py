from telethon import Button
from buttons.inline_buttons import InlineButtons
from functions.database_functions import get_config, get_channels
from settings.config import SUPPORT_USERNAME



class UrlButtonString:
    CONTACT_US = "✍🏻| پیام به ادمین |✍🏻"
    SUPPORT_CHANNEL = "💢| کانال پشتیبانی |💢"


class UrlButtons:
    
    
    CONTACT_US = (
        (
            Button.url(text=UrlButtonString.CONTACT_US, url=f"t.me/{SUPPORT_USERNAME}"),
        ),
    )

    @staticmethod
    async def support_channel(support_channel_url: str):
                
        return (
            (
                Button.url(text=UrlButtonString.SUPPORT_CHANNEL, url=support_channel_url),
            ),
        )
    

    @staticmethod
    async def channels_locked(invited_user_id: int | None = None):
        
        channels = await get_channels()
        
        buttons = []

        for channel in channels:
            
            buttons.append(
                (
                    Button.url(text=channel.channel_name, url=channel.channel_url),
                )
            )

        buttons.append(
            (
                InlineButtons.check_joined(invited_user_id),
            )
        )

        return buttons
