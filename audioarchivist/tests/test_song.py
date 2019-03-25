import os

from unittest import TestCase

from audioarchivist.song import Song

testDirectory = os.path.join(os.path.dirname(__file__))

class TestSong(TestCase):
    def test_create(self):
        song = Song(testDirectory + "/storage/audio/test/My Album/Rhodes - My Album - Purpley.wav")
        self.assertEqual(song.album, "My Album")
