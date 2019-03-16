import sys
import os
import ffmpeg

from destination import Destination
from channels import Channels
from song import Song

replace = True
quiet = True
ogg = False
mp3 = True
m4a = False

destinations = []
if ogg:
    destinations.extend([
        Destination('ogg', 1),
        Destination('ogg', 5),
        Destination('ogg', 10)
    ])
if mp3:
    destinations.extend([
        Destination('mp3', 32),
        Destination('mp3', 64),
        Destination('mp3', 128),
        Destination('mp3', 256)
    ])
if m4a:
    destinations.extend([
        Destination('m4a', 32),
        Destination('m4a', 64),
        Destination('m4a', 128),
        Destination('m4a', 256)
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
            print(f"Converting {destination} : {channels} : {ffmpegArgs}")
            outFile=f"{song.title}/{song.title} - {channels} {destination.variationName}.{destination.ext}"
            (
                ffmpeg
                    .input(audioIn)
                    .output(outFile, **ffmpegArgs)
                    .run(**{
                        'quiet':quiet,
                        'overwrite_output':replace
                    })
            )
