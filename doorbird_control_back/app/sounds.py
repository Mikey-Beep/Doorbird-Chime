"""This module is respobsible for managing sound files.
"""
from pathlib import Path


class SoundManager:
    """This class manages the sounds directory.
    """
    def __init__(self):
        self.sound_directory = Path(__file__).parent.parent / 'sounds'

    def list_sounds(self) -> list[str]:
        """Generates a list of sound files stored in the sound directory.
        """
        return sorted([item.name for item in self.sound_directory.iterdir()])
