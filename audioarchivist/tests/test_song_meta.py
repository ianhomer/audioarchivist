from pathlib import Path
from unittest import TestCase

from audioarchivist.song import Song
from storage import Storage

storage = Storage()

class TestSongMeta(TestCase):
    def test_song_meta(self):
        storage.tmp("meta-artist", "meta/test/meta/.ameta.yaml")
        filename = storage.tmp("mp3", "meta/test/meta/meta.mp3")
        song = Song(filename)
        self.assertEqual("Purpley", song.artist)
        song = Song(filename, True)
        self.assertEqual("meta-artist", song.artist)
