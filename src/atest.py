import sys
from pathlib import Path
import os
import ffmpeg

class Destination:
    def __repr__(self):
        return f"{self.quality} {self.ext}"

    @property
    def variationName(self):
        if self.ext == "ogg":
            return f"q{self.quality}"
        else:
            return f"{self.quality}k"

    def __init__(self, ext, quality):
        self.ext = ext
        self.quality = quality

class Channels:
    def __repr__(self):
        return "Mono" if self.channels == 1 else "Stereo"

    def __init__(self, channels):
        self.channels = channels
        self.channels = channels


destinations = [
    Destination('ogg', 1),
    Destination('ogg', 5)
]

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
            print(f"Converting {destination} : {channels}")
            outFile=f"{title}/{title} - {channels} {destination.variationName}.{destination.ext}"
            stream = ffmpeg.input(audioIn)
            stream = ffmpeg.output(stream, outFile)
            ffmpeg.run(stream)
