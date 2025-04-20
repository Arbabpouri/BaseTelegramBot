from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, mapped_column, Mapped
from sqlalchemy import create_engine
from typing import Any

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


from models import *    


def get_session() -> Session | Any:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
