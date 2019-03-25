import os

from unittest import TestCase

from audioarchivist.song import Song

testDirectory = os.path.join(os.path.dirname(__file__))

class TestSong(TestCase):
    def test_song_from_collections(self):
        song = Song(testDirectory + "/storage/collections/samples/My Album/Sound - My Album - Purpley.wav")
        self.assertEqual(song.album, "My Album")
        self.assertEqual(song.artist, "Purpley")
        self.assertEqual(song.title, "Sound")

    def test_song_from_nometa(self):
        song = Song(testDirectory + "/storage/nometa/samples/Test001 - samples - Purpley.mp3")
        self.assertEqual(song.album, "samples")
        self.assertEqual(song.artist, "Purpley")
        self.assertEqual(song.title, "Test001")
