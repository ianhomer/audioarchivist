#!/usr/bin/env python3

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
    files.extend(list(filter(lambda f : Path(f).suffix[1:] in audioExtensions, filenames)))
    break

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
    print(f"{'name':30s} : {'ext':4s} : {'kb/s':>5s} : {'s':>5s} : " +
        f"{'artist':10s} : {'title':15s} : album")
    print(80*"-")
    files.sort()
    for file in files:
        path = Path(file)
        ext = path.suffix[1:]
        stem = path.stem
        meta = {
            "mp3" : mp3Handler,
            "ogg" : oggHandler
        }.get(ext, defaultHandler)(file)
        print(f"{stem:30s} : {ext:4s} : {meta['bitrate']:5d} : " +
            f"{meta['length']:5d} : {meta['artist']:10s} : " +
            f"{meta['title']:15s} : {meta['album']}")
