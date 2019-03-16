import sys
from pathlib import Path
import os
import ffmpeg

replace = True
quiet = True
ogg = False
mp3 = True
m4a = False

class Destination:
    def __repr__(self):
        return f"{self.quality} {self.ext}"

    @property
    def variationName(self):
        if self.ext == "ogg":
            return f"q{self.quality}"
        else:
            return f"{self.quality}k"

    @property
    def ffmpegArgs(self):
        if self.ext == "ogg":
            return {"qscale:a":self.quality}
        else:
            return {"b:a":f"{self.quality}k"}

    def __init__(self, ext, quality):
        self.ext = ext
        self.quality = quality

class Channels:
    def __repr__(self):
        return "Mono" if self.channels == 1 else "Stereo"

    def __init__(self, channels):
        self.channels = channels
        self.channels = channels


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
    path = Path(audioIn)
    title = path.stem.split('-')[0].strip()
    print(f"Converting audio files for testing : {audioIn} : {title}")
    if not os.path.exists(title):
        print(f"Making directory {title}")
        os.makedirs(title)

    for destination in destinations:
        for channels in channelsList:
            print(f"Converting {destination} : {channels} : {destination.ffmpegArgs}")
            outFile=f"{title}/{title} - {channels} {destination.variationName}.{destination.ext}"
            (
                ffmpeg
                    .input(audioIn)
                    .output(outFile, **destination.ffmpegArgs)
                    .run(**{
                        'quiet':quiet,
                        'overwrite_output':replace
                    })
            )
