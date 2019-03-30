from pathlib import Path
from unittest import TestCase


import audioarchivist.logger
from audioarchivist.album import Album
from storage import Storage

storage = Storage()

class TestSongAlbum(TestCase):
    def test_album(self):
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

    def test_paths(self):
        storage.tmp("meta-artist", "meta/album-master/my-album/.ameta.yaml")
        album = Album(storage.tmpFilename("meta/album-master/my-album"))
        filename = storage.tmpFilename("meta/album-master/my-album/my-song.wav")
        self.assertEqual(album.getPathFromRoot(filename), "album-master/my-album")

    def test_paths_no_meta(self):
        storage.createTmpDirectory("no-meta/album-master/my-album")
        album = Album(storage.tmpFilename("no-meta/album-master/my-album"))
        filename = storage.tmpFilename("no-meta/album-master/my-album/my-song.wav")
        self.assertIsNone(album.getPathFromRoot("album-master/my-album"))
