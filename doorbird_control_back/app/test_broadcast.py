import socket

class TestBroadcaster:
    def __init__(self, port = 6524):
        self.port = port
    
    def broadcast(self, message: bytes):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(message, ('chime', self.port))
