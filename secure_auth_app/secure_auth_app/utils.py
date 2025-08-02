
import pyotp

def generate_otp_secret():
    return pyotp.random_base32()
