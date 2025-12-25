import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

_key = os.environ.get("ENCRYPTION_KEY")

if not _key:
  raise ValueError("ENCRYPTION_KEY environment variable is not set. Please add it to your .env file.")

cipher_suite = Fernet(_key.encode())

def encrypt_content(content: str) -> str:
  """Encrypts a string content."""
  if not content:
    return content
  return cipher_suite.encrypt(content.encode("utf-8")).decode("utf-8")

def decrypt_content(encrypted_content: str) -> str:
  """Decrypts a string content."""
  if not encrypted_content:
    return encrypted_content
  try:
    return cipher_suite.decrypt(encrypted_content.encode("utf-8")).decode("utf-8")
  except Exception as e:
    # Fallback: If decryption fails, assume it might be plain text (migration support)
    # or return the encrypted string if it was indeed encrypted but key is wrong.
    # print(f"Decryption error (returning original): {e}")
    return encrypted_content
