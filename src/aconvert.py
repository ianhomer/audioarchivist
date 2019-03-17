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
    # Enforce 256 bitrate unless input is worse
    bitrate = 256 if song.bitrate > 256 else song.bitrate
    destination = Destination('mp3', bitrate)
    print(f"Converting audio file : {audioIn} : {song} -> {destination}")
    outFile=f"{song.title} - {song.artist}.{destination.ext}"
    ffmpegArgs = {
        **destination.ffmpegArgs,
        **song.ffmpegArgs
    }
    (
        ffmpeg
            .input(audioIn)
            .filter_('loudnorm')
            .output(outFile, **ffmpegArgs)
            .run(**{
                'quiet':quiet,
                'overwrite_output':replace
            })
    )
