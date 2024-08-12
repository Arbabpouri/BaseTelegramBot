from sys import argv
from telethon.events import NewMessage, CallbackQuery
from modules import NewMessageHandlers, CallBackQueryHandlers, client, NewMessageGetInformationsHandlers
from sqlalchemy import exc
from modules.handlers.rules import *
from modules.database import defult_data, create_table

def main():
    
    client.add_event_handler(callback=NewMessageHandlers.cancel, event=NewMessage())
    client.add_event_handler(callback=NewMessageGetInformationsHandlers.user, event=NewMessage(func=get_informations_user))
    client.add_event_handler(callback=NewMessageGetInformationsHandlers.admin, event=NewMessage(func=get_informations_admin))
    client.add_event_handler(callback=NewMessageHandlers.user, event=NewMessage(func=user_move_text))
    client.add_event_handler(callback=NewMessageHandlers.admin, event=NewMessage(func=admin_move_text))
    client.add_event_handler(callback=CallBackQueryHandlers.user, event=CallbackQuery(func=user_move_inline))
    client.add_event_handler(callback=CallBackQueryHandlers.admin, event=CallbackQuery(func=admin_move_inline))

    print("Bot Runned")
    client.run_until_disconnected()


if __name__ == '__main__':

    if len(argv) > 1:
        
        if argv[1] == "create-table":
            create_table()

        elif argv[1] == "defult-data":
            defult_data()

        else:
            print(
                "error in send arg , args must be : \n"
                "\t 1 - \"run-bot\" : for running,\n"
                "\t 2 - \"create-table\" : for create database table\n"
                "\t 3 - \"defult-data\" : for add defult data to database\n"
            )

    else:
        try:
            main()
        except exc.TimeoutError:
            exit(1)
        # run bot

