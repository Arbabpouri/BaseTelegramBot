from telethon import Button
from enum import IntEnum
from models import ChannelModel


# All Inline Button Data
class InlineButtonsData:
    
    BOT_STATS = b"BOT_STATS"
    ADMIN_SETTING_PANEL = b"ADMIN_SETTING_PANEL"
    USER_SETTING_PANEL = b"USER_SETTING_PANEL"
    CHANNEL_PANEL = b"CHANNEL_PANEL"
    SEND_PANEL = b"SEND_PANEL"
    CHANGE_CONFIGS = b"CHANGE_CONFIGS"
    ADD_ADMIN = b"ADD_ADMIN"
    DELETE_ADMIN = b"DELETE_ADMIN"
    SHOW_ADMINS = b"SHOW_ADMIN"
    ADD_CHANNEL = b"ADD_CHANNEL"
    DELETE_CHANNEL = b"DELETE_CHANNEL_"
    SEND_TO_USER = b"SEND_TO_USER"
    SEND_TO_USERS = b"SEND_TO_USERS"
    FORWARD_TO_USER = b"FORWARD_TO_USER"
    FORWARD_TO_USERS = b"FORWARD_TO_USERS"
    BAN_USER = b"BAN_USER"
    UNBAN_USER = b"UNBAN_USER"
    SHOW_USER_INFO = b"SHOW_USER_INFO"
    INCREASE_USER_BALANCE = b"INCREASE_USER_BALANCE"
    REDUCE_USER_BALANCE = b"REDUCE_USER_BALANCE"
    CHANGE_REFERRAL_SETTINGS = b"CHANGE_REFERRAL_SETTINGS"
    CHANGE_TEXTS_SETTINGS = b"CHANGE_TEXTS_SETTINGS"
    CHANGE_RULES_TEXT = b"CHANGE_RULES_TEXT"
    CHANGE_HELP_TEXT = b"CHANGE_HELP_TEXT"
    CHANGE_ENTERY_PRIZE = b"CHANGE_ENTERY_PRIZE"
    CHANGE_SUPPORT_CHANNEL = b"CHANGE_SUPPORT_CHANNEL"
    CHANGE_REFERRAL_BONUS = b"CHANGE_REFERRAL_BONUS"
    CHANGE_START_MENU_TEXT = b"CHANGE_START_MENU_TEXT"
    CHANGE_MESSAGE_TO_SUPPORT_TEXT = b"CHANGE_MESSAGE_TO_SUPPORT_TEXT"
    CHANGE_CARD_INFO = b"CHANGE_CARD_INFO"
    JOINED_IN_CHANNEL = b"JOINED_IN_CHANNEL_"
    BACK_TO_ADMIN = b"BACK_TO_ADMIN"
    BACK_TO_ADMIN_SETTING = b"BACK_TO_ADMIN_SETTING"
    CANCEL_ADMIN = b"CANCEL_ADMIN"
    CANCEL_USER = b"CANCEL_USER"
    MESSAGE_TO_SUPPORT_CONFIRM_RULES = b"MESSAGE_TO_SUPPORT_CONFIRM_RULES"
    ACC_FACTOR = b"ACC_FACTOR"
    REJECT_FACTOR = b"REJECT_FACTOR"
    
    acc_factor = lambda factor_id: f"{InlineButtonsData.ACC_FACTOR.decode()}{factor_id}".encode()
    reject_factor = lambda factor_id: f"{InlineButtonsData.REJECT_FACTOR.decode()}{factor_id}".encode()
    delete_channel = lambda channel_id: f"{InlineButtonsData.DELETE_CHANNEL.decode()}{channel_id}".encode()
    joined_in_channel = lambda user_id: f"{InlineButtonsData.JOINED_IN_CHANNEL.decode()}{user_id}".encode()
    

# All Inline Button Text
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
    SEND_TO_USER = "📩|پیام به کاربر|👤"
    SEND_TO_USERS = "📩|پیام به کاربران|👥"
    FORWARD_TO_USER = "⏩|پیام به کاربر|👤"
    FORWARD_TO_USERS = "⏩|پیام به کاربران|👥"
    BAN_USER = "❌| بن کردن کاربر"
    UNBAN_USER = "✅|  انبن کردن کاربر"
    SHOW_USER_INFO = "👀| مشخصات کاربر"
    INCREASE_USER_BALANCE = "🔋 | افزایش موجودی کاربر"
    REDUCE_USER_BALANCE = "🪫 | کاهش موجودی کاربر"
    CHANGE_REFERRAL_SETTINGS = "📌 | تنظیمات زیرمجموعه گیری"
    CHANGE_TEXTS_SETTINGS = "📌 | تنظیمات متن ها"
    CHANGE_RULES_TEXT = "⚙️| تغییر متن قوانین"
    CHANGE_HELP_TEXT = "⚙️| تغییر متن راهنما"
    CHANGE_ENTERY_PRIZE = "⚙️| تغییر هدیه استارت"
    CHANGE_SUPPORT_CHANNEL = "⚙️| تغییر کانال اعتماد"
    CHANGE_REFERRAL_BONUS = "⚙️| تغییر هزینه زیرمجموعه"
    CHANGE_START_MENU_TEXT = "⚙️| تغییر متن شروع"
    CHANGE_CARD_INFO = "⚙️| تغییر اطلاعات کارت"
    CHANGE_MESSAGE_TO_SUPPORT_TEXT = "⚙️| تغییر متن پشتیبانی"
    JOINED_IN_CHANNEL = "تایید عضویت ✅"
    I_UNDERSTAND = "⁉ متوجه شدم"
    BACK = "📍 | بازگشت"
    ACC = "✔ تایید"
    REJECT = "❌ رد"


