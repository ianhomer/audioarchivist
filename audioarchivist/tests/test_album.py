from pathlib import Path
from unittest import TestCase

import audioarchivist.logger
from audioarchivist.album import Album
from audioarchivist.album import AlbumPath
from audioarchivist.tests.storage import Storage

storage = Storage()
def tmpFilename(filename):
    return storage.tmpFilename(filename)

class TestSongAlbum(TestCase):
    def test_album(self):
        storage.tmp("meta-artist", "meta/album-master/my-album/.ameta.yaml")
        filename = storage.tmp("mp3", "meta/album-master/my-album/Test000.mp3")
        filename = storage.tmp("mp3", "meta/album-master/my-album/Test001.mp3")
        filename = storage.tmp("mp3", "meta/album-master/my-album/my-child-1/Test002.mp3")
        filename = storage.tmp("mp3", "meta/album-master/my-album/my-child-1/Test003.mp3")
        filename = storage.tmp("mp3", "meta/album-master/my-album/my-child-2/Test004.mp3")
        filename = storage.tmp("mp3", "meta/album-master/my-album/my-child-2/my-grandchild-1/Test005.mp3")
        filename = storage.tmp("mp3", "meta/album-release/my-album/Test006.mp3")
        filename = storage.tmp("mp3", "meta/album-release/my-album/my-child-3/Test007.mp3")

        album = Album(storage.tmpFilename("meta/album-master/my-album"))
        self.assertEqual(album.artist, "meta-artist")
        self.assertEqual(album.name, "my-album")
        self.assertEqual(album.collectionName, "album-master")
        self.assertEqual(len(album.children), 3)
        self.assertEqual(len(album.songFileNames), 2)
        self.assertEqual(len(album.songs), 2)

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
        self.assertEqual(album.collectionName,"album-master")
        self.assertEqual(album.pathFromRoot,"album-master/my-album")

        filename = storage.tmpFilename("meta/album-master/my-album/my-song.wav")
        self.assertEqual(album.path.relativeToRoot(filename), "album-master/my-album")
        self.assertEqual(album.path.relativeToCollection(filename), "my-album")

    def test_paths_no_root(self):
        albumPath = AlbumPath(storage.tmpFilename("no-meta/album-master/my-album"))
        filename = storage.tmpFilename("no-meta/album-master/my-album/my-song.wav")
        self.assertIsNone(albumPath.relativeToRoot("album-master/my-album"))
        self.assertIsNone(albumPath.relativeToCollection("album-master/my-album"))
        self.assertIsNone(albumPath.collectionName)
        self.assertIsNone(albumPath.pathFromRoot)

    def test_paths_on_root(self):
        root = storage.tmpFilename("no-meta")
        albumPath = AlbumPath(storage.tmpFilename("no-meta/album-master/my-album"), root)
        for tuple in [
            [tmpFilename("no-meta/album-master/my-album-1/my-song.wav"),"album-master/my-album-1","my-album-1","album-master"],
            [tmpFilename("no-meta/album-master/my-album-2/"),"album-master/my-album-2","my-album-2","album-master"],
            [tmpFilename("no-meta/album-master/my-album-3/."),"album-master/my-album-3","my-album-3","album-master"],
            [tmpFilename("no-meta/album-master/my-album-4"),"album-master/my-album-4","my-album-4","album-master"],
            [tmpFilename("no-meta/album-master"),"album-master",None,"album-master"],
            ["audioarchivist/tests/tmp/no-meta/album-master/my-album-5","album-master/my-album-5","my-album-5","album-master"],
            ["audioarchivist/tests/tmp/no-meta/album-master","album-master",None,"album-master"]

        ]:
            self.assertEqual(albumPath.relativeToRoot(tuple[0]), tuple[1])
            self.assertEqual(albumPath.relativeToCollection(tuple[0]), tuple[2])
            self.assertEqual(albumPath.collectionName, tuple[3])

    def test_album_path_collections(self):
        files = [
            "meta-album-path-collections/collection-1/my-album-1/Test000.mp3",
            "meta-album-path-collections/collection-1/my-album-1/Test001.mp3",
            "meta-album-path-collections/collection-2/my-album-1/Test002.mp3",
            "meta-album-path-collections/collection-3/my-album-1/Test003.mp3",
            "meta-album-path-collections/collection-4/my-album-2/Test004.mp3",
        ]
        for filename in files:
            storage.tmp("mp3", filename)
        album = Album(storage.tmpFilename("meta-album-path-collections"))
        self.assertEqual(len(album.collections), 4)
        album = Album(storage.tmpFilename("meta-album-path-collections/collection-1/my-album-1"))
        self.assertEqual(len(album.collections), 3)
        self.assertEqual(len(album.alternatives), 3)

        album = Album(storage.tmpFilename("meta-album-path-collections/collection-1"))
        self.assertEqual(len(album.collections), 4)
        child = next(a for a in album.children if a.name == "my-album-1")
        self.assertEqual(len(child.collections), 3)


        for filename in files:
            storage.tmpRemove(filename)
