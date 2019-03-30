from pathlib import Path

from .meta import Meta

class Album:
    def __init__(self, directoryName):
        path = Path(directoryName)
        if not path.is_dir():
            raise Exception(f"Cannot create album from {directoryName} since not a directory")
        self.directoryName = directoryName
        self.meta = Meta(directoryName)
        self.artist = self.meta.song.artist if self.meta.song is not None and hasattr(self.meta.song, "artist") else None
        self.name = self.meta.album or path.stem
        self.songMetadata = (self.meta.data["song"] if "song" in self.meta.data else {}) or {}
        self.root = self.meta.data["rootDirectory"]

        absoluteFilename = path.resolve()
        if str(absoluteFilename).startswith(str(self.root)) :
            self.pathFromRoot = str(absoluteFilename.parent)[len(str(self.root)) + 1:]
            firstSlash = self.pathFromRoot.find('/')
            self.collectionName = self.pathFromRoot[:firstSlash] if firstSlash > -1 else self.pathFromRoot
        else:
            self.collectionName = None

    def getPathFromRoot(self, filename):
        absoluteFilename = Path(filename).resolve()
        if str(absoluteFilename).startswith(str(self.root)) :
            return str(absoluteFilename.parent)[len(str(self.root)) + 1:]
        return None
