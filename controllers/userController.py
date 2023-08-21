from models import Users
from schemas import userSchema
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
import uuid

def encryptedPassword(plainPassword):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(plainPassword)

def getUserList(db: Session):
    userList = db.query(Users).order_by((Users.created_at.desc())).all()
    return userList

def findUser(db: Session, schema: userSchema.getUserInfoSchema):
    return db.query(Users).filter(
        Users.email == schema.email,
    ).first()

def createUser(db: Session, request_data: userSchema.createUserSchema):
    createUserQuery = Users(
        user_id = str(uuid.uuid4()),
        fullname = request_data.fullname,
        password = encryptedPassword(request_data.password),
        email = request_data.email,
        created_at = datetime.now(),
    )
    db.add(createUserQuery)
    db.commit() 