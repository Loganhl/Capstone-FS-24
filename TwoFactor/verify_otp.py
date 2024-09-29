import pyotp

def verify_totp(secret, user_input_otp):
    """Verify if the user-input OTP matches the current TOTP."""
    totp = pyotp.TOTP(secret)
    return totp.verify(user_input_otp)
