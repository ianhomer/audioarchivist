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
            return {
                "qscale:a":self.quality,
                "ar":f"{self.samplerate}"
            }
        else:
            return {
                "b:a":f"{self.quality}k",
                "ar":f"{self.samplerate}"
            }

    def __init__(self, ext, quality):
        self.ext = ext
        self.quality = quality
        self.samplerate = 44100
