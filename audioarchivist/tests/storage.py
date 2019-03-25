import os

from pathlib import Path
from shutil import copyfile

testDirectory = os.path.join(os.path.dirname(__file__))
storageDirectory = os.path.join(testDirectory, "storage")
tmpDirectory = os.path.join(testDirectory, "tmp")

protoypes = {
    "mp3": storageDirectory + "/prototypes/Test000 - prototypes - Purpley.mp3"
}

class Storage:
    def __init__(self):
        self.tmpDirectory = tmpDirectory
        self.storageDirectory = storageDirectory

    def filename(self, relativeFilename):
        return os.path.join(storageDirectory, relativeFilename)

    def tmp(self, protoype, name):
        newFilename = os.path.join(tmpDirectory, name)
        directory = Path(newFilename).parent
        if not os.path.exists(directory):
            print(f"Making tests tmp directory {directory}")
            os.makedirs(directory)
        copyfile(protoypes[protoype], newFilename)
        return newFilename
