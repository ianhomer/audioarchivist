import eyed3
import mutagen
import os
import taglib
import wave
import glob
import sys
import re
import traceback

from meta import Meta
from pathlib import Path
from tinytag import TinyTag

from format import Format
from logger import warn, info

NA = "n/a"
# Cache alternative paths from root, since we only support execution in one root directory
ALTERNATIVE_PATHS_FROM_ROOT = None
ALTERNATIVE_GLOBS = ["*.mp3","*.wav"]

NAMING_TITLE_AND_ARTIST = "title-and-artist"

def _Song__getMetadataFromFile(filename):
    data = {}
    try:
        tag = TinyTag.get(filename)
        ext = Path(filename).suffix[1:].lower()
        if tag.artist is not None:
            data["artist"] = tag.artist.rstrip('\0')
        if tag.album is not None:
            data["album"] = tag.album.rstrip('\0')
        if tag.title is not None:
            data["title"] = tag.title.rstrip('\0')
        if tag.year is not None:
            data["year"] = tag.year.rstrip('\0')
        if tag.samplerate is not None:
            data["samplerate"] = tag.samplerate
        if tag.duration is not None:
            data["duration"] = tag.duration
        data["bitdepth"] = -1
        if ext == "flac":
            data["bitdepth"] = mutagen.File(filename).info.bits_per_sample
            data["bitrate"] = tag.bitrate
        elif ext == "wav":
            data["bitdepth"] = wave.open(filename).getsampwidth() * 8
            data["bitrate"] = tag.bitrate
        elif tag.bitrate is None or tag.bitrate > 1000:
            # some m4a files are coming in with bitrates > 300,000 and not matching
            # ffmpeg output, so we'll use mutagen instead
            audiofile = mutagen.File(filename)
            data["bitrate"] = int(audiofile.info.bitrate / 1000)
        else:
            data["bitrate"] = tag.bitrate
    except:
        print(f"Cannot parse {filename}")
        traceback.print_exc()
    return data

def _Song__getMetadataFromFilename(filename):
    metadata = Meta(filename).data
    songMetadata = None
    if "song" in metadata:
        songMetadata = metadata["song"]
    naming = None
    if songMetadata is not None:
        naming = songMetadata.get("naming", None)
    path = Path(filename)
    parts = path.stem.split('-')
    title = parts[0].strip()
    if naming == NAMING_TITLE_AND_ARTIST:
        artist = parts[1].strip() if len(parts) > 1 else "unknown"
    else:
        album = parts[1].strip() if len(parts) > 1 else None
        artist = parts[2].strip() if len(parts) > 2 else "unknown"
    # If variation is specified in brackets
    search = re.search('(.*)(?:\(([^\)]*)\))', title)
    if (search is not None):
        variation = search.group(2).strip()
    else:
        variation = None
    album = path.parent.resolve().name

    if "song" in metadata:
        if "artist" in songMetadata:
            artist = songMetadata["artist"]
        if "album" in songMetadata:
            album = songMetadata["album"]

    return {
        "album"         : album,
        "artist"        : artist,
        "naming"        : naming,
        "rootDirectory" : metadata["rootDirectory"],
        "stem"          : path.stem,
        "title"         : title,
        "variation"     : variation
    }

class Song:
    def __init__(self, filename, byName = False):
        self.filename = filename
        path = Path(filename)
        self.ext = path.suffix[1:].lower()
        self.tags = _Song__getMetadataFromFile(filename)
        self.name = _Song__getMetadataFromFilename(filename)
        data = { **self.tags, **self.name } if byName else { **self.name, **self.tags }
        self.rootDirectory = data["rootDirectory"]
        absoluteFilename = Path(filename).resolve()
        if str(absoluteFilename).startswith(str(self.rootDirectory)) :
            self.pathFromRoot = str(absoluteFilename.parent)[len(str(self.rootDirectory)) + 1:]
            firstSlash = self.pathFromRoot.find('/')
            self.collectionName = self.pathFromRoot[:firstSlash]
            self.pathInCollection = self.pathFromRoot[firstSlash + 1:]
        else:
            self.pathFromRoot = str(path.parent)
            self.collectionName = None

        self.artist = data.get("artist", NA)
        self.album = data.get("album", NA)
        self.title = data.get("title", NA)
        self.year = data.get("year", NA)
        self.variation = data.get("variation")
        self.stem = data.get("stem")
        self.naming = data.get("naming")

        self.samplerate = int(data.get("samplerate", -1))
        self.duration = int(data.get("duration", -1))
        self.bitrate = int(data.get("bitrate", -1))
        self.bitdepth = int(data.get("bitdepth", -1))

        self.aligned = True
        self.stemAligned = True
        self.alt = {}
        for key in (self.name.keys() - ["variation"]):
            valueByName = self.name[key]
            if key == "stem":
                # Special case, we compare stem to standardFilestem
                if valueByName != self.standardFileStem:
                    self.alt[key] = self.standardFileStem
                    self.aligned = False
                    self.stemAligned = False
                else:
                    self.alt[key] = ''
            elif key != "rootDirectory" and key != "naming" :
                # Root directory not relevant for alignment check
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
    def standardFileStem(self):
        standardFilename = self.standardFileTitleStem
        if self.naming == NAMING_TITLE_AND_ARTIST:
            standardFilename += " - " + self.artist
        else:
            standardFilename += " - " + self.album
            standardFilename += " - " + self.artist
        return standardFilename

    @property
    def standardFileTitleStem(self):
        standardFilename = self.title
        return standardFilename

    @property
    def alternativePathsFromRoot(self):
        global ALTERNATIVE_PATHS_FROM_ROOT
        if ALTERNATIVE_PATHS_FROM_ROOT is None:
            ALTERNATIVE_PATHS_FROM_ROOT = list(
                map(
                    lambda child : child.name + "/" + self.pathInCollection,
                    filter(lambda f:
                        not f.name.startswith(".") and f.is_dir(),
                        self.rootDirectory.iterdir()
                    )
                )
            )
        return ALTERNATIVE_PATHS_FROM_ROOT

    @property
    def alternatives(self):
        if self.collectionName is None:
            return []
        alternatives = []
        for pathFromRoot in self.alternativePathsFromRoot:
            if not pathFromRoot.startswith(self.collectionName + "/"):
                for alternativeGlob in ALTERNATIVE_GLOBS:
                    alternativeDirectory = self.rootDirectory.joinpath(pathFromRoot,self.standardFileTitleStem)
                    globPattern = str(alternativeDirectory) + alternativeGlob
                    alternativeFiles = glob.glob(globPattern)
                    for alternativeFile in alternativeFiles:
                        alternatives.append(Song(alternativeFile))
        return alternatives

    def getFilenameInCollection(self,collection):
        return self.rootDirectory.joinpath(collection,self.pathInCollection,self.filename)

    @property
    def format(self):
        return Format(self.ext, self.bitrate)

    @property
    def standardFilename(self):
        return ( Path(self.filename).parent / (self.standardFileStem + "." + self.ext) )

    def save(self):
        if self.aligned:
            warn(f"No tags to save for {self.filename}")
        else:
            if self.ext == "m4a" or self.ext == "wav" or self.ext == "ogg" or self.ext == "flac":
                # eyed3 doesn't support some file types, so we'll use the taglib wrapper
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
