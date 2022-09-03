import motor.motor_asyncio
from config import app_settings

client = motor.motor_asyncio.AsyncIOMotorClient(app_settings.db_url)

db = client[app_settings.slugged_app_name]