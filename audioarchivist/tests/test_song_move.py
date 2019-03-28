from pathlib import Path
from unittest import TestCase

from audioarchivist.song import Song
from storage import Storage

storage = Storage()

class TestSongMove(TestCase):
    def test_song_move(self):
        relativeFilename = "samples/Move - samples - Purpley.mp3"
        filename = storage.tmp("mp3", "meta/samples/" + relativeFilename)
        song = Song(filename)
        song.move("share")
        destination = Path(storage.tmpFilename("meta/share/" + relativeFilename))
        self.assertTrue(destination.exists())
        destination.unlink()
