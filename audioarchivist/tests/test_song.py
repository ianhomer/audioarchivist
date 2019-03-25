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
        self.assertTrue(song.stemAligned)

    def test_song_from_nometa(self):
        song = Song(testDirectory + "/storage/nometa/samples/Test001 - samples - Purpley.mp3")
        self.assertEqual(song.album, "samples")
        self.assertEqual(song.artist, "Purpley")
        self.assertEqual(song.title, "Test001")
        self.assertTrue(song.stemAligned)

    def test_song_title_misaligned(self):
        # when load with out naming flag
        song = Song(testDirectory + "/storage/nometa/samples/Test002 (Title Misaligned) - samples - Purpley.mp3")
        # then title comes from file meta data
        self.assertEqual(song.title, "Test001")
        self.assertEqual(song.album, "samples")
        self.assertEqual(song.artist, "Purpley")
        # and stem is misaligned
        self.assertFalse(song.stemAligned)
        self.assertEqual(song.alt['title'], "Test002 (Title Misaligned)")
        # when load with naming flag
        song = Song(testDirectory + "/storage/nometa/samples/Test002 (Title Misaligned) - samples - Purpley.mp3", True)
        # then title comes from file name
        self.assertEqual(song.title, "Test002 (Title Misaligned)")
