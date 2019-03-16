import sys
from pathlib import Path
import os

def run():
    audioIn = sys.argv[1]
    path = Path(audioIn)
    title = path.stem.split('-')[0].strip()
    print(f"Converting audio files for testing : {audioIn} : {title}")
    if not os.path.exists(title):
        print(f"Making directory {title}")
        os.makedirs(title)
