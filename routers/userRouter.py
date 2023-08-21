from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Users
from schemas import userSchema

router = APIRouter(
    prefix = '/users',
)

@router.get('/', response_model = list[userSchema.Users])
def getUserList(db: Session = Depends(get_db)):
    userList = db.query(Users).order_by((Users.created_at.desc())).all()
    return userList

# @router.post('/signup')
# def createUser(db: Session = Depends(get_db)):
