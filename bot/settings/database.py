from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import create_engine



class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

from settings.config import DEFAULT_ADMINS_USER_ID, ConfigVariableChangable
from models import *
from settings.strings import StringsVariableChangable

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def default_data() -> None:
    
    with SessionLocal() as session:

        for admin in DEFAULT_ADMINS_USER_ID:
            user = session.query(UserModel).filter_by(user_id=admin).first()
            if not user:
                session.add(UserModel(user_id=admin, is_admin=True))
            
        configs = session.query(ConfigsModel).first()
        if not configs:
            configs = ConfigsModel()
            session.add(configs)
            
        StringsVariableChangable.START_MENU = configs.start_menu_text
        StringsVariableChangable.HELP = configs.help_text
        StringsVariableChangable.RULES = configs.rules_text
        StringsVariableChangable.MESSAGE_TO_SUPPORT_TEXT = configs.message_to_support_text
        ConfigVariableChangable.ENTRY_PRIZE = configs.entry_prize
        ConfigVariableChangable.REFERRAL_BONUS = configs.referral_bonus
        ConfigVariableChangable.SUPPORT_CHANNEL_URL = configs.support_channel_url
            
            
        session.commit()
