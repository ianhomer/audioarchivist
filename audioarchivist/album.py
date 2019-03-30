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
        self.name = self.meta.album
        if self.name is None:
            self.name = path.stem
        self.songMetadata = self.meta.data["song"] if "song" in self.meta.data else {}
        if self.songMetadata is None:
            self.songMetadata = {}
