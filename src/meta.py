import hiyapyco
from pathlib import Path

METAFILENAME="meta.yaml"
# If the root meta file is found then parental scanning will stop
ROOT_METAFILENAME="meta-root.yaml"
MAXDEPTH=5

def _Meta__findMetaFiles(path, depth):
    metadataFile = path.parent.resolve().joinpath(METAFILENAME)
    metadataFiles = []
    if metadataFile.exists():
        metadataFiles.extend([metadataFile.as_posix()])

    rootMetadataFile = path.parent.resolve().joinpath(ROOT_METAFILENAME)
    if rootMetadataFile.exists():
        metadataFiles.extend([rootMetadataFile.as_posix()])
        return {
            "files" : metadataFiles,
            "root" : rootMetadataFile
        }
    else:
        parentMetaFiles = _Meta__findMetaFiles(path.parent.resolve(), depth+1)
        if depth < MAXDEPTH :
            metadataFiles.extend(parentMetaFiles['files'])
        return {
            "files" : metadataFiles,
            "root" : parentMetaFiles["root"]
        }


def _Meta__loadMetadata(path, depth):
    metadataFiles = _Meta__findMetaFiles(path, 0)
    return {
        "data" : hiyapyco.load(metadataFiles["files"], method=hiyapyco.METHOD_MERGE),
        "root" : metadataFiles["root"]
    }

class Meta:
    def __init__(self, filename):
        self.filename = filename
        path = Path(filename)
        metadata = __loadMetadata(path, 0)
        self.data = metadata["data"]
        self.data["root"] = metadata["root"]
