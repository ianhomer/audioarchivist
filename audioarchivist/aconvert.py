import argparse
import ffmpeg
import os
import sys

from pathlib import Path

from .format import Format
from .logger import info,warn
from .song import Song
from .channels import Channels

MIN_BITRATE = 128

def run():
    parser = argparse.ArgumentParser(description='Convert audio files.')
    parser.add_argument('file', nargs='+', help='audio file')
    parser.add_argument('-w', '--wav', action='store_true',
                        help='Lossless audio, by converting to wav',
                        default=False)
    parser.add_argument('-f', '--flac', action='store_true',
                        help='Lossless compress audio, by converting to flac',
                        default=False)
    parser.add_argument('-c', '--collection',
                        help='Set collection name for output', default=None)
    parser.add_argument('-v', '--variant', action='store_true',
                        help='Add variant to title', default=False)
    parser.add_argument('--bitrate', help='Set bit rate', default=None)
    parser.add_argument('--bitdepth', help='Set bit depth', default=None)
    parser.add_argument('--mono', help='Convert to mono', action='store_true',
                        default=False)
    parser.add_argument('--quiet', action='store_true', help='Quiet',
                        default=False)
    parser.add_argument('--replace', action='store_true',
                        help='Replace existing files', default=False)
    parser.add_argument('--samplerate', help='Set sample rate (khz)',
                        default=None)
    parser.add_argument('--seconds', help='Crop to number of seconds',
                        default=None)
    parser.add_argument('--start', help='Start at given number of seconds',
                        default=None)
    parser.add_argument('--nomin', action='store_true',
                        help="Don't enforce any minimum standards",
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
        if args.bitrate is not None:
            bitrate = int(args.bitrate)
        bitdepth = song.bitdepth if args.bitdepth is None else int(args.bitdepth)
        samplerate = song.samplerate if args.samplerate is None else int(args.samplerate)

        if bitrate < 1:
            bitrate = MIN_BITRATE

        if not args.nomin and bitrate < MIN_BITRATE:
            # Bitrate below MIN_BITRATE is limited value
            warn(f"Not converting to {bitrate} since below minumum allowed {MIN_BITRATE}")
            return


        if args.wav:
            destination = Format('wav', bitdepth = bitdepth,
                                 samplerate = samplerate)
        elif args.flac:
            destination = Format('flac', bitdepth = bitdepth)
        else:
            destination = Format('mp3', bitrate)

        print(f"Converting audio file : {audioIn} : {song} {song.format}-> {destination}")
        if song.format == destination:
            info("No conversion necessary")
            return

        title = song.title
        if args.variant:
            title += " (" + str(destination.qualityAsString) + ")"

        if args.collection:
            outFile=f"{song.rootDirectory}/{args.collection}/{song.pathInCollection}/{title} - {song.album} - {song.artist}.{destination.ext}"
        else:
            outFile=f"./{title} - {song.artist} - {song.album}.{destination.ext}"

        Path(outFile).parent.mkdir(parents = True, exist_ok = True)

        channels = Channels(1) if args.mono else Channels(2)
        ffmpegArgs = {
            **destination.ffmpegArgs,
            **channels.ffmpegArgs,
            **song.ffmpegArgs
        }
        ffmpegArgs['metadata:g:0']=f"title={title}"
        if args.seconds is not None:
            start = int(args.start) if args.start is not None else 0
            end = int(args.seconds) + start
            ffmpegArgs['ss'] = start
            ffmpegArgs['to'] = end

        print(f"ffmpeg args : {ffmpegArgs}")
        (
            ffmpeg
                .input(audioIn)
                .filter_('loudnorm')
                .output(outFile, **ffmpegArgs)
                .run(**{
                    'quiet':args.quiet,
                    'overwrite_output':args.replace
                })
        )
