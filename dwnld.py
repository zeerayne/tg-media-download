import argparse
import socks
from telethon import TelegramClient, connection


async def download_entity_media(client, entity, media_type):
    entity = await client.get_entity(entity)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads media of specified type from telegram entity.')
    parser.add_argument('-e', '--entity', help='Telegram entity (chat or channel) which media should be downloaded')
    parser.add_argument('-t', '--type', choices=['all', 'audio', 'photo'], default='all', help='Media type')
    parser.add_argument('-i', '--id', help='Telegram api_id')
    parser.add_argument('-x', '--hash', help='Telegram api_hash')

    args = parser.parse_args()

    api_id, api_hash = args.id, args.hash
    with TelegramClient(
            'sessionfile',
            api_id,
            api_hash,
            proxy=proxy,
    ) as client:
        client.loop.run_until_complete(
            download_entity_media(
                client=client,
                entity=args.entity,
                media_type=args.type,
            )
        )
