from pydantic import BaseModel
from typing import Any
import redis


class Permission(BaseModel):
    PART: int
    USER_ID: int | None = None
    EVENT: Any | None = None
    AMOUNT: int | None = None
    WITHDRAW_CODE: str | None = None


class Parts:
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
    FORWARD_TO_USER = 18
    FORWARD_TO_USERS = 19
    CHANGE_START_MENU = 20
    CHANGE_MESSAGE_TO_SUPPORT = 21
    INCREASE_USER_BALANCE = 22
    REDUCE_USER_BALANCE = 23
    GET_USER_FOR_REDUCE_BALANCE = 24
    GET_USER_FOR_INCREASE_BALANCE = 25
    GET_NUMBER_FOR_DEPOSIT_CARD = 26
    GET_FACTOR_FOR_DEPOSIT_CARD = 27
    CHANGE_CARD_INFO = 28
    

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)


class UserStep(BaseModel):
    step: int
    user_geted: int | None = None
    number_geted: int | float | None = None


def set_step(user_id: int, step: int, user_geted: int | None = None, number_geted: int | float | None = None) -> None:
    data = {
        'step': step,
    }
    if user_geted:
        data['user_geted'] = user_geted
    
    if number_geted:
        data['number_geted'] = number_geted

    redis_client.hset(user_id, mapping=data)


def delete_step(user_id: int) -> None:
    redis_client.delete(user_id)


def get_user_step(user_id: int) -> UserStep | None:
    if data := redis_client.hgetall(user_id):
        data = {key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()}
        return UserStep(**data)
    return None
