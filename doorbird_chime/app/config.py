from pathlib import Path
import yaml

class Config:
    def __init__(self, conf_path: Path):
        # Open the config file and read it safely as yaml.
        with conf_path.open() as conf_file:
            config = yaml.safe_load(conf_file)
        # Pull config settings from the yaml.
        self.password = config['password']
        self.user = config['user']
        self.chime_sound = Path(__file__).parent.parent / 'sounds' / config['sound_file']
        self.sleep_start = config['sleep_start']
        self.sleep_end = config['sleep_end']