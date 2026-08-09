import argparse
import asyncio
import os
from enum import Enum

import progressbar
from telethon import TelegramClient, errors
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
)


class MediaTypeChoices(Enum):
    ALL = "all"
    AUDIO = "audio"
    PHOTO = "photo"


def get_media_filter(media_type):
    if media_type == MediaTypeChoices.ALL.value:
        return InputMessagesFilterDocument
    if media_type == MediaTypeChoices.AUDIO.value:
        return InputMessagesFilterMusic
    if media_type == MediaTypeChoices.PHOTO.value:
        return InputMessagesFilterPhotos
    raise ValueError(f"Unsupported media type: {media_type}")


async def download_entity_media(client, entity, media_type, output_dir, overwrite=False):
    os.makedirs(output_dir, exist_ok=True)
    entity = await client.get_entity(entity)
    message_filter = get_media_filter(media_type)
    messages = await client.get_messages(entity, limit=None, filter=message_filter)

    for msg in progressbar.progressbar(messages):
        if msg.file is None:
            continue

        while True:
            try:
                file_name = getattr(msg.file, "name", None) or f"{msg.id}.bin"
                filename = os.path.join(output_dir, file_name)
                if not overwrite and os.path.exists(filename):
                    break
                await msg.download_media(file=filename)
            except errors.FloodError as e:
                wait_seconds = next(
                    (int(part) for part in str(e).split() if part.isdigit()),
                    None,
                )
                if wait_seconds is None:
                    raise
                await asyncio.sleep(wait_seconds)
            else:
                break


def build_parser():
    parser = argparse.ArgumentParser(description="Downloads media of specified type from telegram entity.")
    parser.add_argument("-p", "--phone", help="Phone number to authorize")
    parser.add_argument("-P", "--password", help="If account is 2FA-enabled, password should be provided")
    parser.add_argument("-e", "--entity", help="Telegram entity (chat or channel) which media should be downloaded")
    parser.add_argument(
        "-t",
        "--type",
        choices=[m.value for m in MediaTypeChoices],
        default=MediaTypeChoices.ALL.value,
        help="Media type",
    )
    parser.add_argument("-i", "--id", help="Telegram api_id")
    parser.add_argument("-x", "--hash", help="Telegram api_hash")
    parser.add_argument("-o", "--output_dir", default="./downloads", help="Directory to store downloaded files")
    parser.add_argument(
        "-O", "--overwrite", action="store_true", help="Specifies whether will be files overwritten or skipped"
    )
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    client = TelegramClient("telethon", args.id, args.hash)
    with client.start(phone=args.phone, password=args.password) as client:
        client.loop.run_until_complete(
            download_entity_media(
                client=client,
                entity=args.entity,
                media_type=args.type,
                output_dir=args.output_dir,
                overwrite=args.overwrite,
            )
        )
