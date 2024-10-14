from cryptography.fernet import Fernet

# Generate and store an encryption key securely
def generate_key():
    """Generate and save a new encryption key."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the previously generated encryption key
def load_key():
    """Load the encryption key from a file."""
    return open("secret.key", "rb").read()

# Encrypt data using the encryption key
def encrypt_data(data):
    """Encrypt the given data."""
    key = load_key()  # Load the encryption key
    fernet = Fernet(key)  # Initialize Fernet with the key
    encrypted_data = fernet.encrypt(data.encode())  # Encrypt the data
    return encrypted_data

# Decrypt data using the encryption key
def decrypt_data(encrypted_data):
    """Decrypt the given encrypted data."""
    key = load_key()  # Load the encryption key
    fernet = Fernet(key)  # Initialize Fernet with the key
    decrypted_data = fernet.decrypt(encrypted_data).decode()  # Decrypt the data
    return decrypted_data
