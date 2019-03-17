from pathlib import Path
from meta import Meta
from tinytag import TinyTag

NA = "n/a"

def _Song__getMetadataFromTags(filename):
    tag = TinyTag.get(filename)
    data = {}
    if tag.artist is not None:
        data["artist"] = tag.artist.rstrip('\0')
    if tag.album is not None:
        data["album"] = tag.album.rstrip('\0')
    if tag.title is not None:
        data["title"] = tag.title.rstrip('\0')
    if tag.year is not None:
        data["year"] = tag.year.rstrip('\0')
    return data

def _Song__getMetadataFromFilename(filename):
    metadata = Meta(filename).data
    path = Path(filename)
    parts = path.stem.split('-')
    artist = parts[1].strip() if len(parts) > 1 else "unknown"
    album = path.parent.resolve().name
    if "song" in metadata:
        songMetadata = metadata["song"]
        if "artist" in songMetadata:
            artist = songMetadata["artist"]
        if "album" in songMetadata:
            album = songMetadata["album"]
    title = parts[0].strip()
    return {
        "album"      : album,
        "artist"     : artist,
        "title"      : title,
    }

class Song:
    def __init__(self, filename, metadataPrecedenceFromFileNaming = False):
        self.filename = filename
        self.tags = _Song__getMetadataFromTags(filename)
        self.name = _Song__getMetadataFromFilename(filename)
        if metadataPrecedenceFromFileNaming:
            data = { **self.tags, **self.name }
        else:
            data = { **self.name, **self.tags }
        self.aligned = True
        self.alt = {}
        for key in self.name.keys():
            valueByName = self.name.get(key, NA)
            valueByTag = self.tags.get(key, NA)
            if valueByName != valueByTag:
                if metadataPrecedenceFromFileNaming:
                    self.alt[key] = valueByTag
                else:
                    self.alt[key] = valueByName
                self.aligned = False
            else:
                self.alt[key] = ''
        self.artist = data.get("artist", NA)
        self.album = data.get("album", NA)
        self.title = data.get("title", NA)
        self.year = data.get("year", NA)

    def __repr__(self):
        return f"{self.title} : {self.artist} : {self.album}"

    @property
    def ffmpegArgs(self):
        return {
            'metadata:g:0':f"title={self.title}",
            'metadata:g:1':f"artist={self.artist}",
            'metadata:g:2':f"album={self.album}",
            'metadata:g:3':f"year={self.year}"
        }
