import base64
from socket import *
from config import Config
from pathlib import Path
from encrypted_message import EncryptedMessage
from chime import Chime

class DoorbirdWatcher:
    def __init__(self, port: int):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', port))
    
    def watch(self):
        # Build a blank message for comparison.
        last_message = EncryptedMessage()
        print('Monitoring for doorbell events.')
        while 1:
            mess = self.socket.recvfrom(1024)[0]
            # See if this is a message from the doorbell.
            try:
                mess = EncryptedMessage(mess)
            except ValueError:
                continue
            # Load config from file, this lets us dynamically update the config.
            conf = Config(Path(__file__).parent.parent / 'conf' / 'conf.yml')
            # See if this is a duplicate of the last message.
            not_test_packet = mess != EncryptedMessage(base64.b64decode(conf.test_packet.encode('ascii')))
            if mess == last_message and not_test_packet:
                print('Duplicate event.')
                continue
            print(mess)
            # Store a copy of this message for future comparison.
            if not_test_packet:
                last_message = mess
                log_path = Path(__file__).parent.parent / 'log' / 'message_log.txt'
                log_path.parent.mkdir(parents=True, exist_ok=True)
                with log_path.open('w'):
                    log_path.write_text(f'{mess.message_bytes}\n')
            # Decode the message.
            try:
                decoded = mess.decrypt(conf.password)
            except:
                continue
            print(decoded)
            # Check that this event is for the correct user and that it is not a motion detection event.
            if conf.user[:6] == decoded.id and not decoded.event.startswith('motion'):
                print('Matched user name and this is a button press!')
                chime = Chime(conf)
                chime.make_noise()


if __name__ == '__main__':
    watcher = DoorbirdWatcher(6524)
    watcher.watch()