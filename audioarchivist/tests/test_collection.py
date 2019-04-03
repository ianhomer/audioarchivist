from pathlib import Path
from unittest import TestCase

from audioarchivist.collection import Collection
from storage import Storage

storage = Storage()

class TestCollection(TestCase):
    def test_song_ameta(self):
        filename = storage.tmp("meta-artist", "meta/test/meta/.ameta.yaml")
        Collection("meta").process()
