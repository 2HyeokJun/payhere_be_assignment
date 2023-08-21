from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from models import Users
from schemas import userSchema
from controllers import userController

router = APIRouter(
    prefix = '/users',
)

@router.get('/', response_model = list[userSchema.getUserInfoSchema])
def getUserList(db: Session = Depends(get_db)):
    userList = userController.getUserList(db)
    
    return userList

@router.post('/signup')
def createUser(schema: userSchema.createUserSchema, db: Session = Depends(get_db)):
    userController.createUser(db, schema)
    
    return {
        'status': 'success',
        'message': 'signup succeed'
    }