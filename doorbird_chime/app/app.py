from encrypted_message import EncryptedMessage
from decrypted_message import DecryptedMessage
from doorbird_watcher import DoorbirdWatcher
from logger import DoorbirdLogger
from chime import Chime
from config import Config
from pathlib import Path

if __name__ == '__main__':
    last_message = EncryptedMessage()
    config_path = Path(__file__).parent.parent / 'conf' / 'conf.yml'
    watcher = DoorbirdWatcher()
    logger = DoorbirdLogger()
    while 1:
        encrypted_message = watcher.watch()
        config = Config(config_path)
        if encrypted_message == last_message and encrypted_message != config.test_message:
            print('Received a duplicate message, skipping it.')
            continue
        try:
            decrypted_message = encrypted_message.decrypt(config.password)
        except:
            print('Failed to decrypt message, skipping it.')
            continue
        if encrypted_message != config.test_message:
            logger.log(decrypted_message)
        if config.user[:6] == decrypted_message.id and not decrypted_message.event.startswith('motion'):
            print('Matched user name and this is a button press!')
            chime = Chime(config.chime_sound_path, config.sleep_start, config.sleep_end)
            chime.make_noise()