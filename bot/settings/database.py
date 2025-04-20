from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, mapped_column, Mapped
from contextlib import contextmanager
from sqlalchemy import create_engine
from settings.config import DEFAULT_ADMINS_USER_ID

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


from models import *    


def default_data() -> None:

    with SessionLocal() as session:

        for admin in DEFAULT_ADMINS_USER_ID:
            session.add(UserModel(user_id=admin, is_admin=True))
            
        session.commit()

def create_tables() -> None:
    Base.metadata.create_all(engine)
