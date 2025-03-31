from telethon import Button
from typing import Optional
from functions.database_functions import get_channels

# All Inline Button Data
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
    BACK_TO_ADMIN = "BACK_TO_ADMIN"
    
    
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
    CHANGE_TRUST_CHANNEL = "⚙️| تغییر کانال اعتماد"
    CHANGE_REFERRAL_BONUS = "⚙️| تغییر هزینه زیرمجموعه"
    JOINED_IN_CHANNEL = "تایید عضویت ✅"
    BACK = "📍 | بازگشت"


# All Inline Button
class InlineButtons:

    BACK_TO_ADMIN = (
        Button.inline(text=InlineButtonString.BACK, data=InlineButtonsData.BACK_TO_ADMIN),
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
        
        buttons.append(InlineButtons.BACK_TO_ADMIN)
        return buttons


    @staticmethod
    def check_joined(user_id: int | None = None):
        return Button.inline(text=InlineButtonString.JOINED_IN_CHANNEL, data=InlineButtonsData.joined_in_channel(user_id))


    @staticmethod
    def back_to(
        admin_panel: Optional[bool] = False,
    ):
        
        text = InlineButtonString.BACK
        data = InlineButtonsData.BACK_TO_ADMIN
        
        return Button.inline(text=text, data=data)
