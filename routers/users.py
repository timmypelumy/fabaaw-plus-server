from fastapi import APIRouter, Depends, HTTPException, Path
from models.users import CreateUserInputModel, UserModel
from db import db
from lib.hashing import hash_password
from dependencies import get_authenticated_user, get_user_by_share_id
from pydantic import EmailStr

router = APIRouter(prefix='/users')


@router.get('/authenticated',  response_model=UserModel, response_model_exclude=['salt', 'password_hash', 'kyc'])
async def get_authenticated_user(user: UserModel = Depends(get_authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


@router.get('/share-id/{share_id}', response_model=UserModel, response_model_exclude=['salt', 'password_hash', 'kyc', 'user_id', 'email_address'])
async def get_user_by_share_id(user: UserModel = Depends(get_user_by_share_id)):
    return user




@router.delete('')
async def delete_user(user: UserModel = Depends(get_authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    await db.users.delete_one({'user_id' : user.user_id})


@router.post('', response_model=UserModel, response_model_exclude=['salt', 'password_hash', 'kyc'])
async def create_user(body:  CreateUserInputModel):

    user1 = await db.users.find_one({'phone_number': body.phone_number})
    user2 = await db.users.find_one({'email_address': body.email_address})

    if user1 or user2:
        raise HTTPException(
            status_code=400, detail="User with email/phone number exists already!")

    hash_dict = hash_password(body.password)

    user_model = UserModel(
        firstname=body.firstname,
        lastname=body.lastname,
        middlename=body.middlename,
        gender=body.gender,
        country=body.country,
        email_address=body.email_address,
        phone_number=body.phone_number,
        date_of_birth=body.date_of_birth,
        passwordHash=hash_dict['hash'],
        salt=hash_dict["salt"],
    )

    result = await db.users.insert_one(user_model.dict())

    user = await db.users.find_one({'_id': result.inserted_id})

    return user




@router.post('/check-email-exists/{email}')
async def check_email_exists(email: EmailStr = Path()):

    user = await db.users.find_one({'email_address': email})

    if user:
        return {'exists': True}
    else:
        return {'exists': False}


@router.post('/check-phone-number-exists/{phone}')
async def check_email_exists(phone: str = Path(min_length=8)):

    user = await db.users.find_one({'phone_number': phone})

    if user:
        return {'exists': True}
    else:
        return {'exists': False}
