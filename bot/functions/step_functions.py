from pydantic import BaseModel
from enum import unique, IntEnum
from typing import Any
import redis


class Permission(BaseModel):
    PART: int
    USER_ID: int | None = None
    EVENT: Any | None = None
    AMOUNT: int | None = None
    WITHDRAW_CODE: str | None = None


@unique
class Parts(IntEnum):
    ADD_ADMIN = 0
    DELETE_ADMIN = 1
    SHOW_ADMINS = 2
    ADD_CHANNEL = 3
    DELETE_CHANNEL = 4
    SHOW_CHANNELS = 5
    SEND_TO_USER = 6
    SEND_TO_USERS = 7
    BAN_USER = 8
    UNBAN_USER = 9
    SHOW_USER_INFO = 10
    CHANGE_RULES_TEXT = 11
    CHANGE_HELP_TEXT = 12
    CHANGE_ENTERY_PRIZE = 13
    CHANGE_SUPPORT_CHANNEL = 14
    CHANGE_REFERRAL_BONUS = 15
    GET_MESSAGE = 16
    GET_MESSAGE_SEND_TO_USER = 17

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)


class UserStep(BaseModel):
    step: Parts | int
    user_geted: int | None = None


def set_step(user_id: int, step: Parts | int, user_geted: int | None = None) -> None:
    data = {
        'step': step,
    }
    if user_geted:
        data['user_geted': user_geted]
    redis_client.hmset(user_id, data)


def delete_step(user_id: int) -> None:
    redis_client.delete(user_id)


def get_user_step(user_id: int) -> UserStep | None:
    if data := redis_client.hgetall(user_id):
        return UserStep(**data)
    return None
