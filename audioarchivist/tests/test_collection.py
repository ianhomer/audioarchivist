from pathlib import Path
from unittest import TestCase

from audioarchivist.collection import Collection
from storage import Storage

storage = Storage()

class TestCollection(TestCase):
    def test_song_collection(self):
        filenames = [
            "collection/samples-1/test 1.mp3",
            "collection/samples-1/test 2.mp3",
            "collection/samples-2/test 3.mp3"
        ]

        for filename in filenames:
            storage.tmp("mp3", filename)

        statistics = CollectionStatistics()
        Collection(storage.tmpFilename("collection")).process({
            "album" : statistics.incrementAlbum,
            "song"  : statistics.storeSong,
        })
        self.assertEqual(statistics.songCount, 3)
        self.assertEqual(statistics.albumCount, 2)

        self.assertEqual("|".join(statistics.songs).replace(" ", ""),
            "Test000:None:mp3:32::4:1:Purpley:Test000:prototypes|" +
            "Test000:None:mp3:32::4:1:Purpley:Test000:prototypes|" +
            "Test000:None:mp3:32::4:1:Purpley:Test000:prototypes"
        )

        statistics = CollectionStatistics()
        Collection(storage.tmpFilename("collection")).process({
            "album" : statistics.incrementAlbum,
            "song"  : statistics.storeSong,
        }, args = MockArgs(True) )

        self.assertEqual("|".join(statistics.songs).replace(" ", ""),
            "test1:None:mp3:32::4:1:unknown:test1:samples-1|" +
            "test2:None:mp3:32::4:1:unknown:test2:samples-1|" +
            "test3:None:mp3:32::4:1:unknown:test3:samples-2"
        )

        for filename in filenames:
            storage.tmpRemove(filename)

class MockArgs:
    def __init__(self, byname):
        self.byname = byname

class CollectionStatistics:
    def __init__(self):
        self.albumCount = 0
        self.songCount = 0
        self.songs = []

    def incrementAlbum(self, album):
        self.albumCount += 1

    def incrementSong(self):
        self.songCount += 1

    def storeSong(self, song):
        self.incrementSong()
        self.songs.append(song)
