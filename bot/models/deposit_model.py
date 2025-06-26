import shortuuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime, ForeignKey, Integer
from settings.database import Base, UserModel


class DepositModel(Base):
    __tablename__ = "deposits"
    factor_id: Mapped[str] = mapped_column(String(40), default=shortuuid.uuid(), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    account_name: Mapped[str] = mapped_column(String(300), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    user: Mapped['UserModel'] = relationship('UserModel', back_populates='factors')
    amount: Mapped[float]
    datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[bool] = mapped_column(nullable=True, default=None)
    acc_or_reject_by_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=True, default=None)
    acc_or_reject_by_user: Mapped['UserModel'] = relationship('UserModel')
    