from decrypted_message import DecryptedMessage
from pathlib import Path

class DoorbirdLogger:
    def __init__(self):
        self.log_path = Path(__file__).parent.parent / 'log' / 'log.txt'

    def log(self, message: DecryptedMessage):
        with self.log_path.open() as log_file:
            logs = [line.strip() for line in log_file]
        with self.log_path.open('w+') as log_file:
            logs.append('\u16bc'.join([
                message.id,
                message.event,
                str(message.timestamp)
            ]))
            log_file.write('\n'.join(logs[-100:]))