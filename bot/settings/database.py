from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import create_engine
from settings.config import DEFAULT_ADMINS_USER_ID

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


from models import *    


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
            
        session.commit()

def create_tables() -> None:
    Base.metadata.create_all(engine)
