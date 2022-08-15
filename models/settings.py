from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name : str = "Fabaaw Plus"
    tagline : str  = "Securing your identity"