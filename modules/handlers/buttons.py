from telethon import Button
from typing import List, Tuple, Iterable
from config import BotConfig
from ..database import Session, Configs, engine, Channel

# region TextButton

class TextButtonsString:
    MY_ACCOUNT = "🔐| حساب من |🔐"
    # WITHDRAW = "💸| برداشت |💸"
    DEPOSIT_PANEL = "💳|افزایش موجودی|💳"
    RULES = "⚖️|قوانین|⚖️"
    HELP = "🕵️‍♂️|چطور اعتماد کنم؟|🕵️‍♂️"
    CONTACT_US = "☎️|ارتباط با پشتیبانی|☎️"
    # TRON = "🪙|ترون|🪙"
    REFERRAL = "👥|زیر مجموعه گیری|👥"
    BACK_TO_START = "🔙|بازگشت به منو|🔙"


class TextButtons:

    START_MENU = (
        
        (
            Button.text(text=TextButtonsString.MY_ACCOUNT, resize=True, single_use=True),
            # Button.text(text=TextButtonsString.WITHDRAW, resize=True, single_use=True),
        ),
        (
            Button.text(text=TextButtonsString.DEPOSIT_PANEL, resize=True, single_use=True),
        ),
        (
            Button.text(text=TextButtonsString.HELP, resize=True, single_use=False),
            Button.text(text=TextButtonsString.RULES, resize=True, single_use=True),
        ),
        (
            Button.text(text=TextButtonsString.CONTACT_US, resize=True, single_use=False),
        ),
    )

    DEPOSIT_PLAN = (
        (
            # Button.text(text=TextButtonsString.TRON, resize=True, single_use=True),
            Button.text(text=TextButtonsString.REFERRAL, resize=True, single_use=True),
        ),
        (
            Button.text(text=TextButtonsString.BACK_TO_START, resize=True, single_use=True),
        ),
    )

# endregion

# region InlineButton

class InlineButtonsData:
    BOT_STATS = "BOT_STATS"
    ADMIN_SETTING_PANEL = "ADMIN_SETTING_PANEL"
    USER_SETTING_PANEL = "USER_SETTING_PANEL"
    CHANNEL_PANEL = "CHANNEL_PANEL"
    SEND_PANEL = "SEND_PANEL"
    CHANGE_CONFIGS = "CHANGE_CONFIGS"
    ADD_ADMIN = "ADD_ADMIN"
    DELETE_ADMIN = "DELETE_ADMIN"
    SHOW_ADMINS = "SHOW_ADMIN"
    ADD_CHANNEL = "ADD_CHANNEL"
    DELETE_CHANNEL = "DELETE_CHANNEL-"
    SEND_TO_USER = "SEND_TO_USER"
    SEND_TO_USERS = "SEND_TO_USERS"
    BAN_USER = "BAN_USER"
    UNBAN_USER = "UNBAN_USER"
    SHOW_USER_INFO = "SHOW_USER_INFO"
    CHANGE_RULES_TEXT = "CHANGE_RULES_TEXT"
    CHANGE_HELP_TEXT = "CHANGE_HELP_TEXT"
    CHANGE_ENTERY_PRIZE = "CHANGE_ENTERY_PRIZE"
    CHANGE_TRUST_CHANNEL = "CHANGE_TRUST_CHANNEL"
    CHANGE_REFERRAL_BONUS = "CHANGE_REFERRAL_BONUS"
    JOINED_IN_CHANNEL = "JOINED_IN_CHANNEL_"
    # ACC_PAY = "ACC_PAY_"
    # REJECT_PAY = "REJECT_PAY_"
    BACK_TO_ADMIN = "BACK_TO_ADMIN"
    # ACC_WITHDRAW = "ACC_WITHDRAW_"
    # REJECT_WITHDRAW = "REJECT_WITHDRAW_"
    # SEND_FACTOR = "SEND_FACTOR"

    
    # acc_withdraw = lambda withdraw_code: f"{InlineButtonsData.ACC_WITHDRAW}{withdraw_code}"
    # reject_withdraw = lambda withdraw_code: f"{InlineButtonsData.REJECT_WITHDRAW}{withdraw_code}"
    # acc_pay = lambda user_id: f"{InlineButtonsData.ACC_PAY}{user_id}"
    # reject_pay = lambda user_id: f"{InlineButtonsData.REJECT_PAY}{user_id}"
    delete_channel = lambda channel_id: f"{InlineButtonsData.DELETE_CHANNEL}{channel_id}"
    joined_in_channel = lambda user_id: f"{InlineButtonsData.JOINED_IN_CHANNEL}{user_id}"
    

