from __future__ import annotations
from datetime import time
from pathlib import Path
import base64
import yaml


class Config:
    def __init__(self):
        self.password = ''
        self.user = ''
        self.sound_file = 'chime.wav'
        self.sleep_start = time(0, 0)
        self.sleep_end = time(0, 0)
        self.test_message = b''
        self.log_rotation_length = 100
        self.doorbell_ip = '127.0.0.1'
        self.event_retention_count = 100
        self.ping_freq = 4000
        self.ping_vol = 40
        self.ping_dur = 100

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
        output['test_packet'] = base64.b64encode(
            self.test_message).decode('ascii')
        output['log_rotation_length'] = self.log_rotation_length
        output['doorbell_ip'] = self.doorbell_ip
        output['event_retention_count'] = self.event_retention_count
        output['ping_freq'] = self.ping_freq
        output['ping_vol'] = self.ping_vol
        output['ping_dur'] = self.ping_dur
        return output

    def update(self, config: dict[str, any]) -> None:
        try:
            self.password = config['password']
        except KeyError:
            pass
        try:
            self.user = config['user']
        except KeyError:
            pass
        try:
            self.sound_file = config['sound_file']
        except KeyError:
            pass
        try:
            self.sleep_start = time.fromisoformat(config['sleep_start'])
        except (KeyError, ValueError):
            pass
        try:
            self.sleep_end = time.fromisoformat(config['sleep_end'])
        except (KeyError, ValueError):
            pass
        try:
            self.test_message = base64.b64decode(
                config['test_packet'].encode('ascii'))
        except (KeyError, ValueError):
            pass
        try:
            self.log_rotation_length = int(config['log_rotation_length'])
        except (KeyError, ValueError):
            pass
        try:
            self.doorbell_ip = config['doorbell_ip']
        except KeyError:
            pass
        try:
            self.event_retention_count = int(config['event_retention_count'])
        except (KeyError, ValueError):
            pass
        try:
            self.ping_freq = int(config['ping_freq'])
        except (KeyError, ValueError):
            pass
        try:
            self.ping_vol = int(config['ping_vol'])
        except (KeyError, ValueError):
            pass
        try:
            self.ping_dur = int(config['ping_dur'])
        except (KeyError, ValueError):
            pass
