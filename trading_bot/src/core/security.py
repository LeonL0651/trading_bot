from cryptography.fernet import Fernet

class Security:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data).decode()