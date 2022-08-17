from fastapi import APIRouter
from models.users import CreateUserInputModel, UserModel

router = APIRouter( prefix='/users')


@router.post('',response_model= UserModel)
def create_user( body :  CreateUserInputModel):
    return {}
