import eyed3
import os
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.wavpack import WavPack
from tinytag import TinyTag
import wave
from song import Song

NA = "n/a"
EXPECTED_SAMPLE_RATE = 44
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
        "bitrate"    : int(audio.info.bitrate / 1000),
        "samplerate" : int(audio.info.sample_rate / 1000),
        "length"     : int(audio.info.length)
    }

def oggHandler(file):
    audio = OggVorbis(file)
    tag = TinyTag.get(file)
    return {
        "bitrate"    : int(audio.info.bitrate / 1000),
        "samplerate" : int(audio.info.sample_rate / 1000),
        "length"     : int(audio.info.length)
    }

def wavHandler(file):
    tag = TinyTag.get(file)
    with wave.open(file) as w:
        return {
            "bitrate"    : int(w.getnchannels() * w.getsampwidth() * 8 * w.getframerate() / 1000),
            "samplerate" : int(w.getframerate() / 1000),
            "length"     : int(w.getnframes() / float(w.getframerate()))
        }

def defaultHandler(file):
    return {
        "bitrate"    : -1,
        "samplerate" : -1,
        "length"     : -1
    }

def run():
    header = f" : {'ext':4s} : {'kb/s':>5s} : {'kb':>5s} : {'s':>5s} : {'artist':20s} : {'title':30s} : {'album':20s}"
    files.sort()
    lastParent = ""
    for file in files:
        path = Path(file)
        if (path.parent != lastParent):
            print("")
            print(f"file  {path.parent.name:>43s}/" + header)
            print(170*"-")
            lastParent = path.parent
        ext = path.suffix[1:]
        stem = path.stem
        filesize = int(os.path.getsize(file) / 1024)
        meta = {
            "mp3" : mp3Handler,
            "ogg" : oggHandler,
            "wav" : wavHandler
        }.get(ext, defaultHandler)(file)
        notes=""
        song = Song(file, False)
        # Report any sample rates below 44Mhz, i.e. below expected
        if (meta['samplerate'] < EXPECTED_SAMPLE_RATE):
            notes+=f" low sample rate = {meta['samplerate']}Mhz"
        if (song.year != NA):
            notes+=f" {song.year}"
        print(f"{stem:50s} : {ext:4s} : " +
            f"{meta['bitrate']:5d} : "+
            f"{filesize:5d} : " +
            f"{meta['length']:5d} : {song.artist:20s} : " +
            f"{song.title:30s} : {song.album:20s} {notes}")
