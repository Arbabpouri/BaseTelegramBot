import os
from telethon.events import NewMessage, CallbackQuery
from modules import NewMessageHandlers, CallBackQueryHandlers, client, NewMessageGetInformationsHandlers
import logging
from modules.handlers.rules import *
from modules.database import default_data, create_table

def main():

    logging.basicConfig(filename="log.txt", filemode="a",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    client.add_event_handler(callback=NewMessageHandlers.cancel, event=NewMessage())
    client.add_event_handler(callback=NewMessageGetInformationsHandlers.user, event=NewMessage(func=get_informations_user))
    client.add_event_handler(callback=NewMessageGetInformationsHandlers.admin, event=NewMessage(func=get_informations_admin))
    client.add_event_handler(callback=NewMessageHandlers.user, event=NewMessage(func=user_move_text))
    client.add_event_handler(callback=NewMessageHandlers.admin, event=NewMessage(func=admin_move_text))
    client.add_event_handler(callback=CallBackQueryHandlers.user, event=CallbackQuery(func=user_move_inline))
    client.add_event_handler(callback=CallBackQueryHandlers.admin, event=CallbackQuery(func=admin_move_inline))

    print("Bot Runned")
    client.run_until_disconnected()


def check_db() -> None:

    if os.path.exists('database.db'):
        create_table()
        default_data()

if __name__ == '__main__':

    try:
        check_db()
        main()
    except Exception as e:
        print("Error in run boot :", e)
