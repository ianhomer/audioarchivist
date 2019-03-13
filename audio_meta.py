import eyed3
from os import walk


files = []
for (dirpath, dirnames, filenames) in walk("."):
    files.extend(list(filter(lambda f : f.endswith(".mp3"), filenames)))
    break

for file in files:
    print(file)
    audio = eyed3.load(file)
    if (audio.tag):
        print("Artist : %s" % audio.tag.artist)
    else:
        print("No audio tag")
