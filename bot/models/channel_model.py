from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String
from settings.database import Base


class Channel(Base):
    __tablename__ = "channels"
    channel_id: Mapped[int] = mapped_column(unique=True)
    channel_name: Mapped[str] = mapped_column(String(300))
    channel_url: Mapped[str] = mapped_column(String(350))
