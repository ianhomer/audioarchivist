from pathlib import Path
from unittest import TestCase

from audioarchivist.song import Song
from audioarchivist.tests.storage import Storage

storage = Storage()

class TestSongMeta(TestCase):
    def test_song_meta(self):
        storage.tmp("meta-artist", "meta/test/meta/.ameta.yaml")
        filename = storage.tmp("mp3", "meta/test/meta/Test000.mp3")
        song = Song(filename)
        self.assertEqual("Purpley", song.artist)

        # When load by name
        song = Song(filename, byName = True)
        self.assertEqual("meta-artist", song.artist)
        self.assertEqual(True, song.albumObject.byName)
