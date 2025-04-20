from sqlalchemy.orm import Mapped, relationship, mapped_column, backref
from sqlalchemy import ForeignKey, Integer
from typing import List
from settings.database import Base
from settings.config import DEFAULT_ENTRY_PRIZE


class UserModel(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column(default=DEFAULT_ENTRY_PRIZE)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_ban: Mapped[bool] = mapped_column(default=False)
    referral_active: Mapped[bool] = mapped_column(nullable=True, default=None)
    invited_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True, default=None)
    referrals: Mapped[List["UserModel"]] = relationship('UserModel', remote_side='UserModel.user_id', backref=backref('user_referrals'))
