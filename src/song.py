import eyed3
import mutagen
import os
import taglib

from meta import Meta
from pathlib import Path
from tinytag import TinyTag

from format import Format
from logger import warn, info

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
    if tag.bitrate is None or tag.bitrate > 1000:
        # some m4a files are coming in with bitrates > 300,000 and not matching
        # ffmpeg output, so we'll use mutagen instead
        audiofile = mutagen.File(filename)
        if audiofile is None:
            warn(f"Cannot get audio file from {filename}, estimating bitrate")
            data["bitrate"] = os.path.getsize(filename) * 8 / (tag.duration * 1024)
        else:
            data["bitrate"] = int(audiofile.info.bitrate / 1000)
    else:
        data["bitrate"] = tag.bitrate

    return data

def _Song__getMetadataFromFilename(filename):
    metadata = Meta(filename).data
    path = Path(filename)
    parts = path.stem.split('-')
    artist = parts[1].strip() if len(parts) > 1 else "unknown"
    variation = None
    if len(parts) > 2:
        variation = "-".join(parts[2:]).strip()
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
        "stem"       : path.stem,
        "variation"  : variation
    }

class Song:
    def __init__(self, filename, byName = False):
        self.filename = filename
        path = Path(filename)
        self.ext = path.suffix[1:]
        self.tags = _Song__getMetadataFromTags(filename)
        self.name = _Song__getMetadataFromFilename(filename)
        data = { **self.tags, **self.name } if byName else { **self.name, **self.tags }

        self.artist = data.get("artist", NA)
        self.album = data.get("album", NA)
        self.title = data.get("title", NA)
        self.year = data.get("year", NA)
        self.variation = data.get("variation")
        self.stem = data.get("stem")

        self.samplerate = int(data["samplerate"])
        self.duration = int(data["duration"])
        self.bitrate = int(data["bitrate"])

        self.aligned = True
        self.stemAligned = True
        self.alt = {}
        for key in (self.name.keys() - ["variation"]):
            valueByName = self.name[key]
            if key == "stem":
                # Special case, we compare stem to standardFilestem
                if valueByName != self.standardFilestem:
                    self.alt[key] = self.standardFilestem
                    self.aligned = False
                    self.stemAligned = False
                else:
                    self.alt[key] = ''
            else:
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

    @property
    def standardFilestem(self):
        standardFilename = self.title
        standardFilename += " - " + self.artist
        if self.variation is not None:
            standardFilename += " - " + self.variation
        return standardFilename

    @property
    def format(self):
        return Format(self.ext, self.bitrate)

    @property
    def standardFilename(self):
        return ( Path(self.filename).parent / (self.standardFilestem + "." + self.ext) )

    def save(self):
        if self.aligned:
            warn(f"No tags to save for {self.filename}")
        else:
            if self.ext == "m4a" or self.ext == "wav" or self.ext == "ogg":
                # eyed3 doesn't support wav or m4a, so we'll use the taglib wrapper
                info(f"... Saving tags for WAV : {self.filename}")
                audiofile = taglib.File(self.filename)
                audiofile.tags["ALBUM"] = self.album
                audiofile.tags["ARTIST"] = self.artist
                audiofile.tags["TITLE"] = self.title
                audiofile.save()
            else:
                info(f"Saving tags for {self.filename}")
                audiofile = eyed3.load(self.filename)
                if audiofile is None:
                    warn(f"Can't load audio file {self.filename} with eyed3")
                else:
                    audiofile.tag.album = self.album
                    audiofile.tag.artist = self.artist
                    audiofile.tag.title = self.title
                    audiofile.tag.save()
