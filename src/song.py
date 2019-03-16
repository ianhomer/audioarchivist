from pathlib import Path

class Song:
    def __init__(self, filename):
        self.filename = filename
        path = Path(filename)
        parts = path.stem.split('-')
        self.title = parts[0].strip()
        self.artist = parts[1].strip() if len(parts) > 1 else "unknown"
        self.album = path.parent.resolve().name

    def __repr__(self):
        return f"{self.title} : {self.artist} : {self.album}"

    @property
    def ffmpegArgs(self):
        return {
            'metadata':f"title={self.title}",
            'metadata:':f"artist={self.artist}",
            'metadata:g':f"album={self.album}",
        }
