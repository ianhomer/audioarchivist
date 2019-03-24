import os
import argparse

from pathlib import Path

from .song import Song

def run():
    parser = argparse.ArgumentParser(description='Move audio files.')
    parser.add_argument('file',nargs='+',
        help='audio file')
    parser.add_argument('-c', '--collection',
        help='Set collection name for output',
        default=None)
    args = parser.parse_args()
    if args.collection is None:
        print("Please specifiy a collection to move to")
        return

    for audioIn in args.file:
        song = Song(audioIn)
        source = song.filename
        destination = song.getFilenameInCollection(args.collection)
        print(f"Moving \n... {source} \n -> {destination}")
        directory = str(Path(destination).parent)
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.rename(source, destination)
