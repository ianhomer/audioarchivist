from pathlib import Path
from unittest import TestCase

from audioarchivist.meta import Meta
from audioarchivist.tests.storage import Storage

storage = Storage()

class TestSongMeta(TestCase):
    def test_song_meta(self):
        filename = storage.tmp("meta-artist", "meta/test/meta-meta/collection/my-album/.ameta.yaml")
        storage.tmp("meta-artist-other", "meta/test/meta-meta/collection/.ameta.yaml")
        # when access meta of file
        meta = Meta(filename)
        self.assertEqual("meta-artist", meta.data["song"]["artist"])
        self.assertEqual("meta-artist", meta.song.artist)
        # when access meta of folder
        meta = Meta(storage.tmpFilename("meta/test/meta-meta/collection/my-album"))
        self.assertEqual("meta-artist", meta.data["song"]["artist"])
        self.assertEqual("meta-artist", meta.song.artist)
