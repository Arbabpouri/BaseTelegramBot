from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, backref
from sqlalchemy import String, ForeignKey, create_engine, Integer, Text
from typing import List
from config import BotConfig


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column(default=BotConfig.DEFULT_ENTRY_PRIZE)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_ban: Mapped[bool] = mapped_column(default=False)
    referral_active: Mapped[bool] = mapped_column(nullable=True, default=None)
    invited_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, default=None)
    referrals: Mapped[List["User"]] = relationship('User', remote_side='User.id', backref=backref('user_referrals'))
    # withdraws: Mapped[List["Withdraw"]] = relationship(back_populates="user", cascade="all, delete-orphan")


# class Withdraw(Base):
#     __tablename__ = "withdraws"
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped["User"] = relationship(back_populates="withdraws")
#     amount: Mapped[int]
#     wallet: Mapped[str] = mapped_column(String(300))
#     withdraw_code: Mapped[str] = mapped_column(default=str(uuid4()))
#     is_check: Mapped[bool] = mapped_column(default=False)


class Channel(Base):
    __tablename__ = "channels"
    channel_id: Mapped[int] = mapped_column(unique=True)
    channel_name: Mapped[str] = mapped_column(String(300))
    channel_url: Mapped[str] = mapped_column(String(350))


class Configs(Base):
    __tablename__ = "configs"
    trust_channel_url: Mapped[str] = mapped_column(String(300), default=BotConfig.DEFULT_TRUST_CHANNEL_URL)
    trust_text: Mapped[str] = mapped_column(Text(BotConfig.TEXT_LONG), default=BotConfig.DEFULT_HELP_TEXT)
    rules_text: Mapped[str] = mapped_column(Text(BotConfig.TEXT_LONG), default=BotConfig.DEFULT_RULES_TEXT)
    entry_prize: Mapped[int] = mapped_column(Integer, default=BotConfig.DEFULT_ENTRY_PRIZE)
    referral_bonus: Mapped[int] = mapped_column(Integer, default=BotConfig.DEFULT_REFERRAL_BONUS)


engine = create_engine("sqlite:///database.db", echo=False, pool_size=60, max_overflow=35, pool_timeout=120.0)


def create_table() -> None:
    Base.metadata.create_all(bind=engine)


def defult_data() -> None:

    with Session(bind=engine) as session:

        for admin in BotConfig.DEFULT_ADMINS_USER_ID:
            session.add(User(user_id=admin, is_admin=True))

        configs = Configs()

        session.add_all([configs, ])
        session.commit()
