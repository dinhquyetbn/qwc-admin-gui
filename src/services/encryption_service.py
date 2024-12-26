import os
from cryptography.fernet import Fernet

class EncryptionService:
    # key = Fernet.generate_key()
    key = b'OMw5Ca8eXcePrU1BeGYZYnK4qFKOAozC4u412U-4864='
    cipher_suite = Fernet(key)

    def __init__(self):
        '''
        '''

    def encode_text(self, value):
        encrypted_password = self.cipher_suite.encrypt(value.encode())
        return encrypted_password.decode('utf-8')

    def decode_text(self, value_hash):
        decrypted_password = self.cipher_suite.decrypt(value_hash).decode()
        return decrypted_password