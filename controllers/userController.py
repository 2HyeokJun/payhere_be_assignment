from models import Users
from schemas import userSchema
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext
from dotenv import load_dotenv
from database import redisClient
import os
import uuid
import jwt
import datetime
 
load_dotenv()




def encryptedPassword(plainPassword):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(plainPassword)

def isCorrectPassword(plainPassword, encryptedPassword):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plainPassword, encryptedPassword)

def storeToRedis(key, value, ex = None):
    redisClient.set(key, value, ex)

def deleteFromRedis(key):
    redisClient.delete(key)

def publishAccessToken(userUUID):
    secretKey = os.environ.get('JWT_SECRET_KEY')
    accessToken = jwt.encode(
        {
            'userUUID': userUUID,
            'exp': datetime.datetime.now().timestamp() + 3600,
        },
        secretKey,
        algorithm = 'HS256',
    )
    storeToRedis(userUUID, accessToken, ex = 3600)
    return accessToken

def getUserList(db: Session):
    userList = db.query(Users).order_by((Users.created_at.desc())).all()
    return userList

def findUser(db: Session, schema, checkPassword: bool = False):
    query = db.query(Users).filter(Users.email == schema.email).first()
    if checkPassword:
        if isCorrectPassword(schema.password, query.password):
            return query
        else:
            return None
    else:
        return query

def createUser(db: Session, request_data: userSchema.createUserSchema):
    createUserQuery = Users(
        user_uuid = str(uuid.uuid4()),
        fullname = request_data.fullname,
        password = encryptedPassword(request_data.password),
        email = request_data.email,
        created_at = datetime.datetime.now(),
    )
    db.add(createUserQuery)
    db.commit()
