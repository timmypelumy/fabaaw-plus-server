from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, Form
from models.users import BVNData, CreateUserInputModel, IdentityCard, IdentityCardTypes, UpdateContactInfo, UserBioData, UserModel
from db import db
from lib.hashing import hash_password
from dependencies import get_authenticated_user, get_user_by_share_id
from pydantic import EmailStr
from lib.upload_to_ipfs import upload_to_ipfs
from models.notification import Notification


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

    await db.users.delete_one({'user_id': user.user_id})


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

    await db.notifications.insert_one(Notification(
        type="WELCOME_ALERT",
        user_id=user_model.user_id,
        meta={'firstname': user_model.firstname},
    ).dict())

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


# User Data Updates


@router.put('/id-cards',   response_model=UserModel, response_model_exclude=['salt', 'password_hash', ])
async def update_id_cards(id_number: int = Form(min=100000000, max=999999999999999, alias='idNumber'), doc: UploadFile = Form(), type: IdentityCardTypes = Form(), issue_date: float = Form(alias='issueDate'), expiry_date: float = Form(alias='expiryDate'), user: UserModel = Depends(get_authenticated_user)):

    user_documents = user.documents.dict() if user.documents else {}
    user_documents_cards = user_documents['cards'] if user_documents.get(
        'cards', None) else []

    res = upload_to_ipfs(doc.file)
    id_card = IdentityCard(
        type=type,
        issue_date=issue_date,
        expiry_date=expiry_date,
        id_number=id_number,
        url=res['url'],
    )

    user_documents_cards.append(id_card.dict())
    user_documents['cards'] = user_documents_cards

    await db.users.update_one({'user_id': user.user_id}, {'$set': {'documents': user_documents}})

    return await db.users.find_one({'user_id': user.user_id})


@router.put('/basic-info',  response_model=UserModel, response_model_exclude=['salt', 'password_hash', ])
async def update_user_contact_info(body: UserBioData,  user: UserModel = Depends(get_authenticated_user)):

    user_dict = user.dict()

    user_dict.update(body.dict())

    user_dict.update({'is_valid_tree': True})

    await db.users.update_one({'user_id': user.user_id}, {'$set': user_dict})

    return await db.users.find_one({'user_id': user.user_id})


@router.put('/contact-info',  response_model=UserModel, response_model_exclude=['salt', 'password_hash', ])
async def update_user_contact_info(body: UpdateContactInfo,  user: UserModel = Depends(get_authenticated_user)):

    await db.users.update_one({'user_id': user.user_id}, {'$set': {'email_address': body.email_address, 'phone_number': body.phone_number}})

    return await db.users.find_one({'user_id': user.user_id})


@router.put('/documents/{doc_type}',  response_model=UserModel, response_model_exclude=['salt', 'password_hash', ])
async def update_user_photograph(doc: UploadFile = Form(), doc_type: str = Path(), user: UserModel = Depends(get_authenticated_user)):
    allowed_doc_types = ['photograph', 'signature']
    # MAX_FILE_SIZE = 1024 * 1024 * 3

    SUPPORTED_FORMATS = [
        "image/jpg",
        "image/jpeg",
        "image/webp",
        "image/png",
    ]

    if allowed_doc_types.count(doc_type) == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    if SUPPORTED_FORMATS.count(doc.content_type) == 0:
        raise HTTPException(
            status_code=400, detail="Invalid Content Type for doc")

    res = upload_to_ipfs(doc.file)

    user_docs = user.documents.dict() if user.documents else {}

    user_docs.update({doc_type + '_url': res['url']})
    await db.users.update_one({'user_id': user.user_id}, {'$set': {'documents': user_docs}})

    return await db.users.find_one({'user_id': user.user_id})


@router.put('/bvn',   response_model=UserModel, response_model_exclude=['salt', 'password_hash', ])
async def update_user_bvn_data(bvn: int = Form(min=10000000000, max=99999999999), facePhoto: UploadFile = Form(), signaturePhoto: UploadFile = Form(), user: UserModel = Depends(get_authenticated_user)):

    # MAX_FILE_SIZE = 1024 * 1024 * 3

    SUPPORTED_FORMATS = [
        "image/jpg",
        "image/jpeg",
        "image/webp",
        "image/png",
    ]

    if SUPPORTED_FORMATS.count(facePhoto.content_type) == 0:
        raise HTTPException(
            status_code=400, detail="Invalid Content Type for facePhoto")

    if SUPPORTED_FORMATS.count(signaturePhoto.content_type) == 0:
        raise HTTPException(
            status_code=400, detail="Invalid Content Type for signaturePhotot")

    res_face_photo = upload_to_ipfs(facePhoto.file)
    res_signature_photo = upload_to_ipfs(signaturePhoto.file)

    bvn_data = BVNData(
        bvn=bvn,
        face_photo_url=res_face_photo['url'],
        signature_photo_url=res_signature_photo['url'],
        completed=True
    )

    await db.users.update_one({'user_id': user.user_id}, {'$set': {'bvn_data': bvn_data.dict()}})

    return await db.users.find_one({'user_id': user.user_id})
