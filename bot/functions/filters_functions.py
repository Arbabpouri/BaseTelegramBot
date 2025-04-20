# region imports

from functions.database_functions import user_is_admin
from functions.step_functions import get_user_step, Parts


# endregion

# region rules

async def filter_user_move(event) -> bool:
    return bool(not get_user_step(event.sender_id))

async def filter_admin_move(event) -> bool:
    return bool(await user_is_admin(user_id=event.sender_id) and not get_user_step(event.sender_id))

async def filter_add_admin(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.ADD_ADMIN and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_del_admin(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.DELETE_ADMIN and 
        await user_is_admin(event.sender_id)
    )

async def filter_set_rule(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.CHANGE_RULES_TEXT and 
        await user_is_admin(event.sender_id)
    )

async def filter_set_help(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.CHANGE_HELP_TEXT and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_set_support_channel(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.CHANGE_SUPPORT_CHANNEL and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_set_referral_bonus(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.CHANGE_REFERRAL_BONUS and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_set_entry_prize(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.CHANGE_ENTERY_PRIZE and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_add_channel(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.ADD_CHANNEL and 
        await user_is_admin(event.sender_id)
    )    

async def filter_get_message_send_users(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.SEND_TO_USERS and 
        await user_is_admin(event.sender_id)
    )

async def filter_get_user_send(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.SEND_TO_USER and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_get_message_send_user(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.GET_MESSAGE_SEND_TO_USER and 
        await user_is_admin(event.sender_id)
    )

async def filter_ban_user(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.BAN_USER and 
        await user_is_admin(event.sender_id)
    )

async def filter_unban_user(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.UNBAN_USER and 
        await user_is_admin(event.sender_id)
    )
    
async def filter_user_info(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.SHOW_USER_INFO and 
        await user_is_admin(event.sender_id)
    )

async def filter_(event) -> bool:
    return bool(
        get_user_step(event.sender_id).step == Parts.DELETE_ADMIN and 
        await user_is_admin(event.sender_id)
    )



# endregion