class InlineButtonString:
    BOT_STATS = "👥|امار ربات|👥"
    ADMIN_SETTING_PANEL = "👨🏻‍💻|مدیریت ادمین|🧑🏻‍💻"
    USER_SETTING_PANEL = "👀|مدیریت کاربران|👀"
    CHANNEL_PANEL = "🔐|مدیریت کانال ها|🔐"
    SEND_PANEL = "📨|بخش ارسال|📨"
    CHANGE_CONFIGS = "⚙️|تنظیمات|⚙️"
    ADD_ADMIN = "➕| افزودن ادمین"
    DELETE_ADMIN = "➖| حذف ادمین"
    SHOW_ADMINS = "👁| مشاهده ادمین ها"
    ADD_CHANNEL = "➕| افزودن کانال"
    DELETE_CHANNEL = "➖| حذف کانال"
    SEND_TO_USER = "✍🏻|پیام به کاربر|👤"
    SEND_TO_USERS = "✍🏻|پیام به کاربران|👥"
    BAN_USER = "❌| بن کردن کاربر"
    UNBAN_USER = "✅|  انبن کردن کاربر"
    SHOW_USER_INFO = "👀| مشخصات کاربر"
    CHANGE_RULES_TEXT = "⚙️| تغییر متن قوانین"
    CHANGE_HELP_TEXT = "⚙️| تغییر متن راهنما"
    CHANGE_ENTERY_PRIZE = "⚙️| تغییر هدیه استارت"
    CHANGE_TRUST_CHANNEL = "⚙️| تغییر کانال اعتماد"
    CHANGE_REFERRAL_BONUS = "⚙️| تغییر هزینه زیرمجموعه"
    JOINED_IN_CHANNEL = "تایید عضویت ✅"
    # ACC_PAY = "✅ تایید کردن"
    # REJECT_PAY = "❌ رد کردن"
    # SEND_FACTOR = "💳 ارسال رسید"

    BACK_TO_ADMIN = "📍 | بازگشت"


