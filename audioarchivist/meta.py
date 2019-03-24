import hiyapyco
from pathlib import Path

METAFILENAME=".ameta.yaml"
# If the root meta file is found then parental scanning will stop
ROOT_METAFILENAME=".ameta-root.yaml"
MAXDEPTH=6

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
            "rootDirectory" : Path(rootMetadataFile).parent.resolve()
        }
    else:
        if depth < MAXDEPTH :
            parentMetaFiles = _Meta__findMetaFiles(path.parent.resolve(), depth+1)
            metadataFiles.extend(parentMetaFiles['files'])
            return {
                "files" : metadataFiles,
                "rootDirectory" : parentMetaFiles["rootDirectory"]
            }
        else:
            return {
                "files" : [],
                "rootDirectory" : None
             }


def _Meta__loadMetadata(path, depth):
    metadataFiles = _Meta__findMetaFiles(path, 0)
    return {
        "data" : hiyapyco.load(metadataFiles["files"], method=hiyapyco.METHOD_MERGE),
        "rootDirectory" : metadataFiles["rootDirectory"]
    }

class Meta:
    def __init__(self, filename):
        self.filename = filename
        path = Path(filename)
        metadata = __loadMetadata(path, 0)
        self.data = metadata["data"]
        if self.data is None:
            self.data = {}
        self.data["rootDirectory"] = metadata["rootDirectory"]
