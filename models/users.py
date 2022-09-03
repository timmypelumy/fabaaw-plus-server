from datetime import datetime, timedelta
from enum import Enum
from typing import List, Union
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from uuid import  uuid4

def gen_id():
    return str(uuid4())

def get_datetime_float():
    return datetime.now().timestamp()


LATEST_DATE_OF_BIRTH =  (datetime.now() - timedelta(weeks=  (52 * 18) + 4 )).timestamp()
EARLIEST_DATE_OF_BIRTH =  (datetime.now() - timedelta(weeks=  52 * 50 )).timestamp()

class Gender(str,Enum):
    MALE = 'male'
    FEMALE  = 'female'
    OTHERS = 'others'

class UserKYCData(BaseModel):
    bvn :Union[None, str] = Field( default= None)
    national_id_card_urls :  Union[None, List [HttpUrl]] = Field( default= None, min_items= 2, alias= 'nationalIdCardUrls')
    driving_license_urls :  Union[None, List[HttpUrl]] = Field( default= None, min_items= 2, alias='drivingLicenseUrls')
    national_identity_number : Union[str,None] = Field( default= None, alias='nationalIdentityNumber')

    class Config:
        allow_population_by_field_name = True




class UserBioData(BaseModel):
    firstname : str = Field(min_length= 3, max_length= 25)
    lastname : str = Field(min_length= 3, max_length= 25)
    middlename : Union[str,None] = Field(default=None, min_length= 3, max_length= 25)
    date_of_birth : float = Field( gt= EARLIEST_DATE_OF_BIRTH, lt= LATEST_DATE_OF_BIRTH, alias= 'dateOfBirth' )
    gender : Gender 
    country : str = Field( min_length= 2, max_length= 5)
    phone_number : str = Field( min_length= 10, max_length= 15, alias= 'phoneNumber')
    email_address  : EmailStr = Field( alias='emailAddress' )
    home_address : Union[str,None] = Field( alias='homeAddress', min_length= 64, default= None )
    city : Union[str,None] = Field(  min_length= 3, default= None )
    state : Union[str,None] = Field(  min_length= 3, default= None )
    picture_urls :  Union[None, List [HttpUrl]] = Field( default= None, min_items= 2, alias= 'pictureUrls')


    class Config:
        allow_population_by_field_name = True
    
    
    

class UserModel(UserBioData):
    user_id : str  = Field(default_factory= gen_id, alias = 'userId')
    kyc : Union[ UserKYCData, None] = Field(default= None)
    date_joined : float = Field( default_factory=  get_datetime_float)
    is_active : bool = Field( default= True )
    password_hash : str = Field( min_length= 32, alias= 'passwordHash')
    salt : str =  Field( min_length= 32)
    disabled : bool = Field( default= False)

    class Config:
        allow_population_by_field_name = True

class CreateUserInputModel(UserBioData):
    password : str = Field(min_length= 8, max_length= 25)

    class Config:
        allow_population_by_field_name = True


class Token(BaseModel):
    access_token : str = Field(alias='accessToken')
    token_type : str = Field(alias='tokenType')

    class Config:
        allow_population_by_field_name = True


class TokenData(BaseModel):
    user_id : str 
    class Config:
        allow_population_by_field_name = True