# all backs enum, using for InlineButtons.back_to
class BackToEnum(IntEnum):
    ADMIN_PANEL = 0
    ADMIN_SETTING = 1
    BOT_SETTINGS_PANEL = 2
    

# All Inline Button
class InlineButtons:
    
    
    @staticmethod
    async def channels_panel(channels: list[ChannelModel]):
        
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
        
        buttons.append(
            (
                InlineButtons.back_to(BackToEnum.ADMIN_PANEL),
            )
        )
        return buttons


    @staticmethod
    def check_joined(user_id: int | None = None):
        return Button.inline(text=InlineButtonString.JOINED_IN_CHANNEL, data=InlineButtonsData.joined_in_channel(user_id))
    
    
    @staticmethod
    def back_to(back_to: BackToEnum):
        
        match (back_to):
            
            case BackToEnum.ADMIN_PANEL:
                text = InlineButtonString.BACK
                data = InlineButtonsData.BACK_TO_ADMIN
                
            case BackToEnum.ADMIN_SETTING:
                text = InlineButtonString.BACK
                data = InlineButtonsData.BACK_TO_ADMIN_SETTING
            
            case _:
                text = InlineButtonString.BACK
                data = None
                
        
        return Button.inline(text=text, data=data)


    @staticmethod
    def acc_reject_factor(factor_id: int):
        return (
            Button.inline(text=InlineButtonString.ACC, data=InlineButtonsData.acc_factor(factor_id)),
            Button.inline(text=InlineButtonString.REJECT, data=InlineButtonsData.reject_factor(factor_id)),
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
        (
            back_to(back_to=BackToEnum.ADMIN_PANEL),
        )
    )


    USER_SETTING = (
        (
            Button.inline(text=InlineButtonString.BAN_USER, data=InlineButtonsData.BAN_USER),
            Button.inline(text=InlineButtonString.UNBAN_USER, data=InlineButtonsData.UNBAN_USER),
        ),
        (
            Button.inline(text=InlineButtonString.SHOW_USER_INFO, data=InlineButtonsData.SHOW_USER_INFO),
        ),
        (
            Button.inline(text=InlineButtonString.INCREASE_USER_BALANCE, data=InlineButtonsData.INCREASE_USER_BALANCE),
            Button.inline(text=InlineButtonString.REDUCE_USER_BALANCE, data=InlineButtonsData.REDUCE_USER_BALANCE),
        ),
        (
            back_to(back_to=BackToEnum.ADMIN_PANEL),
        )
    )


    SEND_PANEL = (
        (
            Button.inline(text=InlineButtonString.SEND_TO_USER, data=InlineButtonsData.SEND_TO_USER),
            Button.inline(text=InlineButtonString.SEND_TO_USERS, data=InlineButtonsData.SEND_TO_USERS)
        ),
        (
            Button.inline(text=InlineButtonString.FORWARD_TO_USER, data=InlineButtonsData.FORWARD_TO_USER),
            Button.inline(text=InlineButtonString.FORWARD_TO_USERS, data=InlineButtonsData.FORWARD_TO_USERS)
        ),
        (
            back_to(back_to=BackToEnum.ADMIN_PANEL),
        )
    )


    CONFIGS_PANEL = (
        (
            Button.inline(text=InlineButtonString.CHANGE_TEXTS_SETTINGS, data=InlineButtonsData.CHANGE_TEXTS_SETTINGS),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_REFERRAL_SETTINGS, data=InlineButtonsData.CHANGE_REFERRAL_SETTINGS),
        ),
        (
            back_to(back_to=BackToEnum.ADMIN_PANEL)
        )
    )


    CHANGE_REFERRAL_SETTINGS = (
        (
            Button.inline(text=InlineButtonString.CHANGE_ENTERY_PRIZE, data=InlineButtonsData.CHANGE_ENTERY_PRIZE),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_REFERRAL_BONUS, data=InlineButtonsData.CHANGE_REFERRAL_BONUS),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_SUPPORT_CHANNEL, data=InlineButtonsData.CHANGE_SUPPORT_CHANNEL),
        ),
        (
            back_to(back_to=BackToEnum.BOT_SETTINGS_PANEL),
        )
    )
    
    
    CHANGE_TEXTS_SETTINGS = (
        (
            Button.inline(text=InlineButtonString.CHANGE_START_MENU_TEXT, data=InlineButtonsData.CHANGE_START_MENU_TEXT),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_RULES_TEXT, data=InlineButtonsData.CHANGE_RULES_TEXT),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_HELP_TEXT, data=InlineButtonsData.CHANGE_HELP_TEXT),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_MESSAGE_TO_SUPPORT_TEXT, data=InlineButtonsData.CHANGE_MESSAGE_TO_SUPPORT_TEXT),
        ),
        (
            Button.inline(text=InlineButtonString.CHANGE_CARD_INFO, data=InlineButtonsData.CHANGE_CARD_INFO),
        ),
        (
            back_to(back_to=BackToEnum.BOT_SETTINGS_PANEL),
        ),
        
    )


    CANCEL_ADMIN = (
        Button.inline(text=InlineButtonString.BACK, data=InlineButtonsData.CANCEL_ADMIN),
    )

    
    CANCEL_USER = (
        Button.inline(text=InlineButtonString.BACK, data=InlineButtonsData.CANCEL_USER),
    )


    MESSAGE_TO_SUPPORT = (
        Button.inline(text=InlineButtonString.I_UNDERSTAND, data=InlineButtonsData.MESSAGE_TO_SUPPORT_CONFIRM_RULES),
    )
