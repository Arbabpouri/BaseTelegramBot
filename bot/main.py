import os
import logging
from settings.database import default_data
from handlers import *

def main():

    logging.basicConfig(filename="log.log", filemode="a",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("Bot Runned")
    client.run_until_disconnected()


def check_db() -> None:

    if not os.path.exists('database.db'):
        print('database not found')
        exit(1)
    default_data()
        

if __name__ == '__main__':

    try:
        check_db()
        main()
    except Exception as e:
        print("Error in run bot :", e)
