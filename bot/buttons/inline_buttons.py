from telethon import Button
from enum import IntEnum
from functions.database_functions import get_channels


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
    DELETE_CHANNEL = b"DELETE_CHANNEL-"
    SEND_TO_USER = b"SEND_TO_USER"
    SEND_TO_USERS = b"SEND_TO_USERS"
    BAN_USER = b"BAN_USER"
    UNBAN_USER = b"UNBAN_USER"
    SHOW_USER_INFO = b"SHOW_USER_INFO"
    CHANGE_RULES_TEXT = b"CHANGE_RULES_TEXT"
    CHANGE_HELP_TEXT = b"CHANGE_HELP_TEXT"
    CHANGE_ENTERY_PRIZE = b"CHANGE_ENTERY_PRIZE"
    CHANGE_SUPPORT_CHANNEL = b"CHANGE_SUPPORT_CHANNEL"
    CHANGE_REFERRAL_BONUS = b"CHANGE_REFERRAL_BONUS"
    JOINED_IN_CHANNEL = b"JOINED_IN_CHANNEL_"
    BACK_TO_ADMIN = b"BACK_TO_ADMIN"
    BACK_TO_ADMIN_SETTING = b"BACK_TO_ADMIN_SETTING"
    CANCEL_ADMIN = b"CANCEL_ADMIN"
    CANCEL_USER = b"CANCEL_USER"
    
    
    delete_channel = lambda channel_id: f"{InlineButtonsData.DELETE_CHANNEL}{channel_id}"
    joined_in_channel = lambda user_id: f"{InlineButtonsData.JOINED_IN_CHANNEL}{user_id}"
    

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
    SEND_TO_USER = "✍🏻|پیام به کاربر|👤"
    SEND_TO_USERS = "✍🏻|پیام به کاربران|👥"
    BAN_USER = "❌| بن کردن کاربر"
    UNBAN_USER = "✅|  انبن کردن کاربر"
    SHOW_USER_INFO = "👀| مشخصات کاربر"
    CHANGE_RULES_TEXT = "⚙️| تغییر متن قوانین"
    CHANGE_HELP_TEXT = "⚙️| تغییر متن راهنما"
    CHANGE_ENTERY_PRIZE = "⚙️| تغییر هدیه استارت"
    CHANGE_SUPPORT_CHANNEL = "⚙️| تغییر کانال اعتماد"
    CHANGE_REFERRAL_BONUS = "⚙️| تغییر هزینه زیرمجموعه"
    JOINED_IN_CHANNEL = "تایید عضویت ✅"
    BACK = "📍 | بازگشت"


# all backs enum, using for InlineButtons.back_to
class BackToEnum(IntEnum):
    ADMIN_PANEL = 0
    ADMIN_SETTING = 1
    

# All Inline Button
class InlineButtons:
    
    
    @staticmethod
    async def channels_panel():
        
        buttons = []
        
        channels = await get_channels()

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
            back_to(back_to=BackToEnum.ADMIN_PANEL),
        )
    )


    SEND_PANEL = (
        (
            Button.inline(text=InlineButtonString.SEND_TO_USER, data=InlineButtonsData.SEND_TO_USER),
            Button.inline(text=InlineButtonString.SEND_TO_USERS, data=InlineButtonsData.SEND_TO_USERS)
        ),
        (
            back_to(back_to=BackToEnum.ADMIN_PANEL),
        )
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
            Button.inline(text=InlineButtonString.CHANGE_SUPPORT_CHANNEL, data=InlineButtonsData.CHANGE_SUPPORT_CHANNEL),
        ),
        (
            back_to(back_to=BackToEnum.ADMIN_PANEL),
        )
    )


    CANCEL_ADMIN = (
        Button.inline(text=InlineButtonString.BACK, data=InlineButtonsData.CANCEL_ADMIN),
    )

    
    CANCEL_USER = (
        Button.inline(text=InlineButtonString.BACK, data=InlineButtonsData.CANCEL_USER),
    )
