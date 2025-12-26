import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

key = os.environ.get("ENCRYPTION_KEY")

cipher_suite = Fernet(key.encode())

def encrypt_content(content: str) -> str:
  if not content:
    return content
  return cipher_suite.encrypt(content.encode("utf-8")).decode("utf-8")

def decrypt_content(encrypted_content: str) -> str:
  if not encrypted_content:
    return encrypted_content
  try:
    return cipher_suite.decrypt(encrypted_content.encode("utf-8")).decode("utf-8")
  except Exception as e:
    # Fallback: If decryption fails, assume it's original content (pre-migration)
    # or return the encrypted string if it was encrypted but key is wrong
    return encrypted_content
