"""Encryption utilities."""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

from src.config import get_secret_key


def get_encryption_key() -> bytes:
    """
    Get encryption key from secret key.
    
    Returns:
        Encryption key bytes
    """
    secret = get_secret_key().encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'crash_game_salt',  # In production, use random salt
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret))
    return key


def encrypt_data(data: str) -> str:
    """
    Encrypt data.
    
    Args:
        data: Data to encrypt
    
    Returns:
        Encrypted data (base64)
    """
    key = get_encryption_key()
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_data(encrypted_data: str) -> str:
    """
    Decrypt data.
    
    Args:
        encrypted_data: Encrypted data (base64)
    
    Returns:
        Decrypted data
    """
    key = get_encryption_key()
    f = Fernet(key)
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
    decrypted = f.decrypt(encrypted_bytes)
    return decrypted.decode()
