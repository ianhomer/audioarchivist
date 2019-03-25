class Format:
    def __repr__(self):
        return f"{self.ext} {self.qualityAsString}"

    @property
    def qualityAsString(self):
        if self.ext == "ogg":
            return f"{self.quality} {self.samplerate/1000}Mhz"
        else:
            return f"{self.bitrate}kbs {self.samplerate/1000}Mhz"

    @property
    def variationName(self):
        if self.ext == "ogg":
            return f"q{self.quality}"
        elif self.ext == "wav" or self.ext == "flac":
            return f"s{self.bitdepth}"
        else:
            return f"{self.bitrate}k"

    @property
    def ffmpegArgs(self):
        if self.ext == "ogg":
            return {
                "qscale:a":self.quality,
                "ar":f"{self.samplerate}"
            }
        elif self.ext == "flac":
            return {
                "c:a":"flac",
                "ar":f"{self.samplerate}",
                "compression_level":"12",
                "sample_fmt":f"s{32 if self.bitdepth == 24 else self.bitdepth}"
            }
        else:
            return {
                "b:a":f"{self.bitrate}k",
                "ar":f"{self.samplerate}"
            }

    def __init__(self, ext, bitrate = 256, quality = 5, samplerate = 44100, bitdepth = 24):
        self.ext = ext
        self.quality = quality
        self.bitrate = bitrate
        self.samplerate = samplerate
        self.bitdepth = bitdepth
