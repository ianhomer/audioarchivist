import ffmpeg
import os
import sys

from destination import Destination
from song import Song
replace = False
quiet = False

def run():
    print("Converting audio files")
    audioIn = sys.argv[1]
    if not os.path.exists(audioIn):
        print(f"File {audioIn} does not exist")
        return
    song = Song(audioIn)
    destination = Destination('mp3', 256)
    print(f"Converting audio file : {audioIn} : {song} -> {destination}")
    outFile=f"{song.title} - {song.artist}.{destination.ext}"
    ffmpegArgs = {
        **destination.ffmpegArgs,
        **song.ffmpegArgs
    }
    (
        ffmpeg
            .input(audioIn)
            .output(outFile, **ffmpegArgs)
            .run(**{
                'quiet':quiet,
                'overwrite_output':replace
            })
    )
