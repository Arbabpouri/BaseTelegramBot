from typing import Iterable
from models.channel_model import ChannelModel
from models.config_model import ConfigsModel
from models.user_model import UserModel
from settings.config import BOT_USERNAME, REFERRAL_BONUS, ENTRY_PRIZE


# region functions

def bot_stats(users: int, channels: int) -> str:
    return (
        f"🫂 | کاربران : {users}\n"
        f"🔐 | کانال های قفل شده : {channels}\n"
    )


def my_account(user: UserModel) -> str:
    return (
        f"🔢 شناسه عددی : <code>{user.user_id}</code>\n\n"
        f"💳 موجودی شما : {user.balance:,} تومان\n\n"
        f"👥 تعداد زیر مجموعه های شما : {len(user.user_referrals)}"
    )


def referral_banner(user_id: int) -> str:
    return (
        "⚠️ با تاس🎲 انداختن پول در بیار!\n\n"

        "ربات زیر با تاس🎲 انداختن پول میده باورت میشه؟ :)\n\n"

        f"🎁 به کاربرای جدید هم {ENTRY_PRIZE:,} تومان هدیه خوش آمدگویی میده از دستش نده 🥳👇\n\n"

        f"https://t.me/{BOT_USERNAME}/?start={user_id}"
    )


def referral_reply(user: UserModel) -> str:
    return (
        f"⚠️ بنر بالا را برای دوستانتان ارسال کنید و به ازای هر شخصی که با لینک شما در ربات عضو شود {REFERRAL_BONUS:,} تومان اعتبار هدیه دریافت خواهید کرد.\n\n"

        f"👥 تعداد زیرمجموعه شما: {len(user.user_referrals)}"
    )


def show_admins(admins: Iterable[UserModel]) -> str:
    message = "👥 ادمین ها : \n\n"
    for index, admin in enumerate(admins):
        message += f"👤 <b>{index}</b> - <code>{admin.user_id}</code> \n"

    return message


def message_sended(success_num: int) -> str:
    return f"👥 پیام شما با موفقیت برای {success_num} نفر ارسال شد"


def channel_deleted(channel: ChannelModel) -> str:
    return (
        "📌 کانال به مشخصات زیر به خاطر حذف ربات از ادمین ها دیلیت شد\n\n"
        f"🔸 id : {channel.channel_id}\n"
        f"🔸 title : {channel.channel_name}\n"
        f"🔸 url : {channel.channel_url}\n"
    )


def referral_bonus(invited_user_id: int, amount: int) -> str:
    return (
        f"💰 کاربر عزیز شما زیر مجموعه جدید گرفتید به ایدی <code>{invited_user_id}</code> و مقدار {amount:,} به شما داده شد"
    )


def user_info(user: UserModel) -> str:
    return (
        f"📌 کاربر با ایدی عددی : {user.user_id}\n"
        f"💰 موجودی : {user.balance}\n"
        f"⛓ تعداد زیر مجموعه : {len(user.users_referrals)}"
    )

# endregion

# region variable

START_MENU = "🔹 سلام به ربات خوش اومدی, از منوی زیر انتخاب کن :"
RULES = "متن پیش فرض قوانین"
HELP = "متن پیش فرض راهنما"
MESSAGE_TO_SUPPORT_TEXT = "متن پیشفرض توجیح کاربر برای پیام به پشتیبانی"
ADMIN_PANEL = "💢 به پنل ادمین خوش آمدید"
CONTACT_US = "💬 تنها جهت پیگیری برداشتتان پیام دهید👇"
SELECT = "⭕️ یک مورد را انتخاب کنید👇"
BACKED = "🔙 بازگشتید"
NEW_UPDATE = "💭 در اپدیت های بعدی اضافه میشود"
CANCEL =  "📍 برای کنسل کردن از /cancel استفاده کنید"
CANCELED = "❤ عملیات با موفقیت کنسل شد"
DELETED = "❌ با موفقیت حذف شد"
ADDED = "✅ با موفقیت اضافه شد"
NO_YOU = "⛔ نمیتوانید روی خود کاری کنید"
IS_CREATOR = "⛔ ایشان سازنده ربات است"
USER_EXIST = "👤 این شخص در لیست وجود دارد"
USER_NOT_EXIST = "👤 این شخص در لیست وجود ندارد, دقت کنید"
ENTER_USER_ID = f"🔢 لطفا ایدی عددی را ارسال کنید\n\n{CANCEL}"
ENTER_TEXT = f"📜 لطفا متن را ارسال کنید : \n\n{CANCEL}"
ENTER_VALUE = f"📊 لطفا مقدار را وارد کنید : \n\n{CANCEL}"
ADD_CHANNEL = f"📌 لطفا ابتدا ربات را در کانال ادمین کرده و سپس یک پیام از کانال برای ربات فورارد کنید \n\n {CANCEL}"
ENTER_URL = f"🔑 لطفا لینک را ارسال کنید : \n\n{CANCEL}"
PLEASE_START_BOT = "⚠ باید اول ربات را استارت کند"
ENTER_NUMBER = "⛔ فقط مقدار عددی وارد کنید ⛔"
BOT_NOT_ADMIN = "🤖 ربات ادمین نیست"
ERROR = "⁉💔 مشکلی پیش امد لطفا مجدد تلاش کنید و اگر چندمین بار است این پیام را میبینید به برنامه نویس گزارش کنید"
UPDATED = "💥 اپدیت شد"
TEXT_IS_LONG = "❌ تعداد کاراکتر های ارسالی زیاد است لطفا کوتاه تر کنید"
ENTER_MESSAGE = "💎 لطفا پیام خود را ارسال کنید"
SENDING = "📌 درحال ارسال . . ."
CHANNEL_ALREADY_EXIST = "⚠ این کانال وجود دارد لطفا کانال دیگری را ارسال کنید"
JOIN_TO_CHANNELS = "⚠ برای فعالیت در ربات باید عضو کانال های زیر بشوید"
NOT_SEND = "🧶 پیام ارسال نشد, احتمالا ربات را بلاک کرده است"

# endregion
