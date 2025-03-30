import os
import logging
from handlers import client
from models import default_data, create_table

def main():

    logging.basicConfig(filename="log.txt", filemode="a",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

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
