import os
import logging
from handlers import client


def main():

    logging.basicConfig(filename="log.txt", filemode="a",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("Bot Runned")
    client.run_until_disconnected()


def check_db() -> None:

    if not os.path.exists('database.db'):
        print('database not found')
        from settings.database import Base, engine
        # from models.channel_model import ChannelModel
        # from models.config_model import ConfigsModel
        # from models.user_model import UserModel
        Base.metadata.create_all(bind=engine)
        # exit(1)

if __name__ == '__main__':

    try:
        check_db()
        main()
    except Exception as e:
        print("Error in run boot :", e)
