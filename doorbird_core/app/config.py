import yaml, base64
from datetime import time
from pathlib import Path
from encrypted_message import EncryptedMessage

class Config:
    def __init__(self):
        self.password = ''
        self.user = ''
        self.sound_file = 'chime.wav'
        self.sleep_start = time(0, 0)
        self.sleep_end = time(0, 0)
        self.test_message = EncryptedMessage()
        self.log_rotation_length = 100

    @classmethod
    def from_yaml(cls, conf_path: Path):
        with conf_path.open() as conf_file:
            config = yaml.safe_load(conf_file)
        new_config = Config()
        try:
            new_config.password = config['password']
        except: pass
        try:
            new_config.user = config['user']
        except: pass
        try:
            new_config.sound_file = config['sound_file']
        except: pass
        try:
            new_config.sleep_start =  time.fromisoformat(config['sleep_start'])
        except: pass
        try:
            new_config.sleep_end = time.fromisoformat(config['sleep_end'])
        except: pass
        try:
            new_config.test_message = EncryptedMessage(base64.b64decode(config['test_packet'].encode('ascii')))
        except: pass
        try:
            new_config.log_rotation_length = config['log_rotation_length']
        except: pass
        return new_config
    
    def to_yaml(self):
        output = {}
        output['password'] = self.password
        output['user'] = self.user
        output['sound_file'] = self.sound_file
        output['sleep_start'] = self.sleep_start.isoformat()
        output['sleep_end'] = self.sleep_end.isoformat()
        output['test_packet'] = base64.b64encode(self.test_message.message_bytes).decode('ascii')
        output['log_rotation_length'] = self.log_rotation_length
        return yaml.dump(output)