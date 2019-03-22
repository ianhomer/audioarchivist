import argparse
import ffmpeg
import os
import sys

from format import Format
from logger import warn
from song import Song

replace = False
quiet = False
MIN_BITRATE = 128

def run():
    parser = argparse.ArgumentParser(description='Convert audio files.')
    parser.add_argument('file',nargs='+',
        help='audio file')
    parser.add_argument('-f', '--flac', action='store_true',
        help='Lossless compress audio, by converting to flac',
        default=False)
    args = parser.parse_args()
    for audioIn in args.file:
        print(f"Converting audio file : {audioIn}")
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
        if args.flac:
            destination = Format('flac', bitdepth = song.bitdepth)
        else:
            destination = Format('mp3', bitrate)

        print(f"Converting audio file : {audioIn} : {song} {song.format}-> {destination}")
        if song.format == destination:
            printf("No conversion necessary")
            return

        outFile=f"{song.title} - {song.artist} - {song.album}.{destination.ext}"
        ffmpegArgs = {
            **destination.ffmpegArgs,
            **song.ffmpegArgs
        }
        print(f"ffmpeg args : {ffmpegArgs}")
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
