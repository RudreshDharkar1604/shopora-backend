from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError,VerificationError

ph = PasswordHasher()

def hash_password(password: str):
    return ph.hash(password)

def verify_password(plain: str, hashed: str):
    try:
        ph.verify(hashed, plain)
        return True
    except (VerifyMismatchError, VerificationError):
        return False