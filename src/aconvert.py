import ffmpeg
import os
import sys

from destination import Destination
from song import Song
from logger import warn

replace = False
quiet = False
MIN_BITRATE = 128

def run():
    print("Converting audio files")
    audioIn = sys.argv[1]
    if not os.path.exists(audioIn):
        print(f"File {audioIn} does not exist")
        return
    song = Song(audioIn)
    # Enforce 256 bitrate unless input is worse
    bitrate = 256 if song.bitrate > 256 else song.bitrate
    if (bitrate < MIN_BITRATE):
        # Bitrate below MIN_BITRATE is limited value
        warn(f"Not converting to {bitrate} since below minumum allowed {MIN_BITRATE}")
        return
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
