# region imports


from telethon.tl.functions.channels import GetParticipantRequest
from telethon.types import PeerUser, PeerChannel
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError, ChannelPrivateError
from settings.database import SessionLocal
from typing import Optional
from models import ChannelModel
from settings.client import client
from settings.config import CREATOR_USER_ID
from settings.strings import channel_deleted, JOIN_TO_CHANNELS
from buttons.url_buttons import UrlButtons
# endregion

async def check_join(user_id: int, send_message: Optional[bool] = False, invited_by_user: int | None = None) -> bool:
    "return : yek list az button ha baraya channel haye delete shode ast"

    with SessionLocal() as session:
        channels = session.query(ChannelModel).all()

        if not channels:
            return True

        not_joined = []
        not_admin = []

        for channel in channels:

            try:

                await client(GetParticipantRequest(PeerChannel(channel.channel_id), PeerUser(int(user_id))))

            except UserNotParticipantError:
                not_joined.append(channel)
            
            except (ChatAdminRequiredError, ChannelPrivateError):
                not_admin.append(channel)
                session.delete(channel)

            except Exception as e:
                print(e)
                return True
        
        session.commit()

        for channel in not_admin:
            try:
                await client.send_message((CREATOR_USER_ID), message=channel_deleted(channel))
            except Exception as e:
                print(e)
        
        if not not_joined:
            return True

        try:
            if send_message and not_joined:
                await client.send_message(PeerUser(user_id), JOIN_TO_CHANNELS, buttons=UrlButtons.channels_locked(not_joined, invited_user_id=invited_by_user))
        except Exception as e:
            print("error in send message for join channel : ". e)
        finally:
            return False

