from .meta import Meta

class Album:
    def __init__(self, directoryName):
        self.directoryName = directoryName
        meta = Meta(directoryName)
        self.artist = meta.song.artist if meta.song is not None else None
        self.album = meta.album
