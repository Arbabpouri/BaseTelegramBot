from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# def default_data() -> None:

#     with Session(bind=engine) as session:

#         for admin in BotConfig.DEFULT_ADMINS_USER_ID:
#             session.add(User(user_id=admin, is_admin=True))

#         configs = Configs()

#         session.add_all([configs, ])
#         session.commit()
