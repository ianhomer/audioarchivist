from pathlib import Path

from .meta import Meta

class Album:
    def __init__(self, directoryName):
        if not Path(directoryName).is_dir():
            raise Exception(f"Cannot create album from {directoryName} since not a directory")

        self.directoryName = directoryName
        self.meta = Meta(directoryName)
        self.artist = self.meta.song.artist if self.meta.song is not None and hasattr(self.meta.song, "artist") else None
        self.name = self.meta.album or path.stem
        self.songMetadata = (self.meta.data["song"] if "song" in self.meta.data else {}) or {}
        self.root = self.meta.data["rootDirectory"]
        self.path = AlbumPath(directoryName, self.root)
        self.pathFromRoot = self.path.pathFromRoot
        self.collectionName = self.path.collectionName

class AlbumPath:
    def __init__(self, directoryName, root = None):
        self.path = Path(directoryName)
        self.root = root
        self.exists = self.path.is_dir()
        self.pathFromRoot = self.relativeToRoot(str(self.path.resolve()))
        if self.pathFromRoot is None:
            self.collectionName = None
        else:
            firstSlash = self.pathFromRoot.find('/')
            self.collectionName = self.pathFromRoot[:firstSlash] if firstSlash > -1 else self.pathFromRoot

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
