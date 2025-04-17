from telethon.custom import Message
from telethon.events import CallbackQuery
from telethon.types import PeerChannel, PeerUser, Channel as ChannelInstance
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError, ChatAdminRequiredError, ChannelPrivateError
from uuid import uuid4
from abc import ABC, abstractmethod
from re import match
from typing import Iterable, Any, Optional
from asyncio import sleep

from settings import Strings, BotConfig
from ..buttons.buttons import InlineButtonsData, InlineButtons, TextButtons, TextButtonsString, UrlButtons
from ..models import User, Channel, Session, engine, Configs
from .app import client
from .step import Step, step_limit, Permission


async def check_join(user_id: int, send_message: Optional[bool] = False, invited_by_user: int | None = None) -> bool:
    "return : yek list az button ha baraya channel haye delete shode ast"

    with Session(engine) as session:
        channels = session.query(Channel).all()

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
                await client.send_message((BotConfig.CREATOR_USER_ID), message=Strings.channel_deleted(channel))
            except Exception as e:
                print(e)
        
        if not not_joined:
            return True

        try:
            if send_message and not_joined:
                await client.send_message(PeerUser(user_id), Strings.JOIN_TO_CHANNELS, buttons=UrlButtons.channels_locked(not_joined, invited_user_id=invited_by_user))
        except Exception as e:
            print("error in send message for join channel : ". e)
        finally:
            return False


