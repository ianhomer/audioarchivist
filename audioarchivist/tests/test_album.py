from pathlib import Path
from unittest import TestCase


import audioarchivist.logger
from audioarchivist.album import Album
from audioarchivist.album import AlbumPath
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

    def test_album_not_exists(self):
        exception = False
        try:
            album = Album(storage.tmpFilename("meta/album-master/no-album"))
        except:
            exception = True
        self.assertTrue(exception)

    def test_paths(self):
        storage.tmp("meta-artist", "meta/album-master/my-album/.ameta.yaml")
        album = Album(storage.tmpFilename("meta/album-master/my-album"))
        filename = storage.tmpFilename("meta/album-master/my-album/my-song.wav")
        self.assertEqual(album.path.relativeToRoot(filename), "album-master/my-album")
        self.assertEqual(album.path.relativeToCollection(filename), "my-album")

    def test_paths_no_root(self):
        albumPath = AlbumPath(storage.tmpFilename("no-meta/album-master/my-album"))
        filename = storage.tmpFilename("no-meta/album-master/my-album/my-song.wav")
        self.assertIsNone(albumPath.relativeToRoot("album-master/my-album"))
        self.assertIsNone(albumPath.relativeToCollection("album-master/my-album"))

    def test_paths_on_root(self):
        root = storage.tmpFilename("no-meta")
        albumPath = AlbumPath(storage.tmpFilename("no-meta/album-master/my-album"), root)
        for tuple in [
            ["no-meta/album-master/my-album-1/my-song.wav","album-master/my-album-1","my-album-1"],
            ["no-meta/album-master/my-album-2/","album-master/my-album-2","my-album-2"],
            ["no-meta/album-master/my-album-3/.","album-master/my-album-3","my-album-3"],
            ["no-meta/album-master/my-album-4","album-master/my-album-4","my-album-4"],
            ["no-meta/album-master","album-master",None]
        ]:
            filename = storage.tmpFilename(tuple[0])
            self.assertEqual(albumPath.relativeToRoot(filename), tuple[1])
            self.assertEqual(albumPath.relativeToCollection(filename), tuple[2])
