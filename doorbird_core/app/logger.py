"""This module handles logging of events from the doorbell messages.
"""
from collections import deque
from pathlib import Path
import base64
from decrypted_message import DecryptedMessage
from encrypted_message import EncryptedMessage


class DoorbirdLogger:
    """This class provides a persistent logger to write the messages.
    """
    def __init__(self):
        self.log_path = Path(__file__).parent.parent / 'log' / 'log.txt'

    def log(self, encrypted_message: EncryptedMessage,
            decrypted_message: DecryptedMessage,
            log_rotation_length: int):
        """Log the details of a message.
        """
        logs = deque(maxlen=log_rotation_length)
        try:
            with self.log_path.open() as log_file:
                logs.extend(line.strip() for line in log_file)
        except FileNotFoundError:
            pass
        with self.log_path.open('w+') as log_file:
            logs.append('\u16bc'.join([
                decrypted_message.id,
                decrypted_message.event,
                str(decrypted_message.timestamp),
                base64.b64encode(
                    encrypted_message.message_bytes).decode('ascii')
            ]))
            log_file.write('\n'.join(logs))
