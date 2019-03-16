import sys
from pathlib import Path
import os


class Destination:
    def __repr__(self):
        return f"{self.format} : {self.quality}"

    def __init__(self, format, quality):
        self.format = format
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
    path = Path(audioIn)
    title = path.stem.split('-')[0].strip()
    print(f"Converting audio files for testing : {audioIn} : {title}")
    if not os.path.exists(title):
        print(f"Making directory {title}")
        os.makedirs(title)
    for destination in destinations:
        for channels in channelsList:
            print(f"Converting {destination} : {channels}")
