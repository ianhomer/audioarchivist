class Destination:
    def __repr__(self):
        return f"{self.quality} {self.ext}"

    @property
    def variationName(self):
        if self.ext == "ogg":
            return f"q{self.quality}"
        else:
            return f"{self.quality}k"

    @property
    def ffmpegArgs(self):
        if self.ext == "ogg":
            return {"qscale:a":self.quality}
        else:
            return {"b:a":f"{self.quality}k"}

    def __init__(self, ext, quality):
        self.ext = ext
        self.quality = quality
