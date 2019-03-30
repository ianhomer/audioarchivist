import os

from pathlib import Path
from shutil import copyfile

class Storage:
    def __init__(self):
        self.fileDirectory = os.path.dirname(__file__)
        self.testDirectory = os.path.join(self.fileDirectory)
        self.storageDirectory = os.path.join(self.testDirectory, "storage")
        self.tmpDirectory = os.path.join(self.testDirectory, "tmp")
        self.protoypes = {
            "ameta-root": self.storageDirectory + "/prototypes/ameta-root.yaml",
            "meta-artist": self.storageDirectory + "/prototypes/meta-artist.yaml",
            "meta-empty": self.storageDirectory + "/prototypes/meta-empty.yaml",
            "meta-naming-artist-and-title": self.storageDirectory + "/prototypes/meta-naming-title-and-artist.yaml",
            "mp3": self.storageDirectory + "/prototypes/Test000 - prototypes - Purpley.mp3"
        }

    def filename(self, relativeFilename):
        return os.path.join(self.storageDirectory, relativeFilename)

    def tmpFilename(self, relativeFilename):
        return os.path.join(self.tmpDirectory, relativeFilename)

    def createTmpDirectory(self, relativeFilename):
        directory = os.path.join(self.tmpDirectory, relativeFilename)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def tmpRemove(self, name):
        path = Path(self.tmpFilename(name))
        if path.is_dir():
            path.rmdir()
        else:
            path.unlink()

    def tmp(self, protoype, name):
        newFilename = os.path.join(self.tmpDirectory, name)
        directory = Path(newFilename).parent
        if not os.path.exists(directory):
            print(f"Making tests tmp directory {directory}")
            os.makedirs(directory)
        self.initialiseMeta(name)
        copyfile(self.protoypes[protoype], newFilename)
        return newFilename

    def initialiseMeta(self, name):
        if name.startswith('meta'):
            rootDirectory = name.split('/')[0]
            rootMetaFile = os.path.join(self.tmpDirectory, rootDirectory, ".ameta-root.yaml")
            if not os.path.exists(rootMetaFile):
                copyfile(self.protoypes["ameta-root"], rootMetaFile)
