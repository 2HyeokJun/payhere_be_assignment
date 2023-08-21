from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Users

router = APIRouter(
    prefix = '/users',
)

@router.get('/')
def getUserList(db: Session = Depends(get_db)):
    userList = db.query(Users).order_by((Users.created_at.desc())).all()
    return userList