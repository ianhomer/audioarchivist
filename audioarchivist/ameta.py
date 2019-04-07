import argparse
import eyed3
import wave
import os

from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.wavpack import WavPack
from tinytag import TinyTag
from termcolor import colored

from .logger import warn, info
from .collection import Collection

def run():
    parser = argparse.ArgumentParser(description='Display Audio File meta data.')
    parser.add_argument('-a', '--albumsonly', action='store_true', help='Only display albums', default=False)
    parser.add_argument('-n', '--byname', action='store_true', help='Take metadata from file naming as precedence', default=False)
    parser.add_argument('-s', '--save', action='store_true', help='Save tags to audio file', default=False)
    parser.add_argument('-r', '--rename', action='store_true', help='Rename file to standard naming', default=False)
    parser.add_argument('--root', action='store', help='Root path of meta scan', default='.')
    args = parser.parse_args()
    return Collection(args.root).process({
        "song"  : lambda o : print(o),
        "header": lambda o : print(o),
        "info"  : lambda o : info(o),
        "em"    : lambda o : print(colored(o,"blue"))
    }, args = args)
