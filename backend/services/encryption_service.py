from cryptography.fernet import Fernet

class EncryptionService:

    _fernet = None

    @staticmethod
    def init(key: str):

        EncryptionService._fernet = Fernet(key)

    @staticmethod
    def encrypt_data(data: bytes) -> bytes:
        if not EncryptionService._fernet:
            raise ValueError("EncryptionService not initialized. Call EncryptionService.init(...) first.")
        return EncryptionService._fernet.encrypt(data)

    @staticmethod
    def decrypt_data(enc_data: bytes) -> bytes:
        if not EncryptionService._fernet:
            raise ValueError("EncryptionService not initialized. Call EncryptionService.init(...) first.")
        return EncryptionService._fernet.decrypt(enc_data)
