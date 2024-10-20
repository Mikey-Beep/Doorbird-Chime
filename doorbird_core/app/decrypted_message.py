"""This module handles the messages sent by the doorbell after they have been decrypted.
"""
from __future__ import annotations
from datetime import datetime


class DecryptedMessage:
    """This class models the decrypted messages.
    """
    def __init__(self, cleartext: bytes):
        self.cleartext = cleartext
        # The ID of the device sending the alert.
        self.id = cleartext[:6].decode('utf-8')
        # The type of event sent this will either be 'motion'
        # or the product number of the device sending the alert.
        self.event = cleartext[6:14].decode('utf-8')
        # The UTC time as a timestamp.
        self.timestamp = datetime.utcfromtimestamp(
            int.from_bytes(cleartext[14:], 'big'))

    def __eq__(self, other: DecryptedMessage) -> bool:
        return self.cleartext == other.cleartext

    def __str__(self) -> str:
        return f'ID: {self.id}\nEVENT: {self.event}\nTIMESTAMP: {self.timestamp}'
