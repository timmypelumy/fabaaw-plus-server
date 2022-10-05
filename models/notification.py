from typing import Union
from pydantic import BaseModel, Field
from enum import Enum
from .users import get_datetime_float, get_nano_id


class NOTIFICATION_TYPE(str, Enum):
    welcome_alert = "WELCOME_ALERT"


class Notification(BaseModel):
    type:  NOTIFICATION_TYPE
    user_id: str = Field(alias='userId')
    read: bool = Field(default=False)
    archived: bool = Field(default=False)
    created: float = Field(default_factory=get_datetime_float)
    meta: dict = Field(default={})
    notification_id: str = Field(alias="id", default_factory=get_nano_id)

    class Config:
        allow_population_by_field_name = True
