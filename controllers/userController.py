from models import Users
from sqlalchemy.orm import Session

def getUserList(db: Session):
    userList = db.query(Users).order_by((Users.created_at.desc())).all()
    return userList