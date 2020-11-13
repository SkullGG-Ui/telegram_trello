import time
from telethon import TelegramClient, events

from trello_client import TrelloClient
from settings import *

from datetime import datetime, timedelta

import logging
logging.basicConfig(filename='logs.log',level=logging.DEBUG)
logging.getLogger('telethon').setLevel(level=logging.WARNING)

    

telegram_cli = TelegramClient(USERNAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
logging.info('Initialized Telegram Client')
logging.info({
    'Username': USERNAME,
    'ApiID': TELEGRAM_API_ID,
    'ApiHash': TELEGRAM_API_HASH
})
trello_cli = TrelloClient(TRELLO_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID, TRELLO_LIST_ID)
logging.info("Initialized Trello Client")
logging.info({
    'ApiKey': TRELLO_KEY,
    'ApiToken': TRELLO_TOKEN,
    'BoardID': TRELLO_BOARD_ID,
    'ListID': TRELLO_LIST_ID
})

def get_next_day():
    today = datetime.now()
    next_day = today + timedelta(days=1)
    return next_day.strftime('%m/%d/%Y')


@telegram_cli.on(events.NewMessage)
async def my_event_handler(event):
    if event.to_id.channel_id in DIALOGS_LIST:
        logging.info('New Message from channel {}'.format(event.to_id.channel_id))
        description = ''
        try: 
            if event.message.from_id:
                sender_entity = await telegram_cli.get_entity(event.message.from_id)
                description = 'Заявка від користувача: {} {} з нікнеймом {}'.format(sender_entity.first_name, 
                                                                    sender_entity.last_name,
                                                                    sender_entity.username)
        except Exception as e:
            logging.error(e)
            logging.error(event)
        if event.media:
            image = await telegram_cli.download_media(event.message, file=MEDIA_FOLDER)
            trello_cli.create_card(event.raw_text, get_next_day(), description, image)
            logging.info('Created card with image {}'.format(image))
        else:    
             trello_cli.create_card(event.raw_text, get_next_day(), description)
             logging.info('Created card with text.')

telegram_cli.start()
logging.info('Started telegram client')
telegram_cli.run_until_disconnected()