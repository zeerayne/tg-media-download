import pytest
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterMusic, InputMessagesFilterPhotos

from dwnld import MediaTypeChoices, get_media_filter


def test_get_media_filter_maps_media_types():
    assert get_media_filter(MediaTypeChoices.ALL.value) is InputMessagesFilterDocument
    assert get_media_filter(MediaTypeChoices.AUDIO.value) is InputMessagesFilterMusic
    assert get_media_filter(MediaTypeChoices.PHOTO.value) is InputMessagesFilterPhotos


def test_get_media_filter_rejects_unknown_media_type():
    with pytest.raises(ValueError, match="Unsupported media type"):
        get_media_filter("video")
