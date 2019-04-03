import os

from pathlib import Path
from .song import Song

audioExtensions = ["flac", "m4a", "mp3", "ogg", "wav"]
NA = "n/a"
EXPECTED_SAMPLE_RATE = 44100

class Collection:
    def __init__(self, directoryName):
        self.files = []
        for (dirpath, dirnames, filenames) in os.walk("."):
            self.files.extend(list(
                map(
                    lambda name : os.path.join(dirpath, name),
                    filter(lambda f : Path(f).suffix[1:].lower() in audioExtensions, filenames))
                )
            )
        self.files.sort()

    def print(self, args):
        header = f" : {'':10s} : {'ext':4s} : {'kb/s':>5s} : {'khz':3s} : {'kb':>5s} : {'s':>6s} : {'artist':20s} : {'title':30s} : {'album':20s}"
        lastPath = ""

        for file in self.files:
            song = Song(file, args.byname)
            if song.collectionName is None:
                path = song.pathFromRoot
            else:
                path = song.pathInCollection
            if (str(path) != lastPath):
                print("")
                print(f"{path:>49s}/" + header)
                print(190*"-")
                lastPath = path
            self.displaySong(song, args)
            for alt in song.alternatives:
                self.displaySong(alt, args)


    def displaySong(self, song, args):
        filesize = int(os.path.getsize(song.filename) / 1024)
        # Only display sample rate if not expected value
        unexpectedSamplerate = f"{int(song.samplerate/1000)}" if song.samplerate != EXPECTED_SAMPLE_RATE else ""
        bitdepthOrRate = colored(f"  s{song.bitdepth:2d}",'blue') if song.bitdepth > 0 else f"{song.bitrate:5d}"
        print(f"{song.standardFileTitleStem:50s} : {song.collectionName!s:10s} : {song.ext:4s} : " +
            f"{bitdepthOrRate} : {unexpectedSamplerate:>3s} : " +
            f"{filesize:6d} : " +
            f"{song.duration:5d} : {song.artist:20s} : " +
            f"{song.title:30s} : {song.album:20s}")
        if not song.aligned:
            print(colored(f"{song.alt['stem']:101s} : " +
                f"{song.alt['artist']:20s} : " +
                f"{song.alt['title']:30s} : {song.alt['album']:20s}", 'blue'))
            if args.save:
                song.save()
            if not song.stemAligned and args.rename:
                print(colored(f"...Moving {song.filename} to {song.standardFilename}", 'green'))
                os.rename(song.filename, song.standardFilename)
