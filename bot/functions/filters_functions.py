# region imports

from typing import Optional, List
from models import UserModel
from settings.database import SessionLocal
from functions.step_functions import get_user_step
# endregion

# region rules

def set_filter(
    event,
    is_private_chat: Optional[bool] = True,
    is_group_chat: Optional[bool] = False,
    is_channel_chat: Optional[bool] = False,
    is_admin: Optional[bool] = False,
    data_or_text: Optional[str] = None,
    startswith: Optional[str] = None,
    endswith: Optional[str] = None,
    user_step: Optional[int | List[int]] = None,
) -> bool:

    try:

        if (
            (is_private_chat and not event.is_private) or
            (is_group_chat and not event.is_group) or
            (is_channel_chat and not event.is_channel)
        ):
            return False
        
        if is_admin:
            with SessionLocal() as session:
                if not session.query(UserModel).filter_by(user_id=event.sender_id, is_admin=True).first():
                    return False
        
        if data_or_text:

            if startswith:
                if not data_or_text.startswith(startswith):
                    return False
            
            if endswith:
                if not data_or_text.endswith(startswith):
                    return False
        
        user_step_info = get_user_step(event.sender_id)

        if user_step is None:
            return not bool(user_step_info)
                
        else:

            if not isinstance(user_step, list):
                user_step = [user_step]

            if not user_step_info or user_step_info.step not in user_step:
                return False
            
        return True

    except Exception as e:
        print('error in filters :', e)
        return False

# endregion
