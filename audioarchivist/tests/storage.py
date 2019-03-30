import os

from pathlib import Path
from shutil import copyfile

testDirectory = os.path.join(os.path.dirname(__file__))
storageDirectory = os.path.join(testDirectory, "storage")
tmpDirectory = os.path.join(testDirectory, "tmp")

protoypes = {
    "ameta-root": storageDirectory + "/prototypes/ameta-root.yaml",
    "meta-artist": storageDirectory + "/prototypes/meta-artist.yaml",
    "meta-empty": storageDirectory + "/prototypes/meta-empty.yaml",
    "meta-naming-artist-and-title": storageDirectory + "/prototypes/meta-naming-title-and-artist.yaml",
    "mp3": storageDirectory + "/prototypes/Test000 - prototypes - Purpley.mp3"
}

class Storage:
    def __init__(self):
        self.tmpDirectory = tmpDirectory
        self.storageDirectory = storageDirectory

    def filename(self, relativeFilename):
        return os.path.join(storageDirectory, relativeFilename)

    def tmpFilename(self, relativeFilename):
        return os.path.join(tmpDirectory, relativeFilename)

    def tmpRemove(self, name):
        path = Path(self.tmpFilename(name))
        if path.is_dir():
            path.rmdir()
        else:
            path.unlink()

    def tmp(self, protoype, name):
        newFilename = os.path.join(tmpDirectory, name)
        directory = Path(newFilename).parent
        if not os.path.exists(directory):
            print(f"Making tests tmp directory {directory}")
            os.makedirs(directory)
        self.initialiseMeta(name)
        copyfile(protoypes[protoype], newFilename)
        return newFilename

    def initialiseMeta(self, name):
        if name.startswith('meta'):
            rootDirectory = name.split('/')[0]
            rootMetaFile = os.path.join(tmpDirectory, rootDirectory, ".ameta-root.yaml")
            if not os.path.exists(rootMetaFile):
                copyfile(protoypes["ameta-root"], rootMetaFile)
