from pathlib import Path
from meta import Meta

class Song:
    def __init__(self, filename):
        self.filename = filename
        metadata = Meta(filename).data
        path = Path(filename)
        parts = path.stem.split('-')
        self.artist = parts[1].strip() if len(parts) > 1 else "unknown"
        self.album = path.parent.resolve().name
        if "song" in metadata:
            songMetadata = metadata["song"]
            if "artist" in songMetadata:
                self.artist = songMetadata["artist"]
            if "album" in songMetadata:
                self.album = songMetadata["album"]
        self.title = parts[0].strip()

    def __repr__(self):
        return f"{self.title} : {self.artist} : {self.album}"

    @property
    def ffmpegArgs(self):
        return {
            'metadata':f"title={self.title}",
            'metadata:':f"artist={self.artist}",
            'metadata:g':f"album={self.album}",
        }
