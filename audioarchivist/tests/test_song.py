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
        self.assertIsNone(song.pathFromRoot)
        self.assertTrue(song.stemAligned)
        self.assertTrue(song.exists)

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
        song = Song(filename, byName = True)
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

    def test_songs(self):
        for meta in [
            {
                "filename"  : "prototypes/Test000 - prototypes - Purpley.mp3",
                "album"     : "prototypes",
                "samplerate"  : 44100
            },
            {
                "filename"  : "prototypes/invalid/ID3 With Header With A Zero Byte - Purpley - prototypes.wav",
                "title"     : "Test000",
                "duration"  : 1,
                # Support for this not yet in release of TinyTag, so won't pass in CI
                "enabled"   : False
            },

        ]:
            if "enabled" not in meta or meta["enabled"]:
                song = Song(storage.filename(meta["filename"]))
                if "title" in meta:
                    self.assertEqual(song.title, meta["title"])
                if "album" in meta:
                    self.assertEqual(song.album, meta["album"])
                if "duration" in meta:
                    self.assertEqual(song.duration, meta["duration"])
                if "samplerate" in meta:
                    self.assertEqual(song.samplerate, meta["samplerate"])

    def test_song_not_exists(self):
        song = Song(storage.filename("not-exists.wav"))
        self.assertFalse(song.exists)

    def test_song_naming(self):
        storage.tmp("meta-naming-artist-and-title", "meta/test/naming-title-and-artist/.ameta.yaml")
        song = Song(storage.tmpFilename("meta/test/naming-title-and-artist/my title - my artist.wav"))
        self.assertEquals(song.artist, "my artist")
        storage.tmp("meta-empty", "meta/test/naming-default/.ameta.yaml")
        song = Song(storage.tmpFilename("meta/test/naming-default/my title - my album - my artist.wav"))
        self.assertEquals(song.artist, "my artist")
