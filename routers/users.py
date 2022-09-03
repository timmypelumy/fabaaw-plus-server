from fastapi import APIRouter, Depends, HTTPException
from models.users import CreateUserInputModel, UserModel
from db import db
from lib.hashing import hash_password
from dependencies import get_authenticated_user

router = APIRouter(prefix='/users')


@router.get('/authenticated',  response_model=UserModel, response_model_exclude=['salt', 'password_hash', 'kyc'])
async def get_authenticated_user(user: UserModel = Depends(get_authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


@router.post('', response_model=UserModel, response_model_exclude=['salt', 'password_hash', 'kyc'])
async def create_user(body:  CreateUserInputModel):

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
