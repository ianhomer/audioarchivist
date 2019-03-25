from unittest import TestCase

from audioarchivist.song import Song
from storage import Storage

storage = Storage()

class TestSong(TestCase):
    def test_song_from_collections(self):
        song = Song(storage.filename("collections/samples/My Album/Sound - My Album - Purpley.wav"))
        self.assertEqual(song.album, "My Album")
        self.assertEqual(song.artist, "Purpley")
        self.assertEqual(song.title, "Sound")
        self.assertTrue(song.stemAligned)

    def test_prototypes_song(self):
        song = Song(storage.filename("prototypes/Test000 - prototypes - Purpley.mp3"))
        self.assertEqual(song.album, "prototypes")
        self.assertEqual(song.artist, "Purpley")
        self.assertEqual(song.title, "Test000")
        self.assertTrue(song.stemAligned)

    def test_song_title_misaligned(self):
        filename = storage.tmp("mp3", "nometa/samples/Title Misaligned - prototypes - Purpley.mp3")

        # when load with out naming flag
        song = Song(filename)

        # then title comes from file meta data
        self.assertEqual(song.title, "Test000")
        self.assertEqual(song.album, "prototypes")
        self.assertEqual(song.artist, "Purpley")
        # and stem is misaligned
        self.assertFalse(song.stemAligned)
        self.assertEqual(song.alt['title'], "Title Misaligned")
        # when load with naming flag
        song = Song(filename, True)
        # then title comes from file name
        self.assertEqual(song.title, "Title Misaligned")

    def test_song_mp3_save(self):
        filename = storage.tmp("mp3", "nometa/samples/New Title - prototypes - Purpley.mp3")
        song = Song(filename)
        self.assertEqual(song.title, "Test000")
        song.title = "New Title"
        song.save()
        song = Song(filename)
        self.assertEqual(song.title, "New Title")
