from unittest import TestCase

from audioarchivist.format import Format

class TestFormat(TestCase):
    def test_create(self):
        format = Format('mp3', 256)
        self.assertEqual(f"{format}", "mp3 256kbs 44.1Mhz")
        self.assertEqual(format.ffmpegArgs["b:a"], "256k")
