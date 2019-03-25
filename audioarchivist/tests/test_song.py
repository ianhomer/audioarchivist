from unittest import TestCase

from audioarchivist.song import Song
from audioarchivist.tests.storage import Storage

storage = Storage()

class TestSong(TestCase):
    def test_song_from_collections(self):
        song = Song(storage.getFilename("collections/samples/My Album/Sound - My Album - Purpley.wav"))
        self.assertEqual(song.album, "My Album")
        self.assertEqual(song.artist, "Purpley")
        self.assertEqual(song.title, "Sound")
        self.assertTrue(song.stemAligned)

    def test_prototypes_song(self):
        song = Song(storage.getFilename("prototypes/Test000 - prototypes - Purpley.mp3"))
        self.assertEqual(song.album, "prototypes")
        self.assertEqual(song.artist, "Purpley")
        self.assertEqual(song.title, "Test000")
        self.assertTrue(song.stemAligned)

    def test_song_title_misaligned(self):
        filename = storage.createTmp("mp3", "nometa/samples/Test002 (Title Misaligned) - prototypes - Purpley.mp3")

        # when load with out naming flag
        song = Song(filename)
        # then title comes from file meta data
        self.assertEqual(song.title, "Test000")
        self.assertEqual(song.album, "prototypes")
        self.assertEqual(song.artist, "Purpley")
        # and stem is misaligned
        self.assertFalse(song.stemAligned)
        self.assertEqual(song.alt['title'], "Test002 (Title Misaligned)")
        # when load with naming flag
        song = Song(filename, True)
        # then title comes from file name
        self.assertEqual(song.title, "Test002 (Title Misaligned)")
