from unittest import TestCase

from audioarchivist.format import Format
from storage import Storage

storage = Storage()

class TestStorage(TestCase):
    def test_tmp(self):
        filename = storage.tmpFilename("no-meta/my-song.wav")
