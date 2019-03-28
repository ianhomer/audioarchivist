from pathlib import Path
from unittest import TestCase

from audioarchivist.meta import Meta
from storage import Storage

storage = Storage()

class TestSongMeta(TestCase):
    def test_song_meta(self):
        filename = storage.tmp("meta-artist", "meta/test/meta/.ameta.yaml")
        meta = Meta(filename)
        self.assertEqual("meta-artist", meta.data["song"]["artist"])
        self.assertEqual("meta-artist", meta.song.artist)
