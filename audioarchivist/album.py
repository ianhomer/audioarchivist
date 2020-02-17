from pathlib import Path

from .meta import Meta
from .coresong import CoreSong

AUDIO_EXTENSIONS = [".aac", ".flac", ".m4a", ".mp3", ".mp4", ".ogg", ".wav"]

class Album:
    def __init__(self, directoryName, parent = None, byName = False):
        self.directoryName = directoryName
        if not Path(directoryName).is_dir():
            raise Exception(f"Cannot create album from {directoryName} since not a directory")
        self.parent = parent
        if self.parent:
            self.byName = self.parent.byName
        else:
            self.byName = byName
        self.meta = Meta(directoryName)
        self.artist = self.meta.song.artist if self.meta.song is not None and hasattr(self.meta.song, "artist") else None
        self.name = self.meta.album
        self.songMetadata = (self.meta.data["song"] if "song" in self.meta.data
                             else {}) or {}
        self.root = self.meta.data["rootDirectory"]
        self.path = AlbumPath(directoryName, self.root)
        self.pathFromRoot = self.path.pathFromRoot
        self.collectionName = self.path.collectionName
        if not self.pathFromRoot is None:
            if self.parent:
                self.collections = self.parent.collections
            else:
                self.collections = sorted(
                  [f.name for f in Path(self.root).iterdir()
                    if not f.name.startswith(".") and f.is_dir()])

            # Optimise collections to only include collections that have
            # alternatives provided.  These are collections that have relevant
            # alternatives in place
            if self.path.pathFromCollection:
                self.collections = self.alternativeCollectionNames

    @property
    def alternativeCollectionNames(self):
        alternativeCollectionNames = []
        for collectionName in self.collections:
            alternativeDirectoryName = self.root.joinpath(
              collectionName,self.path.pathFromCollection).as_posix()
            if Path(alternativeDirectoryName).is_dir():
                alternativeCollectionNames.append(collectionName)
        return alternativeCollectionNames

    @property
    def alternatives(self):
        if hasattr(self,"_cached_alternatives"):
            return self._cached_alternatives
        else:
            self._cached_alternatives = []
            if hasattr(self, "collections") and self.path.pathFromCollection:
                for collectionName in self.collections:
                    alternativeDirectoryName = self.root.joinpath(
                      collectionName,self.path.pathFromCollection).as_posix()
                    if Path(alternativeDirectoryName).is_dir():
                        self._cached_alternatives.append(Album(
                          alternativeDirectoryName, self))
            else:
                self._cached_alternatives = [self]
            return self._cached_alternatives

    @property
    def childDirectories(self):
        childDirectories = []
        for a in self.alternatives:
            childDirectories.extend([f.name for f in a.path.path.iterdir()
                                     if f.is_dir()
                                     and not f.name.startswith(".")])
        return sorted(set(childDirectories))

    @property
    def children(self):
        albums = []
        for name in self.childDirectories:
            for a in self.alternatives:
                childDirectoryName = a.directoryName + "/" + name
                if Path(childDirectoryName).is_dir():
                    albums.append(Album(childDirectoryName, self))

        return albums

    @property
    def songFileNames(self):
        return sorted([f.name for f in self.path.path.iterdir()
            if (not f.is_dir()) and f.suffix.lower()
                        in AUDIO_EXTENSIONS])

    @property
    def songs(self):
        songs = []
        for name in self.songFileNames:
            songs.append(CoreSong(self.directoryName + "/" + name, self))

        return songs

    @property
    def hasSongs(self):
        return len(self.songFileNames) > 0

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
