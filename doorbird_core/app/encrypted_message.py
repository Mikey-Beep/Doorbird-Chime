from __future__ import annotations
from nacl import pwhash, secret, bindings
from decrypted_message import DecryptedMessage

class EncryptedMessage:
    def __init__(self, message_bytes: bytes = b'\xde\xad\xbe\x01'):
        self.message_bytes = message_bytes
        # Check for the doorbird signature.
        if message_bytes[:4] != b'\xde\xad\xbe\x01':
            raise ValueError('Not a doorbird event.')
        # This is the doorbird signature in its individual pieces.
        self.ident = message_bytes[:3]
        self.version = message_bytes[3]
        #Allow creation of a dummy message if it lacks the remainder of the payload.
        try:
            # Try to get the decryption variables and encrypted cyphertext.
            self.opslimit = int.from_bytes(message_bytes[4:8], 'big')
            self.memlimit = int.from_bytes(message_bytes[8:12], 'big')
            self.salt = message_bytes[12:28]
            self.nonce = message_bytes[28:36]
            self.ciphertext = message_bytes[36:]
        except:
            pass

    def __eq__(self, other: EncryptedMessage) -> bool:
        # If a message has identical bytes then it is the same message.
        return self.message_bytes == other.message_bytes

    def __str__(self) -> str:
        return '\n'.join([
            f'IDENT: {self.ident}',
            f'VERSION: {self.version}',
            f'OPSLIMIT: {self.opslimit}',
            f'MEMLIMIT: {self.memlimit}',
            f'SALT: {self.salt}',
            f'NONCE: {self.nonce}',
            f'CIPHERTEXT: {self.ciphertext}'
        ])

    def decrypt(self, passwd: str) -> DecryptedMessage:
        """
        Decrypt the message using the provided password.
        """
        # Only the last 5 characters of the password are used!?
        passwd = passwd[:5].encode('utf-8')
        # Use the password and encryption variables to make a key.
        key = pwhash.argon2i.kdf(secret.SecretBox.KEY_SIZE, passwd, self.salt, opslimit = self.opslimit, memlimit = self.memlimit)
        # Use the key and nonce to decrypt the ciphertext.
        cleartext = bindings.crypto_aead_chacha20poly1305_decrypt(self.ciphertext, None, self.nonce, key)
        # Build a DecryptedMessage from the cleartext.
        return DecryptedMessage(cleartext)