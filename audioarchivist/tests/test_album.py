from pathlib import Path
from unittest import TestCase


import audioarchivist.logger
from audioarchivist.album import Album
from storage import Storage

storage = Storage()

class TestSongAlbum(TestCase):
    def test_album(self):
        audioarchivist.logger.DEBUG = True
        storage.tmp("meta-artist", "meta/album-master/my-album/.ameta.yaml")
        filename = storage.tmp("mp3", "meta/album-master/my-album/Test000.mp3")
        filename = storage.tmp("mp3", "meta/album-master/my-album/Test001.mp3")
        album = Album(storage.tmpFilename("meta/album-master/my-album"))
        self.assertEqual(album.artist, "meta-artist")
        self.assertEqual(album.name, "my-album")
        self.assertEqual(album.collectionName, "album-master")
        #self.assertEqual(len(album.songs), 2)

    def test_album_not_directory(self):
        storage.tmp("meta-artist", "meta/album-master/my-album/.ameta.yaml")
        exception = False
        try:
            album = Album(storage.tmpFilename("meta/album-master/my-album/.ameta.yaml"))
        except:
            exception = True
        self.assertTrue(exception)