class InlineButtons:

    BACK_TO_ADMIN = (
        Button.inline(text=InlineButtonString.BACK_TO_ADMIN, data=InlineButtonsData.BACK_TO_ADMIN),
    )

    ADMIN_PANEL = (
        (
            Button.inline(text=InlineButtonString.BOT_STATS, data=InlineButtonsData.BOT_STATS),
        ),
        (
            Button.inline(text=InlineButtonString.ADMIN_SETTING_PANEL, data=InlineButtonsData.ADMIN_SETTING_PANEL),
            Button.inline(text=InlineButtonString.USER_SETTING_PANEL, data=InlineButtonsData.USER_SETTING_PANEL)
        ),
        (
            Button.inline(text=InlineButtonString.SEND_PANEL, data=InlineButtonsData.SEND_PANEL),
            Button.inline(text=InlineButtonString.CHANNEL_PANEL, data=InlineButtonsData.CHANNEL_PANEL)
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_CONFIGS, data=InlineButtonsData.CHANGE_CONFIGS),
        ),
    )

    ADMIN_SETTING = (
        (
            Button.inline(text=InlineButtonString.ADD_ADMIN, data=InlineButtonsData.ADD_ADMIN),
            Button.inline(text=InlineButtonString.DELETE_ADMIN, data=InlineButtonsData.DELETE_ADMIN)
        ),
        (
            Button.inline(text=InlineButtonString.SHOW_ADMINS, data=InlineButtonsData.SHOW_ADMINS),
        ),
        BACK_TO_ADMIN
    )

    USER_SETTING = (
        (
            Button.inline(text=InlineButtonString.BAN_USER, data=InlineButtonsData.BAN_USER),
            Button.inline(text=InlineButtonString.UNBAN_USER, data=InlineButtonsData.UNBAN_USER),
        ),
        (
            Button.inline(text=InlineButtonString.SHOW_USER_INFO, data=InlineButtonsData.SHOW_USER_INFO),
        ),
        BACK_TO_ADMIN
    )

    SEND_PANEL = (
        (
            Button.inline(text=InlineButtonString.SEND_TO_USER, data=InlineButtonsData.SEND_TO_USER),
            Button.inline(text=InlineButtonString.SEND_TO_USERS, data=InlineButtonsData.SEND_TO_USERS)
        ),
        BACK_TO_ADMIN
    )

    CONFIGS_PANEL = (
        (
            Button.inline(text=InlineButtonString.CHANGE_RULES_TEXT, data=InlineButtonsData.CHANGE_RULES_TEXT),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_HELP_TEXT, data=InlineButtonsData.CHANGE_HELP_TEXT),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_ENTERY_PRIZE, data=InlineButtonsData.CHANGE_ENTERY_PRIZE),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_REFERRAL_BONUS, data=InlineButtonsData.CHANGE_REFERRAL_BONUS),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_TRUST_CHANNEL, data=InlineButtonsData.CHANGE_TRUST_CHANNEL),
        ),
        BACK_TO_ADMIN
    )

    # SEND_FACTOR = (
    #     Button.inline(text=InlineButtonString.SEND_FACTOR, data=InlineButtonsData.SEND_FACTOR),
    # )


    # @staticmethod
    # def acc_reject_pay(user_id: int) -> Tuple[Tuple[Button]]:
    #     return (
    #         (
    #             Button.inline(text=InlineButtonString.ACC_PAY, data=InlineButtonsData.acc_pay(user_id)),
    #             Button.inline(text=InlineButtonString.REJECT_PAY, data=InlineButtonsData.reject_pay(user_id))
    #         ),
    #     )


    # @staticmethod
    # def acc_reject_withdraw(withdraw_code) -> Tuple[Tuple[Button]]:
    #     return (
    #         (
    #             Button.inline(text=InlineButtonString.ACC_PAY, data=InlineButtonsData.acc_withdraw(withdraw_code)),
    #             Button.inline(text=InlineButtonString.REJECT_PAY, data=InlineButtonsData.reject_withdraw(withdraw_code))
    #         ),
    #     )


    @staticmethod
    def channels_panel(channels: Iterable[Channel]) -> List[Tuple[Channel]]:
        
        buttons = []

        for channel in channels:
            buttons.append(
                (
                    Button.inline(text=InlineButtonString.DELETE_CHANNEL, data=InlineButtonsData.delete_channel(channel.channel_id)),
                    Button.url(text=channel.channel_name, url=channel.channel_url),
                )
            )

        buttons.append(
            (
                Button.inline(text=InlineButtonString.ADD_CHANNEL, data=InlineButtonsData.ADD_CHANNEL),
            )
        )
        buttons.append(InlineButtons.BACK_TO_ADMIN)

        return buttons


    @staticmethod
    def check_joined(user_id: int | None = None) -> Tuple[Button]:
        return Button.inline(text=InlineButtonString.JOINED_IN_CHANNEL, data=InlineButtonsData.joined_in_channel(user_id))
        

# endregion

# region UrlButton


class UrlButtonString:
    CONTACT_US = "✍🏻| پیام به ادمین |✍🏻"
    TRUST_CHANNEL = "💰|کانال واریزی ها|💰"


class UrlButtons:
    
    
    CONTACT_US = (
        (
            Button.url(text=UrlButtonString.CONTACT_US, url=f"t.me/{BotConfig.SUPPORT_USERNAME}"),
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
    def channels_locked(channels: Iterable[Channel], invited_user_id: int | None = None) -> List[Tuple[Button]]:
        
        buttons = []

        for channel in channels:
            
            try:
                buttons.append((Button.url(text=channel.channel_name, url=channel.channel_url),))
            except Exception as e:
                print(e)

        buttons.append((InlineButtons.check_joined(invited_user_id),))

        return buttons


# endregion
