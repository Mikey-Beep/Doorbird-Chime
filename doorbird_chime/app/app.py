from encrypted_message import EncryptedMessage
from decrypted_message import DecryptedMessage
from doorbird_watcher import DoorbirdWatcher
from logger import DoorbirdLogger
from chime import Chime
from config import Config
from pathlib import Path

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

if __name__ == '__main__':
    last_message = EncryptedMessage()
    config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
    config = load_config(config_path)
    watcher = DoorbirdWatcher()
    logger = DoorbirdLogger()
    while 1:
        encrypted_message = watcher.watch()
        config = load_config(config_path)
        if encrypted_message == last_message and encrypted_message != config.test_message:
            print('Received a duplicate message, skipping it.')
            continue
        last_message = encrypted_message
        try:
            decrypted_message = encrypted_message.decrypt(config.password)
        except:
            print('Failed to decrypt message, skipping it.')
            continue
        if encrypted_message != config.test_message:
            logger.log(decrypted_message, config.log_rotation_length)
        if config.user[:6] == decrypted_message.id and not decrypted_message.event.startswith('motion'):
            print('Matched user name and this is a button press!')
            chime = Chime(config.chime_sound_path, config.sleep_start, config.sleep_end)
            chime.make_noise()