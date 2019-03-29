from .meta import Meta

class Album:
    def __init__(self, directoryName):
        self.directoryName = directoryName
        meta = Meta(directoryName)
        self.artist = meta.song.artist
        self.album = meta.album
