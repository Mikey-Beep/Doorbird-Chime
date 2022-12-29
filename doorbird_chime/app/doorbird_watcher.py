import base64
from socket import *
from config import Config
from pathlib import Path
from encrypted_message import EncryptedMessage
from chime import Chime

class DoorbirdWatcher:
    def __init__(self, port: int = 6524):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', port))
    
    def watch(self, last_message: EncryptedMessage = EncryptedMessage()):
        print('Monitoring for doorbell events.')
        while 1:
            inbound_message = self.socket.recvfrom(1024)[0]
            # See if this is a message from the doorbell.
            try:
                encrypted_message = EncryptedMessage(inbound_message)
            except ValueError:
                continue
            # Load config from file, this lets us dynamically update the config.
            conf = Config(Path(__file__).parent.parent / 'conf' / 'conf.yml')
            # See if this is a duplicate of the last message.
            is_test_packet = encrypted_message != EncryptedMessage(base64.b64decode(conf.test_packet.encode('ascii')))
            if encrypted_message == last_message and not is_test_packet:
                print('Duplicate event.')
                continue
            print(encrypted_message)
            # Store a copy of this message for future comparison.
            if not is_test_packet:
                last_message = encrypted_message
                log_path = Path(__file__).parent.parent / 'log' / 'message_log.txt'
                log_path.parent.mkdir(parents=True, exist_ok=True)
                with log_path.open('w'):
                    log_path.write_text(f'{encrypted_message.message_bytes}\n')
            # Decode the message.
            try:
                decoded_message = encrypted_message.decrypt(conf.password)
            except:
                continue
            print(decoded_message)
            # Check that this event is for the correct user and that it is not a motion detection event.
            if conf.user[:6] == decoded_message.id and not decoded_message.event.startswith('motion'):
                print('Matched user name and this is a button press!')
                chime = Chime(conf)
                chime.make_noise()


if __name__ == '__main__':
    watcher = DoorbirdWatcher()
    watcher.watch()