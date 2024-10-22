"""This module is responsible for handling the configuration for the doorbell."""
from __future__ import annotations
from datetime import time
from pathlib import Path
import base64
import yaml


class Config:
    """The object holding the configuration.
    """
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
        self.ping_freq = '45:10'
        self.ping_dur = 2
        self.plex_ping_freq = '45::10'
        self.plex_ping_dur = 3

    @classmethod
    def from_yaml(cls, config_path: Path) -> Config:
        """Creates a Config from a yaml file.
        """
        with config_path.open() as config_file:
            config = yaml.safe_load(config_file)
        new_config = Config()
        new_config.update(config)
        return new_config

    def to_yaml(self) -> str:
        """Writes a Config to a yaml file.
        """
        return yaml.dump(self.to_dict())

    def to_dict(self) -> dict[str, any]:
        """Converts a Config to a dictionary.
        """
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
        output['ping_dur'] = self.ping_dur
        output['plex_ping_freq'] = self.plex_ping_freq
        output['plex_ping_dur'] = self.plex_ping_dur
        return output

    def update(self, config: dict[str, any]) -> None:
        """Updates the current config from a dictionary.
        """
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
            self.ping_freq = config['ping_freq']
        except KeyError:
            pass
        try:
            self.ping_dur = int(config['ping_dur'])
        except (KeyError, ValueError):
            pass
        try:
            self.plex_ping_freq = config['plex_ping_freq']
        except KeyError:
            pass
        try:
            self.plex_ping_dur = int(config['plex_ping_dur'])
        except (KeyError, ValueError):
            pass
