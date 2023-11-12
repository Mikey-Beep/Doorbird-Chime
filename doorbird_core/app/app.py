"""This module handles the monitoring of doorbell events.
"""
from pathlib import Path
from datetime import datetime, time
import requests
from encrypted_message import EncryptedMessage
from doorbird_listener import DoorbirdListener
from logger import DoorbirdLogger
from common.config.config import Config


def load_config(conf_path: Path):
    """Load the config from the yaml file.
    """
    try:
        conf = Config.from_yaml(conf_path)
        print('Config loaded.')
    except FileNotFoundError:
        print('Config file not found, creating it.')
        conf = Config()
        conf_path.parent.mkdir(parents=True, exist_ok=True)
        with conf_path.open('w') as conf_file:
            conf_file.write(conf.to_yaml())
    return conf


def send_chime_req(sleep_start_time: time, sleep_end_time: time, sound_file: str) -> None:
    """Trigger a chime event.
    """
    if all((sleep_start_time != sleep_end_time,
        (sleep_start_time < datetime.now().time() < sleep_end_time))):
        print('Inside sleep time, not making a sound.')
        return
    url = 'http://chime/chime'
    requests.post(url, json={'sound_file': sound_file}, timeout=10)


def send_ping_req() -> None:
    """Trigger a ping event.
    """
    url = 'http://chime/ping'
    requests.post(url, timeout=10)


if __name__ == '__main__':
    last_message = EncryptedMessage()
    config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
    config = load_config(config_path)
    with config_path.open('w') as config_file:
        config_file.write(config.to_yaml())
    listener = DoorbirdListener()
    logger = DoorbirdLogger()
    while 1:
        encrypted_message = listener.listen()
        config = load_config(config_path)
        if all((encrypted_message == last_message,
            encrypted_message != EncryptedMessage(config.test_message))):
            print('Received a duplicate message, skipping it.')
            continue
        last_message = encrypted_message
        try:
            decrypted_message = encrypted_message.decrypt(config.password)
        except:
            print('Failed to decrypt message, skipping it.')
            continue
        if encrypted_message != EncryptedMessage(config.test_message):
            logger.log(encrypted_message, decrypted_message,
                       config.log_rotation_length)
        if all((config.user[:6] == decrypted_message.id,
            not decrypted_message.event.startswith('motion'))):
            print('Matched user name and this is a button press!')
            requests.get('http://watcher/ring', timeout=10)
            send_chime_req(config.sleep_start,
                           config.sleep_end, config.sound_file)
        elif config.user[:6] == decrypted_message.id:
            print('Matched user name and this is a motion event.')
            requests.get('http://watcher/motion', timeout=10)
            send_ping_req()
