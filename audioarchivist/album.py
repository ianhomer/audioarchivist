from pathlib import Path

from .meta import Meta

class Album:
    def __init__(self, directoryName):
        path = Path(directoryName)
        if not path.is_dir():
            raise Exception(f"Cannot create album from {directoryName} since not a directory")
        self.directoryName = directoryName
        self.meta = Meta(directoryName)
        self.artist = self.meta.song.artist if self.meta.song is not None else None
        self.album = self.meta.album
