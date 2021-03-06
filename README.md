# Background

Audio Archivist.

Helps manage collection of audio assets, with reporting on audio resolution,
opinionated file naming, audio tagging and audio conversion.

## Pre-requisites

Install [taglib](https://taglib.org/), e.g. on mac

    brew install taglib

And install the pytaglib python library

    pip3 install pytaglib

If you want to use `aconvert` you'll also need [ffmpeg](https://ffmpeg.org/),
e.g. on mac

    brew install ffmpeg

## tl;dr

Install

    pip3 install -r requirements.txt
    pip3 install -e .

Report on audio meta data

    ameta

And convert an audio file to release format

    aconvert my.wav

## Meta data configuration

The meta data for the audio files can be taken from the file and directory
naming, and if you want be written directly to the audio files so that when the
audio file is run on audio players you see the desired song name, album name and
artist name.

To take meta data from file names, place the audio file in a directory named
as the album name, and place the album directory in a directory named after the
artist.

Meta data can also be overridden by creating a `meta.yaml` file in current
directory or parent directory to define artist and album metadata, e.g

    song:
      artist: Me

With this structure in place open up the command line in the artist directory
(or directory above that if you're sorting out multiple artists), and run

    ameta -n

This will report on the meta data that you can then apply with:

    ameta -sn

If you want to also rename the files using a consistent naming pattern (with
artist, album and song name in), then run

    ameta -snr

Create a `meta-root.yaml` in the root directory of your audio files to provide
support for collections.

## Command line arguments

See supported command line arguments with

    ameta -h
    aconvert -h

## Creating variety of audio file formats for testings

Create a variety of audio formats from a given audio file in a sub-directory
called `Test`.

    atest my.wav

This can help you decide what format is best for your specific purpose.

## Running Tests

    pytest

With coverage

    pytest --cov=. --cov-report term-missing
