from decrypted_message import DecryptedMessage
from encrypted_message import EncryptedMessage
from pathlib import Path
import base64

class DoorbirdLogger:
    def __init__(self):
        self.log_path = Path(__file__).parent.parent / 'log' / 'log.txt'

    def log(self, encrypted_message: EncryptedMessage, decrypted_message: DecryptedMessage, log_rotation_length: int):
        try:
            with self.log_path.open() as log_file:
                logs = [line.strip() for line in log_file]
        except:
            logs = []
        with self.log_path.open('w+') as log_file:
            logs.append('\u16bc'.join([
                decrypted_message.id,
                decrypted_message.event,
                str(decrypted_message.timestamp),
                base64.b64encode(encrypted_message.message_bytes).decode('ascii')
            ]))
            log_file.write('\n'.join(logs[-log_rotation_length:]))