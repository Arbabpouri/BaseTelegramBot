from telethon import Button
from typing import Iterable, Tuple, List
from buttons.inline_buttons import InlineButtons
from models.channel_model import ChannelModel
from settings.config import SUPPORT_USERNAME

class UrlButtonString:
    CONTACT_US = "✍🏻| پیام به ادمین |✍🏻"
    TRUST_CHANNEL = "💰|کانال واریزی ها|💰"


class UrlButtons:
    
    
    CONTACT_US = (
        (
            Button.url(text=UrlButtonString.CONTACT_US, url=f"t.me/{SUPPORT_USERNAME}"),
        ),
    )

    @staticmethod
    def trust_channel() -> Tuple[Tuple[Button]]:
        with Session(engine) as session:
            info = session.query(Configs).first()
        
        return (
            (
                Button.url(text=UrlButtonString.TRUST_CHANNEL, url=info.trust_channel_url)
            ),
        )
    

    @staticmethod
    def channels_locked(channels: Iterable[ChannelModel], invited_user_id: int | None = None) -> List[Tuple[Button]]:
        
        buttons = []

        for channel in channels:
            
            try:
                buttons.append((Button.url(text=channel.channel_name, url=channel.channel_url),))
            except Exception as e:
                print(e)

        buttons.append((InlineButtons.check_joined(invited_user_id),))

        return buttons
