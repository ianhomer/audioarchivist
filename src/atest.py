import sys
import os
import ffmpeg

from format import Format
from channels import Channels
from song import Song

replace = False
quiet = True
ogg = True
mp3 = True
m4a = True
flac = True

destinations = []
if ogg:
    destinations.extend([
        Format('ogg', quality = 1),
        Format('ogg', quality = 5),
        Format('ogg', quality = 10)
    ])
if mp3:
    destinations.extend([
        Format('mp3', 32),
        Format('mp3', 64),
        Format('mp3', 128),
        Format('mp3', 256)
    ])
if m4a:
    destinations.extend([
        Format('m4a', 32),
        Format('m4a', 64),
        Format('m4a', 128),
        Format('m4a', 256)
    ])
if flac:
    destinations.extend([
        Format('flac', bitdepth = 16),
        Format('flac', bitdepth = 32)
    ])

channelsList = [Channels(1), Channels(2)]

def run():
    audioIn = sys.argv[1]
    if not os.path.exists(audioIn):
        print(f"File {audioIn} does not exist")
        return
    song = Song(audioIn)
    print(f"Converting audio files for testing : {audioIn} : {song}")
    if not os.path.exists(song.title):
        print(f"Making directory {song.title}")
        os.makedirs(song.title)

    for destination in destinations:
        for channels in channelsList:
            ffmpegArgs = {
                **destination.ffmpegArgs,
                **channels.ffmpegArgs,
                **song.ffmpegArgs
            }
            outFile=f"{song.title}/{song.title} - {song.artist} - {channels} {destination.variationName}.{destination.ext}"
            if replace or not os.path.exists(outFile):
                print(f"Converting {destination} : {channels} : {ffmpegArgs}")
                (
                    ffmpeg
                        .input(audioIn)
                        .output(outFile, **ffmpegArgs)
                        .run(**{
                            'quiet':quiet,
                            'overwrite_output':replace
                        })
                )
            else:
                print(f"Already converted {destination}")
