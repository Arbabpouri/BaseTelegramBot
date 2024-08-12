from telethon.custom import Message
from telethon.events import CallbackQuery
from telethon.types import PeerChannel, PeerUser, Channel as ChannelInstance
from telethon.tl.types import InputMediaDice as Dice
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError, ChatAdminRequiredError, ChannelPrivateError
from uuid import uuid4
from abc import ABC, abstractmethod
from re import match
from typing import Iterable, Any
from asyncio import sleep
import logging

from config import Strings, BotConfig
from .buttons import InlineButtonsData, InlineButtons, TextButtons, TextButtonsString, UrlButtons
from ..database import User, Channel, Session, engine, Configs
from .app import client
from .step import Step, step_limit, Permission


logging.basicConfig(filename="log.txt", filemode="a",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_join(user_id: int, invited_by_user_id: int | None = None) -> bool:

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
                await client.send_message(PeerUser(BotConfig.CREATOR_USER_ID), message=Strings.channel_deleted(channel))
            except Exception as e:
                print(e)
        if not_joined:
            await client.send_message(PeerUser(user_id), Strings.JOIN_TO_CHANNELS, buttons=UrlButtons.channels_locked(not_joined, invited_by_user_id))
            return False
        return True



# function for add new users if not database
async def add_user(user_id: int, invited_by_user_id: int | None = None) -> None:
    
    with Session(engine) as session:

        is_joined = await check_join(user_id, invited_by_user_id)

        user = session.query(User).filter_by(user_id=int(user_id)).first()

        if not user:

            configs = session.query(Configs).first()
            user = User(user_id=int(user_id), balance=configs.entry_prize)
            
            if invited_by_user_id and str(invited_by_user_id).isnumeric():
                inviter_user = session.query(User).filter_by(user_id=int(invited_by_user_id)).first()
                if inviter_user:
                    user.invited_by = inviter_user.id
                    user.referral_active = False
                    if is_joined:
                        user.referral_active = True
                        inviter_user.balance += configs.referral_bonus
                        try:
                            await client.send_message(PeerUser(inviter_user.user_id), Strings.referral_bonus(user.user_id, configs.referral_bonus), parse_mode="html")
                        except Exception as e:
                            print(e)

            session.add(user)
            session.commit()
            return True
        
        elif user and user.referral_active == False and user.invited_by and is_joined:
            user.referral_active = True
            configs = session.query(Configs).first()
            inviter = session.query(User).filter_by(id=int(user.invited_by)).first()
            inviter.balance += configs.referral_bonus
            try:
                await client.send_message(PeerUser(inviter.user_id), Strings.referral_bonus(user.user_id, configs.referral_bonus), parse_mode="html")
            except Exception as e:
                print(e)
            session.commit()
            return True
        
        else:
            return is_joined
               

# del user from step
def del_step(user_id: int) -> bool:
    if int(user_id) in step_limit:
        del step_limit[int(user_id)]
        return True
    return False


# send message to users function
async def send_to_users(users_id: Iterable[int], message: Any) -> int:
    secsess = 0

    for user in users_id:
        try:
            
            await client.send_message(entity=PeerUser(user), message=message)
            secsess += 1
            await sleep(0.3)
        except FloodWaitError as e:
            await sleep(e.seconds + 2)
        
        except Exception as e:
            print(e)
        
    return secsess


class HandlerBase(ABC):

    @abstractmethod
    async def user(event) -> None:
        pass


    @abstractmethod
    async def admin(event) -> None:
        pass


class CallBackQueryHandlers(HandlerBase):

    @staticmethod
    async def user(event: CallbackQuery.Event) -> None:

        try:

            data = str(event.data.decode())
            invited_by_user_id = None

            if data.startswith(InlineButtonsData.JOINED_IN_CHANNEL):
                
                invited_by = data.replace(InlineButtonsData.JOINED_IN_CHANNEL, '')
                data = InlineButtonsData.JOINED_IN_CHANNEL
                if invited_by.isnumeric():
                    invited_by_user_id = int(invited_by)

            if not await add_user(event.sender_id, invited_by_user_id):
                return
        
            match (data):

                case InlineButtonsData.JOINED_IN_CHANNEL:
                    await event.delete()
                    await client.send_message(event.chat_id, Strings.START_MENU, buttons=TextButtons.START_MENU)

                # case data if (data.startswith(InlineButtonsData.DICE_PLAN)):
                #     dice_id, amount = data.replace(InlineButtonsData.DICE_PLAN, '').split('_')

                #     with Session(engine) as session:
                #         dice_plan = session.query(DicePlan).filter_by(id=int(dice_id)).first()
                #         if not dice_plan:
                #             return

                #         await event.edit(
                #             Strings.dice_info(dice_plan.title, dice_plan.coefficient , amount), 
                #             buttons=InlineButtons.acc_reject_dice(dice_id, amount)
                #         )

                # case InlineButtonsData.SEND_FACTOR:
                #     step = Permission(PART=Step.GET_PAY)
                #     step_limit[int(event.sender_id)] = step
                #     await event.edit(Strings.GET_PAY)

        except Exception as e:
            print(e)

    @staticmethod
    async def admin(event: CallbackQuery.Event) -> None:

        try:

            data = str(event.data.decode())

            match(data):

                case InlineButtonsData.BACK_TO_ADMIN:
                    await event.edit(Strings.BACKED, buttons=InlineButtons.ADMIN_PANEL)

                case InlineButtonsData.BOT_STATS:
                    with Session(engine) as session:
                        users = session.query(User).count()
                        channels = session.query(Channel).count()
                    
                    await event.answer(Strings.bot_stats(users, channels), alert=True)

                case InlineButtonsData.ADMIN_SETTING_PANEL:
                    await event.edit(Strings.SELECT, buttons=InlineButtons.ADMIN_SETTING)

                case InlineButtonsData.USER_SETTING_PANEL:
                    await event.edit(Strings.SELECT, buttons=InlineButtons.USER_SETTING)

                case InlineButtonsData.CHANNEL_PANEL:
                    with Session(engine) as session:
                        channels = session.query(Channel).all()
                    await event.edit(Strings.SELECT, buttons=InlineButtons.channels_panel(channels))

                case InlineButtonsData.SEND_PANEL:
                    await event.edit(Strings.SELECT, buttons=InlineButtons.SEND_PANEL)

                case InlineButtonsData.SEND_TO_USER:
                    step = Permission(PART=Step.SEND_TO_USER)
                    step_limit[int(event.sender_id)] = step
                    await event.reply(Strings.ENTER_USER_ID)

                case InlineButtonsData.SEND_TO_USERS:
                    step = Permission(PART=Step.SEND_TO_USERS)
                    step_limit[int(event.sender_id)] = step
                    await event.reply(Strings.ENTER_MESSAGE)

                case InlineButtonsData.CHANGE_CONFIGS:
                    await event.edit(Strings.SELECT, buttons=InlineButtons.CONFIGS_PANEL)

                case InlineButtonsData.ADD_ADMIN | InlineButtonsData.DELETE_ADMIN:
                    step = Permission(PART=Step.ADD_ADMIN if data == InlineButtonsData.ADD_ADMIN else Step.DELETE_ADMIN)
                    step_limit[int(event.sender_id)] = step
                    await event.edit(Strings.ENTER_USER_ID)

                case InlineButtonsData.SHOW_ADMINS:
                    with Session(engine) as session:
                        admins = session.query(User).filter_by(is_admin=True).all()
                    await event.edit(Strings.show_admins(admins), buttons=InlineButtons.ADMIN_SETTING, parse_mode='html')

                case InlineButtonsData.ADD_CHANNEL:
                    step = Permission(PART=Step.ADD_CHANNEL)
                    step_limit[int(event.sender_id)] = step
                    await event.edit(Strings.ADD_CHANNEL)

                case data if (str(data).startswith(InlineButtonsData.DELETE_CHANNEL)):
                    channel_id = str(data).replace(InlineButtonsData.DELETE_CHANNEL, '')
                    with Session(engine) as session:
                        channel = session.query(Channel).filter_by(channel_id=int(channel_id)).first()

                        if channel:
                            session.delete(channel)
                            session.commit()
                            channels = session.query(Channel).all()
                            await event.edit(Strings.DELETED, buttons=InlineButtons.channels_panel(channels))

                case InlineButtonsData.BAN_USER | InlineButtonsData.UNBAN_USER:
                    step = Permission(PART=Step.BAN_USER if data == InlineButtonsData.BAN_USER else Step.UNBAN_USER)
                    step_limit[int(event.sender_id)] = step
                    await event.edit(Strings.ENTER_USER_ID)

                case InlineButtonsData.SHOW_USER_INFO:
                    await event.answer(Strings.NEW_UPDATE)

                case InlineButtonsData.CHANGE_ENTERY_PRIZE:
                    step = Permission(PART=Step.CHANGE_ENTERY_PRIZE)
                    step_limit[int(event.sender_id)] = step
                    await event.edit(Strings.ENTER_VALUE)

                case InlineButtonsData.CHANGE_REFERRAL_BONUS:
                    step = Permission(PART=Step.CHANGE_REFERRAL_BONUS)
                    step_limit[int(event.sender_id)] = step
                    await event.edit(Strings.ENTER_VALUE)

                case InlineButtonsData.CHANGE_HELP_TEXT:
                    step = Permission(PART=Step.CHANGE_HELP_TEXT)
                    step_limit[int(event.sender_id)] = step
                    await event.edit(Strings.ENTER_TEXT)

                case InlineButtonsData.CHANGE_RULES_TEXT:
                    step = Permission(PART=Step.CHANGE_RULES_TEXT)
                    step_limit[int(event.sender_id)] = step
                    await event.edit(Strings.ENTER_TEXT)

                case InlineButtonsData.CHANGE_TRUST_CHANNEL:
                    step = Permission(PART=Step.CHANGE_TRUST_CHANNEL)
                    step_limit[int(event.sender_id)] = step
                    await event.edit(Strings.ENTER_URL)

                # case data if (data.startswith(InlineButtonsData.ACC_PAY)):
                #     user_id = data.replace(InlineButtonsData.ACC_PAY, '')

                #     try:
                #         await client.send_message(event.sender_id, Strings.GET_PAY_AMOUNT)
                #         await event.answer(Strings.CHECK_PV, alert=True)
                #         step = Permission(PART=Step.GET_PAY_AMOUNT, USER_ID=int(user_id), EVENT=event)
                #         step_limit[int(event.sender_id)] = step
                #     except Exception as e:
                #         print(e)
                #         await event.answer(Strings.PLEASE_START_BOT)

                # case data if (data.startswith(InlineButtonsData.REJECT_PAY)):
                #     withdraw_code = data.replace(InlineButtonsData.REJECT_PAY, '')

                #     with Session(engine) as session:

                #         withdraw_req = session.query(Withdraw).filter_by(withdraw_code=withdraw_code).first()

                #         if not withdraw_code:
                #             await event.delete()
                #             return

                #         await event.edit(Strings.REJECTED)
                #         try:
                #             await client.send_message(PeerUser(int(withdraw_req.user.user_id)), Strings.PAY_REJECTED)
                #             session.delete(withdraw_req)
                #             session.commit()
                #         except Exception as e:
                #             print(e)

                # case data if (data.startswith(InlineButtonsData.ACC_WITHDRAW)):
                #     withdraw_code = data.replace(InlineButtonsData.ACC_WITHDRAW, '')
                #     with Session(engine) as session:
                #         withdraw_req = session.query(Withdraw).filter_by(withdraw_code=withdraw_code).first()

                #         if not withdraw_code:
                #             await event.delete()
                #             return

                #         try:
                #             await client.send_message(event.sender_id, Strings.ENTER_TXID)
                #             await event.answer(Strings.CHECK_PV, alert=True)
                #             step = Permission(
                #                 PART=Step.GET_TXID_WITHDRAW, 
                #                 WITHDRAW_CODE=withdraw_req.withdraw_code,
                #                 EVENT=event
                #             )
                #             step_limit[int(event.sender_id)] = step
                #         except Exception as e:
                #             print(e)
                #             await event.answer(Strings.PLEASE_START_BOT)

                # case data if (data.startswith(InlineButtonsData.REJECT_WITHDRAW)):
                #     withdraw_code = data.replace(InlineButtonsData.REJECT_WITHDRAW, '')

                #     await event.edit(Strings.REJECTED)

                #     with Session(engine) as session:
                #         withdraw = session.query(Withdraw).filter_by(withdraw_code=withdraw_code).first()
                #         if withdraw and not withdraw.is_check:
                #             withdraw.user.balance += withdraw.amount
                #             withdraw.is_check = True

                #             try:
                #                 await client.send_message(PeerUser(int(withdraw.user.user_id)), Strings.PAY_REJECTED)
                #             except Exception as e:
                #                 print(e)
                    
                #             session.commit()
        
        except Exception as e:
            print(e)


class NewMessageHandlers(HandlerBase):

    @staticmethod
    async def user(event: Message) -> None:

        try:

            text = str(event.message.message)
            invited_by_user_id = None

            # this condition for get referraler user id
            # if text.startswith("/start "):
                
            #     invited_by = text.replace("/start ", '')
            #     text = "/start"
            #     if invited_by.isnumeric():
            #         invited_by_user_id = int(invited_by)

            if not await add_user(event.sender_id, invited_by_user_id):
                return
            
            match (text):

                case "/start":
                    del_step(event.sender_id)
                    await client.send_message(event.chat_id, Strings.START_MENU, buttons=TextButtons.START_MENU)

                case TextButtonsString.RULES:
                    with Session(engine) as session:
                        config = session.query(Configs).first()
                    await client.send_message(entity=event.chat_id, message=config.rules_text, buttons=TextButtons.START_MENU)

                case TextButtonsString.HELP:
                    with Session(engine) as session:
                        config = session.query(Configs).first()
                    await client.send_message(entity=event.chat_id, message=config.trust_text, buttons=UrlButtons.trust_channel(), parse_mode="html")

                case TextButtonsString.CONTACT_US:
                    await client.send_message(entity=event.chat_id, message=Strings.CONTACT_US, buttons=UrlButtons.CONTACT_US)

                case TextButtonsString.MY_ACCOUNT:
                    with Session(engine) as session:
                        user = session.query(User).filter_by(user_id=int(event.sender_id)).first()
                        await client.send_message(entity=event.chat_id, message=Strings.my_account(user), buttons=TextButtons.START_MENU, parse_mode='html')

                # case TextButtonsString.WITHDRAW:

                #     with Session(engine) as session:
                #         user = session.query(User).filter_by(user_id=int(event.sender_id)).first()
                #         if len(user.user_referrals) < 10:
                #             await event.reply(Strings.NEED_REFERRAL)
                #             return
                        
                #         step = Permission(PART=Step.GET_WITHDRAW_AMOUNT)
                #         step_limit[int(event.sender_id)] = step
                #         await event.reply(Strings.ENTER_AMOUNT)

                case TextButtonsString.DEPOSIT_PANEL:
                    await client.send_message(entity=event.chat_id, message=Strings.SELECT, buttons=TextButtons.DEPOSIT_PLAN)

                # case TextButtonsString.TRON:
                    
                #     await client.send_message(
                #         entity=event.chat_id, 
                #         message=Strings.send_crypto(BotConfig.WALLET), 
                #         parse_mode="html", 
                #         buttons=InlineButtons.SEND_FACTOR
                #     )

                case TextButtonsString.REFERRAL:
                    with Session(engine) as session:

                        user = session.query(User).filter_by(user_id=int(event.sender_id)).first()
                        configs = session.query(Configs).first()

                        message = await client.send_file(entity=event.chat_id, file=BotConfig.REFERRAL_IMAGE_ADDRESS, caption=Strings.referral_banner(event.sender_id, configs))
                        await client.send_message(entity=event.chat_id, message=Strings.referral_reply(user, configs), buttons=TextButtons.DEPOSIT_PLAN, reply_to=message)

                case TextButtonsString.BACK_TO_START:
                    await client.send_message(entity=event.chat_id, message=Strings.BACKED, buttons=TextButtons.START_MENU)

        
        except Exception as e:
            print(e)

    @staticmethod
    async def admin(event: Message) -> None:

        try:
        
            match (str(event.message.message)):
                case "/admin" | "/panel":
                    await client.send_message(entity=event.chat_id, message=Strings.ADMIN_PANEL, buttons=InlineButtons.ADMIN_PANEL)

        except Exception as e:
            print(e)


    @staticmethod
    async def cancel(event: Message) -> None:

        try:
            if str(event.message.message) == "/cancel" and del_step(event.sender_id):    
                await event.reply(Strings.CANCELED, buttons=TextButtons.START_MENU)
        except Exception as e:
            print(e)


class NewMessageGetInformationsHandlers(HandlerBase):

    @staticmethod
    async def user(event: Message) -> None:

        try:
        
            info = step_limit.get(int(event.sender_id))

            if not info:
                return
            
            # this switch for get information
            
            # match (info.PART):

                # case Step.GET_PAY:
                #     try:

                #         send = await client.send_message(PeerChannel(BotConfig.PAYMNET_CHANNEL), event.message)
                #         await client.send_message(
                #             PeerChannel(BotConfig.PAYMNET_CHANNEL), 
                #             Strings.deposit_request(event.sender_id), 
                #             buttons=InlineButtons.acc_reject_pay(event.sender_id),
                #             reply_to=send
                #         )
                #         message = Strings.PAY_GETED
                #     except Exception as e:
                #         print(e)
                #         message = Strings.PAY_NOT_GETED

                #     await client.send_message(event.chat_id, message, buttons=TextButtons.START_MENU)
                #     del_step(event.sender_id)

                # case Step.GET_WITHDRAW_AMOUNT:
                #     amount = str(event.message.message)

                #     if not amount.isnumeric():
                #         await event.reply(Strings.ENTER_NUMBER)
                #         return

                #     with Session(engine) as session:
                #         user = session.query(User).filter_by(user_id=int(event.sender_id)).first()
                    
                #         if int(amount) > user.balance:
                #             await event.reply(Strings.BAD_AMOUNT)
                #             return
                
                #     step = Permission(PART=Step.GET_WALLET, AMOUNT=int(amount))
                #     step_limit[int(event.sender_id)] = step

                #     await event.reply(Strings.ENTER_WALLET)

                # case Step.GET_WALLET:

                #     wallet = str(event.message.message)

                #     if not wallet:
                #         await event.reply(Strings.ENTER_WALLET)
                #         return
                    
                #     try:
                    
                #         with Session(engine) as session:
                #             user = session.query(User).filter_by(user_id=int(event.sender_id)).first()
                #             code = str(uuid4())
                #             obj = Withdraw(user_id=user.id, amount=int(info.AMOUNT), wallet=wallet, withdraw_code=code)
                    
                #             await client.send_message(
                #                 entity=PeerChannel(BotConfig.WITHDRAW_CHANNEL), 
                #                 message=Strings.withdraw_request(user_id=event.sender_id, amount=info.AMOUNT, wallet=wallet),
                #                 buttons=InlineButtons.acc_reject_withdraw(code),
                #                 parse_mode="html"
                #             )
                #             message = Strings.REQUEST_GETED
                #             user.balance -= int(info.AMOUNT)
                #             session.add(obj)
                #             session.commit()
                #     except Exception as e:
                #         print(e)
                #         message = Strings.REQUEST_NOT_GETED

                #     del_step(event.sender_id)
                #     await event.reply(message, buttons=TextButtons.START_MENU)

                
        except Exception as e:
            print(e)


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
                        
                # case Step.GET_PAY_AMOUNT:

                #     amonut = str(event.message.message)

                #     if not amonut.isnumeric():
                #         await event.reply(Strings.ENTER_NUMBER)
                #         return

                #     with Session(engine) as session:
                #         user = session.query(User).filter_by(user_id=int(info.USER_ID)).first()

                #         if not user:
                #             await event.reply(Strings.USER_NOT_EXIST)
                #             await info.EVENT.delete()
                #             del_step(event.sender_id)
                #             return

                #         user.balance += int(amonut)
                #         session.commit()

                #     try:
                #         await client.send_message(entity=PeerUser(info.USER_ID), message=Strings.PAY_ACCEPTED)
                #         await event.reply(Strings.ACCPTED)
                #         await info.EVENT.edit(Strings.ACCPTED)
                #     except Exception as e:
                #         print(e)

                #     del_step(event.sender_id)

                # case Step.GET_TXID_WITHDRAW:
                    
                #     if not event.message.message:
                #         await event.reply(Strings.ENTER_TXID)
                #         return
                    
                #     try:

                #         with Session(engine) as session:
                #             withdraw = session.query(Withdraw).filter_by(withdraw_code=info.WITHDRAW_CODE).first()

                #             if not withdraw:
                #                 await event.reply(Strings.ERROR)
                #                 await info.EVENT.delete()
                #                 return
                                
                #             await client.send_message(
                #                 entity=PeerChannel(BotConfig.WITHDRAW_CHANNEL_LOG),
                #                 message=Strings.withdraw_request(withdraw.user.user_id, withdraw.amount, withdraw.wallet, event.message.message),
                #                 parse_mode="html"
                #             )
                #             await info.EVENT.edit(Strings.ACCPTED)
                #             await event.reply(Strings.UPDATED)
                #             withdraw.is_check = True
                #             session.commit()

                #     except Exception as e:
                #         await event.reply(Strings.BOT_NOT_ADMIN)
                #         print(e)

                #     del_step(event.sender_id)
        
        except Exception as e:
            print(e)
