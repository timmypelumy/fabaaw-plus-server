from db import db
from .hashing import verify_password
from datetime import datetime, timedelta
from jose import jwt
from config import app_settings as settings


async def authenticate_user( username, password):
    user = await db.users.find_one({"email_address" : username})

    if not user:
        return None

    if verify_password(password, user['salt'], user['password_hash']):
        return user
    else:
        return False





def create_access_token( data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= settings.token_expiration)
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.hash_algorithm )
    return encoded_jwt