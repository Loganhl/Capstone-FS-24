import pyotp

def generate_totp(secret):
    """Generate a TOTP (Time-based OTP) using a secret key."""
    totp = pyotp.TOTP(secret)
    return totp.now()  # This generates the current OTP
