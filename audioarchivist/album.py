from pathlib import Path

from .meta import Meta
from .coresong import CoreSong

AUDIO_EXTENSIONS = [".flac", ".m4a", ".mp3", ".ogg", ".wav"]

class Album:
    def __init__(self, directoryName, byName = False):
        if not Path(directoryName).is_dir():
            raise Exception(f"Cannot create album from {directoryName} since not a directory")

        self.directoryName = directoryName
        self.byName = byName
        self.meta = Meta(directoryName)
        self.artist = self.meta.song.artist if self.meta.song is not None and hasattr(self.meta.song, "artist") else None
        self.name = self.meta.album or path.stem
        self.songMetadata = (self.meta.data["song"] if "song" in self.meta.data else {}) or {}
        self.root = self.meta.data["rootDirectory"]
        self.path = AlbumPath(directoryName, self.root)
        self.pathFromRoot = self.path.pathFromRoot
        self.collectionName = self.path.collectionName

    def childDirectories(self):
        return sorted([f.name for f in self.path.path.iterdir() if f.is_dir()])

    @property
    def children(self):
        albums = []
        for name in self.childDirectories():
            albums.append(Album(self.directoryName + "/" + name))

        return albums

    @property
    def songFileNames(self):
        return sorted([f.name for f in self.path.path.iterdir() if (not f.is_dir()) and f.suffix in AUDIO_EXTENSIONS])

    @property
    def songs(self):
        songs = []
        for name in self.songFileNames:
            songs.append(CoreSong(self.directoryName + "/" + name, self))

        return songs

    def allContainedDirectoryNames(self):
        return self.childDirectories()

    def __repr__(self):
        return f"Album : {self.directoryName}"

class AlbumPath:
    def __init__(self, directoryName, root = None):
        self.path = Path(directoryName)
        self.root = root
        self.exists = self.path.is_dir()
        resolvedPath = str(self.path.resolve())
        self.pathFromRoot = self.relativeToRoot(resolvedPath)
        if self.pathFromRoot is None:
            self.collectionName = None
        else:
            firstSlash = self.pathFromRoot.find('/')
            self.collectionName = self.pathFromRoot[:firstSlash] if firstSlash > -1 else self.pathFromRoot
            self.pathFromCollection = self.relativeToCollection(resolvedPath)

    def relativeToRoot(self, filename):
        path = Path(filename)
        absoluteFilename = path.resolve()
        if str(absoluteFilename).startswith(str(self.root)) :
            directory = absoluteFilename if not path.suffix else absoluteFilename.parent
            return str(directory)[len(str(self.root)) + 1:]
        return None

    def relativeToCollection(self, filename):
        relativeToRoot = self.relativeToRoot(filename)
        if relativeToRoot is None:
            return None
        firstSlash = relativeToRoot.find('/')
        return relativeToRoot[firstSlash + 1:] if firstSlash > -1 else None
