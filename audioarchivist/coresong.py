import eyed3
import mutagen
import os
import wave
import glob
import sys
import re
import traceback

# Travis build fails with installing taglib, so we can't unit test it.  Lazy load as work around.
import importlib
taglib_spec = importlib.util.find_spec("taglib")
if taglib_spec is not None:
    taglib = importlib.util.module_from_spec(taglib_spec)
    taglib_spec.loader.exec_module(taglib)

from pathlib import Path
from tinytag import TinyTag

from .meta import Meta
from .format import Format
from .logger import warn, info

NA = "n/a"
# Cache alternative paths from root, since we only support execution in one root directory
ALTERNATIVE_PATHS_FROM_ROOT = None
ALTERNATIVE_GLOBS = ["*.mp3","*.wav"]

NAMING_TITLE_AND_ARTIST = "title-and-artist"

def _CoreSong__getMetadataFromFile(filename):
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
            audiofile = taglib.File(filename)
            # Special case where tinytag couldn't extract tags for wav
            if tag.album is None and "ALBUM" in audiofile.tags and audiofile.tags["ALBUM"][0] :
                data["album"] = audiofile.tags["ALBUM"][0]
            if tag.artist is None and "ARTIST" in audiofile.tags and audiofile.tags["ARTIST"][0] :
                data["artist"] = audiofile.tags["ARTIST"][0]
            if tag.title is None and "TITLE" in audiofile.tags and audiofile.tags["TITLE"][0] :
                data["title"] = audiofile.tags["TITLE"][0]
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

def _CoreSong__getMetadataFromFilename(album, filename):
    metadata = album.meta.data
    naming = album.songMetadata.get("naming", None)
    path = Path(filename)
    parts = path.stem.split('-')
    title = parts[0].strip()
    if naming == NAMING_TITLE_AND_ARTIST:
        artist = parts[1].strip() if len(parts) > 1 else "unknown"
    else:
        artist = parts[2].strip() if len(parts) > 2 else "unknown"
    # If variation is specified in brackets
    search = re.search('(.*)(?:\(([^\)]*)\))', title)
    if search is not None:
        variation = search.group(2).strip()
    else:
        variation = None

    if "artist" in album.songMetadata:
        artist = album.songMetadata["artist"]

    return {
        "album"         : album.name,
        "artist"        : artist,
        "naming"        : naming,
        "rootDirectory" : album.root,
        "stem"          : path.stem,
        "title"         : title,
        "variation"     : variation
    }

class CoreSong:
    def __init__(self, filename, album):
        self.filename = filename
        path = Path(filename)
        self.albumObject = album
        self.exists = path.exists()
        if not self.exists:
            warn(f"Song {filename} does not exist")
        self.ext = path.suffix[1:].lower()
        self.basename = path.name
        self.tags = _CoreSong__getMetadataFromFile(filename) if self.exists else {}
        self.name = _CoreSong__getMetadataFromFilename(self.albumObject, filename)
        data = { **self.tags, **self.name } if self.albumObject.byName else { **self.name, **self.tags }
        self.rootDirectory = data["rootDirectory"]
        absoluteFilename = Path(filename).resolve()
        self.collectionName = self.albumObject.collectionName
        self.pathFromRoot = self.albumObject.path.relativeToRoot(filename)
        self.pathInCollection = self.albumObject.path.relativeToCollection(filename)

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
            # Special case, we compare stem to standardFilestem
            if key == "stem":
                if valueByName != self.standardFileStem:
                    self.alt[key] = self.standardFileStem
                    self.aligned = False
                    self.stemAligned = False
                else:
                    self.alt[key] = ''
            # Root directory not relevant for alignment check
            elif key != "rootDirectory" and key != "naming" :
                if key not in self.tags:
                    self.aligned = False
                    self.alt[key] = "(no tag)"
                else:
                    valueByTag = self.tags[key]
                    if valueByName != valueByTag:
                        self.alt[key] = valueByTag if self.albumObject.byName else valueByName
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
                        alternatives.append(CoreSong(alternativeFile, self.albumObject))
        return alternatives

    def getFilenameInCollection(self,collection):
        return self.rootDirectory.joinpath(collection, self.pathInCollection, self.basename)

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
                audiofile = taglib.File(self.filename)
                audiofile.tags["ALBUM"] = [self.album]
                audiofile.tags["ARTIST"] = [self.artist]
                audiofile.tags["TITLE"] = [self.title]
                info(f"... Saving tags for WAV : {self.filename}")
                audiofile.save()
            else:
                audiofile = eyed3.load(self.filename)
                if audiofile is None:
                    warn(f"Can't load audio file {self.filename} with eyed3")
                else:
                    info(f"Saving tags for {self.filename}")
                    audiofile.tag.album = self.album
                    audiofile.tag.artist = self.artist
                    audiofile.tag.title = self.title
                    audiofile.tag.save()

    def move(self, collection):
        source = self.filename
        destination = self.getFilenameInCollection(collection)
        print(f"Moving to {collection}\n... {source} \n -> {destination}")
        directory = str(Path(destination).parent)
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.rename(source, destination)
