from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer, String
from settings.database import Base
from settings.config import TEXT_LONG, DEFAULT_RULES_TEXT, DEFAULT_REFERRAL_BONUS, DEFAULT_ENTRY_PRIZE, DEFAULT_HELP_TEXT, DEFAULT_SUPPORT_CHANNEL_URL


class ConfigsModel(Base):
    __tablename__ = "configs"
    support_channel_url: Mapped[str] = mapped_column(String(300), default=DEFAULT_SUPPORT_CHANNEL_URL)
    help_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=DEFAULT_HELP_TEXT)
    rules_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=DEFAULT_RULES_TEXT)
    entry_prize: Mapped[int] = mapped_column(Integer, default=DEFAULT_ENTRY_PRIZE)
    referral_bonus: Mapped[int] = mapped_column(Integer, default=DEFAULT_REFERRAL_BONUS)
