from models.channel_model import ChannelModel
from models.config_model import ConfigsModel
from models.user_model import UserModel
from settings.database import get_session


# def default_data() -> None:

#     with Session(bind=engine) as session:

#         for admin in BotConfig.DEFULT_ADMINS_USER_ID:
#             session.add(User(user_id=admin, is_admin=True))

#         configs = Configs()

#         session.add_all([configs, ])
#         session.commit()


# region user

# get user, return UserModel if user in db else None
async def get_user(user_id: int) -> UserModel | None:
    "get user, return UserModel if user in db else None"

    session = get_session()
    return session.query(UserModel).filter_by(user_id=int(user_id)).first()


# check user is admin ? True or False
async def user_is_admin(user_id: int) -> bool:
    "check user is admin ? True or False"

    user = await get_user(user_id=user_id)
    return bool(user and user.is_admin)


# check user is ban ? True or False
async def user_is_ban(user_id: int) -> bool:
    "check user is ban ? True or False"
    
    user = await get_user(user_id=user_id)
    return bool(user and user.is_ban)


# add bot admin, change user from manual user to admin user
async def add_admin(user_id: int) -> UserModel | None:
    "add bot admin, change user from manual user to admin user"
    pass


# remove bot admin, change user from admin user to manual user
async def remove_admin(user_id: int) -> UserModel | None:
    "remove bot admin, change user from admin user to manual user"
    pass


# add new user to database
async def add_user(user_id: int, is_admin: bool) -> UserModel:
    "add new user to database"
    
    session = get_session()
    user = session.query(UserModel).filter_by(user_id=int(user_id)).first()
    
    if not user:
        user = UserModel(user_id=int(user_id), is_admin=bool(is_admin))
        session.add(user)
        session.commit()

    return user
    

# end region
