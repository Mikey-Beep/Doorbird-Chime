from socket import *
from encrypted_message import EncryptedMessage

class DoorbirdWatcher:
    def __init__(self, port: int = 6524):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', port))
    
    def watch(self) -> EncryptedMessage:
        print('Watching for doorbell events.')
        while 1:
            inbound_message = self.socket.recvfrom(1024)[0]
            try:
                return EncryptedMessage(inbound_message)
            except ValueError:
                continue