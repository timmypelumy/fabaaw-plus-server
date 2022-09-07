from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    app_name : str = "Fabaaw Plus"
    slugged_app_name : str = "FabaawPlus"
    tagline : str  = "Securing your identity"
    env : str = "development"
    db_url : str = 'mongodb://localhost:27017'
    token_expiration : int = 30
    secret_key : str = os.urandom(128).hex()
    hash_algorithm : str = 'HS256'
    client_url : str = 'http://localhost:3000'