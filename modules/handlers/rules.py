from ..database import User, engine
from .buttons import InlineButtonsData
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .step import step_limit


def is_admin(user_id: int) -> bool:
    with Session(engine) as session:
        is_admin = session.query(User).filter(and_(User.user_id == int(user_id), User.is_admin == True)).first()
    return bool(is_admin)


def is_ban(user_id: int) -> bool:
    with Session(engine) as session:
        user = session.query(User).filter_by(user_id=int(user_id)).first()
        if user and user.is_ban:
            return True
    
    return False


async def user_move_text(event) -> bool:
    return ((event.message.message == "/start" or event.sender_id not in step_limit.keys()) and event.is_private and not is_ban(event.sender_id))

async def user_move_inline(event) -> bool:
    return (event.sender_id not in step_limit and not is_ban(event.sender_id))

async def admin_move_text(event) -> bool:
    return (await user_move_text(event) and is_admin(user_id=event.sender_id) and not is_ban(event.sender_id))

async def admin_move_inline(event) -> bool:
    return (await user_move_inline(event) and is_admin(user_id=event.sender_id))

async def get_informations_user(event) -> bool:
    return (
        int(event.sender_id) in step_limit and
        event.is_private and
        not is_ban(event.sender_id)
    )

async def get_informations_admin(event) -> bool:
    return (
        int(event.sender_id) in step_limit and
        is_admin(user_id=event.sender_id) and 
        event.is_private and
        not is_ban(event.sender_id)
    )
