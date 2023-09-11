from models.sqlalchemy_schemas import UserSchema
from schemas import userSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import uuid
import os
import jwt
import datetime

class Users:
    def __init__(self, db: Session):
        self.db = db

    def enroll(self, schema: userSchema.createUserSchema):
        def __encryptPassword(plainPassword):
            return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(plainPassword)
        user_uuid = str(uuid.uuid4())
        encrypted_password = __encryptPassword(schema.password)
        user = UserSchema(user_uuid = user_uuid, phone_number = schema.phoneNumber, password = encrypted_password)
        self.db.add(user)
        self.db.commit()
        return user

    def login(self, schema: userSchema.createUserSchema):
        def __isCorrectPassword(plainPassword, encryptedPassword):
            print('plainPassword:', plainPassword)
            print('encryptedPassword:', encryptedPassword)
            print('result:', CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plainPassword, encryptedPassword))
            return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plainPassword, encryptedPassword)

        def __publishAccessToken(user_uuid):
            secretKey = os.environ.get('JWT_SECRET_KEY')
            expiresAt = os.environ.get('TOKEN_EXPIRES_AT')
            accessToken = jwt.encode(
                {
                    'userUUID': user_uuid,
                    'exp': datetime.datetime.now().timestamp() + int(expiresAt),
                },
                secretKey,
                algorithm = 'HS256',
            )
            # self.__storeToRedis(user_uuid, accessToken, ex = expiresAt)
            return accessToken

        def __storeToRedis(key, value, ex = None):
            # redisClient.set(key, value, ex)
            return None

        query = self.__findUser(schema)
        if not query:
            raise ValueError #TODO:
        isCorrectPassword = __isCorrectPassword(schema.password, query.password)
        if query and isCorrectPassword:
            return __publishAccessToken(query.user_uuid)
        else:
            raise ValueError #TODO:

    def logout(self, user_uuid):
        def __deleteFromRedis(key):
            return None
        # redisClient.delete(key)
        __deleteFromRedis(user_uuid)

    

    def __findUser(self, schema):
        query = self.db.query(UserSchema).filter(UserSchema.phone_number == schema.phoneNumber).first()
        return query if True else None

    

    