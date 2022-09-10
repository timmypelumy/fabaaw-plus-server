from pydantic import BaseSettings
import os
from typing import Dict

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
    ipfs_node_url: str = 'https://ipfs.infura.io:5001'
    infura_project_id : str = '2CASClsLixgaD7e6qlO5LfIYA4b'
    infura_project_secret : str = '3a6dfcb5e77b97ba69b90f55e1f7b326'
    ipfs_read_nodes: Dict = {
        'cloudflare': ' https://cloudflare-ipfs.com/ipfs'
    }