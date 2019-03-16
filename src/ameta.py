import eyed3
import os
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.wavpack import WavPack

NA = "n/a"

audioExtensions = ["mp3", "wav", "ogg"]

files = []
for (dirpath, dirnames, filenames) in os.walk("."):
    files.extend(list(
        map(
            lambda name : os.path.join(dirpath, name),
            filter(lambda f : Path(f).suffix[1:] in audioExtensions, filenames))
        )
    )

def mp3Handler(file):
    id3 = eyed3.load(file)
    audio = MP3(file)
    return {
        "album"     : id3.tag.album or NA,
        "artist"    : id3.tag.artist or NA,
        "title"     : id3.tag.title or NA,
        "bitrate"   : int(audio.info.bitrate / 1000),
        "length"    : int(audio.info.length)
    }

def oggHandler(file):
    audio = OggVorbis(file)
    return {
        "album"     : NA,
        "artist"    : NA,
        "title"     : NA,
        "bitrate"   : int(audio.info.bitrate / 1000),
        "length"    : int(audio.info.length)
    }

def defaultHandler(file):
    return {
        "album"     : NA,
        "artist"    : NA,
        "title"     : NA,
        "bitrate"   : -1,
        "length"    : -1
    }

def run():
    header = f" : {'ext':4s} : {'kb/s':>5s} : {'kb':>5s} : {'s':>4s} : {'artist':20s} : {'title':30s} : album"
    print(f"{'name':50s}" + header)
    print(170*"-")
    files.sort()
    lastParent = ""
    for file in files:
        path = Path(file)
        if (path.parent != lastParent):
            print("")
            print(f"- - - {path.parent.name:>43s}/" + header)
            print(170*"-")
            lastParent = path.parent
        ext = path.suffix[1:]
        stem = path.stem
        filesize = int(os.path.getsize(file) / 1024)
        meta = {
            "mp3" : mp3Handler,
            "ogg" : oggHandler
        }.get(ext, defaultHandler)(file)
        print(f"{stem:50s} : {ext:4s} : {meta['bitrate']:5d} : " +
            f"{filesize:5d} :" +
            f"{meta['length']:5d} : {meta['artist']:20s} : " +
            f"{meta['title']:30s} : {meta['album']}")
