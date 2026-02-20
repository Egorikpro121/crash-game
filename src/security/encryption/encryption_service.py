"""Encryption service."""
from src.security.encryption import encrypt_data, decrypt_data


class EncryptionService:
    """Encryption service wrapper."""
    
    def encrypt(self, data: str) -> str:
        """Encrypt data."""
        return encrypt_data(data)
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data."""
        return decrypt_data(encrypted_data)
