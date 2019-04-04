from pathlib import Path

from .coresong import CoreSong
from .album import Album

class Song(CoreSong):
    def __init__(self, filename, album = None, byName = False):
        super().__init__(
            filename,
            album or Album(Path(filename).parent, byName = byName)
        )
