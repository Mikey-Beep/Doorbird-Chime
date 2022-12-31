import yaml, base64
from datetime import time
from pathlib import Path
from encrypted_message import EncryptedMessage

class Config:
    def __init__(self, conf_path: Path):
        # Open the config file and read it safely as yaml.
        with conf_path.open() as conf_file:
            config = yaml.safe_load(conf_file)
        # Pull config settings from the yaml.
        self.password = config['password']
        self.user = config['user']
        # Get the chime sound file from the sounds directory.
        self.chime_sound_path = Path(__file__).parent.parent / 'sounds' / config['sound_file']
        self.sleep_start =  time(*list(map(int, config['sleep_start'].split(':'))))
        self.sleep_end = time(*list(map(int, config['sleep_end'].split(':'))))
        self.test_message = EncryptedMessage(base64.b64decode(config['test_packet'].encode('ascii')))
        self.log_rotation_length = config['log_rotation_length']