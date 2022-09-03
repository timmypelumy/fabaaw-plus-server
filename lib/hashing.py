import scrypt
import os


def hash_password(password: str):
    salt = os.urandom(64).hex()
    return {

        'hash': scrypt.hash(password,  salt).hex(),
        'salt': salt

    }

def verify_password(password: str, salt : str, hash : str):

    return hash ==  scrypt.hash(password, salt).hex() 