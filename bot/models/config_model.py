from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer, String
from settings.database import Base
from settings.config import TEXT_LONG, REFERRAL_BONUS, ENTRY_PRIZE, SUPPORT_CHANNEL_URL
from settings.strings import START_MENU, RULES, HELP, MESSAGE_TO_SUPPORT_TEXT

class ConfigsModel(Base):
    __tablename__ = "configs"
    start_menu_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=START_MENU)
    support_channel_url: Mapped[str] = mapped_column(String(300), default=SUPPORT_CHANNEL_URL)
    message_to_support_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=MESSAGE_TO_SUPPORT_TEXT)
    help_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=HELP)
    rules_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=RULES)
    entry_prize: Mapped[int] = mapped_column(Integer, default=ENTRY_PRIZE)
    referral_bonus: Mapped[int] = mapped_column(Integer, default=REFERRAL_BONUS)
