import os

from pathlib import Path
from termcolor import colored

from .album import Album
from .logger import error
from .song import Song

NA = "n/a"
EXPECTED_SAMPLE_RATE = 44100
HEADER = f" : {'':10s} : {'ext':4s} : {'kb/s':>5s} : {'khz':3s} : {'kb':>6s} : {'s':>6s} : {'artist':20s} : {'title':30s} : {'album':20s}"

class Collection:
    def __init__(self, directoryName):
        self.directoryName = directoryName

    def process(self, do = {}, args = None):
        if not "album" in do:
            do["album"] = lambda o : None
        if not "em" in do:
            do["em"] = lambda o : None
        if not "header" in do:
            do["header"] = lambda o : None
        if not "song" in do:
            do["song"] = lambda o : None

        return self.processAlbum(
            Album(
                self.directoryName,
                byName = getattr(args, "byname", False)
            ), do, args
        )

    def processAlbum(self, album, do, args):
        lastPath = ""
        hasSongs = False
        songCount = 0

        for a in album.alternatives:
            if a.hasSongs:
                if a.collectionName is None:
                    path = a.pathFromRoot
                else:
                    path = a.path.pathFromCollection

                if path is None:
                    path = "."

                if (str(path) != lastPath):
                    do["header"]("")
                    do["header"](f"{path:>49s}/" + HEADER)
                    do["header"](190*"-")
                    lastPath = path

                if not args.albumsonly:
                    songs = a.songs
                    if len(a.songs) > 0:
                        hasSongs = True
                        songCount += len(a.songs)

                    for song in songs:
                        self.processSong(song, do, args)

        if hasSongs:
            do["album"](album.directoryName)

        for child in album.children:
            songCount += self.processAlbum(child, do, args)

        return songCount

    def processSong(self, song, do, args):
        filesize = int(os.path.getsize(song.filename) / 1024)
        # Only display sample rate if not expected value
        unexpectedSamplerate = f"{int(song.samplerate/1000)}" if song.samplerate != EXPECTED_SAMPLE_RATE else ""
        bitdepthOrRate = colored(f"  s{song.bitdepth:2d}",'blue') if song.bitdepth > 0 else f"{song.bitrate:5d}"
        do["song"](f"{song.standardFileTitleStem:50s} : {song.collectionName!s:10s} : {song.ext:4s} : " +
            f"{bitdepthOrRate} : {unexpectedSamplerate:>3s} : " +
            f"{filesize:7d} : " +
            f"{song.duration:5d} : {song.artist:20s} : " +
            f"{song.title:30s} : {song.album:20s}")
        if not song.aligned:
            do["em"](f"{song.alt['stem']:102s} : " +
                f"{song.alt['artist']:20s} : " +
                f"{song.alt['title']:30s} : {song.alt['album']:20s}")
            if getattr(args, "save", False):
                song.save()
            if not song.stemAligned and getattr(args, "rename", False):
                do["info"](f"...Moving {song.filename} to {song.standardFilename}")
                os.rename(song.filename, song.standardFilename)
