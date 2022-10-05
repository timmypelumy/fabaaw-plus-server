from pydantic import BaseSettings
from typing import Dict


class Settings(BaseSettings):
    app_name: str = "Fabaaw Plus"
    slugged_app_name: str = "FabaawPlus"
    tagline: str = "Securing your identity"
    env: str = "development"
    db_url: str = 'mongodb://localhost:27017'
    token_expiration: int = 30
    secret_key: str = "c3126bf2dc199fe90b3f50abc06e3a1afb899af286b073e966bc7927f79641f781482d52dcee6fe34c25b201faead36a5a617813f8ded6c7b699de2c30b3914b8e632fa4db3d1db1e6292e1b4b1ab217b9ff377982d23ea57ed1c2359ab0a33d5893f72173f0f270861b7681e8785997982bf4813a747bbf46ceffbef3d4eb07"
    hash_algorithm: str = 'HS256'
    client_url: str = 'http://localhost:3000'
    ipfs_node_url: str = 'https://ipfs.infura.io:5001'
    infura_project_id: str = '2CASClsLixgaD7e6qlO5LfIYA4b'
    infura_project_secret: str = '3a6dfcb5e77b97ba69b90f55e1f7b326'
    ipfs_read_nodes: Dict = {
        'cloudflare': ' https://cloudflare-ipfs.com/ipfs',
        'ipfsIo': 'https://ipfs.io/ipfs'
    }
