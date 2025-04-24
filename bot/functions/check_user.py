# region imports


from telethon.tl.functions.channels import GetParticipantRequest
from telethon.types import PeerUser, PeerChannel
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError, ChannelPrivateError
from settings.database import SessionLocal
from typing import Optional
from models import ChannelModel, UserModel, ConfigsModel
from settings.client import client
from settings.config import CREATOR_USER_ID
from settings.strings import channel_deleted, JOIN_TO_CHANNELS, referral_bonus
from buttons.url_buttons import UrlButtons
# endregion

async def check_join(user_id: int, send_message: Optional[bool] = False, invited_by_user: int | None = None) -> bool:

    with SessionLocal() as session:
        channels = session.query(ChannelModel).all()

        if not channels:
            return True

        not_joined = []

        for channel in channels:

            try:

                await client(GetParticipantRequest(PeerChannel(channel.channel_id), PeerUser(int(user_id))))

            except UserNotParticipantError:
                not_joined.append(channel)
            
            except (ChatAdminRequiredError, ChannelPrivateError):
                try:
                    await client.send_message((CREATOR_USER_ID), message=channel_deleted(channel))
                except Exception as e:
                    print(e)
                    
                session.delete(channel)

            except Exception as e:
                print(e)
                return True
        
        session.commit()

        
        if not not_joined:
            return True

        try:
            if send_message and not_joined:
                await client.send_message(PeerUser(user_id), JOIN_TO_CHANNELS, buttons=UrlButtons.channels_locked(not_joined, invited_user_id=invited_by_user))
        except Exception as e:
            print("error in send message for join channel : ". e)
        finally:
            return False

async def check_user(user_id: int, invited_by_user_id: int | None = None) -> bool:
    is_joined = await check_join(user_id=user_id, send_message=True)
    with SessionLocal() as session:

        user = session.query(UserModel).filter_by(user_id=int(user_id)).first()
        
        if invited_by_user_id or (user and user.invited_by):
            invited_by_user_id: UserModel = session.query(UserModel).filter_by(user_id=int(invited_by_user_id or user.invited_by)).first()
            
        if not user:
            user = UserModel(
                user_id=int(user_id), 
                invited_by=invited_by_user_id.user_id if invited_by_user_id else None, 
                referral_active=False if invited_by_user_id != None else None, 
            )
            session.add(user)
            session.commit()
        
        if not is_joined:
            return False
        
        if is_joined and invited_by_user_id and not user.referral_active:
            config = session.query(ConfigsModel).first()
            user.referral_active = True
            invited_by_user_id.balance += config.referral_bonus
        
            try:
                await client.send_message(PeerUser(invited_by_user_id.user_id), referral_bonus(user_id, config.referral_bonus))
            except: pass
            session.commit()
            
        return True
