from telethon import Button


class TextButtonsString:
    MY_ACCOUNT = "🔐| حساب من |🔐"
    DEPOSIT_PANEL = "💳|افزایش موجودی|💳"
    RULES = "⚖️|قوانین|⚖️"
    HELP = "🕵️‍♂️|چطور اعتماد کنم؟|🕵️‍♂️"
    CONTACT_US = "☎️|ارتباط با پشتیبانی|☎️"
    REFERRAL = "👥|زیر مجموعه گیری|👥"
    BACK_TO_START = "🔙|بازگشت به منو|🔙"
    DEPOSIT_WITH_CARD = "💳|کارت به کارت|💳"
    CANCEL_USER = "❌ لفو عملیات"


class TextButtons:

    START_MENU = (
        
        (
            Button.text(text=TextButtonsString.MY_ACCOUNT, resize=True, single_use=True),
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
            Button.text(text=TextButtonsString.DEPOSIT_WITH_CARD, resize=True, single_use=True),
        ),
        (
            Button.text(text=TextButtonsString.REFERRAL, resize=True, single_use=True),
        ),
        (
            Button.text(text=TextButtonsString.BACK_TO_START, resize=True, single_use=True),
        ),
    )

    CANCEL_USER = (
        Button.text(text=TextButtonsString.CANCEL_USER, resize=True, single_use=True),
    )
    