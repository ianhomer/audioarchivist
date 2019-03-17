import eyed3
import os
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.wavpack import WavPack
from tinytag import TinyTag
import wave
from song import Song
import argparse
from termcolor import colored

NA = "n/a"
EXPECTED_SAMPLE_RATE = 44
audioExtensions = ["m4a", "mp3", "ogg", "wav"]

files = []
for (dirpath, dirnames, filenames) in os.walk("."):
    files.extend(list(
        map(
            lambda name : os.path.join(dirpath, name),
            filter(lambda f : Path(f).suffix[1:] in audioExtensions, filenames))
        )
    )

def run():
    parser = argparse.ArgumentParser(description='Display Audio File meta data.')
    parser.add_argument('-n', '--byname',
        help='Take metadata from file naming as precedence',
        default=False)
    args = parser.parse_args()

    header = f" : {'ext':4s} : {'kb/s':>5s} : {'kb':>5s} : {'s':>5s} : {'artist':20s} : {'title':30s} : {'album':20s}"
    files.sort()
    lastParent = ""
    for file in files:
        path = Path(file)
        if (path.parent != lastParent):
            print("")
            print(f"file  {path.parent.name:>43s}/" + header)
            print(170*"-")
            lastParent = path.parent
        ext = path.suffix[1:]
        stem = path.stem
        filesize = int(os.path.getsize(file) / 1024)
        notes=""
        song = Song(file, args.byname)
        # Report any sample rates below 44Mhz, i.e. below expected
        if (song.samplerate < EXPECTED_SAMPLE_RATE):
            notes+=f" low sample rate = {song.samplerate}Mhz"
        if (song.year != NA):
            notes+=f" {song.year}"
        print(f"{stem:50s} : {ext:4s} : " +
            f"{song.bitrate:5d} : "+
            f"{filesize:5d} : " +
            f"{song.duration:5d} : {song.artist:20s} : " +
            f"{song.title:30s} : {song.album:20s} {notes}")
        if not song.aligned:
            print(colored(f"{' . . . ':81s} : " +
                f"{song.alt['artist']:20s} : " +
                f"{song.alt['title']:30s} : {song.alt['album']:20s}", 'blue'))
