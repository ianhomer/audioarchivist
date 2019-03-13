import eyed3
import os
from pathlib import Path

audioExtensions = ["mp3", "wav", "ogg"]

files = []
for (dirpath, dirnames, filenames) in os.walk("."):
    files.extend(list(filter(lambda f : Path(f).suffix[1:] in audioExtensions, filenames)))
    break

def mp3handler(file):
    audio = eyed3.load(file)
    return {
        "album"     : audio.tag.album,
        "artist"    : audio.tag.artist,
        "title"     : audio.tag.title
    }

def defaultHandler(file):
    return {
        "album"     : "n/a",
        "artist"    : "n/a",
        "title"     : "n/a"
    }

print(f"{'ext':4s} : {'name':30s} : {'artist':10s} : {'title':15s} : album")
print(80*"-")
for file in files:
    path = Path(file)
    ext = path.suffix[1:]
    stem = path.stem
    meta = {"mp3" : mp3handler}.get(ext, defaultHandler)(file)
    print(f"{ext:4s} : {stem:30s} : {meta['artist']:10s} : {meta['title']:15s} : {meta['album']}")
