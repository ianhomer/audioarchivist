import argparse
from pathlib import Path
from unittest import TestCase, mock

from storage import Storage
from audioarchivist.ameta import run

storage = Storage()

class TestAMeta(TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
        return_value=argparse.Namespace(
            byname=False, albumsonly=False, save=False, rename=False,
            root=['audioarchivist/tests/tmp/meta-ameta']))
    def test_song_collection(self, mock_args):
        for filename in [ "meta-ameta/collection-1/samples-1/test 1.mp3",   "meta-ameta/collection-1/samples-1/test 2.mp3"]:
            storage.tmp("mp3", filename)
        songCount = run()
        self.assertEqual(2, songCount)
