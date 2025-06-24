# region imports

from models import UserModel
from settings.database import SessionLocal
from functions.step_functions import get_user_step, Parts
from buttons.inline_buttons import InlineButtonsData


# endregion


async def user_is_admin(user_id: int) -> bool:
    
    with SessionLocal() as session:
        return bool(session.query(UserModel).filter_by(user_id=int(user_id), is_admin=True).first())
    
    
# region rules

async def filter_user_move(event) -> bool:
    return event.is_private and not get_user_step(event.sender_id)

async def filter_admin_move(event) -> bool:
    return (
        event.is_private and 
        await user_is_admin(user_id=event.sender_id) and 
        not get_user_step(event.sender_id)
    )

async def filter_add_admin(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.ADD_ADMIN and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_del_admin(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.DELETE_ADMIN and 
        await user_is_admin(event.sender_id)
    )

async def filter_set_rule(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.CHANGE_RULES_TEXT and 
        await user_is_admin(event.sender_id)
    )

async def filter_set_help(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.CHANGE_HELP_TEXT and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_set_support_channel(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.CHANGE_SUPPORT_CHANNEL and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_set_referral_bonus(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.CHANGE_REFERRAL_BONUS and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_set_entry_prize(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.CHANGE_ENTERY_PRIZE and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_add_channel(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.ADD_CHANNEL and 
        await user_is_admin(event.sender_id)
    )  

async def filter_delete_channel(event) -> bool:
    return (
        event.is_private and
        str(event.data.decode()).startswith(InlineButtonsData.DELETE_CHANNEL.decode()) and 
        await filter_admin_move(event)
    )

async def filter_get_message_send_users(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step in (Parts.SEND_TO_USERS, Parts.FORWARD_TO_USERS) and 
        await user_is_admin(event.sender_id)
    )

async def filter_get_user_send(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step in (Parts.SEND_TO_USER, Parts.FORWARD_TO_USER) and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_get_message_send_user(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.GET_MESSAGE_SEND_TO_USER and 
        await user_is_admin(event.sender_id)
    )

async def filter_ban_user(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.BAN_USER and 
        await user_is_admin(event.sender_id)
    )

async def filter_unban_user(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.UNBAN_USER and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_user_info(event) -> bool:
    if not event.is_private:
        return False
    user_step = get_user_step(event.sender_id)
    return (
        user_step and
        user_step.step == Parts.SHOW_USER_INFO and 
        await user_is_admin(event.sender_id)
    )

# async def filter_(event) -> bool:
#     return bool(
#         get_user_step(event.sender_id).step == Parts.DELETE_ADMIN and 
#         await user_is_admin(event.sender_id)
#     )



# endregion