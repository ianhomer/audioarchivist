import hiyapyco
from pathlib import Path

METAFILENAME="meta.props"
MAXDEPTH=5

def _Meta__findMetaFiles(path, depth):
    metadataFile = path.parent.resolve().joinpath(METAFILENAME)
    metadataFiles = []
    if metadataFile.exists():
        metadataFiles.extend([metadataFile.as_posix()])
    if depth < MAXDEPTH :
        metadataFiles.extend(_Meta__findMetaFiles(path.parent.resolve(), depth+1))
    return metadataFiles


def _Meta__loadMetadata(path, depth):
    metadataFiles = _Meta__findMetaFiles(path, 0)
    return hiyapyco.load(metadataFiles, method=hiyapyco.METHOD_MERGE)

class Meta:
    def __init__(self, filename):
        self.filename = filename
        path = Path(filename)
        self.data = __loadMetadata(path, 0)
