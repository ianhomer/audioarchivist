import os
import argparse

from pathlib import Path

from .song import Song

def run():
    parser = argparse.ArgumentParser(description='Move audio files.')
    parser.add_argument('file',nargs='+', help='audio file')
    parser.add_argument('-c', '--collection', help='Set collection name for output', default=None)
    parser.add_argument('-s', '--share', action='store_const', const='share', dest='collection',
        help='Set collection name to share for output')
    args = parser.parse_args()
    if args.collection is None:
        print("Please specifiy a collection to move to")
        return

    for audioIn in args.file:
        song = Song(audioIn)
        if song.exists:
            song.move(args.collection)
