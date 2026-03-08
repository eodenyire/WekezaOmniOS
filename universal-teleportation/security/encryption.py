from cryptography.fernet import Fernet

class EncryptionManager:

    def __init__(self):

        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data):

        return self.cipher.encrypt(data)

    def decrypt(self, data):

        return self.cipher.decrypt(data)
