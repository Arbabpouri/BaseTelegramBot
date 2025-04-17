from models.channel_model import ChannelModel
from models.config_model import ConfigsModel
from models.user_model import UserModel
from settings.database import get_session
from settings.config import DEFAULT_ADMINS_USER_ID


# region call in start

async def default_data() -> None:

    for admin in DEFAULT_ADMINS_USER_ID:
        await add_user(user_id=admin, is_admin=True)

    await update_configs()


# endregion


# region user

# get user, return UserModel if user in db else None
async def get_user(user_id: int) -> UserModel | None:
    "get user, return UserModel if user in db else None"

    session = get_session()
    return session.query(UserModel).filter_by(user_id=int(user_id)).first()


# get users, return list[UserModel] if users else empty list
async def get_users() -> list[UserModel]:
    "get users, return list[UserModel] if users else empty list"

    session = get_session()
    return session.query(UserModel).all()


# check user is admin ? True or False
async def user_is_admin(user_id: int) -> bool:
    "check user is admin ? True or False"

    user = await get_user(user_id=user_id)
    return bool(user and user.is_admin)


# get admins, return list[UserModel] if admins else empty list 
async def get_admins() -> list[UserModel] | None:
    "get admins, return list[UserModel] if admins else empty list"
    session = get_session()
    return session.query(UserModel).filter_by(is_admin=True).all()
    

# check user is ban ? True or False
async def user_is_ban(user_id: int) -> bool:
    "check user is ban ? True or False"
    
    user = await get_user(user_id=user_id)
    return bool(user and user.is_ban)


# add bot admin, change user from manual user to admin user
async def add_admin(user_id: int) -> UserModel | None:
    "add bot admin, change user from manual user to admin user"
    
    session = get_session()
    user = session.query(UserModel).filter_by(user_id=int(user_id)).first()

    if user:
        user.is_admin = True
        session.commit()
        return user
    
    return None
        

# remove bot admin, change user from admin user to manual user
async def remove_admin(user_id: int) -> UserModel | None:
    "remove bot admin, change user from admin user to manual user"
    
    "add bot admin, change user from manual user to admin user"
    
    session = get_session()
    user = session.query(UserModel).filter_by(user_id=int(user_id)).first()

    if user:
        user.is_admin = False
        session.commit()
        return user
    
    return None


# add new user to database
async def add_user(user_id: int, is_admin: bool, invited_by: int | None = None, referral_active: bool | None = None) -> UserModel:
    "add new user to database"
    
    session = get_session()
    user = session.query(UserModel).filter_by(user_id=int(user_id)).first()

    if user:
        user.referral_active = referral_active

    else:
        user = UserModel(user_id=int(user_id), is_admin=bool(is_admin), invited_by=invited_by, referral_active=referral_active)
        session.add(user)
    
    
    session.commit()


    return user
    

# endregion


# region channel


# get channel, return ChannelModel or None
async def get_channel(channel_id: int) -> ChannelModel | None:
    "get channel, return ChannelModel or None"

    session = get_session()
    return session.query(ChannelModel).filter_by(channel_id=int(channel_id)).first()


# get channels, return a list of ChannelModel or empty list
async def get_channels() -> list[ChannelModel]:
    "get channels, return a list of ChannelModel or empty list"

    session = get_session()
    return session.query(ChannelModel).all()


# add channel, add new channel to db
async def add_channel(channel_id: int, channel_name: str, channel_url: str) -> ChannelModel:
    "add channel, add new channel to db, return ChannelModel"

    session = get_session()
    channel = session.query(ChannelModel).filter_by(channel_id=int(channel_id)).first()

    if not channel:    
        channel = ChannelModel(channel_id=int(channel_id), channel_name=str(channel_name), channel_url=str(channel_url))
        session.add(channel)
        session.commit()

    return channel
    

# remove channel, remove channel from db
async def remove_channel(channel_id: int) -> ChannelModel | None:
    "remove channel, remove channel from db, if return None: channel not exist else return ChannelModel"

    session = get_session()
    channel = session.query(ChannelModel).filter_by(channel_id=int(channel_id)).first()

    if channel:    
        session.delete(channel)
        session.commit()
        return channel
    
    return None


# endregion


# region config


# update bot configs
async def update_configs(support_channel_url: str | None = None, help_text: str | None = None, rules_text: str | None = None, entry_prize: int | None = None, referral_bonus: int | None = None) -> ConfigsModel:
    "update bot configs"

    session = get_session()
    config = session.query(ConfigsModel).first()
    
    if not config:
        config = ConfigsModel()
        session.add(config)
        
    if support_channel_url:
        config.support_channel_url = str(support_channel_url)
    
    if help_text:
        config.help_text = str(help_text)
        
    if rules_text:
        config.rules_text = str(rules_text)
        
    if entry_prize:
        config.entry_prize = int(entry_prize)
    
    if referral_bonus:
        config.referral_bonus = int(referral_bonus)
    
    session.commit()
    
    return config


# get config
async def get_config() -> ConfigsModel:
    "get config"
    
    session = get_session()
    config = session.query(ConfigsModel).first()
    
    if not config:
        config = ConfigsModel()
        session.add(config)
        
    return config


# endregion
