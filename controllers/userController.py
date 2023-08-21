from models import Users
from schemas import userSchema
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

def getUserList(db: Session):
    userList = db.query(Users).order_by((Users.created_at.desc())).all()
    return userList

def createUser(db: Session, request_data: userSchema.createUserSchema):
    createUserQuery = Users(
        user_id = str(uuid.uuid4()),
        fullname = request_data.fullname,
        password = request_data.password,
        email = request_data.email,
        created_at = datetime.now(),
    )
    print('createUserQuery:', createUserQuery)
    db.add(createUserQuery)
    db.commit()