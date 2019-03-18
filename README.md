# Background

Collection of Utilities to Ease Management of Audio Assets

# Pre-requisites

    brew install taglib
    pip3 install pytaglib

# TL;DR;

install

    pip3 install -e src

report on audio meta data

    ameta

and convert to release format

    aconvert my.wav

# Creating reference files for testings

To create a variety of formats for testing use

    atest

# Local configuration of meta metadata

Create a meta.yaml file in current directory or parent directory to define
artist and album metadata, e.g

    song:
      artist: Me

# Fix meta tags

Fill in empty tags based on file naming

    ameta -s

Correct meta tags to those controlled by file naming (and meta.yaml files)

    ameta -sn
