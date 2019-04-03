from pathlib import Path
from unittest import TestCase

from audioarchivist.collection import Collection
from storage import Storage

storage = Storage()

class TestCollection(TestCase):
    def test_song_collection(self):
        filename = storage.tmp("mp3", "collection/samples/test-1.mp3")
        filename = storage.tmp("mp3", "collection/samples/test-2.mp3")
        response = Collection(storage.tmpFilename("collection")).process()
        self.assertEqual(response.count, 2)
