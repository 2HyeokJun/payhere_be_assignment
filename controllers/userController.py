from models import Users
from schemas import userSchema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import uuid
import jwt
import datetime
# from redis import redis_client


load_dotenv()

# def isTokenExists(accessToken):
#     return redis_client.exists(accessToken)

def encryptedPassword(plainPassword):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(plainPassword)

def isCorrectPassword(plainPassword, encryptedPassword):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plainPassword, encryptedPassword)

def publishAccessToken(userUUID):
    expiresIn = datetime.datetime.now().timestamp() + 3600
    secretKey = os.environ.get('JWT_SECRET_KEY')
    accessToken = jwt.encode(
        {
            'userUUID': userUUID,
            'expiresIn': expiresIn,
        },
        secretKey,
        algorithm = 'HS256',
    )
    # redis_client.setex(user_uuid, timedelta(hours = 1), value = accessToken)
    return accessToken

# def revokeToken(accessToken):
#     secretKey = os.environ.get('JWT_SECRET_KEY')
#     userUUID = jwt.decode(accessToken, secretKey, algorithms = 'HS256')
#     print('decoded_result:', userUUID)
    # redis_client.delete(accessToken)

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
