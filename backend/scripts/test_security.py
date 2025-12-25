import sys
import os

# Add the parent directory to sys.path to allow importing from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.security import encrypt_content, decrypt_content

def test_encryption_flow():
  print("--- Testing Encryption Flow ---")
  original_text = "This is a secret message."
  print(f"Original: {original_text}")

  encrypted = encrypt_content(original_text)
  print(f"Encrypted: {encrypted}")

  if encrypted == original_text:
    print("FAILURE: Text was not encrypted.")
    return

  decrypted = decrypt_content(encrypted)
  print(f"Decrypted: {decrypted}")

  if decrypted == original_text:
    print("SUCCESS: Encryption/Decryption cycle works.")
  else:
    print(f"FAILURE: Decrypted text '{decrypted}' does not match original.")

def test_fallback():
  print("\n--- Testing Fallback Mechanism ---")
  plain_text = "This is not encrypted."
  # This should fail decryption and return the original text (fallback)
  result = decrypt_content(plain_text)
  print(f"Input: {plain_text}")
  print(f"Result: {result}")
  
  if result == plain_text:
    print("SUCCESS: Fallback mechanism works (returned original text).")
  else:
    print("FAILURE: Fallback mechanism failed.")

if __name__ == "__main__":
  try:
    test_encryption_flow()
    test_fallback()
  except Exception as e:
    print(f"FAILED with error: {e}")
    sys.exit(1)
