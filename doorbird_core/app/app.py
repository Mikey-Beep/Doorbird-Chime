from encrypted_message import EncryptedMessage
from doorbird_watcher import DoorbirdWatcher
from logger import DoorbirdLogger
from common.config.config import Config
from pathlib import Path
from datetime import *
import requests

def load_config(config_path: Path):
    try:
        config = Config.from_yaml(config_path)
        print('Config loaded.')
    except FileNotFoundError:
        print('Config file not found, creating it.')
        config = Config()
        config_path.parent.mkdir(parents = True, exist_ok = True)
        with config_path.open('w') as config_file:
            config_file.write(config.to_yaml())
    return config

def send_chime_req(sleep_start_time: time, sleep_end_time: time, sound_file: str):
    if datetime.now().time() > sleep_start_time or datetime.now().time() < sleep_end_time:
            print('Inside sleep time, not making a sound.')
            return
    url = 'http://chime/chime'
    requests.request("POST", url, json={'sound_file': sound_file})

if __name__ == '__main__':
    last_message = EncryptedMessage()
    config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
    config = load_config(config_path)
    with config_path.open('w') as config_file:
        config_file.write(config.to_yaml())
    watcher = DoorbirdWatcher()
    logger = DoorbirdLogger()
    while 1:
        encrypted_message = watcher.watch()
        config = load_config(config_path)
        if encrypted_message == last_message and encrypted_message != EncryptedMessage(config.test_message):
            print('Received a duplicate message, skipping it.')
            continue
        last_message = encrypted_message
        try:
            decrypted_message = encrypted_message.decrypt(config.password)
        except:
            print('Failed to decrypt message, skipping it.')
            continue
        if encrypted_message != EncryptedMessage(config.test_message):
            logger.log(decrypted_message, config.log_rotation_length)
        if config.user[:6] == decrypted_message.id and not decrypted_message.event.startswith('motion'):
            print('Matched user name and this is a button press!')
            requests.get('http://watcher/ring')
            send_chime_req(config.sleep_start, config.sleep_end, config.sound_file)
        elif config.user[:6] == decrypted_message.id:
            print('Matched user name and this is a motion event"')
            requests.request('GET', 'http://watcher/motion')