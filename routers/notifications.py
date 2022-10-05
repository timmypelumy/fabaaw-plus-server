from fastapi import APIRouter, Depends, HTTPException, Path
from models.notification import Notification
from db import db
from models.users import UserModel
from dependencies import get_authenticated_user
from typing import List

router = APIRouter(prefix='/notifications')


@router.get('/unread', response_model=List[Notification])
async def get_unread_notifications(user: UserModel = Depends(get_authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    await db.notifications.insert_one({
        "type": "WELCOME_ALERT",
        "user_id": user.user_id,
        "read": False,
        "archived": False,
    })

    cursor = db.notifications.find(
        {'user_id': user.user_id, 'read': False, 'archived': False}).sort('created', -1)

    notifications = await cursor.to_list(length=1000)

    return notifications


@router.get('/all', response_model=List[Notification])
async def get_all_notifications(user: UserModel = Depends(get_authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    cursor = db.notifications.find(
        {'user_id': user.user_id}).sort('created', -1)

    notifications = await cursor.to_list(length=100)

    return notifications


@router.get('/archived', response_model=List[Notification])
async def get_archived_notifications(user: UserModel = Depends(get_authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    cursor = db.notifications.find(
        {'user_id': user.user_id, 'archived': True}).sort('created', -1)

    notifications = await cursor.to_list(length=100)

    return notifications


@router.put('/set-as-read/{notification_id}', status_code=200)
async def set_as_read(user: UserModel = Depends(get_authenticated_user), notification_id: str = Path()):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = await db.notifications.update_one({'notification_id': notification_id, 'user_id': user.user_id},  {'$set': {'read': True}})

    if result.modified_count == 0:
        raise HTTPException(
            status_code=400, detail="Notification could not be updated!")


@router.put('/set-as-archived/{notification_id}', status_code=200)
async def set_as_archived(user: UserModel = Depends(get_authenticated_user), notification_id: str = Path()):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = await db.notifications.update_one({'notification_id': notification_id, 'user_id': user.user_id},  {'$set': {'archived': True}})

    if result.modified_count == 0:
        raise HTTPException(
            status_code=400, detail="Notification could not be updated!")


@router.put('/set-as-unread/{notification_id}', status_code=200)
async def set_as_unread(user: UserModel = Depends(get_authenticated_user), notification_id: str = Path()):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = await db.notifications.update_one({'notification_id': notification_id, 'user_id': user.user_id},  {'$set': {'read': False}})

    if result.modified_count == 0:
        raise HTTPException(
            status_code=400, detail="Notification could not be updated!")


@router.put('/set-as-unarchived/{notification_id}', status_code=200)
async def set_as_unarchived(user: UserModel = Depends(get_authenticated_user), notification_id: str = Path()):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    result = await db.notifications.update_one({'notification_id': notification_id, 'user_id': user.user_id},  {'$set': {'archived': False}})

    if result.modified_count == 0:
        raise HTTPException(
            status_code=400, detail="Notification could not be updated!")


@router.delete('/delete/all', status_code=200)
async def get_all_notifications(user: UserModel = Depends(get_authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    await db.notifications.delete_many(
        {'user_id': user.user_id})


@router.delete('/delete/{notification_id}', status_code=200)
async def delete_notification(user: UserModel = Depends(get_authenticated_user), notification_id: str = Path()):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    await db.notifications.delete_one({'notification_id': notification_id, 'user_id': user.user_id})
