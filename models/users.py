from datetime import datetime, timedelta
from enum import Enum
from typing import List, Union
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from uuid import uuid4
from nanoid import generate



def gen_id():
    return str(uuid4())


def get_datetime_float():
    return datetime.now().timestamp()


def get_nano_id():
    alph = 'abcdefghijklmnopqrstuvwxyz'
    return generate(f"{alph}{alph.upper()}0123456789", 10)


def generate_vid():
    seed = '0123456789'
    return f"1{generate(seed, 14)}"


eighteenYears = (18 * 365 * 24 * 60 * 60) - (30 * 24 * 60 * 60)
threshold = datetime.now().timestamp() - eighteenYears


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHERS = 'others'


class BVNData(BaseModel):
    bvn: str = Field(min_length=11, max_length=11)
    face_photo_url:  HttpUrl = Field(alias="facePhotoUrl")
    signature_photo_url:  HttpUrl = Field(alias='signaturePhotoUrl')
    completed: bool = False

    class Config:
        allow_population_by_field_name = True


class IdentityCardTypes(str, Enum):
    driving_license = "DRIVING_LICENSE"
    national_id = 'NATIONAL_ID_CARD'
    voters_card = "VOTER_CARD"
    students_id = "SCHOOL_CARD"
    nimc = "NIMC"


class IdentityCardBaseModel(BaseModel):
    type: IdentityCardTypes
    reason: Union[str, None] = None
    issue_date: float = Field(alias='issueDate')
    expiry_date: float = Field(alias='expiryDate')
    uid: str = Field(default_factory=get_nano_id)
    id_number: int = Field(
        alias='idNumber', min=100000000, max=999999999999999)

    class Config:
        allow_population_by_field_name = True

class IdentityCard(IdentityCardBaseModel):
    url:  HttpUrl

    class Config:
        allow_population_by_field_name = True



class DocumentsData(BaseModel):
    photograph_url:  Union[HttpUrl, None] = Field(alias="photographUrl")
    signature_url: Union[HttpUrl, None] = Field(alias="signatureUrl")
    cards: Union[None, List[IdentityCard]] = Field(default=None)

    class Config:
        allow_population_by_field_name = True


class UpdateBVNInput(BaseModel):
    bvn_number: int = Field(
        alias='bvnNumber', min=10000000000, max=99999999999)


class UserKYCData(BaseModel):
    bvn: Union[None, str] = Field(default=None)
    national_id_card_urls:  Union[None, List[HttpUrl]] = Field(
        default=None, min_items=2, alias='nationalIdCardUrls')
    driving_license_urls:  Union[None, List[HttpUrl]] = Field(
        default=None, min_items=2, alias='drivingLicenseUrls')
    national_identity_number: Union[str, None] = Field(
        default=None, alias='nationalIdentityNumber')

    class Config:
        allow_population_by_field_name = True


class MaritalStatuses(str, Enum):
    married = "married"
    single = "single"
    divorced = "divorced"


class UserBioData(BaseModel):
    firstname: str = Field(min_length=3, max_length=25)
    lastname: str = Field(min_length=3, max_length=25)
    middlename: Union[str, None] = Field(
        default=None, min_length=3, max_length=25)
    date_of_birth: float = Field(lt=threshold, alias='dateOfBirth')
    gender: Gender
    country: str = Field(min_length=2, max_length=5)
    phone_number: str = Field(
        min_length=10, max_length=15, alias='phoneNumber')
    email_address: EmailStr = Field(alias='emailAddress')
    home_address: Union[str, None] = Field(
        alias='homeAddress', min_length=64, default=None)
    city: Union[str, None] = Field(min_length=3, default=None)
    state: Union[str, None] = Field(min_length=3, default=None)
    picture_urls:  Union[None, List[HttpUrl]] = Field(
        default=None, min_items=2, alias='pictureUrls')
    marital_status: Union[MaritalStatuses, None] = Field(alias='maritalStatus')
    nationality: Union[str, None] = Field(min_length=2, max_length=5)
    place_of_birth: Union[str, None] = Field(
        min_length=3, default=None, alias='placeOfBirth')
    mother_maiden_name: Union[str, None] = Field(
        min_length=3, max_length=25, alias='motherMaidenName')
    is_valid_tree: bool = Field(default=False, alias='isValidTree')

    class Config:
        allow_population_by_field_name = True


class UserModel(UserBioData):
    user_id: str = Field(default_factory=gen_id, alias='userId')
    share_id: str = Field(default_factory=get_nano_id, alias='shareId')
    kyc: Union[UserKYCData, None] = Field(default=None)
    date_joined: float = Field(default_factory=get_datetime_float)
    is_active: bool = Field(default=True)
    password_hash: str = Field(min_length=32, alias='passwordHash')
    salt: str = Field(min_length=32)
    disabled: bool = Field(default=False)
    bvn_data: Union[BVNData, None] = Field(default=None, alias='bvnData')
    documents: Union[None, DocumentsData] = Field(default=None)
    vid: str = Field(default_factory=generate_vid)

    class Config:
        allow_population_by_field_name = True


class UpdateContactInfo(BaseModel):
    phone_number: str = Field(
        min_length=10, max_length=15, alias='phoneNumber')
    email_address: EmailStr = Field(alias='emailAddress')

    class Config:
        allow_population_by_field_name = True


class CreateUserInputModel(UserBioData):
    password: str = Field(min_length=8, max_length=25)

    class Config:
        allow_population_by_field_name = True


class Token(BaseModel):
    access_token: str = Field(alias='accessToken')
    token_type: str = Field(alias='tokenType')

    class Config:
        allow_population_by_field_name = True


class TokenData(BaseModel):
    user_id: str

    class Config:
        allow_population_by_field_name = True
