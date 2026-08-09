from pathlib import Path
from types import SimpleNamespace

import pytest
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterMusic, InputMessagesFilterPhotos

from dwnld import MediaTypeChoices, build_parser, download_entity_media, get_media_filter


class FakeMessage:
    def __init__(self, file_name=None, msg_id=1):
        self.id = msg_id
        self.file = None if file_name is None else SimpleNamespace(name=file_name)

    async def download_media(self, file):
        Path(file).write_bytes(b"downloaded")


class FakeClient:
    def __init__(self, messages):
        self.messages = messages
        self.entity = "chat-id"

    async def get_entity(self, entity):
        return entity

    async def get_messages(self, entity, limit=None, filter=None):
        return self.messages


def test_get_media_filter_maps_media_types():
    assert get_media_filter(MediaTypeChoices.ALL.value) is InputMessagesFilterDocument
    assert get_media_filter(MediaTypeChoices.AUDIO.value) is InputMessagesFilterMusic
    assert get_media_filter(MediaTypeChoices.PHOTO.value) is InputMessagesFilterPhotos


def test_get_media_filter_rejects_unknown_media_type():
    with pytest.raises(ValueError, match="Unsupported media type"):
        get_media_filter("video")


def test_build_parser_parses_cli_arguments():
    args = build_parser().parse_args(
        [
            "--id",
            "123",
            "--hash",
            "abc",
            "--phone",
            "+123456789",
            "--entity",
            "example_chat",
            "--type",
            "photo",
            "--output_dir",
            "/tmp/media",
            "--overwrite",
        ]
    )

    assert args.id == "123"
    assert args.hash == "abc"
    assert args.phone == "+123456789"
    assert args.entity == "example_chat"
    assert args.type == "photo"
    assert args.output_dir == "/tmp/media"
    assert args.overwrite is True


@pytest.mark.asyncio
async def test_download_entity_media_skips_messages_without_file_and_downloads_valid_one(tmp_path):
    messages = [
        FakeMessage(file_name=None, msg_id=1),
        FakeMessage(file_name="track.mp3", msg_id=2),
    ]
    client = FakeClient(messages)

    await download_entity_media(client, "chat-id", MediaTypeChoices.AUDIO.value, str(tmp_path))

    assert (tmp_path / "track.mp3").read_bytes() == b"downloaded"


@pytest.mark.asyncio
async def test_download_entity_media_does_not_overwrite_existing_files(tmp_path):
    target = tmp_path / "photo.jpg"
    target.write_bytes(b"existing")

    class ExistingFileMessage(FakeMessage):
        def __init__(self):
            super().__init__(file_name="photo.jpg", msg_id=3)

        async def download_media(self, file):
            raise AssertionError("download_media should not be called for existing files when overwrite is False")

    client = FakeClient([ExistingFileMessage()])

    await download_entity_media(client, "chat-id", MediaTypeChoices.PHOTO.value, str(tmp_path), overwrite=False)

    assert target.read_bytes() == b"existing"
