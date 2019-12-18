import argparse
import asyncio
import os
import progressbar
from enum import Enum
from telethon import TelegramClient
from telethon.tl.types import (
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
    InputMessagesFilterDocument
)
from telethon import errors


class MediaTypeChoices(Enum):
    ALL = 'all'
    AUDIO = 'audio'
    PHOTO = 'photo'


async def download_entity_media(client, entity, media_type, output_dir, overwrite=False):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    entity = await client.get_entity(entity)
    if media_type == MediaTypeChoices.ALL.value:
        filter=InputMessagesFilterDocument
    if media_type == MediaTypeChoices.AUDIO.value:
        filter=InputMessagesFilterMusic
    if media_type == MediaTypeChoices.PHOTO.value:
        filter = InputMessagesFilterPhotos
    messages = await client.get_messages(entity, limit=None, filter=filter)
    for msg in progressbar.progressbar(messages):
        while True:
            try:
                filename = os.path.join(output_dir, msg.file.name)
                if not overwrite and os.path.exists(filename):
                    break
                await msg.download_media(file=filename)
            except errors.FloodError as e:
                delay = [int(s) for s in e.message.split() if s.isdigit()][0]
                await asyncio.sleep(delay)
            else:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads media of specified type from telegram entity.')
    parser.add_argument('-p', '--phone', help='Phone number to authorize')
    parser.add_argument('-P', '--password', help='If account is 2FA-enabled, password should be provided')
    parser.add_argument('-e', '--entity', help='Telegram entity (chat or channel) which media should be downloaded')
    parser.add_argument(
        '-t', '--type',
        choices=[m.value for m in MediaTypeChoices],
        default=MediaTypeChoices.ALL,
        help='Media type'
    )
    parser.add_argument('-i', '--id', help='Telegram api_id')
    parser.add_argument('-x', '--hash', help='Telegram api_hash')
    parser.add_argument('-o', '--output_dir', default='./downloads', help='Directory to store downloaded files')
    parser.add_argument('-O', '--overwrite', action='store_true', help='Specifies whether will be files overwritten or skipped')

    args = parser.parse_args()

    api_id, api_hash = args.id, args.hash
    phone_number, password = args.phone, args.password
    client = TelegramClient(
            'telethon',
            api_id,
            api_hash,
    )
    with client.start(phone=phone_number, password=password) as client:
        client.loop.run_until_complete(
            download_entity_media(
                client=client,
                entity=args.entity,
                media_type=args.type,
                output_dir=args.output_dir,
                overwrite=args.overwrite,
            )
        )
