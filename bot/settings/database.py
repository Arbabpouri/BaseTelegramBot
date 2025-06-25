from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import create_engine
from settings.config import DEFAULT_ADMINS_USER_ID, ENTRY_PRIZE, REFERRAL_BONUS, SUPPORT_CHANNEL_URL
from settings.strings import (
    START_MENU,
    MESSAGE_TO_SUPPORT_TEXT,
    HELP,
    RULES
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


from models import *    


def default_data() -> None:
    
    global START_MENU, HELP, RULES, MESSAGE_TO_SUPPORT_TEXT, ENTRY_PRIZE, REFERRAL_BONUS, SUPPORT_CHANNEL_URL

    with SessionLocal() as session:

        for admin in DEFAULT_ADMINS_USER_ID:
            user = session.query(UserModel).filter_by(user_id=admin).first()
            if not user:
                session.add(UserModel(user_id=admin, is_admin=True))
            
            configs = session.query(ConfigsModel).first()
            if not configs:
                configs = ConfigsModel()
                session.add(configs)
            
            START_MENU = configs.start_menu_text
            HELP = configs.help_text
            RULES = configs.rules_text
            MESSAGE_TO_SUPPORT_TEXT = configs.message_to_support_text
            ENTRY_PRIZE = configs.entry_prize
            REFERRAL_BONUS = configs.referral_bonus
            SUPPORT_CHANNEL_URL = configs.support_channel_url
            
            
        session.commit()

def create_tables() -> None:
    Base.metadata.create_all(engine)
