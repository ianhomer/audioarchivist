from pathlib import Path
from unittest import TestCase

from audioarchivist.collection import Collection, CollectionStatistics
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
        statistics = Collection(storage.tmpFilename("collection")).process({
            "album" : lambda s, statistics : statistics.incrementAlbum(),
            "song"  : lambda s, statistics : statistics.storeSong(s),
        }, state = CollectionStatistics())
        self.assertEqual(statistics.songCount, 3)
        self.assertEqual(statistics.albumCount, 2)

        self.assertEqual("|".join(statistics.songs).replace(" ", ""),
            "Test000:None:mp3:32::4:1:Purpley:Test000:prototypes|" +
            "Test000:None:mp3:32::4:1:Purpley:Test000:prototypes|" +
            "Test000:None:mp3:32::4:1:Purpley:Test000:prototypes"
        )

        statistics = Collection(storage.tmpFilename("collection")).process({
            "album" : lambda s, statistics : statistics.incrementAlbum(),
            "song"  : lambda s, statistics : statistics.storeSong(s),
        }, state = CollectionStatistics(), args = MockArgs(True) )

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
