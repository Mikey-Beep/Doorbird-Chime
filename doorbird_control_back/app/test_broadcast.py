"""This module is responsible for sending test broadcasts.
"""
import socket


class TestBroadcaster:
    """This class handles sending test broadcasts.
    """
    def __init__(self, port=6524):
        self.port = port

    def broadcast(self, message: bytes) -> None:
        """Sends a test broadcast, emulating the doorbell.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(message, ('core', self.port))
