from pathlib import Path
from meta import Meta
from tinytag import TinyTag
import eyed3
import mutagen
import taglib

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
    data["samplerate"] = tag.samplerate
    data["duration"] = tag.duration
    if (tag.bitrate > 1000):
        # some m4a files are coming in with bitrates > 300,000 and not matching
        # ffmpeg output, so we'll use mutagen instead
        data["bitrate"] = int(mutagen.File(filename).info.bitrate / 1000)
    else:
        data["bitrate"] = tag.bitrate
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
    def __init__(self, filename, byName = False):
        self.filename = filename
        path = Path(filename)
        self.ext = path.suffix[1:]
        self.tags = _Song__getMetadataFromTags(filename)
        self.name = _Song__getMetadataFromFilename(filename)
        data = { **self.tags, **self.name } if byName else { **self.name, **self.tags }
        self.aligned = True
        self.alt = {}
        for key in self.name.keys():
            valueByName = self.name[key]
            if key not in self.tags:
                self.aligned = False
                self.alt[key] = "(no tag)"
            else:
                valueByTag = self.tags[key]
                if valueByName != valueByTag:
                    self.alt[key] = valueByTag if byName else valueByName
                    self.aligned = False
                else:
                    self.alt[key] = ''
        self.artist = data.get("artist", NA)
        self.album = data.get("album", NA)
        self.title = data.get("title", NA)
        self.year = data.get("year", NA)
        self.samplerate = int(data["samplerate"] / 1000)
        self.duration = int(data["duration"])
        self.bitrate = int(data["bitrate"])

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

    def save(self):
        if self.aligned:
            print(f"No tags to save for {self.filename}")
        else:
            if self.ext == "m4a" or self.ext == "wav":
                # eyed3 doesn't support wav or m4a, so we'll use the taglib wrapper
                print(f"Saving tags for WAV : {self.filename}")
                audiofile = taglib.File(self.filename)
                audiofile.tags["ALBUM"] = self.album
                audiofile.tags["ARTIST"] = self.artist
                audiofile.tags["TITLE"] = self.title
                audiofile.save()
            else:
                print(f"Saving tags for {self.filename}")
                audiofile = eyed3.load(self.filename)
                audiofile.tag.album = self.album
                audiofile.tag.artist = self.artist
                audiofile.tag.title = self.title
                audiofile.tag.save()