class NewMessageGetInformationsHandlers:

    @staticmethod
    async def admin(event: Message) -> None:

        try:
        
            info = step_limit.get(int(event.sender_id))
            if not info:
                return
            
            match(info.PART):

                case Step.ADD_ADMIN | Step.DELETE_ADMIN:
                    user_id = str(event.message.message)

                    if user_id == str(event.sender_id):
                        await event.reply(Strings.NO_YOU)

                    elif user_id == str(BotConfig.CREATOR_USER_ID):
                        await event.reply(Strings.IS_CREATOR)

                    elif user_id.isnumeric():

                        with Session(engine) as session:
                            user = session.query(User).filter_by(user_id=int(user_id)).first()

                            if user:

                                if user.is_admin:

                                    if info.PART == Step.ADD_ADMIN:
                                        await event.reply(Strings.USER_EXIST)
                                    else:
                                        user.is_admin = False
                                        session.commit()
                                        await event.reply(Strings.DELETED, buttons=InlineButtons.ADMIN_SETTING)
                                        del_step(event.sender_id)
                                else:

                                    if info.PART == Step.ADD_ADMIN:
                                        user.is_admin = True
                                        session.commit()
                                        await event.reply(Strings.ADDED, buttons=InlineButtons.ADMIN_SETTING)
                                        del_step(event.sender_id)
                                    else:
                                        await event.reply(Strings.USER_NOT_EXIST)

                            else:
                                await event.reply(Strings.USER_NOT_EXIST)
                    else:

                        await event.reply(Strings.ENTER_NUMBER)

                case Step.ADD_CHANNEL:
                    if event.forward and (isinstance((channel := await event.forward.get_chat()), ChannelInstance)):
                        try:
                            if channel.admin_rights:
                                with Session(engine) as session:
                                    get_channel = session.query(Channel).filter_by(channel_id=channel.id).first()
                                    
                                    try:

                                        if not get_channel:
                                            channel_info = await client(GetFullChannelRequest(PeerChannel(int(channel.id))))
                                            add_channel = Channel(channel_id=int(channel.id), channel_name=channel.title, channel_url=channel_info.full_chat.exported_invite.link)
                                            session.add(add_channel)
                                            session.commit()
                                            del_step(event.sender_id)
                                            await event.reply(Strings.ADDED, buttons=InlineButtons.ADMIN_PANEL)
                                    
                                        else:
                                            await event.reply(Strings.CHANNEL_ALREADY_EXIST)

                                    except Exception as e:
                                        print(e)
                                        await event.reply(Strings.BOT_NOT_ADMIN)

                            else:
                                await event.reply(Strings.BOT_NOT_ADMIN)

                        except Exception as e:
                            print(e)
                            await event.reply(Strings.ERROR, buttons=InlineButtons.ADMIN_PANEL)
                            del_step(event.sender_id)
                    
                    else:
                        await event.reply(Strings.ADD_CHANNEL)

                case Step.BAN_USER | Step.UNBAN_USER:
                    user_id = str(event.message.message)
                    if user_id.isnumeric():
                        
                        with Session(engine) as session:
                            user = session.query(User).filter_by(user_id=int(user_id)).first()

                            if user:
                                
                                user.is_ban = True if info.PART == Step.BAN_USER else False
                                session.commit()
                                del_step(event.sender_id)
                                await event.reply(Strings.UPDATED, buttons=InlineButtons.USER_SETTING)

                            else:
                                await event.reply(Strings.USER_NOT_EXIST)

                    else:
                        await event.reply(Strings.ENTER_NUMBER)

                case Step.SEND_TO_USER:
                    user_id = str(event.message.message)

                    if user_id.isnumeric():
                        with Session(engine) as session:
                            user = session.query(User).filter_by(user_id=int(user_id)).first()
                        if user:
                            step = Permission(PART=Step.GET_MESSAGE, USER_ID=int(user_id))
                            step_limit[int(event.sender_id)] = step
                            await event.reply(Strings.ENTER_MESSAGE)
                        else:
                            await event.reply(Strings.USER_NOT_EXIST)

                    else:
                        await event.reply(Strings.ENTER_NUMBER)

                case Step.SEND_TO_USERS | Step.GET_MESSAGE:
                    
                    
                    if info.PART == Step.SEND_TO_USERS:
                        with Session(engine) as session:
                            users = session.query(User).all()
                            users = [user.user_id for user in users]

                    else:
                        users = (info.USER_ID, )
                    
                    del_step(event.sender_id)
                    await event.reply(Strings.SENDING, buttons=InlineButtons.SEND_PANEL)
                    sucsess = await send_to_users(users_id=users, message=event.message)
                    await event.reply(Strings.message_sended(success_num=sucsess))

                case Step.SHOW_USER_INFO:
                    await event.reply(Strings.NEW_UPDATE, buttons=InlineButtons.USER_SETTING)
                    del_step(event.sender_id)

                case Step.CHANGE_ENTERY_PRIZE | Step.CHANGE_REFERRAL_BONUS:
                    value = str(event.message.message)

                    if value.isnumeric():
                        
                        with Session(engine) as session:
                            configs = session.query(Configs).first()
                        
                            if info.PART == Step.CHANGE_ENTERY_PRIZE:
                                configs.entry_prize = int(value)
                            else:
                                configs.referral_bonus = int(value)
                            
                            session.commit()
                            del_step(event.sender_id)
                            
                            await event.reply(Strings.UPDATED, buttons=InlineButtons.CONFIGS_PANEL)

                    else:
                        await event.reply(Strings.ENTER_NUMBER)

                case Step.CHANGE_HELP_TEXT | Step.CHANGE_RULES_TEXT:
                    
                    text = str(event.message.message)

                    if len(text) <= BotConfig.TEXT_LONG:
                        
                        with Session(engine) as session:
                            
                            configs = session.query(Configs).first()

                            if info.PART == Step.CHANGE_HELP_TEXT:
                                configs.trust_text = text
                            else:
                                configs.rules_text = text
                            
                            session.commit()
                            del_step(event.sender_id)
                            await event.reply(Strings.UPDATED, buttons=InlineButtons.CONFIGS_PANEL)

                    else:

                        await event.reply(Strings.TEXT_IS_LONG)

                case Step.CHANGE_TRUST_CHANNEL:
                    text = str(event.message.message)
                    if match(r'^(?:https://telegram\.me/|https://t\.me/|t\.me/|telegram\.me/|@)[A-Za-z0-9_+]+', text):
                        with Session(engine) as session:
                            
                            configs = session.query(Configs).first()
                            if text.startswith("@"):
                                text = text.replace("@", "t.me/")
                            configs.trust_channel_url = text
                            session.commit()
                        
                        del_step(event.sender_id)
                        await event.reply(Strings.UPDATED, buttons=InlineButtons.CONFIGS_PANEL)
                    
                    else:
                        await event.reply(Strings.ENTER_URL)
                        
        
        except Exception as e:
            print(e)
