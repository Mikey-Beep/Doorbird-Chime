from pathlib import Path

class SoundManager:
    def __init__(self):
        self.sound_directory = Path(__file__).parent.parent / 'sounds'

    def list_sounds(self) -> list[str]:
        return sorted([item.name for item in self.sound_directory.iterdir()])