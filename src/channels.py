class Channels:
    def __repr__(self):
        return "Mono" if self.channels == 1 else "Stereo"

    def __init__(self, channels):
        self.channels = channels
        self.channels = channels
