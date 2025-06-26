from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer, String
from settings.database import Base
from settings.config import TEXT_LONG, ConfigVariableChangable
from settings.strings import StringsVariableChangable

class ConfigsModel(Base):
    __tablename__ = "configs"
    start_menu_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=StringsVariableChangable.START_MENU)
    card_info: Mapped[str] = mapped_column(Text(TEXT_LONG), default=ConfigVariableChangable.CARD_INFO)
    support_channel_url: Mapped[str] = mapped_column(String(300), default=ConfigVariableChangable.SUPPORT_CHANNEL_URL)
    message_to_support_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=StringsVariableChangable.MESSAGE_TO_SUPPORT_TEXT)
    help_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=StringsVariableChangable.HELP)
    rules_text: Mapped[str] = mapped_column(Text(TEXT_LONG), default=StringsVariableChangable.RULES)
    entry_prize: Mapped[int] = mapped_column(Integer, default=ConfigVariableChangable.ENTRY_PRIZE)
    referral_bonus: Mapped[int] = mapped_column(Integer, default=ConfigVariableChangable.REFERRAL_BONUS)
