from __future__ import annotations
import base64, yaml
from datetime import time
from pathlib import Path

class Config:
    def __init__(self):
        self.password = ''
        self.user = ''
        self.sound_file = 'chime.wav'
        self.sleep_start = time(0, 0)
        self.sleep_end = time(0, 0)
        self.test_message = b''
        self.log_rotation_length = 100
        self.doorbell_ip = ''
        self.event_retention_count = 100

    @classmethod
    def from_yaml(cls, config_path: Path) -> Config:
        with config_path.open() as config_file:
            config = yaml.safe_load(config_file)
        new_config = Config()
        new_config.update(config)
        return new_config
    
    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict())

    def to_dict(self) -> dict[str, any]:
        output = {}
        output['password'] = self.password
        output['user'] = self.user
        output['sound_file'] = self.sound_file
        output['sleep_start'] = self.sleep_start.isoformat()
        output['sleep_end'] = self.sleep_end.isoformat()
        output['test_packet'] = base64.b64encode(self.test_message).decode('ascii')
        output['log_rotation_length'] = self.log_rotation_length
        output['doorbell_ip'] = self.doorbell_ip
        output['event_retention_count'] = self.event_retention_count
        return output

    def update(self, config: dict[str, any]) -> None:
        try:
            self.password = config['password']
        except: pass
        try:
            self.user = config['user']
        except: pass
        try:
            self.sound_file = config['sound_file']
        except: pass
        try:
            self.sleep_start =  time.fromisoformat(config['sleep_start'])
        except: pass
        try:
            self.sleep_end = time.fromisoformat(config['sleep_end'])
        except: pass
        try:
            self.test_message = base64.b64decode(config['test_packet'].encode('ascii'))
        except: pass
        try:
            self.log_rotation_length = int(config['log_rotation_length'])
        except: pass
        try:
            self.doorbell_ip = config['doorbell_ip']
        except: pass
        try:
            self.event_retention_count = int(config['event_retention_count'])
        except: pass