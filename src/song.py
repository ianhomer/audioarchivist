from pathlib import Path
from meta import Meta
from tinytag import TinyTag

NA = "n/a"

def _Song__getMetadataFromTags(filename):
    tag = TinyTag.get(filename)
    data = {}
    if tag.artist is not None:
        data["artist"] = tag.artist
    if tag.album is not None:
        data["album"] = tag.album
    if tag.title is not None:
        data["title"] = tag.title
    if tag.year is not None:
        data["year"] = tag.year
    return data

def _Song__getMetadataFromFileNaming(filename):
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
        if metadataPrecedenceFromFileNaming:
            data = {
                **_Song__getMetadataFromTags(filename),
                **_Song__getMetadataFromFileNaming(filename)
            }
        else:
            data = {
                **_Song__getMetadataFromFileNaming(filename),
                **_Song__getMetadataFromTags(filename)
            }
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
